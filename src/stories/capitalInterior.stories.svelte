<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber, HorizontalStackedBarChart, colorScales, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import {
    capitalInteriorStackedData,
    percInteriorPagamentos,
    valorInteriorTotal,
    valorRuralTotal,
  } from '$lib/data/section1';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);
  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 1/capitalInterior',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
    decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Interior concentra a esmagadora maioria dos agentes contemplados**

Dos recursos executados pelos estados, **${percInteriorPagamentos}%** dos pagamentos foram destinados a agentes culturais em **cidades do interior** — totalizando **${formatBRL(valorInteriorTotal)}**. As capitais, apesar de concentrarem maior proporção do valor, representam apenas uma fração dos beneficiários.

A comparação entre o percentual do valor recebido e o percentual de agentes contemplados revela que as capitais concentram proporcionalmente mais recursos do que beneficiários, enquanto o interior apresenta o padrão inverso.

A zona rural recebeu **${formatBRL(valorRuralTotal)}** no total.

**Fonte**: \`aggregate_values_by_capital.csv\` (execução estadual) e \`executed_value_zone_by_uf.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="BigNumber — % pagamentos para o interior">
  {#snippet template()}
    <BigNumber value={percInteriorPagamentos.toFixed(1)} suffix="%" fontSize={96} />
  {/snippet}
</Story>

<Story name="BigNumber — valor total para o interior">
  {#snippet template()}
    <BigNumber value={formatBRL(valorInteriorTotal)} fontSize={72} />
  {/snippet}
</Story>

<Story name="BigNumber — valor total para zona rural">
  {#snippet template()}
    <BigNumber value={formatBRL(valorRuralTotal)} fontSize={72} />
  {/snippet}
</Story>

<Story name="Stacked — capital vs interior (valor e quantidade)">
  {#snippet template()}
    <div style="padding-left: 60px;">
      <HorizontalStackedBarChart
        data={capitalInteriorStackedData}
        keys={['capital', 'interior']}
        labels={{ capital: 'Capital', interior: 'Interior' }}
        colors={[colorScales.orange[2], colorScales.blue[2]]}
        format={formatPct}
        showTotalLabel={false}
      />
    </div>
  {/snippet}
</Story>
