<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber } from 'sniic-design-system';
  // @ts-ignore
  import { valorTotalPJ, valorTotalMEI } from '$lib/data/section3';

  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(v);

  const { Story } = defineMeta({
    title: 'Section 3/pfPjValueBigNumbers',
    component: BigNumber,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Valor recebido por pessoas jurídicas e MEIs**

Apesar de representarem apenas 19,3% dos contemplados, as **pessoas jurídicas** receberam **${formatBRL(valorTotalPJ)}** — 55,9% do valor total distribuído.

Dentre elas, os **MEIs** (Microempreendedores Individuais) responderam por **${formatBRL(valorTotalMEI)}**, equivalente a 8,4% do total.
          `,
        },
      },
    },
    argTypes: {
      value: { control: 'text' },
      suffix: { control: 'text' },
      fontSize: { control: { type: 'range', min: 24, max: 200, step: 4 } },
      color: { control: 'color' },
    },
  });
</script>

<Story name="Pessoas jurídicas — valor recebido (55,9%)">
  {#snippet template()}
    <BigNumber
      value={formatBRL(valorTotalPJ)}
      fontSize={96}
    />
  {/snippet}
</Story>

<Story name="MEIs — valor recebido (8,4%)">
  {#snippet template()}
    <BigNumber
      value={formatBRL(valorTotalMEI)}
      fontSize={96}
    />
  {/snippet}
</Story>
