<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import {
    TreemapChart,
    BubbleChart,
    DivergingBarChart,
    HorizontalBarChart,
    categorical8,
    colorPairs,
    colorScales,
  } from 'sniic-design-system';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  // @ts-ignore
  import { hierarchy, treemap as d3treemap } from 'd3-hierarchy';
  import {
    porteTreemapData,
    porteDivergingData,
    porteBubbleData,
    porteStackedKeys,
    porteStackedLabels,
    porteStackedData,
    porteRaw,
    porteMeanData,
  } from '$lib/data/section1';

  // @ts-ignore
  const formatBRLM  = (v) => `R$ ${(v / 1e6).toFixed(1)}M`;
  // @ts-ignore
  const formatBRLpc = (v) =>
    `R$ ${v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

  // ── Fixed porte color palette ──────────────────────────────────────────────
  const PORTE_NAME_COLORS = {
    'Grande':     categorical8[0], // azul
    'Médio':      categorical8[3], // amarelo
    'Pequeno I':  categorical8[1], // laranja
    'Pequeno II': categorical8[2], // verde
  };
  // @ts-ignore
  const PORTE_KEY_COLORS = {
    grande:     categorical8[0],
    medio:      categorical8[3],
    pequeno_i:  categorical8[1],
    pequeno_ii: categorical8[2],
  };

  // ── Treemap SVG (pre-computed at fixed width for export) ───────────────────
  const TM_W_PORTE = 728;
  const TM_H_PORTE = 420;

  // @ts-ignore
  function contrastColor(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.55 ? '#1a1a1a' : '#ffffff';
  }

  const porteRoot = hierarchy({ children: porteTreemapData.children })
    .sum((/** @type {{value?: number}} */ d) => d.value ?? 0)
    .sort((/** @type {{value?: number}} */ a, /** @type {{value?: number}} */ b) => (b.value ?? 0) - (a.value ?? 0));
  d3treemap().size([TM_W_PORTE, TM_H_PORTE]).padding(2).paddingOuter(4)(porteRoot);
  // @ts-ignore
  const porteLeaves = porteRoot.leaves();
  // Color map keyed by name from fixed palette
  // @ts-ignore
  const porteColorMap = new Map(porteLeaves.map((l) => [l.data.name, PORTE_NAME_COLORS[l.data.name] ?? categorical8[0]]));
  // @ts-ignore
  const porteRawByName = new Map(porteRaw.map((d) => [d.porte, d]));
  // @ts-ignore
  const porteLegendSorted = porteLeaves.map((l) => {
    const raw = porteRawByName.get(l.data.name);
    return {
      label: l.data.name,
      color: PORTE_NAME_COLORS[l.data.name] ?? categorical8[0],
      value: raw?.valor_total ?? 0,
      perc:  raw?.perc_valor  ?? 0,
    };
  });

  const PORTE_LEG_SEP    = 28;
  const PORTE_LEG_ROW_H  = 28;
  const LEG_INDENT       = 4; // matches paddingOuter(4) of the treemap
  const LEG_VAL_X        = TM_W_PORTE - 130;
  const LEG_PCT_X        = TM_W_PORTE - 4;
  const TM_TOTAL_H_PORTE = TM_H_PORTE + PORTE_LEG_SEP + porteLegendSorted.length * PORTE_LEG_ROW_H + 8;

  // Colors in key/data order for each chart type
  // @ts-ignore
  const porteStackedColors = porteStackedKeys.map((k) => PORTE_KEY_COLORS[k]);
  // @ts-ignore
  const porteBubbleColors  = porteRaw.map((d) => PORTE_NAME_COLORS[d.porte]);

  // ── Bars — Métricas por Porte (stacked) ────────────────────────────────────
  const pmKeys    = ['pequeno_i', 'pequeno_ii', 'medio', 'grande'];
  // @ts-ignore
  const pmColors  = pmKeys.map((k) => PORTE_KEY_COLORS[k]);
  const pmLabels  = { grande: 'Grande', pequeno_i: 'Pequeno I', pequeno_ii: 'Pequeno II', medio: 'Médio' };
  const pmByLabel = Object.fromEntries(porteMeanData.map((d) => [d.label, d]));
  const pmTotalMun   = porteMeanData.reduce((s, d) => s + d.municipios, 0);
  const pmMedianData = porteMeanData.map((d) => ({ label: d.label, value: d.valor_mediano }));
  const _g   = pmByLabel['Grande']    || { municipios: 0, perc_quantidade: 0, perc_valor: 0 };
  const _pi  = pmByLabel['Pequeno I'] || { municipios: 0, perc_quantidade: 0, perc_valor: 0 };
  const _pii = pmByLabel['Pequeno II']|| { municipios: 0, perc_quantidade: 0, perc_valor: 0 };
  const _m   = pmByLabel['Médio']     || { municipios: 0, perc_quantidade: 0, perc_valor: 0 };

  // ── Stacked — Recurso e Contemplados por Porte ─────────────────────────────
  const pmPercStackedData = [
    {
      cat: '% do recurso executado',
      grande:     _g.perc_valor,
      pequeno_i:  _pi.perc_valor,
      pequeno_ii: _pii.perc_valor,
      medio:      _m.perc_valor,
    },
    {
      cat: '% dos contemplados',
      grande:     _g.perc_quantidade,
      pequeno_i:  _pi.perc_quantidade,
      pequeno_ii: _pii.perc_quantidade,
      medio:      _m.perc_quantidade,
    },
  ];
  const pmStackedData = [
    {
      cat: 'Municípios (%)',
      grande:     _g.municipios   / pmTotalMun * 100,
      pequeno_i:  _pi.municipios  / pmTotalMun * 100,
      pequeno_ii: _pii.municipios / pmTotalMun * 100,
      medio:      _m.municipios   / pmTotalMun * 100,
    },
    {
      cat: 'Beneficiários (%)',
      grande:     _g.perc_quantidade,
      pequeno_i:  _pi.perc_quantidade,
      pequeno_ii: _pii.perc_quantidade,
      medio:      _m.perc_quantidade,
    },
    {
      cat: 'Valor investido (%)',
      grande:     _g.perc_valor,
      pequeno_i:  _pi.perc_valor,
      pequeno_ii: _pii.perc_valor,
      medio:      _m.perc_valor,
    },
  ];

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);

  // @ts-ignore
  const formatPerc = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 1/valuesByPopulationSize',
    component: TreemapChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Porte municipal: municípios grandes recebem mais do que representam**

O PNAB atendeu municípios de todos os portes populacionais — mas os números revelam uma assimetria profunda.

Os **332 municípios de grande porte** (acima de 100 mil habitantes) concentraram **52,5% do valor total investido**. Os **3.401 municípios Pequenos I** (até 20 mil habitantes), sendo mais de dez vezes mais cidades, receberam apenas **19,1%**.

O gráfico de barras empilhadas torna explícita essa lacuna de equidade: municípios grandes têm uma fatia de valor muito superior à sua fatia de beneficiários (52,5% do valor vs. 21,6% dos beneficiários). Municípios Pequenos I e II têm o padrão inverso — atendem mais pessoas proporcionalmente do que o valor que recebem.

O gráfico de bolhas complementa esse retrato: municípios pequenos são muitos, mas recebem pouco — e atendem muitos beneficiários com poucos recursos.
          `,
        },
      },
    },
  });
