<script lang="ts">
  import type { Snippet } from 'svelte';
  import { downloadSvg } from 'sniic-design-system';
  import { addons } from 'storybook/preview-api';

  let { children, filename = 'chart.svg', storyId = '' }: { children: Snippet; filename?: string; storyId?: string } = $props();

  const STORAGE_KEY = 'storybook-hidden';
  const CHANNEL_EVENT = 'hide-story/visibility-changed';

  function getHidden(): Set<string> {
    try {
      return new Set(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '[]'));
    } catch {
      return new Set();
    }
  }

  const key = $derived(storyId || filename);

  let hidden = $state(getHidden().has(key));

  let container: HTMLDivElement | undefined = $state();

  // ── Rawline embedding ──────────────────────────────────────────────────────
  // Exported SVGs are opened in apps (InDesign, etc.) that don't have Rawline
  // installed, so the font-family chain falls back to system-ui/sans-serif
  // (often rendered as Helvetica). We embed the Rawline weights as base64
  // @font-face rules inside the SVG so the type travels with the file.
  const RAWLINE_WEIGHTS = [400, 500, 600, 700];
  const SVG_NS = 'http://www.w3.org/2000/svg';

  let fontStyleCss: string | null = null;

  async function fetchFontBase64(weight: number): Promise<string> {
    const res = await fetch(`/fonts/rawline-${weight}.ttf`);
    const buf = await res.arrayBuffer();
    const bytes = new Uint8Array(buf);
    let binary = '';
    for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
    return btoa(binary);
  }

  async function buildFontStyleCss(): Promise<string> {
    if (fontStyleCss) return fontStyleCss;
    const faces = await Promise.all(
      RAWLINE_WEIGHTS.map(async (w) => {
        const b64 = await fetchFontBase64(w);
        return `@font-face{font-family:'Rawline';font-style:normal;font-weight:${w};src:url(data:font/ttf;base64,${b64}) format('truetype');}`;
      }),
    );
    fontStyleCss = faces.join('');
    return fontStyleCss;
  }

  async function exportSvg() {
    const svg = container?.querySelector('svg');
    if (!svg) return;
    let styleEl: SVGStyleElement | null = null;
    try {
      const css = await buildFontStyleCss();
      styleEl = document.createElementNS(SVG_NS, 'style') as SVGStyleElement;
      styleEl.textContent = css;
      svg.insertBefore(styleEl, svg.firstChild);
      downloadSvg(svg as SVGSVGElement, filename);
    } catch (err) {
      console.error('Falha ao embutir Rawline no SVG; exportando sem fonte embutida.', err);
      if (styleEl && styleEl.parentNode) styleEl.parentNode.removeChild(styleEl);
      styleEl = null;
      downloadSvg(svg as SVGSVGElement, filename);
    } finally {
      if (styleEl && styleEl.parentNode) styleEl.parentNode.removeChild(styleEl);
    }
  }

  function emitVisibilityChanged() {
    try {
      addons.getChannel().emit(CHANNEL_EVENT);
    } catch {}
  }

  function toggleHide() {
    const set = getHidden();
    if (hidden) {
      set.delete(key);
    } else {
      set.add(key);
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...set]));
    hidden = !hidden;
    emitVisibilityChanged();
  }
</script>

{#if hidden}
  <div class="hidden-placeholder">
    <span class="hidden-label">Story oculta: <code>{filename}</code></span>
    <button class="toggle-btn show-btn" onclick={toggleHide}>Mostrar</button>
  </div>
{:else}
  <div bind:this={container}>
    {@render children()}
  </div>
  <div class="export-bar">
    <button class="toggle-btn hide-btn" onclick={toggleHide}>Ocultar</button>
    <button class="export-btn" onclick={exportSvg}>Export SVG</button>
  </div>
{/if}

<style>
  .export-bar {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    padding: 8px;
  }

  .export-btn,
  .toggle-btn {
    cursor: pointer;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 12px;
    border: 1px solid #ccc;
  }

  .export-btn {
    background: #f0f0f0;
  }

  .hide-btn {
    background: #fff3cd;
    border-color: #ffc107;
    color: #856404;
  }

  .show-btn {
    background: #d1e7dd;
    border-color: #198754;
    color: #0a3622;
  }

  .hidden-placeholder {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    background: #f8f9fa;
    border: 1px dashed #adb5bd;
    border-radius: 4px;
    color: #6c757d;
    font-size: 13px;
  }

  .hidden-label code {
    font-family: monospace;
    background: #e9ecef;
    padding: 1px 4px;
    border-radius: 3px;
  }
</style>
