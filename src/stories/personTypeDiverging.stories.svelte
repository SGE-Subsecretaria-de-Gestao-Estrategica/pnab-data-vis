<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DivergingBarChart, HorizontalStackedBarChart, colorPairs, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import { valorDivergingData, benefVsValorData } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 3/personTypeDiverging',
    component: DivergingBarChart,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**O desequilíbrio CPF vs CNPJ varia por esfera executora**

A proporção do valor destinada a pessoas físicas (CPF) ou entidades (CNPJ) muda conforme a esfera que executa o recurso.

Nos repasses **estaduais**, o CNPJ domina com quase **64,7%** do valor — mesmo representando apenas **32%** dos beneficiários desse nível. Nos **municípios**, a divisão é mais próxima do equilíbrio (47% CNPJ), mas ainda desproporcional em relação à sua fatia de beneficiários (17%).

O "flip" evidencia a inversão: no eixo de **beneficiários**, o CPF domina com 80,7%; no eixo de **valor recebido**, o CNPJ vira maioria (55,9%). A mesma esquerda–direita, com os lados trocados.
          `,
        },
      },
    },
  });
</script>

<Story name="Divergente — % do valor por esfera (CPF vs CNPJ)">
  {#snippet template()}
    <DivergingBarChart
      data={valorDivergingData}
      leftLabel="CPF — % do valor"
      rightLabel="CNPJ — % do valor"
      referenceValue={50}
      referenceLabel="Equidade"
      colors={colorPairs.blueOrange}
      marginLeft={220}
    />
  {/snippet}
</Story>

<Story name="Stacked — Beneficiários vs Valor (o flip CPF/CNPJ)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={benefVsValorData}
      keys={['cpf', 'cnpj']}
      labels={{ cpf: 'CPF', cnpj: 'CNPJ' }}
      colors={colorPairs.blueOrange}
      format={formatPct}
      showTotalLabel={false}
    />
  {/snippet}
</Story>
