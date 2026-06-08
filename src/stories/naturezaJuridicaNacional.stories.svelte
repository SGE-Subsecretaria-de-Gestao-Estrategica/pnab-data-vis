<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { naturezaJuridicaData } from '$lib/data/section3';

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 3/naturezaJuridicaNacional',
    component: HorizontalBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**% - Distribuição de Agentes Culturais Pessoas Jurídicas Contemplados na Aldir Blanc por Natureza Jurídica**

Os dados revelam forte presença de estruturas de pequeno porte e organizações da sociedade civil. A expressiva participação das entidades sem fins lucrativos (32,7%) reflete o peso dessas organizações na execução de ações culturais. A soma de MEIs (28,1%) e microempresas (30,4%) representa quase 58,5% dos contemplados, evidenciando a predominância de agentes econômicos de menor porte.

**Fonte**: \`aggregate_cnpj_natureza_juridica.csv\` (cruzamento PNAB × Receita Federal).
          `,
        },
      },
    },
  });
</script>

<Story name="Distribuição por Natureza Jurídica">
  {#snippet template()}
    <HorizontalBarChart
      data={naturezaJuridicaData}
      color={categorical8[4]}
      format={formatPct}
      xLabel="% de CNPJs contemplados"
      title="% - Distribuição de Agentes Culturais Pessoas Jurídicas Contemplados na Aldir Blanc por Natureza Jurídica"
      margin={{ top: 20, right: 80, bottom: 40, left: 230 }}
    />
  {/snippet}
</Story>
