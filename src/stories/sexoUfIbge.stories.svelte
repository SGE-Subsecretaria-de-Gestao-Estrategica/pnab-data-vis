<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  import { colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { sexoUfData, sexoUfSeriesLabels } from '$lib/data/section3';

  const { Story } = defineMeta({
    title: 'Section 3/sexoUfIbge',
    component: HorizontalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição por sexo nas UFs: contemplados vs. população IBGE**

Comparação entre o percentual de agentes culturais pessoas físicas contemplados na Aldir Blanc por sexo e o percentual correspondente na população de cada Unidade Federativa, segundo o Censo 2022 do IBGE.

As cores claras representam a referência populacional (IBGE) e as cores cheias representam os contemplados.
          `,
        },
      },
    },
  });

  const colors = [
    colorScales.blue[1],
    colorScales.blue[2],
    colorScales.yellow[2],
    colorScales.yellow[3],
  ];
</script>

<Story name="Contemplados vs IBGE por sexo e UF">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={sexoUfData}
      seriesLabels={sexoUfSeriesLabels}
      {colors}
      format={(v) => v.toFixed(1) + '%'}
      xLabel="% do total de contemplados / população"
      margin={{ top: 20, right: 70, bottom: 44, left: 40 }}
      barHeight={10}
      barPad={3}
      legendBottom={true}
    />
  {/snippet}
</Story>
