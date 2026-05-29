<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BoxPlotChart } from 'sniic-design-system';
  // @ts-ignore
  import { brasilBoxPlotData } from '$lib/data/section2';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 0,
    }).format(v);

  const { Story } = defineMeta({
    title: 'Section 2/brasilBoxPlot',
    component: BoxPlotChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição geral dos valores recebidos no Brasil**

Box plot síntese da distribuição dos valores recebidos por todos os **166.886 agentes culturais** contemplados no Brasil.

- **P1**: R$2.824 — o piso da distribuição
- **Q1 (25%)**: R$12.500 — metade inferior abaixo desse valor
- **Mediana (50%)**: R$30.000 — valor central da distribuição
- **Q3 (75%)**: R$60.000 — 75% dos beneficiários abaixo desse valor
- **P99**: R$500.000 — cauda superior da distribuição

O intervalo interquartil (IQR = R$47.500) mostra uma distribuição moderadamente concentrada, com cauda direita longa — resultado da coexistência de muitos pequenos beneficiários (CPF) com poucos recebedores de alto valor (CNPJ).

**Fonte**: quartis_brasil.csv — calculado a partir dos dados completos de pagamentos PNAB.
          `,
        },
      },
    },
  });
</script>

<Story name="BoxPlot — Distribuição geral dos valores recebidos no Brasil">
  {#snippet template()}
    <BoxPlotChart
      data={brasilBoxPlotData}
      xLabel="Abrangência"
      yLabel="Valor recebido (R$)"
      format={formatBRL}
      showOutliers={false}
    />
  {/snippet}
</Story>
