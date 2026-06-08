<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  import { colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { representacaoUfGroupedData } from '$lib/data/section5';

  const { Story } = defineMeta({
    title: 'Section 5/cadunicoRepresentacaoByUf',
    component: HorizontalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Comparativo entre Distribuição de Agentes Culturais PF Contemplados na Aldir Blanc com CadÚnico por UF x Distribuição de Pessoas com CadÚnico por UF**

Compara o peso de cada UF no total de contemplados na Aldir Blanc que estão no CadÚnico com o peso de cada UF na população total inscrita no CadÚnico.
Estados com barra laranja maior que a teal apresentam sobrerrepresentação; o inverso indica sub-representação.

**Fonte**: \`aggregate_cadunico_representacao_by_uf.csv\`, colunas \`perc_qtd_contemplados_cadunico\` e \`perc_qtd_cadunico_brasil\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Distribuição CadÚnico — Contemplados PNAB vs Pessoas CadÚnico por UF">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={representacaoUfGroupedData}
      seriesLabels={[
        '% contemplados PNAB/CadÚnico (UF)',
        '% pessoas CadÚnico (UF)',
      ]}
      colors={[colorScales.teal[2], colorScales.orange[2]]}
      format={(v) => `${v.toFixed(1)}%`}
      margin={{ top: 28, right: 90, bottom: 40, left: 50 }}
    />
  {/snippet}
</Story>
