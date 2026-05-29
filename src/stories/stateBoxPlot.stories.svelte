<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BoxPlotChart } from 'sniic-design-system';
  // @ts-ignore
  import { estadosBoxPlotData } from '$lib/data/section2';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 0,
    }).format(v);

  const { Story } = defineMeta({
    title: 'Section 2/stateBoxPlot',
    component: BoxPlotChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição dos pagamentos por estado**

Cada caixa representa a distribuição dos valores recebidos pelos agentes culturais de um estado. Os quartis são estimados por interpolação linear dentro das faixas de pagamento disponíveis nos dados (até R$2k, R$2–10k, R$10–50k, R$50–200k, acima de R$200k).

**Como ler:**
- Linha central: mediana (50% dos beneficiários recebeu menos que isso)
- Extremidades da caixa: Q1 (25%) e Q3 (75%)
- Bigodes: P1 e P99

**Padrões observados:**
- **SP, RS e GO** têm as maiores medianas e maior dispersão — reflexo de mais CNPJs e projetos de maior escala
- **RO, PB e RR** têm distribuições comprimidas nas faixas inferiores — perfil predominante de beneficiários individuais (CPF)
- A variação entre estados é expressiva: a mediana de SP (~R$148k) é mais de 15x a de RO (~R$9k)

**Fonte**: quartis_estados.csv — calculado a partir de faixa_valor_box_plot_qtd_contemplados_state.csv com interpolação linear dentro de faixas.
          `,
        },
      },
    },
  });
</script>

<Story name="BoxPlot — Distribuição de pagamentos por estado">
  {#snippet template()}
    <BoxPlotChart
      data={estadosBoxPlotData}
      xLabel="Estado"
      yLabel="Valor recebido (R$)"
      format={formatBRL}
      showOutliers={false}
      height={440}
    />
  {/snippet}
</Story>
