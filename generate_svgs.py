#!/usr/bin/env python3
"""Generate SVG exports from Storybook stories.

Requires Storybook running at http://localhost:6006.
Usage: python3 generate_svgs.py
"""

import json
import re
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:6006"
SVGS_DIR = Path(__file__).parent / "svgs"


def safe_filename(name: str) -> str:
    """Convert story name to safe filename."""
    name = name.replace("/", "-").replace("\\", "-")
    name = re.sub(r'[<>:"|?*]', "", name)
    name = re.sub(r'\s+', "_", name)
    return name.strip("._-")


def section_dir(section_num: str) -> Path:
    d = SVGS_DIR / f"section_{section_num}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def main():
    print("Fetching story index from Storybook...")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/index.json", timeout=10) as r:
            index = json.loads(r.read())
    except Exception as e:
        print(f"ERROR: Could not reach Storybook at {BASE_URL} — {e}")
        print("Make sure Storybook is running: npm run storybook")
        return

    entries = index.get("entries", {})
    stories = {
        sid: info
        for sid, info in entries.items()
        if info.get("type") == "story"
    }

    print(f"Found {len(stories)} stories\n")

    saved = 0
    skipped = 0
    errors = 0

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()

        for story_id, info in stories.items():
            title = info.get("title", "")
            name = info.get("name", story_id)

            m = re.match(r"Section (\d+)/", title)
            if not m:
                continue

            section_num = m.group(1)
            out_dir = section_dir(section_num)
            out_path = out_dir / (safe_filename(name) + ".svg")

            url = f"{BASE_URL}/iframe.html?id={story_id}&viewMode=story"
            label = f"[S{section_num}] {name}"
            print(f"{label}...", end=" ", flush=True)

            try:
                page.goto(url, wait_until="networkidle", timeout=25000)
                # Extra wait for D3 animations / async rendering
                page.wait_for_timeout(2000)

                svg_content = page.evaluate("""() => {
                    const svgs = Array.from(document.querySelectorAll('svg'));
                    if (!svgs.length) return null;

                    // Pick the SVG with the largest bounding area
                    const largest = svgs.reduce((best, svg) => {
                        const r = svg.getBoundingClientRect();
                        const bestR = best.getBoundingClientRect();
                        return (r.width * r.height) > (bestR.width * bestR.height) ? svg : best;
                    }, svgs[0]);

                    // Ensure xmlns is present for standalone SVG files
                    if (!largest.getAttribute('xmlns')) {
                        largest.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
                    }

                    return new XMLSerializer().serializeToString(largest);
                }""")

                if svg_content and len(svg_content) > 200:
                    out_path.write_text(svg_content, encoding="utf-8")
                    print("saved")
                    saved += 1
                else:
                    print("skip (no SVG rendered)")
                    skipped += 1

            except Exception as e:
                print(f"ERROR: {e}")
                errors += 1

        browser.close()

    print(f"\nDone — saved: {saved}  skipped: {skipped}  errors: {errors}")
    print(f"Output: {SVGS_DIR}")


if __name__ == "__main__":
    main()
