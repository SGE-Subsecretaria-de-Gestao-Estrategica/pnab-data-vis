<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { GroupedColumnChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import {
    ageGroupValueQtyData,
    ageGroupValueQtyKeys,
    ageGroupValueQtyLabels,
  } from '$lib/data/section3';

  // @ts-ignore
  const formatPct = (v) =>
    (v * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  // valor = orange, quantidade = blue
  const colors = [colorScales.blue[2], colorScales.yellow[2]];

  const { Story } = defineMeta({
    title: 'Section 3/ageGroupValueQty',
    component: GroupedColumnChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição de valor e quantidade por faixa etária**

Comparação entre o percentual do valor total recebido e o percentual de agentes culturais contemplados, por faixa etária.

A faixa **25–54 anos** concentra cerca de **74,6%** do valor distribuído e **70,5%** dos contemplados. Jovens de **15–24 anos** recebem proporcionalmente menos valor (5,9%) do que sua participação em quantidade (8,0%), enquanto adultos de **55–64 anos** mostram o padrão inverso.
          `,
        },
      },
    },
  });
</script>

<Story name="Valor e quantidade por faixa etária (% do total)">
  {#snippet template()}
    <GroupedColumnChart
      data={ageGroupValueQtyData}
      keys={ageGroupValueQtyKeys}
      categoryKey="faixa_etaria"
      labels={ageGroupValueQtyLabels}
      colors={colors}
      format={formatPct}
      height={420}
    />
  {/snippet}
</Story>
