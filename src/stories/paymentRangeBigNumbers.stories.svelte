<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber, SvgExportDecorator } from 'sniic-design-system';

  const { Story } = defineMeta({
    title: 'Section 3/paymentRangeBigNumbers',
    component: BigNumber,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Como os pagamentos foram estruturados? Distribuição por faixa de valor**

A Política Nacional Aldir Blanc contemplou **166.886 agentes culturais**. Para compreender se houve concentração de recursos com poucos proponentes, os pagamentos foram divididos em faixas de valor.

A distribuição revela um programa de amplo alcance social: **71% dos agentes** receberam até R$10 mil. Ao mesmo tempo, cerca de **6%** dos contemplados receberam acima de R$50 mil, absorvendo a maior parte do orçamento.

| Faixa | Agentes | % |
|---|---|---|
| Até R$2 mil | 49.037 | 29% |
| R$2–R$10 mil | 70.493 | 42% |
| R$10–R$50 mil | 37.661 | 23% |
| R$50–R$200 mil | 8.348 | 5% |
| Acima de R$200 mil | 1.347 | 1% |
          `,
        },
      },
    },
    argTypes: {
      value: { control: 'text' },
      suffix: { control: 'text' },
      fontSize: { control: { type: 'range', min: 24, max: 200, step: 4 } },
    },
  });
</script>

<Story name="Até R$2 mil — 29% dos agentes (49.037)">
  {#snippet template()}
    <BigNumber value={29} suffix="%" fontSize={96} />
  {/snippet}
</Story>

<Story name="R$2–R$10 mil — 42% dos agentes (70.493)">
  {#snippet template()}
    <BigNumber value={42} suffix="%" fontSize={96} />
  {/snippet}
</Story>

<Story name="R$10–R$50 mil — 23% dos agentes (37.661)">
  {#snippet template()}
    <BigNumber value={23} suffix="%" fontSize={96} />
  {/snippet}
</Story>

<Story name="R$50–R$200 mil — 5% dos agentes (8.348)">
  {#snippet template()}
    <BigNumber value={5} suffix="%" fontSize={96} />
  {/snippet}
</Story>

<Story name="Acima de R$200 mil — 1% dos agentes (1.347)">
  {#snippet template()}
    <BigNumber value={1} suffix="%" fontSize={96} />
  {/snippet}
</Story>
