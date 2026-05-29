<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import {
    TreemapChart,
    BubbleChart,
    DivergingBarChart,
    HorizontalStackedBarChart,
    categorical8,
    colorPairs,
  } from 'sniic-design-system';
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

  const pmMaxTotal = Math.max(...porteMeanData.map((d) => d.total));
  const pmMaxAvg   = Math.max(...porteMeanData.map((d) => d.value));
  const pmBarW     = 290;
  const pmRowH     = 82;
  const pmLabelW   = 150;

  const porteLegend = porteRaw.map((d, i) => ({ label: d.porte, color: categorical8[i] }));

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
    <div style="padding-left: 100px;">
      <HorizontalStackedBarChart
        data={porteStackedData}
        keys={porteStackedKeys}
        labels={porteStackedLabels}
        colors={categorical8}
        format={formatPerc}
        showTotalLabel={true}
      />
    </div>
  {/snippet}
</Story>

<Story name="Dual Bars — Valor Total e Médio por Porte">
  {#snippet template()}
    <svg
      viewBox="0 0 560 {30 + porteMeanData.length * pmRowH}"
      style="width: 100%; max-width: 560px; overflow: visible; display: block; font-family: system-ui, sans-serif;"
      role="img"
      aria-label="Valor total e médio por porte de município"
    >
      <!-- Legend -->
      <rect x={pmLabelW}       y={2}  width={12} height={12} fill={categorical8[0]} rx={2} />
      <text x={pmLabelW + 16}  y={12} font-size="10" fill="#334155" dominant-baseline="middle">Valor total executado</text>
      <rect x={pmLabelW + 170} y={2}  width={12} height={12} fill={categorical8[2]} rx={2} />
      <text x={pmLabelW + 186} y={12} font-size="10" fill="#334155" dominant-baseline="middle">Valor médio por município</text>

      {#each porteMeanData as d, i}
        {@const rowY   = 30 + i * pmRowH}
        {@const wTotal = (d.total / pmMaxTotal) * pmBarW}
        {@const wAvg   = (d.value / pmMaxAvg)   * pmBarW}

        <!-- Category label + municipality count -->
        <text x={0} y={rowY + 14} font-size="13" font-weight="700" fill="#334155" dominant-baseline="middle">{d.label}</text>
        <text x={0} y={rowY + 30} font-size="11" fill="#334155" opacity="0.55" dominant-baseline="middle">{d.qtd.toLocaleString('pt-BR')} municípios</text>

        <!-- Total value bar -->
        <rect x={pmLabelW} y={rowY}      width={pmBarW} height={16} fill="#f1f5f9" rx={2} />
        <rect x={pmLabelW} y={rowY}      width={wTotal} height={16} fill={categorical8[0]} rx={2} />
        <text x={pmLabelW + wTotal + 6}  y={rowY + 12}  font-size="11" font-weight="600" fill="#334155" dominant-baseline="middle">{formatBRLM(d.total)}</text>

        <!-- Avg value bar -->
        <rect x={pmLabelW} y={rowY + 24} width={pmBarW} height={16} fill="#f1f5f9" rx={2} />
        <rect x={pmLabelW} y={rowY + 24} width={wAvg}   height={16} fill={categorical8[2]} rx={2} />
        <text x={pmLabelW + wAvg + 6}    y={rowY + 36}  font-size="11" font-weight="600" fill="#334155" dominant-baseline="middle">{formatBRLpc(d.value)}</text>

        <!-- Row divider -->
        {#if i < porteMeanData.length - 1}
          <line x1={0} y1={rowY + pmRowH - 8} x2={560} y2={rowY + pmRowH - 8} stroke="#e2e8f0" stroke-width={1} />
        {/if}
      {/each}
    </svg>
  {/snippet}
</Story>
