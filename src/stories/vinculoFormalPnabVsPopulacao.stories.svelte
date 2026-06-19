<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  import HorizontalDiffBarChart from '$lib/components/HorizontalDiffBarChart.svelte';
  import ConnectedDotPlot from '$lib/components/ConnectedDotPlot.svelte';
  // @ts-ignore
  import { ufComparisonGroupedData, regionComparisonGroupedData, ufDiffData } from '$lib/data/section4';

  // @ts-ignore
  const formatPctN = (v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalPnabVsPopulacao',
    component: HorizontalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Formalização dos contemplados PNAB vs. população geral por UF e região**

Compara, para cada UF e região, o percentual de contemplados pela PNAB com vínculo formal com o percentual de vínculos formais na RAIS 2024.
          `,
        },
      },
    },
  });
</script>

<Story name="Grafico 24 — Distribuicao por UF PNAB vs RAIS">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={ufComparisonGroupedData}
      seriesLabels={['Contemplados PNAB', 'Vínculos RAIS 2024']}
      colors={[colorScales.yellow[2], colorScales.blue[2]]}
      format={formatPctN}
      xLabel="% do total"
      margin={{ top: 20, right: 80, bottom: 40, left: 50 }}
      barHeight={34}
      barPad={4}
      rx={0}
      crispEdges
      labelsInside
      legendBottom={true}
    />
  {/snippet}
</Story>

<Story name="Grafico 24 variante — Diferenca PNAB menos RAIS por UF">
  {#snippet template()}
    <HorizontalDiffBarChart
      data={ufDiffData}
      colorPositive={colorScales.yellow[2]}
      colorNegative={colorScales.blue[2]}
      xLabel="Diferença percentual (PNAB − RAIS)"
      margin={{ top: 16, right: 70, bottom: 90, left: 50 }}
    />
  {/snippet}
</Story>

<Story name="Grafico 24 variante dot plot — PNAB vs RAIS por UF">
  {#snippet template()}
    <ConnectedDotPlot
      data={ufComparisonGroupedData}
      seriesLabels={['Contemplados PNAB', 'Vínculos RAIS 2024']}
      colors={[colorScales.yellow[2], colorScales.blue[2]]}
      format={formatPctN}
      margin={{ top: 20, right: 56, bottom: 56, left: 44 }}
      rowHeight={28}
      dotRadius={5}
    />
  {/snippet}
</Story>

<Story name="Por regiao — PNAB vs RAIS">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={regionComparisonGroupedData}
      seriesLabels={['Contemplados PNAB', 'Vínculos RAIS 2024']}
      colors={[colorScales.yellow[2], colorScales.blue[2]]}
      format={formatPctN}
      xLabel="% do total"
      margin={{ top: 20, right: 80, bottom: 40, left: 120 }}
      barHeight={20}
      rx={0}
      crispEdges
      labelsInside
      legendBottom={true}
    />
  {/snippet}
</Story>
