<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales, categorical8 } from 'sniic-design-system';
  import DonutChartWithLegend from '$lib/components/DonutChartWithLegend.svelte';
  // @ts-ignore
  import { rendaDonutData, situacaoRendaDonutData } from '$lib/data/section5';

  // @ts-ignore
  const formatNum = (v) => v.toLocaleString('pt-BR');

  const totalRenda = rendaDonutData.reduce((s, d) => s + d.value, 0);
  const totalSituacao = situacaoRendaDonutData.reduce((s, d) => s + d.value, 0);

  const { Story } = defineMeta({
    title: 'Section 5/cadunicoRenda',
    component: DonutChartWithLegend,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Vulnerabilidade socioeconômica — renda per capita e situação de renda**

A maioria dos contemplados no CadÚnico vive em famílias com renda per capita muito baixa. Mais de **34%** estão na faixa de pobreza extrema (até R$109/mês). Somando as faixas abaixo de meio salário mínimo, chegamos a mais de **65%** do total.

Dois donuts mostram as distribuições: por faixa de renda per capita (5 categorias) e por situação de renda simplificada (Pobreza / Baixa renda / Acima de 1/2 salário mínimo).

**Fonte**: \`aggregate_cadunico_by_fx_renda_per_capita.csv\`, \`aggregate_cadunico_by_situacao_renda.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Grafico 31.1">
  {#snippet template()}
    <DonutChartWithLegend
      data={rendaDonutData}
      colors={categorical8}
      centerLabel="pessoas"
      centerValue={formatNum(totalRenda)}
      format={formatNum}
      height={400}
    />
  {/snippet}
</Story>

<Story name="Grafico 31.2">
  {#snippet template()}
    <DonutChartWithLegend
      data={situacaoRendaDonutData}
      colors={categorical8.slice(0, 3)}
      centerLabel="pessoas"
      centerValue={formatNum(totalSituacao)}
      format={formatNum}
      height={360}
    />
  {/snippet}
</Story>
