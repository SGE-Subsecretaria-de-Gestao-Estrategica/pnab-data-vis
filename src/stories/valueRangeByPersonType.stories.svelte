<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart, categorical8, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import { bandStackedData, BAND_STACK_KEYS, BAND_LABELS } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 2/valueRangeByPersonType',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Perfis completamente opostos: CPF concentrado em baixo valor, CNPJ distribuído até milhões**

Quando separamos os beneficiários por tipo — CPF (pessoas físicas) e CNPJ (entidades) — surgem dois perfis radicalmente distintos de distribuição de valor.

**CPF**: mais de **79%** dos beneficiários pessoas físicas receberam até R$10 mil. A faixa de R$2k a R$10k representa sozinha **44%** do grupo. Acima de R$200 mil, praticamente não há CPFs.

**CNPJ**: a distribuição é muito mais espalhada. Quase **57%** das entidades receberam acima de R$10 mil, com presença relevante em todas as faixas até dezenas de milhões. A faixa "R$10k–R$50k" sozinha representa **38,8%** do grupo.

Esses dois perfis raramente se sobrepõem — são programas dentro de um mesmo programa.
          `,
        },
      },
    },
  });
</script>

<Story name="Faixas de valor — CPF vs CNPJ (% dentro de cada tipo)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={bandStackedData}
      keys={BAND_STACK_KEYS}
      labels={BAND_LABELS}
      colors={categorical8}
      format={formatPct}
      showTotalLabel={false}
    />
  {/snippet}
</Story>
