<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { ageGroupStackedData, ageGroupKeys, ageGroupLabels } from '$lib/data/section4';

  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalByAge',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Trabalhadores mais velhos têm muito menos vínculo formal**

A faixa de **25 a 54 anos** é a única em que a maioria dos beneficiários possui vínculo formal (51,7%). Entre os **idosos (65+)**, a informalidade atinge **88%** — reflexo de carreiras construídas inteiramente fora do mercado formal ao longo de décadas no setor cultural.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras empilhadas — Sem vs. com vínculo por faixa etária">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={ageGroupStackedData}
      keys={[...ageGroupKeys]}
      labels={ageGroupLabels}
      colors={[colorScales.red[2], colorScales.blue[2]]}
      format={formatPct}
      showTotalLabel={false}
    />
  {/snippet}
</Story>
