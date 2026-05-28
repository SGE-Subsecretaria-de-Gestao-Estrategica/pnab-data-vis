<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { regiaoDistData } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 2/culturalAgentsByRegion',
    component: HorizontalBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição de pagamentos por região**

A Política Nacional Aldir Blanc contemplou agentes culturais em todo o país, com distribuição regional que se distancia do peso demográfico de cada região.

**Nordeste** liderou amplamente, concentrando **47,7%** de todos os agentes culturais contemplados — quase metade do total, proporção muito acima dos 26,9% da população nacional que reside na região.

**Sudeste** apresentou proporção de contemplados (27,4%) inferior à sua participação na população nacional (41,7%), indicando maior concentração de recursos em um número menor de agentes com valores mais elevados.

Norte, Centro-Oeste e Sul apresentaram participação de contemplados bastante próxima à proporção de suas populações em relação ao total nacional.
          `,
        },
      },
    },
  });
</script>

<Story name="Agentes culturais contemplados por região (% do total)">
  {#snippet template()}
    <HorizontalBarChart
      data={regiaoDistData}
      color={colorScales.blue[2]}
      format={formatPct}
      xLabel="% dos agentes culturais"
      margin={{ top: 20, right: 80, bottom: 40, left: 140 }}
    />
  {/snippet}
</Story>
