<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { VerticalStackedBarChart, categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { ufBandPercData, UF_BAND_KEYS, UF_BAND_LABELS } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 2/valueRangeByUf',
    component: VerticalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Faixa de valor pago × UF — perfil de pagamentos por estado**

Cada barra representa um estado, ordenado pelos que têm **maior proporção de beneficiários nas faixas mais altas** (acima de R$50 mil) à esquerda.

A visualização conecta a narrativa CPF/CNPJ ao território: estados onde o CNPJ tem maior presença tendem a concentrar fatias mais expressivas nas faixas acima de R$50 mil. No extremo oposto, estados do Nordeste e Norte onde predominam pequenos agricultores e extrativistas (CPF) têm suas barras dominadas pelas faixas de até R$10 mil.

**Fonte**: execução estadual (**executed_value_by_state.csv**, Section 1). Valores normalizados como % dentro de cada UF.
          `,
        },
      },
    },
  });
</script>

<Story name="Faixa de valor pago por UF - pct dentro de cada estado">
  {#snippet template()}
    <VerticalStackedBarChart
      data={ufBandPercData}
      keys={[...UF_BAND_KEYS]}
      labels={UF_BAND_LABELS}
      colors={categorical8}
      format={formatPct}
      yLabel="% dos beneficiários"
      normalize={true}
      showLegend={true}
      height={480}
    />
  {/snippet}
</Story>
