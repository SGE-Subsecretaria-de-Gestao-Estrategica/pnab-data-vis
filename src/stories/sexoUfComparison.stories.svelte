<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import SexoUfStackedComparison from '$lib/components/SexoUfStackedComparison.svelte';
  import { colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { sexoUfComparisonData } from '$lib/data/section3';

  const { Story } = defineMeta({
    title: 'Section 3/sexoUfComparison',
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
    {@const colorMasc = colorScales.teal[2]}
    {@const colorFem = colorScales.yellow[2]}
    <div style="width: 100%; font-family: 'Space Grotesk', system-ui, sans-serif;">
      <div style="display: flex; border: 0.5px solid rgba(0,0,0,0.25); margin-bottom: 16px; margin-left: 52px; margin-right: 20px;">
        {#each [
          { label: 'Masculino – contemplados', bg: '#317a68',              text: '#fffffe' },
          { label: 'Feminino – contempladas',  bg: '#f6c341',              text: '#1a1a1a' },
          { label: 'Masculino – população',    bg: 'rgba(49,122,104,0.4)', text: '#1a1a1a' },
          { label: 'Feminino – população',     bg: 'rgba(246,195,65,0.4)', text: '#1a1a1a' },
        ] as item, ci}
          <div style="flex: 1; text-align: center; background: {item.bg}; color: {item.text}; padding: 7px 8px; font-size: 12px; font-weight: 600; font-family: 'Space Grotesk', system-ui, sans-serif; {ci < 3 ? 'border-right: 0.5px solid rgba(0,0,0,0.25);' : ''}">
            {item.label}
          </div>
        {/each}
      </div>
      <SexoUfStackedComparison
        data={sexoUfComparisonData}
        colorMasc={colorMasc}
        colorFem={colorFem}
        barHeight={22}
        pairGap={4}
        groupGap={14}
        margin={{ top: 24, right: 20, bottom: 28, left: 130 }}
      />
    </div>
  {/snippet}
</Story>
