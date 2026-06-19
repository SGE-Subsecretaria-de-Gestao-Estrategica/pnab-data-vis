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

  function exportSvg() {
    const svg = container?.querySelector('svg');
    if (svg) downloadSvg(svg as SVGSVGElement, filename);
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
