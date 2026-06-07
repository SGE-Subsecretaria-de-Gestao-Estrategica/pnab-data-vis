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

  const porteLegend = porteRaw.map((d, i) => ({ label: d.porte, color: categorical8[i] }));

  // ── Bars — Métricas por Porte (stacked) ────────────────────────────────────
  const pmKeys    = ['pequeno_i', 'pequeno_ii', 'medio', 'grande'];
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
    <div style="display:flex; flex-direction:column; gap:12px;">
      <TreemapChart
        data={porteTreemapData}
        height={420}
        format={formatBRL}
        colors={categorical8}
      />
      <div style="display:flex; flex-wrap:wrap; gap:16px; padding:0 8px;">
        {#each porteLegend as item}
          <span style="display:flex; align-items:center; gap:6px; font-size:13px; font-family:system-ui, sans-serif;">
            <span style="display:inline-block; width:12px; height:12px; border-radius:2px; background:{item.color};"></span>
            {item.label}
          </span>
        {/each}
      </div>
    </div>
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
      colors={categorical8}
    />
  {/snippet}
</Story>

<Story name="Stacked Bars — Equidade: Valor Investido vs Beneficiários">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={porteStackedData}
      keys={porteStackedKeys}
      labels={porteStackedLabels}
      colors={categorical8}
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
      colors={categorical8}
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
      colors={categorical8}
      format={formatPerc}
      showTotalLabel={true}
      marginLeft={220}
    />
  {/snippet}
</Story>
