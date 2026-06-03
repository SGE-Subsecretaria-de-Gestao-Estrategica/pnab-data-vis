<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  // @ts-ignore
  import { faixaGroupedData } from '$lib/data/section2';

  const seriesLabels = ['Número de Contemplados', 'Recurso Executado'];
  const colors = ['#c0504d', '#4472c4'];

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 2/faixaGrouped',
    component: HorizontalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição de pagamentos e recursos por faixa de valor (nacional)**

A maioria dos contemplados (**71,6%**) recebeu valores até R$ 10 mil, mas esse grupo representou apenas **15,2%** dos recursos totais. A maior parte do recurso (**31,5%**) foi destinada à faixa de R$ 10 mil a R$ 50 mil. Contemplados acima de R$ 200 mil representam somente **0,8%** dos pagamentos.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras horizontais agrupadas — Faixa de valor nacional">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={faixaGroupedData}
      seriesLabels={seriesLabels}
      colors={colors}
      format={formatPct}
      margin={{ top: 30, right: 90, bottom: 60, left: 160 }}
      barHeight={18}
      barPad={5}
      legendBottom={true}
    />
  {/snippet}
</Story>
