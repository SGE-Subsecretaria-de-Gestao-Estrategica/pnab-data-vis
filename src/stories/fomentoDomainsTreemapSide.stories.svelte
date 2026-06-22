<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { hierarchy, treemap as d3treemap } from 'd3-hierarchy';
  // @ts-ignore
  import { fomentoDomainsRows } from '$lib/data/section6';

  const TREEMAP_W = 560;
  const TREEMAP_H = 520;
  const GAP = 28;
  const LEG_W = 460;
  const TOTAL_W = TREEMAP_W + GAP + LEG_W;
  const HEADER_H = 20;
  const NUM_ROWS = fomentoDomainsRows.length;
  const LEG_ROW_H = Math.floor((TREEMAP_H - HEADER_H) / NUM_ROWS);
  const LEG_X = TREEMAP_W + GAP;
  const LEG_NAME_MAX_X = LEG_X + 240;
  const LEG_VAL_X = LEG_X + LEG_W - 60;
  const LEG_PCT_X = LEG_X + LEG_W;
  const FONT = "'Rawline', system-ui, sans-serif";

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(v);

  // @ts-ignore
  function contrastColor(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.55 ? '#1a1a1a' : '#ffffff';
  }

  const palette15 = [
    ...categorical8,
    '#7ba0d4', '#f0956b', '#62a898', '#f9d878', '#c280a5', '#a8c860', '#de7872',
  ];

  // @ts-ignore
  const domainColorMap = new Map(fomentoDomainsRows.map((r, i) => [r.name, palette15[i]]));

  const root = hierarchy({ children: fomentoDomainsRows })
    .sum((/** @type {{ value?: number }} */ d) => d.value ?? 0)
    .sort((/** @type {{ value?: number }} */ a, /** @type {{ value?: number }} */ b) => (b.value ?? 0) - (a.value ?? 0));

  d3treemap()
    .size([TREEMAP_W, TREEMAP_H])
    .padding(2)
    .paddingOuter(4)(root);

  // @ts-ignore
  const leaves = root.leaves();

  const { Story } = defineMeta({
    title: 'Section 6/fomentoDomainsTreemap',
    component: {},
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuicao por Dominio — Fomento Cultural (legenda lateral)**

Versao alternativa com legenda posicionada ao lado direito do treemap.

**Fonte**: \`capitulo_6_grafico_3.csv\`
          `,
        },
      },
    },
  });
</script>

<Story name="Treemap — Dominios (legenda lateral)">
  {#snippet template()}
    <svg width={TOTAL_W} height={TREEMAP_H} font-family={FONT} font-size="12" style="display:block;margin:0 16px">
      <defs>
        {#each leaves as leaf, i}
          {@const cw = leaf.x1 - leaf.x0}
          {@const ch = leaf.y1 - leaf.y0}
          <clipPath id="tms-clip-{i}">
            <rect x={leaf.x0 + 3} y={leaf.y0 + 3} width={Math.max(0, cw - 6)} height={Math.max(0, ch - 6)} />
          </clipPath>
        {/each}
      </defs>

      <!-- treemap cells -->
      {#each leaves as leaf, i}
        {@const w = leaf.x1 - leaf.x0}
        {@const h = leaf.y1 - leaf.y0}
        {@const cx = leaf.x0 + w / 2}
        {@const cy = leaf.y0 + h / 2}
        {@const color = domainColorMap.get(leaf.data.name) ?? categorical8[0]}
        {@const showBoth = w >= 90 && h >= 48}
        {@const isSmall = w < 45 || h < 20}
        {@const pctFontSize = isSmall ? 8 : 12}
        <rect x={leaf.x0} y={leaf.y0} width={w} height={h} fill={color} shape-rendering="crispEdges" />
        <text
          x={cx} y={showBoth ? cy - 7 : cy}
          text-anchor="middle" dominant-baseline="middle"
          fill={contrastColor(color)}
          font-size={pctFontSize} font-weight="700"
          pointer-events="none"
          clip-path={isSmall ? undefined : `url(#tms-clip-${i})`}
        >{leaf.data.pct.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%</text>
        {#if showBoth}
          <text
            x={cx} y={cy + 10}
            text-anchor="middle" dominant-baseline="middle"
            fill={contrastColor(color)}
            font-size="9"
            pointer-events="none" clip-path="url(#tms-clip-{i})"
          >{leaf.data.name}</text>
        {/if}
      {/each}

      <!-- legend column headers -->
      <text x={LEG_X + 18} y={12} fill="var(--chart-fg-muted, #666)" font-size="10">Dominio</text>
      <text x={LEG_VAL_X} y={12} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">Valor estimado</text>
      <text x={LEG_PCT_X} y={12} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">%</text>
      <line x1={LEG_X} y1={HEADER_H} x2={LEG_X + LEG_W} y2={HEADER_H} stroke="var(--chart-grid, #e0e0e0)" />

      <!-- legend rows -->
      {#each fomentoDomainsRows as row, i}
        {@const ry = HEADER_H + i * LEG_ROW_H}
        {@const cy = ry + LEG_ROW_H / 2}
        {@const color = palette15[i]}
        {#if i > 0}
          <line x1={LEG_X} y1={ry} x2={LEG_X + LEG_W} y2={ry} stroke="var(--chart-grid, #e0e0e0)" stroke-opacity="0.6" />
        {/if}
        <rect x={LEG_X} y={cy - 5} width={10} height={10} rx="2" fill={color} />
        <text x={LEG_X + 18} y={cy - 2} dominant-baseline="middle" fill="var(--chart-fg, #1a1a1a)" font-size="11">{row.name}</text>
        <text x={LEG_X + 18} y={cy + 12} dominant-baseline="middle" fill="var(--chart-fg-muted, #666)" font-size="9">IC95%: {formatBRL(row.p025)} – {formatBRL(row.p975)}</text>
        <text x={LEG_VAL_X} y={cy} dominant-baseline="middle" text-anchor="end" fill="var(--chart-fg-strong, #111)" font-weight="600" font-size="11">{formatBRL(row.value)}</text>
        <text x={LEG_PCT_X} y={cy} dominant-baseline="middle" text-anchor="end" fill={color} font-size="12" font-weight="700">{row.pct.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%</text>
      {/each}
    </svg>
  {/snippet}
</Story>
