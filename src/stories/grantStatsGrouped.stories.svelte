<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BoxPlotChart, SvgExportDecorator } from 'sniic-design-system';
  import { boxPlotData } from '$lib/data/section1';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency', currency: 'BRL',
      notation: 'compact', maximumFractionDigits: 0,
    }).format(v);

  const { Story } = defineMeta({
    title: 'Section 1/grantStatsBoxPlot',
    component: BoxPlotChart,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Como são os repasses por região? Distribuição dos valores típicos por estado**

Cada box representa uma região do Brasil. Os valores plotados são as **medianas de repasse** de cada estado dentro da região — ou seja, o valor típico que um beneficiário recebe em cada UF.

A caixa abrange o intervalo entre o 1º e o 3º quartil dos estados da região; a linha central é a mediana regional; os whiskers mostram o mínimo e o máximo (excluindo outliers).

- **Centro-Oeste** tem a maior dispersão: MS (R$ 15k) convive com DF e SP (R$ 100k).
- **Norte** apresenta grande amplitude, de RO (R$ 6k) a AM (R$ 50k).
- **Nordeste** concentra os menores valores típicos, com a maioria dos estados abaixo de R$ 40k.
- **Sul** e **Sudeste** têm distribuições mais compactas, mas com outliers elevados (RS e SP em R$ 80–100k).
          `,
        },
      },
    },
  });
</script>

<Story name="BoxPlot — Distribuição da mediana de repasse por região">
  {#snippet template()}
    <BoxPlotChart
      data={boxPlotData}
      xLabel="Região"
      yLabel="Mediana do repasse por estado (R$)"
      format={formatBRL}
      showOutliers={true}
    />
  {/snippet}
</Story>
