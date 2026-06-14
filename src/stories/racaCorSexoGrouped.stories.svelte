<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  import { colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { racaCorSexoGroupedData } from '$lib/data/section4';

  const seriesLabels = ['Feminino', 'Masculino'];
  const colors = [colorScales.lime[2], colorScales.red[2]];

  const { Story } = defineMeta({
    title: 'Section 4/racaCorSexoGrouped',
    component: HorizontalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Pardos e brancos dominam, com desigualdade entre sexos em todos os grupos**

Em todos os grupos raciais, **homens superam mulheres** tanto em quantidade de beneficiários com vínculo formal quanto em valor pago. O maior grupo é o de **homens pardos** (31,3% do total), seguido de **homens brancos** (19,1%). Mulheres pretas/negras têm participação proporcionalmente maior no valor pago (7,6%) do que na quantidade (4,4%), sugerindo valores médios mais altos nesse subgrupo.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras horizontais agrupadas — Raça/cor por sexo">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={racaCorSexoGroupedData}
      seriesLabels={seriesLabels}
      colors={colors}
      xLabel="% do total de beneficiários com vínculo formal"
      margin={{ top: 20, right: 80, bottom: 40, left: 120 }}
      barHeight={12}
      barPad={4}
      legendBottom={true}
    />
  {/snippet}
</Story>
