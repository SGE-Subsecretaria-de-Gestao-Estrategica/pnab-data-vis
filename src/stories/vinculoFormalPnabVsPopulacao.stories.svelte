<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  // @ts-ignore
  // import { ufIbgeByRegionData, ufIbgeRegionLegend, regionIbgeComparisonData, regionIbgeComparisonLegend } from '$lib/data/section4'; // CSV faltante: aggregate_vinculo_formal_labor_by_uf_ibge.csv

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalPnabVsPopulacao',
    component: HorizontalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Formalização dos contemplados PNAB vs. população geral por UF, agrupado por região**

Compara, para cada UF, o percentual de trabalhadores formais na população geral (RAIS 2024) com o percentual de contemplados pela PNAB que possuem vínculo formal. Estados agrupados por região, cada uma com sua família de cores.
          `,
        },
      },
    },
  });
</script>

<!-- DISABLED: aggregate_vinculo_formal_labor_by_uf_ibge.csv faltante
<Story name="PNAB vs. população geral — vínculo formal por UF e região">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={ufIbgeByRegionData}
      seriesLabels={[]}
      legendItems={ufIbgeRegionLegend}
      format={(v) => `${v.toFixed(1)}%`}
      xLabel="% do total nacional"
      margin={{ top: 16, right: 60, bottom: 150, left: 44 }}
      barHeight={7}
      barPad={2}
      legendBottom={true}
    />
  {/snippet}
</Story>

<Story name="Por região — PNAB vs. população geral">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={regionIbgeComparisonData}
      seriesLabels={[]}
      legendItems={regionIbgeComparisonLegend}
      format={(v) => `${v.toFixed(1)}%`}
      xLabel="% Agentes Culturais Contemplados com Vínculo Formal de Trabalho"
      margin={{ top: 16, right: 60, bottom: 56, left: 120 }}
      barHeight={18}
      barPad={5}
      legendBottom={true}
    />
  {/snippet}
</Story>
-->
