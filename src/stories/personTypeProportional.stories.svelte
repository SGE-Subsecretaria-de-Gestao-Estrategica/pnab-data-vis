<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { ProportionalAreaChart, colorPairs, SvgExportDecorator } from 'sniic-design-system';
  // @ts-ignore
  import { mediaPorTipoData } from '$lib/data/section2';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(v);

  const { Story } = defineMeta({
    title: 'Section 2/personTypeProportional',
    component: ProportionalAreaChart,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Em média, cada CNPJ recebe 6,5× mais que cada CPF**

A área de cada círculo é proporcional ao **valor médio recebido por beneficiário** dentro de cada tipo.

- **CPF**: média de **R$9.634** por pessoa física
- **CNPJ**: média de **R$62.742** por entidade

A diferença de escala — visível diretamente na área dos círculos — resume em forma o que os números dizem: cada entidade recebe, em média, o equivalente ao que **6,5 pessoas físicas** receberiam juntas.

Este gráfico não mostra o total acumulado (que seria próximo entre os dois grupos), mas a concentração *por beneficiário* — a dimensão que revela o desequilíbrio estrutural do programa.
          `,
        },
      },
    },
  });
</script>

<Story name="Área proporcional — Valor médio por beneficiário (CPF vs CNPJ)">
  {#snippet template()}
    <ProportionalAreaChart
      data={mediaPorTipoData}
      maxRadius={130}
      colors={colorPairs.blueOrange}
      format={formatBRL}
      showLabels={true}
    />
  {/snippet}
</Story>
