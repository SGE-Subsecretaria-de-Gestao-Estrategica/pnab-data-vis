<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { hierarchy, treemap as d3treemap } from 'd3-hierarchy';
  // @ts-ignore
  import { fomentoDomainsRows } from '$lib/data/section6';

  const TW = 728; // treemap width (760 - 32px margins)
  const TREEMAP_H = 480;
  const TREEMAP_LEG_SEP = 28;
  const TREEMAP_LEG_ROW_H = 44;
  const TOTAL_H = TREEMAP_H + TREEMAP_LEG_SEP + fomentoDomainsRows.length * TREEMAP_LEG_ROW_H + 8;
  const LEG_VAL_X = TW - 150;
  const LEG_PCT_X = TW - 4;
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

  // 15-color palette: categorical8 + 7 lighter variants to avoid repeats
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
    .size([TW, TREEMAP_H])
    .padding(2)
    .paddingOuter(4)(root);

  // @ts-ignore
  const leaves = root.leaves();

  const { Story } = defineMeta({
    title: 'Section 6/Grafico 37',
    component: {},
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição por Domínio — Fomento Cultural**

Valor estimado investido por domínio cultural no âmbito do Fomento Cultural.

Os três maiores domínios — Festivais, feiras e mercados (~20,7%), Artes Cênicas (~17,8%) e Educação Artística e Cultural (~12,8%) — concentram mais da metade dos recursos.

**Fonte**: \`capitulo_6_grafico_3.csv\`
          `,
        },
      },
    },
  });
</script>

<Story name="Treemap — Domínios de Fomento Cultural">
  {#snippet template()}
    <svg width={TW} height={TOTAL_H} font-family={FONT} font-size="12" style="display:block;margin:0 16px">
      <defs>
        {#each leaves as leaf, i}
          {@const cw = leaf.x1 - leaf.x0}
          {@const ch = leaf.y1 - leaf.y0}
          <clipPath id="tm-clip-{i}">
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
          clip-path={isSmall ? undefined : `url(#tm-clip-${i})`}
        >{leaf.data.pct.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%</text>
        {#if showBoth}
          <text
            x={cx} y={cy + 10}
            text-anchor="middle" dominant-baseline="middle"
            fill={contrastColor(color)}
            font-size="9"
            pointer-events="none" clip-path="url(#tm-clip-{i})"
          >{leaf.data.name}</text>
        {/if}
      {/each}

      <!-- legend separator -->
      <line x1={0} y1={TREEMAP_H + 12} x2={TW} y2={TREEMAP_H + 12} stroke="var(--chart-grid, #e0e0e0)" />

      <!-- legend column headers -->
      <text x={LEG_VAL_X} y={TREEMAP_H + 24} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">Valor estimado (IC95%)</text>
      <text x={LEG_PCT_X} y={TREEMAP_H + 24} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">% do total</text>

      <!-- legend rows -->
      {#each fomentoDomainsRows as row, i}
        {@const ry = TREEMAP_H + TREEMAP_LEG_SEP + 16 + i * TREEMAP_LEG_ROW_H}
        {@const color = palette15[i]}
        {#if i > 0}
          <line x1={0} y1={ry - 6} x2={TW} y2={ry - 6} stroke="var(--chart-grid, #e0e0e0)" />
        {/if}
        <rect x={0} y={ry + 1} width={10} height={10} rx="2" fill={color} />
        <text x={18} y={ry + 6} dy="0.35em" fill="var(--chart-fg, #1a1a1a)">{row.name}</text>
        <text x={LEG_VAL_X} y={ry}      dy="0.85em" text-anchor="end" fill="var(--chart-fg-strong, #111)" font-weight="600">{formatBRL(row.value)}</text>
        <text x={LEG_VAL_X} y={ry + 16} dy="0.85em" text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">IC95%: {formatBRL(row.p025)} – {formatBRL(row.p975)}</text>
        <text x={LEG_PCT_X} y={ry + 6}  dy="0.35em" text-anchor="end" fill={color} font-size="13" font-weight="700">{row.pct.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%</text>
      {/each}
    </svg>
  {/snippet}
</Story>
