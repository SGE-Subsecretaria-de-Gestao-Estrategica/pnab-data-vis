<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart, RegionSilhouetteChart, colorScales, categorical8 } from 'sniic-design-system';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  // @ts-ignore
  import { regionStackedData, regionSilhouetteData, regionComparisonGroupedData, ageGroupKeys, ageGroupLabels } from '$lib/data/section4';

  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;
  // @ts-ignore
  const formatPctN = (v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';
  // @ts-ignore
  const formatN = (v) => v.toLocaleString('pt-BR');

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalByRegion',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Nordeste concentra a maior informalidade regional**

O **Nordeste** tem a maior proporção de beneficiários sem vínculo formal (58,5%). **Centro-Oeste** e **Norte** apresentam distribuição mais equilibrada, próxima de 50/50.

Em números absolutos, o Nordeste também lidera em beneficiários com vínculo formal — consequência do maior volume total de beneficiários na região.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras empilhadas — Sem vs. com vínculo por região">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={regionStackedData}
      keys={[...ageGroupKeys]}
      labels={ageGroupLabels}
      colors={[colorScales.red[2], colorScales.lime[2]]}
      format={formatPct}
      showTotalLabel={false}
    />
  {/snippet}
</Story>

<Story name="Silhueta — Beneficiarios com vinculo formal por regiao">
  {#snippet template()}
    <RegionSilhouetteChart
      data={regionSilhouetteData}
      maxSize={100}
      colors={categorical8}
      format={formatN}
      showLabels={true}
    />
  {/snippet}
</Story>

<Story name="Grafico 23 — Distribuicao por regiao PNAB vs RAIS">
  {#snippet template()}
    <HorizontalGroupedBarChart width={600}
      data={regionComparisonGroupedData}
      seriesLabels={['Contemplados PNAB', 'Vínculos RAIS 2024']}
      colors={[colorScales.yellow[2], colorScales.blue[2]]}
      format={formatPctN}
      xLabel="% do total"
      margin={{ top: 20, right: 80, bottom: 40, left: 120 }}
      barHeight={34}
      groupPad={24}
      rx={0}
      crispEdges
      labelsInside
      legendBottom={true}
    />
  {/snippet}
</Story>
