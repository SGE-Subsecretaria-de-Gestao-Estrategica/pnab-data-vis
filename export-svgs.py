"""
Exports all chart SVGs from Storybook stories to svgs/section_X/ directories.
Usage: python3 export-svgs.py
"""

import base64
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

                    // 2. No chart SVG — build native SVG text elements from the BigNumber component
                    function esc(s) {
                        return String(s)
                            .replace(/&/g, '&amp;')
                            .replace(/</g, '&lt;')
                            .replace(/>/g, '&gt;')
                            .replace(/"/g, '&quot;')
                            .replace(/\\u00a0/g, '&#160;');
                    }

                    const root = document.getElementById('storybook-root');
                    if (!root) return null;

                    const bigNumberEl = root.querySelector('[class*="big-number"]');
                    if (!bigNumberEl) return null;

                    const valueEl = bigNumberEl.querySelector('[class*="value"]');
                    if (!valueEl) return null;
                    const labelEl = bigNumberEl.querySelector('[class*="label"]');

                    const vcs = getComputedStyle(valueEl);
                    const valueText = valueEl.textContent.trim();
                    const fontSize = parseFloat(vcs.fontSize) || 72;
                    const fillColor = vcs.color || '#000';
                    const fontFamily = (vcs.fontFamily || 'system-ui').replace(/['"]/g, '');
                    const fontWeight = vcs.fontWeight || '700';

                    // Detect stroke from text-shadow (multiple offsets = outline effect)
                    let strokeColor = null;
                    let strokeWidth = 0;
                    const ts = vcs.textShadow;
                    if (ts && ts !== 'none') {
                        const cm = ts.match(/^(rgba?\\([^)]+\\))/);
                        if (cm) strokeColor = cm[1];
                        const offsets = [...ts.matchAll(/(-?[\\d.]+)px\\s+(-?[\\d.]+)px/g)];
                        strokeWidth = offsets.reduce(
                            (m, [, x, y]) => Math.max(m, Math.abs(parseFloat(x)), Math.abs(parseFloat(y))), 0
                        );
                    }

                    const labelText = labelEl ? labelEl.textContent.trim() : '';
                    const lcs = labelEl ? getComputedStyle(labelEl) : null;
                    const labelSize = lcs ? (parseFloat(lcs.fontSize) || 14) : 14;
                    const labelColor = lcs ? (lcs.color || '#555') : '#555';
                    const labelWeight = lcs ? (lcs.fontWeight || '600') : '600';

                    // Background: body or storybook-root background
                    const bodyBg = getComputedStyle(document.body).backgroundColor;
                    const bg = (bodyBg && bodyBg !== 'rgba(0, 0, 0, 0)') ? bodyBg : 'white';

                    const pad = 32;
                    const lineH = fontSize * 1.2;
                    const gap = labelText ? 12 : 0;
                    const labelH = labelText ? labelSize * 1.4 : 0;
                    const svgH = Math.ceil(pad * 2 + lineH + gap + labelH);
                    const svgW = Math.max(Math.ceil(fontSize * 0.65 * valueText.length + pad * 2), 280);
                    const cx = svgW / 2;
                    const valueY = pad + fontSize;
                    const labelY = valueY + gap + labelSize;

                    const parts = [
                        `<svg xmlns="http://www.w3.org/2000/svg" width="${svgW}" height="${svgH}">`,
                        `  <rect width="${svgW}" height="${svgH}" fill="${bg}"/>`,
                    ];

                    // Stroke pass (outline)
                    if (strokeColor && strokeWidth > 0) {
                        parts.push(
                            `  <text x="${cx}" y="${valueY}" text-anchor="middle" ` +
                            `font-family="${esc(fontFamily)}, system-ui, sans-serif" ` +
                            `font-size="${fontSize}" font-weight="${fontWeight}" ` +
                            `fill="${strokeColor}" stroke="${strokeColor}" ` +
                            `stroke-width="${strokeWidth * 2}" stroke-linejoin="round" ` +
                            `paint-order="stroke fill">${esc(valueText)}</text>`
                        );
                    }
                    // Fill pass
                    parts.push(
                        `  <text x="${cx}" y="${valueY}" text-anchor="middle" ` +
                        `font-family="${esc(fontFamily)}, system-ui, sans-serif" ` +
                        `font-size="${fontSize}" font-weight="${fontWeight}" ` +
                        `fill="${fillColor}">${esc(valueText)}</text>`
                    );

                    if (labelText) {
                        parts.push(
                            `  <text x="${cx}" y="${labelY}" text-anchor="middle" ` +
                            `font-family="${esc(fontFamily)}, system-ui, sans-serif" ` +
                            `font-size="${labelSize}" font-weight="${labelWeight}" ` +
                            `fill="${labelColor}">${esc(labelText)}</text>`
                        );
                    }

                    parts.push(`</svg>`);
                    return parts.join('\\n');
                }""")

                if not svg_content:
                    # Final fallback: screenshot the rendered element, embed PNG in SVG
                    root_el = page.locator('#storybook-root')
                    bbox = root_el.bounding_box()
                    if bbox and bbox['width'] > 0 and bbox['height'] > 0:
                        png_bytes = root_el.screenshot()
                        png_b64 = base64.b64encode(png_bytes).decode()
                        w, h = int(bbox['width']), int(bbox['height'])
                        svg_content = (
                            f'<svg xmlns="http://www.w3.org/2000/svg" '
                            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
                            f'width="{w}" height="{h}">\n'
                            f'  <image href="data:image/png;base64,{png_b64}" '
                            f'width="{w}" height="{h}"/>\n'
                            f'</svg>'
                        )
                    else:
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
