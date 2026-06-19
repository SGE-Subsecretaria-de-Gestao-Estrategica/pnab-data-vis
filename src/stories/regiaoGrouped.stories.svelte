<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  import { colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { regiaoGroupedData } from '$lib/data/section2';

  const seriesLabels = ['% agentes contemplados', '% população'];
  const colors = [colorScales.blue[2], colorScales.purple[2]];

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 2/regiaoGrouped',
    component: HorizontalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição de agentes contemplados vs. população por região**

O Nordeste concentra **47,6%** dos contemplados, bem acima de sua participação populacional (**26,9%**). O Sudeste, com **41,7%** da população, recebeu apenas **27,4%** dos contemplados.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras horizontais agrupadas — Contemplados vs. população por região">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={regiaoGroupedData}
      seriesLabels={seriesLabels}
      colors={colors}
      format={formatPct}
      margin={{ top: 30, right: 90, bottom: 60, left: 140 }}
      barHeight={22}
      barPad={6}
      rx={0}
      legendBottom={true}
      labelsInside={true}
    />
  {/snippet}
</Story>
