<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, colorScales, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import { faixaValorPercData } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 2/valueConcentrationByRange',
    component: HorizontalBarChart,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Onde está o dinheiro? A concentração nas faixas intermediárias**

Enquanto a maioria dos agentes culturais recebe valores pequenos, o grosso dos recursos se concentra nas faixas intermediárias e altas.

As faixas de **R$10 a R$200 mil** absorvem **60%** do total executado, atendendo cerca de 30% dos agentes contemplados. Já as faixas mais baixas (até R$10 mil), que concentram 71% dos beneficiários, respondem por apenas **15%** do valor total.

Aproximadamente **R$2,1 bilhões** (75% do orçamento total executado) foram destinados a mais de 165 mil agentes com valores individuais de até R$200 mil.
          `,
        },
      },
    },
  });
</script>

<Story name="% do valor total por faixa de pagamento">
  {#snippet template()}
    <HorizontalBarChart
      data={faixaValorPercData}
      color={colorScales.blue[2]}
      format={formatPct}
      xLabel="% do valor total"
      margin={{ top: 20, right: 80, bottom: 40, left: 200 }}
    />
  {/snippet}
</Story>
