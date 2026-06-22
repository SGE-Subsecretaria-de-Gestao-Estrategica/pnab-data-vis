<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import ConnectedDotPlot from '$lib/components/ConnectedDotPlot.svelte';
  import { colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { representacaoUfGroupedData } from '$lib/data/section5';

  const { Story } = defineMeta({
    title: 'Section 5/Grafico 32',
    component: ConnectedDotPlot,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Comparativo entre Distribuição de Agentes Culturais PF Contemplados na Aldir Blanc com CadÚnico por UF x Distribuição de Pessoas com CadÚnico por UF**

Compara o peso de cada UF no total de contemplados na Aldir Blanc que estão no CadÚnico com o peso de cada UF na população total inscrita no CadÚnico.
Dot laranja à direita do teal indica sobrerrepresentação; à esquerda indica sub-representação.

**Fonte**: \`aggregate_cadunico_representacao_by_uf.csv\`, colunas \`perc_qtd_contemplados_cadunico\` e \`perc_qtd_cadunico_brasil\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Distribuição CadÚnico — Contemplados PNAB vs Pessoas CadÚnico por UF">
  {#snippet template()}
    <ConnectedDotPlot width={600}
      data={representacaoUfGroupedData}
      seriesLabels={[
        '% contemplados PNAB/CadUnico (UF)',
        '% pessoas CadUnico (UF)',
      ]}
      colors={[colorScales.blue[2], colorScales.purple[2]]}
      format={(v) => `${v.toFixed(1)}%`}
      margin={{ top: 20, right: 56, bottom: 56, left: 44 }}
      rowHeight={28}
      dotRadius={5}
    />
  {/snippet}
</Story>
