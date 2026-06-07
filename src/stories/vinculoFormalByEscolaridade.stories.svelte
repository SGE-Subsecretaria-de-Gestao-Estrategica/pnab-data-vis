<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, VerticalBarChart, colorScales } from 'sniic-design-system';
  import VerticalGroupedBarChart from '$lib/components/VerticalGroupedBarChart.svelte';
  import VerticalBarChartCustom from '$lib/components/VerticalBarChartCustom.svelte';
  // @ts-ignore
  import { escolaridadeBarData, escolaridadeValorMedioData, escolaridadeProporcionalData, escolaridadeGroupedData } from '$lib/data/section4';

  // @ts-ignore
  const formatN = (v) => v.toLocaleString('pt-BR');
  // @ts-ignore
  const formatBRL = (v) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(v);
  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;

  // Labels abreviadas para o gráfico vertical (labels originais são longas demais para eixo X)
  const escolaridadeLabelAbrev = {
    'Médio completo / superior incompleto':    'Médio/sup. incompl.',
    'Superior completo':                       'Superior compl.',
    'Fundamental completo / médio incompleto': 'Fund./méd. incompl.',
    'Sem instrução / fund. incompleto':        'Sem instrução',
    'Mestrado ou doutorado':                   'Mestrado/dout.',
  };
  // @ts-ignore
  const escolaridadeProporcionalVertData = escolaridadeProporcionalData.map((d) => ({
    ...d,
    label: escolaridadeLabelAbrev[d.label] ?? d.label,
  }));

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalByEscolaridade',
    component: HorizontalBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Quanto mais estudo, mais vínculo formal**

Entre os beneficiários com vínculo formal, o perfil educacional é elevado: **médio completo / superior incompleto** e **superior completo** concentram juntos mais de 87% do grupo. Apenas 3,2% têm pós-graduação, mas esse grupo recebe proporcionalmente mais — reflexo de remunerações maiores no emprego formal do setor cultural.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras — Beneficiários com vínculo formal por escolaridade">
  {#snippet template()}
    <HorizontalBarChart
      data={escolaridadeProporcionalData}
      color={colorScales.blue[2]}
      format={formatPct}
      xLabel="% dos trabalhadores formais"
      margin={{ top: 20, right: 60, bottom: 40, left: 260 }}
    />
  {/snippet}
</Story>

<Story name="Barras horizontais — Valor médio por escolaridade">
  {#snippet template()}
    <HorizontalBarChart
      data={escolaridadeValorMedioData}
      color={colorScales.orange[2]}
      format={formatBRL}
      xLabel="Valor médio pago (R$)"
      margin={{ top: 20, right: 180, bottom: 40, left: 260 }}
    />
  {/snippet}
</Story>

<Story name="Barras verticais — Participacao proporcional por escolaridade">
  {#snippet template()}
    <VerticalBarChartCustom
      data={escolaridadeProporcionalVertData}
      color={colorScales.red[2]}
      format={formatPct}
      yLabel="% dos trabalhadores formais"
      margin={{ top: 30, right: 20, bottom: 60, left: 60 }}
      height={420}
    />
  {/snippet}
</Story>

<Story name="Barras verticais agrupadas — PNAB vs. Brasil por escolaridade">
  {#snippet template()}
    <VerticalGroupedBarChart
      data={escolaridadeGroupedData}
      seriesLabels={['PNAB', 'Brasil (RAIS 2024)']}
      colors={[colorScales.blue[2], colorScales.orange[2]]}
      format={(v) => `${v.toFixed(1)}%`}
      barWidth={36}
      barPad={6}
      innerH={300}
      margin={{ top: 20, right: 20, bottom: 70, left: 20 }}
    />
  {/snippet}
</Story>
