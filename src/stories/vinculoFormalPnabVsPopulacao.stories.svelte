<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { categorical8 } from 'sniic-design-system';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  // @ts-ignore
  import { ufComparisonGroupedData, regionComparisonGroupedData } from '$lib/data/section4';

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
      colors={[categorical8[0], '#cb4034']}
      format={formatPctN}
      xLabel="% do total"
      margin={{ top: 20, right: 80, bottom: 40, left: 50 }}
      barHeight={14}
      barPad={3}
      rx={0}
      crispEdges
      labelsInside
      legendBottom={true}
    />
  {/snippet}
</Story>

<Story name="Por regiao — PNAB vs RAIS">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={regionComparisonGroupedData}
      seriesLabels={['Contemplados PNAB', 'Vínculos RAIS 2024']}
      colors={[categorical8[0], '#cb4034']}
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
