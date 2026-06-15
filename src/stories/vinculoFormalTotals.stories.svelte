<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber, ProportionalAreaChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import {
    percSemVinculo, percComVinculo,
    totalBenef, totalSemVinculo, totalComVinculo,
    valorAreaData,
  } from '$lib/data/section4';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalTotals',
    component: BigNumber,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Maioria dos beneficiários está fora do mercado formal**

Do total de beneficiários do PNAB analisados, mais da metade — **${percSemVinculo.toFixed(1)}%** — não possui vínculo com o trabalho formal. Apenas **${percComVinculo.toFixed(1)}%** têm registro formal de emprego.

Esses dados resultam do cruzamento da base de contemplados do PNAB com a RAIS (Relação Anual de Informações Sociais), revelando que o programa atende majoritariamente trabalhadores informais do setor cultural.
          `,
        },
      },
    },
  });
</script>

<Story name="% sem vínculo formal">
  {#snippet template()}
    <BigNumber value={percSemVinculo.toFixed(1)} suffix="%" fontSize={96} />
  {/snippet}
</Story>

<Story name="% com vínculo formal">
  {#snippet template()}
    <BigNumber value={percComVinculo.toFixed(1)} suffix="%" fontSize={96} />
  {/snippet}
</Story>

<Story name="Área proporcional — Valor pago por grupo">
  {#snippet template()}
    <ProportionalAreaChart
      data={valorAreaData}
      maxRadius={120}
      colors={[colorScales.red[2], colorScales.lime[2]]}
      format={formatBRL}
      showLabels={true}
    />
  {/snippet}
</Story>
