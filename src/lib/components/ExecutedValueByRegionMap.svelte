<script lang="ts">
  import { geoMercator, geoPath } from 'd3-geo';
  import {
    loadBrazilGeoJSON,
    categorical5,
    getContrastColor,
    typography,
  } from 'sniic-design-system';

  const FONT_FAMILY = typography.chartValueFontFamily;

  const STATE_TO_REGION: Record<string, string> = {
    AC: 'Norte', AM: 'Norte', AP: 'Norte', PA: 'Norte', RO: 'Norte', RR: 'Norte', TO: 'Norte',
    AL: 'Nordeste', BA: 'Nordeste', CE: 'Nordeste', MA: 'Nordeste', PB: 'Nordeste',
    PE: 'Nordeste', PI: 'Nordeste', RN: 'Nordeste', SE: 'Nordeste',
    DF: 'Centro-Oeste', GO: 'Centro-Oeste', MS: 'Centro-Oeste', MT: 'Centro-Oeste',
    ES: 'Sudeste', MG: 'Sudeste', RJ: 'Sudeste', SP: 'Sudeste',
    PR: 'Sul', RS: 'Sul', SC: 'Sul',
  };

  interface Props {
    regions: Record<string, any>;
    metric: string;
    format?: (v: number) => string;
    formatLine2?: (row: any) => string;
  }

  let {
    regions,
    metric,
    format = (v: number) => v.toLocaleString('pt-BR'),
    formatLine2 = undefined,
  }: Props = $props();

  let geojson = $state<any>(null);
  let containerEl: HTMLDivElement | undefined = $state();
  let width = $state(600);

  $effect(() => {
    if (!containerEl) return;
    width = containerEl.clientWidth;
    const ro = new ResizeObserver(([e]) => { width = e.contentRect.width; });
    ro.observe(containerEl);
    return () => ro.disconnect();
  });

  $effect(() => {
    loadBrazilGeoJSON().then((g: any) => { geojson = g; });
  });

  const mapH = $derived(Math.round(width * 0.72));

  const valueMap = $derived(
    new Map(Object.entries(regions).map(([name, d]) => [name, (d[metric] ?? 0) as number]))
  );

  const REGIONS = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'] as const;
  const regionColorMap: Record<string, string> = Object.fromEntries(
    REGIONS.map((r, i) => [r, categorical5[i]])
  );

  function regionColor(region: string | undefined): string {
    return region ? (regionColorMap[region] ?? '#ccc') : '#ccc';
  }

  const projection = $derived.by(() => {
    if (!geojson || width <= 0) return null;
    return geoMercator().fitSize([width, mapH], geojson);
  });

  const pathFn = $derived(projection ? geoPath(projection) : null);

  const regionLabels = $derived.by(() => {
    if (!pathFn || !geojson) return [];
    const acc: Record<string, { xs: number[]; ys: number[] }> = {};

    for (const f of geojson.features as any[]) {
      const sigla = f.properties.sigla as string;
      const region = STATE_TO_REGION[sigla];
      if (!region) continue;
      const c = pathFn.centroid(f) as [number, number];
      if (!isFinite(c[0]) || !isFinite(c[1])) continue;
      if (!acc[region]) acc[region] = { xs: [], ys: [] };
      acc[region].xs.push(c[0]);
      acc[region].ys.push(c[1]);
    }

    return Object.entries(acc).map(([name, { xs, ys }]) => {
      const val = valueMap.get(name) ?? 0;
      const fill = regionColor(name);
      return {
        name,
        cx: xs.reduce((a, b) => a + b, 0) / xs.length,
        cy: ys.reduce((a, b) => a + b, 0) / ys.length,
        val,
        fill,
        row: regions[name],
      };
    });
  });

  const lineCount = $derived(formatLine2 ? 3 : 2);
  const labelBlockH = $derived((lineCount - 1) * 14);
</script>

<div bind:this={containerEl} style="width: 100%">
  {#if geojson && pathFn && width > 0}
    <svg {width} height={mapH}>
      {#each geojson.features as f (f.properties.name)}
        {@const region = STATE_TO_REGION[f.properties.sigla]}
        {@const d = pathFn(f)}
        {#if d}
          <path d={d} fill={regionColor(region)} stroke="white" stroke-width="0.5" />
        {/if}
      {/each}

      {#each regionLabels as item (item.name)}
        {@const textFill = getContrastColor(item.fill)}
        <text
          x={item.cx}
          y={item.cy}
          text-anchor="middle"
          font-size="11"
          font-family={FONT_FAMILY}
          fill={textFill}
          pointer-events="none"
        >
          <tspan x={item.cx} dy={-(labelBlockH / 2)} font-weight="700" font-size="12">{item.name}</tspan>
          <tspan x={item.cx} dy="14">{format(item.val)}</tspan>
          {#if formatLine2}
            <tspan x={item.cx} dy="14">{formatLine2(item.row)}</tspan>
          {/if}
        </text>
      {/each}
    </svg>
  {/if}
</div>
