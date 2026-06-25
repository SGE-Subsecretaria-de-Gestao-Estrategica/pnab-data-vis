#!/usr/bin/env python3
"""
Captura screenshots de alta resolucao (2x) de todas as stories do Storybook.
Requer o Storybook rodando em http://localhost:6006

Uso:
  python3 screenshot_stories.py [--scale 2] [--section 1]

Flags:
  --scale N    Device pixel ratio (padrao: 2 para qualidade retina)
  --section N  Captura apenas a secao N (padrao: todas)
  --url URL    URL do Storybook (padrao: http://localhost:6006)
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright


def slugify_name(name: str) -> str:
    """Mesma logica do preview.ts: makeFilename()"""
    slug = name
    slug = re.sub(r'[–—]', '-', slug)
    slug = re.sub(r'[^\w\s\-áéíóúàèìòùâêîôûãõçÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÇ]', '', slug)
    slug = slug.strip()
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug


def make_filename(title: str, name: str) -> str:
    if '/' in title:
        group = title.split('/')[1]
    else:
        group = re.sub(r'\s+', '', title)
    slug = slugify_name(name)
    return f'{group}--{slug}.png'


def fetch_stories(storybook_url: str) -> dict:
    url = f'{storybook_url}/index.json'
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f'Erro ao buscar {url}: {e}')
        print('Verifique se o Storybook esta rodando em', storybook_url)
        sys.exit(1)


NUMBERED_RE = re.compile(r'(Gr[aá]fico|Tabela|Infogr[aá]fico)\s+\d+', re.IGNORECASE)


def is_numbered(title: str, name: str) -> bool:
    return bool(NUMBERED_RE.search(title) or NUMBERED_RE.match(name))


def screenshot_stories(storybook_url: str, output_dir: Path, scale: int, only_section: str | None, numbered_only: bool = False):
    index = fetch_stories(storybook_url)
    entries = index.get('entries', {})

    stories = [
        (id_, entry)
        for id_, entry in entries.items()
        if entry.get('type') == 'story'
    ]

    if only_section:
        stories = [
            (id_, e) for id_, e in stories
            if re.match(rf'Section\s+{only_section}\b', e.get('title', ''), re.IGNORECASE)
        ]

    if numbered_only:
        stories = [
            (id_, e) for id_, e in stories
            if is_numbered(e.get('title', ''), e.get('name', ''))
        ]

    if not stories:
        print('Nenhuma story encontrada com os filtros fornecidos.')
        sys.exit(1)

    print(f'{len(stories)} stories encontradas. Iniciando capturas a {scale}x...\n')

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(
            device_scale_factor=scale,
            viewport={'width': 1400, 'height': 900},
        )

        for story_id, entry in stories:
            title = entry.get('title', '')
            name = entry.get('name', '')

            # Extrai numero da secao do titulo (ex: 'Section 1/component')
            section_match = re.match(r'Section\s+(\d+)', title, re.IGNORECASE)
            if not section_match:
                print(f'  [skip] titulo sem secao: {title}')
                continue

            section_num = section_match.group(1)
            section_dir = output_dir / f'section{section_num}'
            section_dir.mkdir(parents=True, exist_ok=True)

            filename = make_filename(title, name)
            output_path = section_dir / filename

            url = f'{storybook_url}/iframe.html?id={story_id}&viewMode=story'

            page = context.new_page()
            try:
                page.goto(url, wait_until='networkidle', timeout=30_000)

                # Esconde o botao de exportar SVG e garante fundo transparente
                page.add_style_tag(content='.export-bar { display: none !important; } body, #storybook-root { background: transparent !important; }')

                # Aguarda animacoes e renderizacao completa
                page.wait_for_timeout(800)

                # Captura apenas o container do grafico (primeiro filho do root)
                container = page.query_selector('#storybook-root > div:first-child')
                if container:
                    container.screenshot(path=str(output_path), omit_background=True)
                else:
                    page.screenshot(path=str(output_path), full_page=True, omit_background=True)

                size = output_path.stat().st_size // 1024
                print(f'  ok  {section_dir.name}/{filename} ({size}KB)')

            except Exception as e:
                print(f'  ERR {filename}: {e}')
            finally:
                page.close()

        browser.close()

    print(f'\nPronto! Screenshots salvas em: {output_dir.resolve()}')


def main():
    parser = argparse.ArgumentParser(description='Screenshot stories do Storybook em alta resolucao')
    parser.add_argument('--scale', type=int, default=2, help='Device pixel ratio (padrao: 2)')
    parser.add_argument('--section', type=str, default=None, help='Captura apenas a secao N')
    parser.add_argument('--url', type=str, default='http://localhost:6006', help='URL do Storybook')
    parser.add_argument('--out', type=str, default='pngs', help='Diretorio de saida (padrao: pngs)')
    parser.add_argument('--numbered-only', action='store_true', help='Captura apenas stories com Grafico/Tabela/Infografico N no titulo')
    args = parser.parse_args()

    output_dir = Path(args.out)
    screenshot_stories(args.url, output_dir, args.scale, args.section, args.numbered_only)


if __name__ == '__main__':
    main()
