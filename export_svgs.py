#!/usr/bin/env python3
"""
Extrai SVGs das stories do Storybook e salva na pasta svgs/.

Requer o Storybook rodando em http://localhost:6006
  python3 export_svgs.py [--section N] [--url URL]
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

STORYBOOK_URL = 'http://localhost:6006'
SVG_DIR = Path('svgs')


def fetch_stories(url: str) -> dict:
    try:
        with urllib.request.urlopen(f'{url}/index.json', timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f'Erro ao buscar index.json: {e}')
        sys.exit(1)


def build_mapping(entries: dict) -> list[tuple[str, Path]]:
    """
    Retorna lista de (story_id, output_path) para exportar.

    Regras de mapeamento:
      1. Título "Section N/Grafico M" → svgs/sectionN/graficoM.svg
      2. Título "Section N/Tabela M"  → svgs/sectionN/tabelaM.svg
      3. Nome da story "Grafico M" (ou "Grafico M — ...")
         dentro de "Section N/qualquerCoisa"  → svgs/sectionN/graficoM.svg
      4. Nome da story "Infografico M" → svgs/sectionN/infograficoM.svg
      5. Nome da story "Grafico 31.1" / "Grafico 31.2" → grafico31-1.svg / grafico31-2.svg
    """
    # Prefer primary variant for stories with multiple variants of same number
    # We collect all candidates and then pick by preference rules
    candidates: dict[Path, list[tuple[int, str]]] = {}  # path → [(priority, story_id)]

    for sid, entry in entries.items():
        if entry.get('type') != 'story':
            continue
        title: str = entry['title']
        name: str = entry['name']

        sec_m = re.match(r'Section\s+(\d+)', title, re.IGNORECASE)
        if not sec_m:
            continue
        sec = sec_m.group(1)

        output_path: Path | None = None
        priority = 10  # lower = better

        # Rule 1/2: title = "Section N/Grafico M" or "Section N/Tabela M"
        title_m = re.search(
            r'/(Gr[aá]fico|Tabela|Infogr[aá]fico)\s+(\d+)$', title, re.IGNORECASE
        )
        if title_m:
            typ = title_m.group(1).lower()
            num = title_m.group(2)
            typ_norm = _norm_type(typ)
            output_path = SVG_DIR / f'section{sec}' / f'{typ_norm}{num}.svg'
            # Stories that are the primary (no "variante") get higher priority
            if 'variante' in name.lower():
                priority = 20
            elif re.search(r'\(blue\b|bluePurple|blue e orange', name):
                priority = 15
            else:
                priority = 5

        # Rule 3/4/5: name = "Grafico N", "Tabela N", "Infografico N", "Grafico 31.1"
        if output_path is None:
            name_m = re.match(
                r'(Gr[aá]fico|Tabela|Infogr[aá]fico)\s+(\d+)(?:\.(\d+))?', name, re.IGNORECASE
            )
            if name_m:
                typ = name_m.group(1).lower()
                num = name_m.group(2)
                sub = name_m.group(3)
                typ_norm = _norm_type(typ)
                if sub:
                    filename = f'{typ_norm}{num}-{sub}.svg'
                else:
                    filename = f'{typ_norm}{num}.svg'
                output_path = SVG_DIR / f'section{sec}' / filename
                priority = 5

        if output_path:
            candidates.setdefault(output_path, []).append((priority, sid))

    # For each output path, pick the story with lowest priority value
    result: list[tuple[str, Path]] = []
    for path, opts in sorted(candidates.items()):
        opts.sort()
        _, best_sid = opts[0]
        result.append((best_sid, path))

    return result


def _norm_type(typ: str) -> str:
    t = typ.lower()
    if t.startswith('gr'):
        return 'grafico'
    if t.startswith('tab'):
        return 'tabela'
    if t.startswith('inf'):
        return 'infografico'
    return t


def export_svgs(url: str, mapping: list[tuple[str, Path]]):
    print(f'{len(mapping)} SVGs para exportar...\n')

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={'width': 1400, 'height': 900})

        for sid, out_path in mapping:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            story_url = f'{url}/iframe.html?id={sid}&viewMode=story'
            page = ctx.new_page()
            try:
                page.goto(story_url, wait_until='networkidle', timeout=30_000)
                page.wait_for_timeout(800)

                svg_content: str | None = page.evaluate('''() => {
                    const root = document.querySelector("#storybook-root > div:first-child");
                    const svg = root ? root.querySelector("svg") : document.querySelector("svg");
                    if (!svg) return null;
                    // Ensure xmlns is set
                    if (!svg.getAttribute("xmlns")) {
                        svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
                    }
                    svg.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
                    return new XMLSerializer().serializeToString(svg);
                }''')

                if svg_content:
                    out_path.write_text(svg_content, encoding='utf-8')
                    size = out_path.stat().st_size // 1024
                    print(f'  ok  {out_path}  ({size} KB)')
                else:
                    print(f'  SKIP {out_path}  (sem SVG na story {sid})')

            except Exception as e:
                print(f'  ERR  {out_path}: {e}')
            finally:
                page.close()

        browser.close()

    print(f'\nConcluído. SVGs salvos em {SVG_DIR.resolve()}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--section', type=str, default=None, help='Exporta apenas a seção N')
    parser.add_argument('--url', type=str, default=STORYBOOK_URL)
    args = parser.parse_args()

    index = fetch_stories(args.url)
    entries = index.get('entries', {})

    mapping = build_mapping(entries)

    if args.section:
        mapping = [(sid, p) for sid, p in mapping if f'/section{args.section}/' in str(p)]

    if not mapping:
        print('Nenhuma story encontrada com os filtros.')
        sys.exit(1)

    for sid, path in sorted(mapping, key=lambda x: str(x[1])):
        print(f'  {path}  ←  {sid}')
    print()

    export_svgs(args.url, mapping)


if __name__ == '__main__':
    main()
