"""
Exports all chart SVGs from Storybook stories to svgs/section_X/ directories.
Usage: python3 export-svgs.py
"""

import json
import os
import re
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
STORYBOOK_DIR = ROOT / "storybook-static"
SVGS_DIR = ROOT / "svgs"
PORT = 16006


def make_filename(title: str, name: str) -> str:
    """Mirrors makeFilename() from .storybook/preview.ts"""
    if "/" in title:
        group = title.split("/")[1]
    else:
        group = re.sub(r"\s+", "", title)

    slug = name
    slug = re.sub(r"[–—]", "-", slug)
    slug = re.sub(r"[^\w\s\-áéíóúàèìòùâêîôûãõçÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÇ]", "", slug)
    slug = slug.strip()
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return f"{group}--{slug}.svg"


def get_section_dir(title: str) -> str:
    m = re.match(r"^Section (\d+)", title, re.IGNORECASE)
    return f"section_{m.group(1)}" if m else "misc"


class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STORYBOOK_DIR), **kwargs)

    def log_message(self, format, *args):
        pass  # suppress request logs


def start_server():
    server = HTTPServer(("127.0.0.1", PORT), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Static server started on http://localhost:{PORT}")
    return server


def main():
    index_path = STORYBOOK_DIR / "index.json"
    if not index_path.exists():
        print("storybook-static/index.json not found. Run: npm run build-storybook")
        return

    index = json.loads(index_path.read_text())
    stories = [e for e in index["entries"].values() if e.get("type") == "story"]
    print(f"Found {len(stories)} stories")

    server = start_server()
    time.sleep(0.5)  # let server start

    exported = 0
    failed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for story in stories:
            title = story["title"]
            name = story["name"]
            sid = story["id"]

            section_dir = get_section_dir(title)
            filename = make_filename(title, name)
            out_dir = SVGS_DIR / section_dir
            out_path = out_dir / filename

            try:
                page.goto(
                    f"http://localhost:{PORT}/iframe.html?id={sid}",
                    wait_until="networkidle",
                    timeout=15000,
                )
                page.wait_for_timeout(400)

                svg_content = page.evaluate("""() => {
                    // 1. Try to find a visible chart SVG (skip the hidden a11y filter SVG)
                    const svgs = Array.from(document.querySelectorAll('svg'));
                    const chartSvg = svgs.find(s =>
                        s.id !== 'storybook-a11y-vision-filters' &&
                        getComputedStyle(s).display !== 'none' &&
                        s.getBoundingClientRect().width > 0
                    );
                    if (chartSvg) {
                        if (!chartSvg.getAttribute('width') && !chartSvg.getAttribute('height') && chartSvg.viewBox.baseVal) {
                            const vb = chartSvg.viewBox.baseVal;
                            chartSvg.setAttribute('width', String(vb.width));
                            chartSvg.setAttribute('height', String(vb.height));
                        }
                        return chartSvg.outerHTML;
                    }

                    // 2. No chart SVG — wrap rendered HTML in foreignObject
                    const root = document.getElementById('storybook-root');
                    if (!root || !root.firstElementChild) return null;
                    const el = root.firstElementChild;
                    const rect = el.getBoundingClientRect();
                    const width = Math.ceil(rect.width) || 400;
                    const height = Math.ceil(rect.height) || 120;

                    // Collect all stylesheet text
                    const styles = Array.from(document.styleSheets).map(sheet => {
                        try { return Array.from(sheet.cssRules).map(r => r.cssText).join('\\n'); }
                        catch { return ''; }
                    }).join('\\n');

                    return [
                        `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}">`,
                        `  <foreignObject x="0" y="0" width="${width}" height="${height}">`,
                        `    <div xmlns="http://www.w3.org/1999/xhtml">`,
                        `      <style>${styles}</style>`,
                        `      ${el.outerHTML}`,
                        `    </div>`,
                        `  </foreignObject>`,
                        `</svg>`,
                    ].join('\\n');
                }""")

                if not svg_content:
                    print(f"  [SKIP] No content: {title} / {name}")
                    failed += 1
                    continue

                out_dir.mkdir(parents=True, exist_ok=True)
                out_path.write_text(svg_content, encoding="utf-8")
                print(f"  [OK]   {section_dir}/{filename}")
                exported += 1

            except Exception as e:
                print(f"  [FAIL] {title} / {name}: {e}")
                failed += 1

        browser.close()

    server.shutdown()
    print(f"\nDone: {exported} exported, {failed} failed/skipped")


if __name__ == "__main__":
    main()
