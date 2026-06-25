<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  import ConnectedDotPlot from '$lib/components/ConnectedDotPlot.svelte';
  // @ts-ignore
  import { specialExecByUfData, specialExecByUfDotData } from '$lib/data/section1';

  // @ts-ignore
  const formatBRL = (v) => `R$ ${(v / 1e6).toFixed(1)}M`;
  // @ts-ignore
  const formatBRLDot = (v) => `R$${(v / 1e6).toFixed(0)}M`;

  const { Story } = defineMeta({
    title: 'Section 1/Grafico 7',
    component: HorizontalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Valor executado em territorios especiais por UF — Estado vs Municipio**

Distribuicao do valor executado em territorios especiais (favelas, comunidades urbanas, agrupamentos indigenas e quilombolas) por Unidade Federativa, distinguindo a participacao dos governos estaduais e municipais.

**Fonte**: \`special_territory_executed_value_uf.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Valor executado em territorios especiais por UF — dot plot">
  {#snippet template()}
    <ConnectedDotPlot width={600}
      data={specialExecByUfDotData}
      seriesLabels={['Governo Estadual', 'Governo Municipal']}
      colors={[colorScales.blue[2], colorScales.orange[2]]}
      format={formatBRLDot}
      margin={{ top: 20, right: 56, bottom: 56, left: 44 }}
      rowHeight={28}
      dotRadius={5}
    />
  {/snippet}
</Story>

<Story name="Grafico 7">
  {#snippet template()}
    <HorizontalStackedBarChartCustom width={600}
      data={specialExecByUfData}
      keys={['valor_executado_estado', 'valor_executado_municipio']}
      categoryKey="label"
      labels={{ valor_executado_estado: 'Governo Estadual', valor_executado_municipio: 'Governo Municipal' }}
      colors={[colorScales.blue[2], colorScales.orange[2]]}
      format={formatBRL}
      marginLeft={50}
      showTotalLabel={true}
      hideSegmentLabelsFor={['RJ', 'MG', 'AP']}
    />
  {/snippet}
</Story>
