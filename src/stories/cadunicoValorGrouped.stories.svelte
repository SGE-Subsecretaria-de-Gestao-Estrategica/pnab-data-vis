<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
  // @ts-ignore
  import { valorGroupedData } from '$lib/data/section5';

  const { Story } = defineMeta({
    title: 'Section 5/Grafico 33',
    component: HorizontalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição por faixa de valor — CadÚnico vs. total PNAB**

Compara o percentual de contemplados por faixa de valor recebido entre os cadastrados no CadÚnico e o universo geral da Aldir Blanc. Os inscritos no CadÚnico concentram-se ainda mais nas faixas menores: **86,8%** receberam até R$10 mil, frente a **71,6%** no total da PNAB. O valor médio foi de **R$6.262** (CadÚnico) vs. **R$17.053** (total).

**Fonte**: \`aggregate_cadunico_by_value_group.csv\` + \`aggregate_valor_by_value_group.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="HorizontalGroupedBarChart — faixa de valor CadÚnico vs PNAB">
  {#snippet template()}
    <HorizontalGroupedBarChart width={600}
      data={valorGroupedData}
      seriesLabels={['% contemplados PNAB/CadUnico', '% contemplados PNAB']}
      colors={[colorScales.blue[2], colorScales.purple[2]]}
      format={(v) => `${v.toFixed(1)}%`}
      margin={{ top: 28, right: 20, bottom: 40, left: 160 }}
      barHeight={34}
      barPad={4}
      groupPad={12}
      legendBottom={true}
      labelsInside={true}
    />
  {/snippet}
</Story>
