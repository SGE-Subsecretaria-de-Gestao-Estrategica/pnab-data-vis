<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import HorizontalBarChartCustom from '$lib/components/HorizontalBarChartCustom.svelte';
  // @ts-ignore
  import { cadunicoValorData } from '$lib/data/section5';

  const { Story } = defineMeta({
    title: 'Section 5/cadunicoByValue',
    component: HorizontalBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição dos beneficiários CadÚnico por faixa de valor recebido**

Quase metade dos beneficiários CadÚnico recebeu até R$2 mil, e mais de **86%** ficaram abaixo de R$10 mil — concentração ainda maior do que a observada no conjunto geral da Aldir Blanc.

**Fonte**: \`aggregate_cadunico_by_value_group.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="HorizontalBarChart — distribuição por faixa de valor (blue)">
  {#snippet template()}
    <HorizontalBarChartCustom
      data={cadunicoValorData}
      color={colorScales.orange[2]}
      format={(v) => `${v.toFixed(1)}%`}
      xLabel="% dos beneficiários CadÚnico"
      margin={{ top: 20, right: 80, bottom: 40, left: 160 }}
      rowHeight={52}
    />
  {/snippet}
</Story>

<Story name="HorizontalBarChart — distribuição por faixa de valor (teal)">
  {#snippet template()}
    <HorizontalBarChartCustom
      data={cadunicoValorData}
      color={colorScales.teal[2]}
      format={(v) => `${v.toFixed(1)}%`}
      xLabel="% dos beneficiários CadÚnico"
      margin={{ top: 20, right: 80, bottom: 40, left: 160 }}
      rowHeight={52}
    />
  {/snippet}
</Story>
