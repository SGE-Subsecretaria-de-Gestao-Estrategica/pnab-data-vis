<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import SexoUfStackedComparison from '$lib/components/SexoUfStackedComparison.svelte';
  import { colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { sexoUfComparisonData } from '$lib/data/section3';

  const { Story } = defineMeta({
    title: 'Section 3/Grafico 19',
    component: SexoUfStackedComparison,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição por sexo por UF: Aldir Blanc vs. população IBGE**

Duas barras empilhadas por UF — a barra superior (cor cheia) mostra a distribuição por sexo dos agentes culturais contemplados na Aldir Blanc; a barra inferior (cor clara) mostra a distribuição na população segundo o Censo 2022 do IBGE.

Permite identificar rapidamente quais UFs apresentam maior ou menor sub-representação feminina em relação à composição populacional.
          `,
        },
      },
    },
  });
</script>

<Story name="Aldir Blanc vs IBGE por sexo e UF">
  {#snippet template()}
    <SexoUfStackedComparison width={600}
      data={sexoUfComparisonData}
      colorMasc={colorScales.blue[2]}
      colorFem={colorScales.yellow[2]}
      barHeight={22}
      pairGap={4}
      groupGap={14}
      margin={{ top: 24, right: 20, bottom: 64, left: 130 }}
    />
  {/snippet}
</Story>
