<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { specialExecByUfData } from '$lib/data/section1';

  // @ts-ignore
  const formatBRL = (v) => `R$ ${(v / 1e6).toFixed(1)}M`;

  const { Story } = defineMeta({
    title: 'Section 1/specialTerritoryExecByUf',
    component: HorizontalStackedBarChart,
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

<Story name="Valor executado em territorios especiais por UF">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={specialExecByUfData}
      keys={['valor_executado_estado', 'valor_executado_municipio']}
      categoryKey="label"
      labels={{ valor_executado_estado: 'Governo Estadual', valor_executado_municipio: 'Governo Municipal' }}
      colors={[colorScales.blue[2], colorScales.red[2]]}
      format={formatBRL}
      showTotalLabel={true}
    />
  {/snippet}
</Story>
