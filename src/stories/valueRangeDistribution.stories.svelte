<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { faixaDistData } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 2/valueRangeDistribution',
    component: HorizontalBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**A maioria dos beneficiários recebe menos de R$10 mil**

Olhando todos os **166.886 beneficiários** do PNAB no Brasil, a distribuição é fortemente concentrada nos valores mais baixos.

Mais de **71%** dos contemplados receberam até R$10 mil — sendo que a faixa de R$2k a R$10k sozinha representa **42%** do total. As faixas acima de R$200 mil correspondem a menos de **0,8%** dos beneficiários, e apenas **2 entidades** receberam acima de R$10 milhões.

A cauda direita existe — e ela importa para entender a concentração de valor — mas é estatisticamente rara.
          `,
        },
      },
    },
  });
</script>

<Story name="Distribuição nacional — % de beneficiários por faixa de valor">
  {#snippet template()}
    <HorizontalBarChart
      data={faixaDistData}
      color={colorScales.purple[2]}
      format={formatPct}
      xLabel="% dos beneficiários"
      margin={{ top: 20, right: 80, bottom: 40, left: 160 }}
    />
  {/snippet}
</Story>
