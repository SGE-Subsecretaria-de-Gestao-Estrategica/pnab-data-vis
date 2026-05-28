<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart, RegionSilhouetteChart, colorScales, categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { regionStackedData, regionSilhouetteData, ageGroupKeys, ageGroupLabels } from '$lib/data/section4';

  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;
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
      colors={[colorScales.red[2], colorScales.blue[2]]}
      format={formatPct}
      showTotalLabel={false}
    />
  {/snippet}
</Story>

<Story name="Silhueta — Beneficiários com vínculo formal por região">
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
