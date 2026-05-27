<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BoxPlotChart, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import { boxPlotData } from '$lib/data/section2';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 0,
    }).format(v);

  const { Story } = defineMeta({
    title: 'Section 2/personTypeBoxPlot',
    component: BoxPlotChart,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**A dispersão revela a concentração extrema do CNPJ**

O box plot compara a distribuição completa de valores entre CPF (pessoas físicas) e CNPJ (entidades). Q1 e Q3 são estimados por interpolação linear dentro das faixas de valor disponíveis nos dados.

**CPF**:
- Mediana: **R$3.800** — metade das pessoas físicas recebeu menos que isso
- Caixa (Q1–Q3): ~R$1.500 a ~R$9.300
- Máximo: R$735.000

**CNPJ**:
- Mediana: **R$13.500** — mais de 3× a mediana do CPF
- Caixa (Q1–Q3): ~R$6.400 a ~R$45.600
- Máximo: R$22.109.765

O detalhe mais revelador: o **Q1 do CNPJ (~R$6.400) já supera o Q3 do CPF (~R$9.300)**. As duas distribuições mal se tocam — são populações de beneficiários operando em escalas de valor completamente diferentes dentro do mesmo programa.
          `,
        },
      },
    },
  });
</script>

<Story name="BoxPlot — Distribuição de valores por tipo de beneficiário (CPF vs CNPJ)">
  {#snippet template()}
    <BoxPlotChart
      data={boxPlotData}
      xLabel="Tipo de beneficiário"
      yLabel="Valor recebido (R$)"
      format={formatBRL}
      showOutliers={false}
    />
  {/snippet}
</Story>
