<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  import { categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { naturezaJuridicaRegiaoData, naturezaJuridicaSeriesLabels } from '$lib/data/section3';

  const { Story } = defineMeta({
    title: 'Section 3/naturezaJuridicaByRegion',
    component: HorizontalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Natureza jurídica das pessoas jurídicas contempladas por região**

Percentual de CNPJs contemplados por natureza jurídica dentro de cada região do Brasil.

As **entidades sem fins lucrativos** lideram em volume de recursos em todas as regiões. **MEIs e microempresas** juntos representam a maioria dos contemplados em quantidade, especialmente no Sudeste e no Sul.
          `,
        },
      },
    },
  });
</script>

<Story name="Percentual por natureza juridica e regiao">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={naturezaJuridicaRegiaoData}
      seriesLabels={naturezaJuridicaSeriesLabels}
      colors={categorical8.slice(0, 6)}
      margin={{ top: 20, right: 80, bottom: 40, left: 110 }}
      barHeight={12}
      barPad={3}
      legendBottom={true}
    />
  {/snippet}
</Story>
