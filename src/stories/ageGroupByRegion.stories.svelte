<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { GroupedColumnChart, categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { ageGroupRegionData, ageGroupRegionKeys, ageGroupRegionLabels } from '$lib/data/section3';

  // @ts-ignore
  const formatNum = (v) => v.toLocaleString('pt-BR');

  const { Story } = defineMeta({
    title: 'Section 3/ageGroupByRegion',
    component: GroupedColumnChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Nordeste lidera em todas as faixas etárias**

O gráfico de colunas agrupadas compara a quantidade de agentes culturais contemplados por faixa etária em cada região do Brasil.

Em todas as faixas etárias, o **Nordeste** concentra o maior número de contemplados — reflexo tanto de sua população como dos critérios redistributivos do programa. O **Sudeste** aparece consistentemente em segundo lugar, enquanto o **Centro-Oeste** registra os menores volumes em todas as faixas.

A faixa de **25 a 54 anos** é dominante em todas as regiões, confirmando o padrão nacional visto na pirâmide etária: o programa alcança principalmente a população economicamente ativa do setor cultural.
          `,
        },
      },
    },
  });
</script>

<Story name="Agentes culturais por faixa etária e região">
  {#snippet template()}
    <GroupedColumnChart
      data={ageGroupRegionData}
      keys={ageGroupRegionKeys}
      categoryKey="faixa_etaria"
      labels={ageGroupRegionLabels}
      colors={categorical8}
      format={formatNum}
      height={420}
    />
  {/snippet}
</Story>
