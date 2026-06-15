<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  import { capitalInteriorByUfData } from '$lib/data/section1';

  const colorCapital = '#4271b5';       // azul
  const colorMetropolitana = '#ea662f'; // laranja
  const colorInterior = '#317a68';      // verde

  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 1/capitalInteriorByUf',
    component: HorizontalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição dos contemplados por local de residência (Capital, Região Metropolitana e Interior) — por UF**

Cada barra representa 100% dos agentes culturais contemplados pela execução **estadual** de uma UF, divididos em três grupos:
- **Capital** — residentes na capital do estado
- **Região Metropolitana** — residentes em municípios da RM (exceto capital)
- **Interior** — demais municípios

Estados ordenados pelo maior percentual de contemplados no interior. Destaque para **MG** e **PE**, onde o interior concentra mais da metade dos beneficiários estaduais.

**Fonte**: \`aggregate_estado_by_uf_local_residencia.csv\`
          `,
        },
      },
    },
  });
</script>

<Story name="Stacked — Contemplados por Capital, RM e Interior (por UF)">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={capitalInteriorByUfData}
      keys={['interior', 'metropolitana', 'capital']}
      labels={{ interior: 'Interior', metropolitana: 'Região Metropolitana', capital: 'Capital' }}
      colors={[colorInterior, colorMetropolitana, colorCapital]}
      format={formatPct}
      showTotalLabel={false}
      marginLeft={50}
      rowHeight={36}
    />
  {/snippet}
</Story>

<Story name="Stacked — Contemplados por Capital, RM e Interior — cores categorical8">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={capitalInteriorByUfData}
      keys={['capital', 'metropolitana', 'interior']}
      labels={{ capital: 'Capital', metropolitana: 'Região Metropolitana', interior: 'Interior' }}
      colors={[colorCapital, colorMetropolitana, colorInterior]}
      format={formatPct}
      showTotalLabel={false}
      marginLeft={50}
      rowHeight={36}
    />
  {/snippet}
</Story>
