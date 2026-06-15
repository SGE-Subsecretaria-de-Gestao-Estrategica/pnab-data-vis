<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HeatMap, colorScales, categorical8 } from 'sniic-design-system';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  // @ts-ignore
  import { racaCorSexoHeatmapData, racaCorSexoComparisonData } from '$lib/data/section4';

  // @ts-ignore
  const formatN = (v) => v.toLocaleString('pt-BR');
  // @ts-ignore
  const formatPctN = (v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalRacaSexo',
    component: HeatMap,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Intersecção raça e sexo: homens pardos lideram**

O cruzamento de raça/cor com sexo revela que **homens pardos** formam o maior grupo com vínculo formal (16.465), seguidos de **homens brancos** (10.045). Em todos os grupos raciais, os homens superam as mulheres — reforçando o padrão de desvantagem feminina no mercado formal de trabalho cultural.
          `,
        },
      },
    },
  });
</script>

<Story name="Heatmap — Raca-cor por sexo (azul)">
  {#snippet template()}
    <HeatMap
      data={racaCorSexoHeatmapData}
      height={320}
      colorRange={colorScales.lime}
      xLabel="Sexo"
      yLabel="Raça/cor"
      format={formatN}
      showValues={true}
      showLegend={true}
      cellRadius={3}
      cellGap={4}
    />
  {/snippet}
</Story>

<Story name="Heatmap — Raca-cor por sexo (teal)">
  {#snippet template()}
    <HeatMap
      data={racaCorSexoHeatmapData}
      height={320}
      colorRange={colorScales.red}
      xLabel="Sexo"
      yLabel="Raça/cor"
      format={formatN}
      showValues={true}
      showLegend={true}
      cellRadius={3}
      cellGap={4}
    />
  {/snippet}
</Story>

<Story name="Grafico 27 — Raca/cor por sexo PNAB">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={racaCorSexoComparisonData}
      seriesLabels={['Masculino', 'Feminino']}
      colors={[categorical8[0], '#cb4034']}
      format={formatPctN}
      xLabel="% do total de beneficiários com vínculo formal"
      margin={{ top: 20, right: 80, bottom: 40, left: 120 }}
      barHeight={20}
      rx={0}
      crispEdges
      labelsInside
      legendBottom={true}
    />
  {/snippet}
</Story>
