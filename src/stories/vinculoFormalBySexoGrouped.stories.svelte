<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import VerticalGroupedBarChart from '$lib/components/VerticalGroupedBarChart.svelte';
  import { colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { sexoVinculoFormalGroupedData } from '$lib/data/section4';

  // Feminino: red, Masculino: purple — from sniic palette
  const colors = [colorScales.lime[2], colorScales.red[2]];
  const seriesLabels = ['Feminino', 'Masculino'];

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalBySexoGrouped',
    component: VerticalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Homens dominam o vínculo formal, tanto no PNAB quanto no Brasil**

Entre os contemplados pelo PNAB com vínculo formal, **58,3%** são homens e **41,7%** são mulheres. A distribuição no mercado formal brasileiro (RAIS 2024) é de **55% homens e 45% mulheres** — mostrando que a desigualdade de gênero na formalização é ainda mais acentuada entre os beneficiários do programa.
          `,
        },
      },
    },
  });
</script>

<Story name="Vínculo formal por sexo — PNAB vs. Brasil">
  {#snippet template()}
    <VerticalGroupedBarChart
      data={sexoVinculoFormalGroupedData}
      seriesLabels={seriesLabels}
      colors={colors}
      format={(v) => `${v.toFixed(1)}%`}
      barWidth={40}
      barPad={8}
      innerH={280}
      margin={{ top: 20, right: 20, bottom: 10, left: 64 }}
    />
  {/snippet}
</Story>
