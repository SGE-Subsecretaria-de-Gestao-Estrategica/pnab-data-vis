<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { categorical8 } from 'sniic-design-system';
  import DonutChartWithLegend from '$lib/components/DonutChartWithLegend.svelte';
  // @ts-ignore
  import { ageGroupDonutData, pyramidData } from '$lib/data/section3';

  // @ts-ignore
  const formatMi = (v) => {
    const mi = v / 1_000_000;
    return `R$ ${mi.toLocaleString('pt-BR', { maximumFractionDigits: 0 })} mi`;
  };

  const totalContemplados = pyramidData.reduce((s, d) => s + d.left + d.right, 0);

  const { Story } = defineMeta({
    title: 'Section 3/ageGroupDonut',
    component: DonutChartWithLegend,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuicao percentual por faixa etaria**

Donut mostrando a proporcao de contemplados em cada faixa etaria. A faixa de 25 a 54 anos concentra cerca de 70% do total.

**Fonte**: \`aggregate_valor_quantity_by_age_group_sexo_wide.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Donut — distribuicao por faixa etaria">
  {#snippet template()}
    <DonutChartWithLegend
      data={ageGroupDonutData}
      colors={[categorical8[0], categorical8[1], categorical8[2], categorical8[3]]}
      centerLabel="Agentes contemplados"
      centerValue={totalContemplados.toLocaleString('pt-BR')}
      format={formatMi}
      height={360}
    />
  {/snippet}
</Story>
