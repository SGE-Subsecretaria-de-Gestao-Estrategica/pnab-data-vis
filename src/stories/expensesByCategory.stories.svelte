<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { MarimekkoChart, categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import {
    expensesChartData,
    expensesKeys,
    expensesLabels,
    expensesLegendItems,
    expensesGrandTotal,
  } from '$lib/data/section6';

  const CHART_HEIGHT = 520;
  const MARGIN = { top: 16, right: 16, bottom: 16, left: 16 };
  const COLUMN_GAP = 2;
  const INNER_H = CHART_HEIGHT - MARGIN.top - MARGIN.bottom; // 520 - 16 - 16 = 488
  const MIN_LABEL_HEIGHT = 28;

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

  const { Story } = defineMeta({
    title: 'Section 6/expensesByCategory',
    component: MarimekkoChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição dos recursos por tipo de despesa**

As três principais categorias — Fomento Cultural, Política Nacional de Cultura Viva e Subsídio e Manutenção de Espaços — concentram cerca de **88,4%** do total investido.

Os demais investimentos somam aproximadamente **R$ 154,6M**, distribuídos entre obras e reformas, operacionalização da política e outros gastos.
          `,
        },
      },
    },
  });
</script>

<Story name="Despesas por Categoria — Marimekko">
  {#snippet template()}
    {@const containerWidth = 900}
    {@const innerW = containerWidth - MARGIN.left - MARGIN.right}
    {@const totalWidth = expensesChartData.reduce((s, d) => s + d.total, 0)}
    {@const gapTotal = Math.max(0, expensesChartData.length - 1) * COLUMN_GAP}
    {@const availableW = innerW - gapTotal}
    <div style="max-width:{containerWidth}px;position:relative">
      <div style="overflow:hidden;height:{CHART_HEIGHT}px;width:100%">
        <MarimekkoChart
          data={expensesChartData}
          keys={expensesKeys}
          labels={expensesLabels}
          height={CHART_HEIGHT}
          format={formatBRL}
          margin={MARGIN}
          pctFormat={() => ''}
        />
      </div>

      <!-- category name overlay (fixed 900px width for storybook) -->
      {#each expensesChartData as datum, colIdx}
        {@const colW = datum.total / totalWidth * availableW}
        {@const colX = expensesChartData.slice(0, colIdx).reduce((s, d) => s + d.total / totalWidth * availableW + COLUMN_GAP, 0)}
        {@const segTotal = expensesKeys.reduce((s, k) => s + (Number(datum[k]) || 0), 0)}
        {#each expensesKeys as key, keyIdx}
          {@const value = Number(datum[key]) || 0}
          {#if value > 0}
            {@const h = (value / segTotal) * INNER_H}
            {@const segY = expensesKeys.slice(0, keyIdx).reduce((s, k) => s + (Number(datum[k]) || 0) / segTotal * INNER_H, 0)}
            {#if h >= MIN_LABEL_HEIGHT}
              {@const legendItem = expensesLegendItems.find((l) => l.key === key)}
              {@const color = categorical8[keyIdx]}
              {@const realValue = legendItem?.valor ?? value}
              {@const pct = (realValue / expensesGrandTotal * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}
              {@const showLabel = h >= 60 && colW >= 150}
              <div style="position:absolute;left:{MARGIN.left + colX}px;top:{MARGIN.top + segY}px;width:{colW}px;height:{h}px;pointer-events:none;overflow:hidden">
                <span style="position:absolute;top:50%;transform:translateY(-50%);left:0;right:0;text-align:center;font-family:'Space Grotesk',system-ui,sans-serif;font-size:0.72rem;font-weight:400;line-height:1.4;padding:0 8px;color:{contrastColor(color)}">
                  <strong style="display:block;font-size:0.9rem;font-weight:700">{pct}%</strong>
                  {#if showLabel}{legendItem?.label ?? key}{/if}
                </span>
              </div>
            {/if}
          {/if}
        {/each}
      {/each}
    </div>

    <div style="padding:0 16px;box-sizing:border-box">
      <table style="width:100%;border-collapse:collapse;margin-top:0.75rem;font-family:'Space Grotesk',system-ui,sans-serif;font-size:0.8rem">
        <tbody>
          {#each expensesLegendItems as item}
            {@const colorIdx = expensesKeys.indexOf(item.key)}
            <tr style="border-top:1px solid #e0e0e0">
              <td style="width:20px;padding:0.35rem 0.5rem 0.35rem 0;vertical-align:middle">
                <span style="display:inline-block;width:12px;height:12px;border-radius:2px;background:{categorical8[colorIdx]}"></span>
              </td>
              <td style="padding:0.35rem 1rem 0.35rem 0">{item.label}</td>
              <td style="padding:0.35rem 0;font-weight:600;text-align:right">
                {item.value}
                <span style="display:block;font-weight:400;font-size:0.7rem;color:#666;white-space:nowrap">({item.ci})</span>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/snippet}
</Story>
