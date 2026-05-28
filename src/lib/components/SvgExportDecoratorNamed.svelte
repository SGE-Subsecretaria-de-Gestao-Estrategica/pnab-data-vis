<script lang="ts">
  import type { Snippet } from 'svelte';
  import { downloadSvg } from 'sniic-design-system';

  let { children, filename = 'chart.svg' }: { children: Snippet; filename?: string } = $props();

  let container: HTMLDivElement | undefined = $state();

  function exportSvg() {
    const svg = container?.querySelector('svg');
    if (svg) downloadSvg(svg as SVGSVGElement, filename);
  }
</script>

<div bind:this={container}>
  {@render children()}
</div>
<div class="export-bar">
  <button class="export-btn" onclick={exportSvg}>Export SVG</button>
</div>

<style>
  .export-bar {
    display: flex;
    justify-content: flex-end;
    padding: 8px;
  }

  .export-btn {
    cursor: pointer;
    padding: 4px 12px;
    background: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 12px;
  }
</style>
