<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, categorical8, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { hierarchy, treemap as d3treemap } from 'd3-hierarchy';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  // @ts-ignore
  import { racaCorGroupedData, racaCorComparisonGroupedData, racaCorTreemapData, racaCorTreemapValorData } from '$lib/data/section4';

  // @ts-ignore
  const formatN = (v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const FONT  = "'Rawline', system-ui, sans-serif";
  const TM_W  = 728;
  const TM_H  = 380;

  // Color map keyed by name (original children order) so both treemaps share the same palette
  const racaColorMap = new Map(
    racaCorTreemapData.children.map((/** @type {{name:string}} */ d, i) => [d.name, categorical8[i % categorical8.length]])
  );

  // @ts-ignore
  function contrastColor(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.55 ? '#1a1a1a' : '#ffffff';
  }

  // Pre-compute treemap layouts at fixed width (no reactive state needed in stories)
  // @ts-ignore
  function buildLeaves(data) {
    const root = hierarchy({ children: data.children })
      .sum((/** @type {{value?: number}} */ d) => d.value ?? 0)
      .sort((/** @type {{value?: number}} */ a, /** @type {{value?: number}} */ b) => (b.value ?? 0) - (a.value ?? 0));
    d3treemap().size([TM_W, TM_H]).padding(2).paddingOuter(4)(root);
    return root.leaves();
  }
  const racaLeaves      = buildLeaves(racaCorTreemapData);
  const racaValorLeaves = buildLeaves(racaCorTreemapValorData);

  // Legend: original children order keeps color consistency across both treemaps
  const racaLegend = racaCorTreemapData.children.map((/** @type {{name:string}} */ d, i) => ({
    label: d.name,
    color: categorical8[i % categorical8.length],
  }));

  const ITEMS_PER_ROW = 5;           // 5 short labels fit in 728px
  const ITEM_W        = Math.floor(TM_W / ITEMS_PER_ROW);
  const LEG_SEP       = 12;
  const LEG_ROW_H     = 22;
  const legRows       = Math.ceil(racaLegend.length / ITEMS_PER_ROW);
  const TOTAL_H       = TM_H + LEG_SEP + legRows * LEG_ROW_H;

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalByRaca',
    component: HorizontalBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Pardos e brancos dominam o emprego formal no setor cultural**

Entre os beneficiários com vínculo formal, **pardos** respondem por 44,9% e **brancos** por 30,3%. **Pretos/negros** representam apenas 9,6% — desproporcionalmente baixo em relação à presença na população geral.

O treemap torna visível a concentração: Parda e Branca juntas ocupam mais de três quartos do espaço.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras — Beneficiarios com vinculo formal por raca/cor">
  {#snippet template()}
    <HorizontalGroupedBarChart width={600}
      data={racaCorGroupedData}
      seriesLabels={['PNAB', 'Total Trabalhadores Formais']}
      colors={[colorScales.lime[2], colorScales.red[2]]}
      format={formatN}
      xLabel="% do total de trabalhadores formais"
      margin={{ top: 20, right: 60, bottom: 40, left: 120 }}
    />
  {/snippet}
</Story>

<Story name="Grafico 26 — Raca/cor PNAB vs RAIS">
  {#snippet template()}
    <HorizontalGroupedBarChart width={600}
      data={racaCorComparisonGroupedData}
      seriesLabels={['Contemplados', 'Total RAIS']}
      colors={[colorScales.yellow[2], colorScales.blue[2]]}
      format={formatN}
      xLabel="% do total"
      margin={{ top: 20, right: 80, bottom: 40, left: 120 }}
      barHeight={34}
      rx={0}
      crispEdges
      labelsInside
      legendBottom={true}
    />
  {/snippet}
</Story>

<Story name="Treemap — Proporção por raça/cor">
  {#snippet template()}
    <svg width={TM_W} height={TOTAL_H} font-family={FONT} font-size="12" style="display:block">
      {#each racaLeaves as leaf}
        {@const w        = leaf.x1 - leaf.x0}
        {@const h        = leaf.y1 - leaf.y0}
        {@const cx       = leaf.x0 + w / 2}
        {@const cy       = leaf.y0 + h / 2}
        {@const color    = racaColorMap.get(leaf.data.name) ?? categorical8[0]}
        {@const showBoth = w >= 80 && h >= 40}
        {@const showVal  = w >= 40 && h >= 20}
        <rect x={leaf.x0} y={leaf.y0} width={w} height={h} fill={color} shape-rendering="crispEdges" />
        {#if showVal}
          <text x={cx} y={showBoth ? cy - 7 : cy}
                text-anchor="middle" dominant-baseline="middle"
                fill={contrastColor(color)} font-size="12" font-weight="700" pointer-events="none"
          >{formatN(leaf.data.value)}</text>
        {/if}
        {#if showBoth}
          <text x={cx} y={cy + 10}
                text-anchor="middle" dominant-baseline="middle"
                fill={contrastColor(color)} font-size="9" pointer-events="none"
          >{leaf.data.name}</text>
        {/if}
      {/each}

      <!-- legend -->
      {#each racaLegend as item, i}
        {@const col = i % ITEMS_PER_ROW}
        {@const row = Math.floor(i / ITEMS_PER_ROW)}
        {@const lx  = col * ITEM_W}
        {@const ly  = TM_H + LEG_SEP + row * LEG_ROW_H}
        <rect x={lx} y={ly + 1} width={10} height={10} rx="2" fill={item.color} />
        <text x={lx + 16} y={ly + 6} dy="0.35em" fill="#1a1a1a" font-size="12">{item.label}</text>
      {/each}
    </svg>
  {/snippet}
</Story>

<Story name="Treemap — Valor pago por raça/cor">
  {#snippet template()}
    <svg width={TM_W} height={TOTAL_H} font-family={FONT} font-size="12" style="display:block">
      {#each racaValorLeaves as leaf}
        {@const w        = leaf.x1 - leaf.x0}
        {@const h        = leaf.y1 - leaf.y0}
        {@const cx       = leaf.x0 + w / 2}
        {@const cy       = leaf.y0 + h / 2}
        {@const color    = racaColorMap.get(leaf.data.name) ?? categorical8[0]}
        {@const showBoth = w >= 80 && h >= 40}
        {@const showVal  = w >= 40 && h >= 20}
        <rect x={leaf.x0} y={leaf.y0} width={w} height={h} fill={color} shape-rendering="crispEdges" />
        {#if showVal}
          <text x={cx} y={showBoth ? cy - 7 : cy}
                text-anchor="middle" dominant-baseline="middle"
                fill={contrastColor(color)} font-size="12" font-weight="700" pointer-events="none"
          >{formatN(leaf.data.value)}</text>
        {/if}
        {#if showBoth}
          <text x={cx} y={cy + 10}
                text-anchor="middle" dominant-baseline="middle"
                fill={contrastColor(color)} font-size="9" pointer-events="none"
          >{leaf.data.name}</text>
        {/if}
      {/each}

      <!-- legend -->
      {#each racaLegend as item, i}
        {@const col = i % ITEMS_PER_ROW}
        {@const row = Math.floor(i / ITEMS_PER_ROW)}
        {@const lx  = col * ITEM_W}
        {@const ly  = TM_H + LEG_SEP + row * LEG_ROW_H}
        <rect x={lx} y={ly + 1} width={10} height={10} rx="2" fill={item.color} />
        <text x={lx + 16} y={ly + 6} dy="0.35em" fill="#1a1a1a" font-size="12">{item.label}</text>
      {/each}
    </svg>
  {/snippet}
</Story>
