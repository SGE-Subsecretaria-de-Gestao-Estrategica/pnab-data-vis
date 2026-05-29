<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, VerticalBarChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { escolaridadeBarData, escolaridadeValorMedioData, escolaridadeProporcionalData } from '$lib/data/section4';

  // @ts-ignore
  const formatN = (v) => v.toLocaleString('pt-BR');
  // @ts-ignore
  const formatBRL = (v) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(v);
  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;

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
      data={escolaridadeBarData}
      color={colorScales.blue[2]}
      format={formatN}
      xLabel="Beneficiários com vínculo formal"
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
    <VerticalBarChart
      data={escolaridadeProporcionalData}
      color={colorScales.red[2]}
      yLabel="% dos trabalhadores formais"
      margin={{ top: 30, right: 20, bottom: 100, left: 60 }}
      height={420}
    />
  {/snippet}
</Story>
