<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { GroupedColumnChart, categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { regionByAgeGroupPctData, ageGroupPctKeys } from '$lib/data/section3';

  // @ts-ignore
  const formatPct = (v) =>
    (v * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 3/regionByAgeGroup',
    component: GroupedColumnChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição de contemplados por faixa etária em cada região**

Percentual do total de agentes culturais contemplados, agrupado por região e faixa etária.

O **Nordeste** concentra os maiores volumes em todas as faixas, enquanto o **Centro-Oeste** registra os menores. A faixa **25–54 anos** é dominante em todas as regiões.
          `,
        },
      },
    },
  });
</script>

<Story name="Percentual de contemplados por região e faixa etária">
  {#snippet template()}
    <GroupedColumnChart
      data={regionByAgeGroupPctData}
      keys={ageGroupPctKeys}
      categoryKey="regiao"
      colors={categorical8}
      format={formatPct}
      height={420}
    />
  {/snippet}
</Story>