</script>

<Story name="Treemap — Distribuição de Valores por Porte">
  {#snippet template()}
    <svg width={TM_W_PORTE} height={TM_TOTAL_H_PORTE} font-family="'Space Grotesk', system-ui, sans-serif" font-size="12" style="display:block">
      {#each porteLeaves as leaf}
        {@const w        = leaf.x1 - leaf.x0}
        {@const h        = leaf.y1 - leaf.y0}
        {@const cx       = leaf.x0 + w / 2}
        {@const cy       = leaf.y0 + h / 2}
        {@const color    = porteColorMap.get(leaf.data.name) ?? categorical8[0]}
        {@const showBoth = w >= 80 && h >= 40}
        {@const showVal  = w >= 40 && h >= 20}
        <rect x={leaf.x0} y={leaf.y0} width={w} height={h} fill={color} shape-rendering="crispEdges" />
        {#if showVal}
          <text x={cx} y={showBoth ? cy - 7 : cy}
                text-anchor="middle" dominant-baseline="middle"
                fill={contrastColor(color)} font-size="12" font-weight="700" pointer-events="none"
          >{formatBRL(leaf.data.value)}</text>
        {/if}
        {#if showBoth}
          <text x={cx} y={cy + 10}
                text-anchor="middle" dominant-baseline="middle"
                fill={contrastColor(color)} font-size="9" pointer-events="none"
          >{leaf.data.name}</text>
        {/if}
      {/each}

      <!-- legend separator -->
      <line x1={LEG_INDENT} y1={TM_H_PORTE + 12} x2={TM_W_PORTE} y2={TM_H_PORTE + 12} stroke="var(--chart-grid, #e0e0e0)" />

      <!-- legend column headers -->
      <text x={LEG_VAL_X} y={TM_H_PORTE + 22} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">Valor total</text>
      <text x={LEG_PCT_X} y={TM_H_PORTE + 22} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">% do total</text>

      <!-- legend rows -->
      {#each porteLegendSorted as item, i}
        {@const ry = TM_H_PORTE + PORTE_LEG_SEP + 16 + i * PORTE_LEG_ROW_H}
        {#if i > 0}
          <line x1={LEG_INDENT} y1={ry - 6} x2={TM_W_PORTE} y2={ry - 6} stroke="var(--chart-grid, #e0e0e0)" />
        {/if}
        <rect x={LEG_INDENT} y={ry + 1} width={10} height={10} rx="2" fill={item.color} />
        <text x={LEG_INDENT + 14} y={ry + 6} dy="0.35em" fill="var(--chart-fg, #1a1a1a)" font-size="12">{item.label}</text>
        <text x={LEG_VAL_X} y={ry + 6} dy="0.35em" text-anchor="end" fill="var(--chart-fg-strong, #111)" font-weight="600" font-size="12">{formatBRL(item.value)}</text>
        <text x={LEG_PCT_X} y={ry + 6} dy="0.35em" text-anchor="end" fill={item.color} font-size="13" font-weight="700">{item.perc.toFixed(1)}%</text>
      {/each}
    </svg>
  {/snippet}
</Story>

<Story name="Diverging Bars — Proporção Urbano vs Rural por Porte">
  {#snippet template()}
    <div style="overflow: hidden;">
      <div style="margin-left: -80px; width: calc(100% + 80px);">
        <DivergingBarChart
          data={porteDivergingData}
          leftLabel="Urbano"
          rightLabel="Rural"
          referenceValue={50}
          referenceLabel="50%"
          colors={colorPairs.blueOrange}
        />
      </div>
    </div>
  {/snippet}
</Story>

<Story name="Bubble — Municípios vs Valor Total (tamanho = beneficiários)">
  {#snippet template()}
    <BubbleChart
      data={porteBubbleData}
      xLabel="Nº de municípios"
      yLabel="Valor total (R$)"
      sizeLabel="Beneficiários"
      yFormat={(v) => `${(v / 1e6).toFixed(0)}M`}
      xFormat={(v) => v.toLocaleString('pt-BR')}
      colors={porteBubbleColors}
    />
  {/snippet}
</Story>

<Story name="Stacked Bars — Equidade: Valor Investido vs Beneficiários">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={porteStackedData}
      keys={porteStackedKeys}
      labels={porteStackedLabels}
      colors={porteStackedColors}
      format={formatPerc}
      showTotalLabel={true}
      marginLeft={180}
    />
  {/snippet}
</Story>

<Story name="Bars — Métricas por Porte">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={pmStackedData}
      keys={pmKeys}
      categoryKey="cat"
      labels={pmLabels}
      colors={pmColors}
      format={formatPerc}
      showTotalLabel={true}
      marginLeft={180}
    />
    <div style="margin-top: 1.5rem;">
      <HorizontalBarChart
        data={pmMedianData}
        color={colorScales.blue[2]}
        format={formatBRLpc}
        xLabel="Valor mediano por município (R$)"
        margin={{ top: 20, right: 120, bottom: 40, left: 120 }}
      />
    </div>
  {/snippet}
</Story>

<Story name="Stacked — Recurso e Contemplados por Porte">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={pmPercStackedData}
      keys={pmKeys}
      categoryKey="cat"
      labels={pmLabels}
      colors={pmColors}
      format={formatPerc}
      showTotalLabel={true}
      marginLeft={220}
    />
  {/snippet}
</Story>
