<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { VerticalStackedBarChart, categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { stateBandPercData, UF_BAND_KEYS, UF_BAND_LABELS } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 2/valueRangeByState',
    component: VerticalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Faixa de valor pago × estado (executor estadual)**

Cada barra representa um estado, ordenado pela **proporção de beneficiários nas faixas mais altas** (acima de R$50 mil) nos repasses executados diretamente pelos governos estaduais.

Diferente do gráfico por UF (que agrega todos os executores), este mostra somente a execução estadual — permitindo isolar o perfil de distribuição de cada governo estadual independentemente dos municípios.

Estados com maior presença de CNPJs e projetos institucionais tendem a concentrar mais beneficiários nas faixas superiores. A comparação entre este gráfico e o de execução total por UF revela em quais estados a esfera estadual diverge do padrão municipal.

**Fonte**: aggregate_faixa_valor_ju_wide_by_state.csv — somente executor estadual.
          `,
        },
      },
    },
  });
</script>

<Story name="Faixa de valor pago por estado (executor estadual)">
  {#snippet template()}
    <VerticalStackedBarChart
      data={stateBandPercData}
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
