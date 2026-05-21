<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart, colorScales } from 'sniic-design-system';

  const redBlue = [colorScales.red[2], colorScales.blue[2]];

  function sortByRuralProportion(data) {
    return [...data].sort(
      (a, b) =>
        b.valor_rural / (b.valor_urbano + b.valor_rural) -
        a.valor_rural / (a.valor_urbano + a.valor_rural)
    );
  }

  // Data from data/section_1/executed_value_zone_by_uf_state.csv
  const stateData = [
    { label: 'AC', valor_urbano: 15461300, valor_rural: 2281760 },
    { label: 'AL', valor_urbano: 32487649, valor_rural: 2640500 },
    { label: 'AM', valor_urbano: 41203385, valor_rural: 2429476 },
    { label: 'AP', valor_urbano: 16152299, valor_rural: 968000 },
    { label: 'BA', valor_urbano: 68126864, valor_rural: 7781358 },
    { label: 'CE', valor_urbano: 73067327, valor_rural: 5660592 },
    { label: 'DF', valor_urbano: 21002241, valor_rural: 307003 },
    { label: 'ES', valor_urbano: 27332722, valor_rural: 2534129 },
    { label: 'GO', valor_urbano: 52344105, valor_rural: 3591500 },
    { label: 'MA', valor_urbano: 59878797, valor_rural: 2463505 },
    { label: 'MG', valor_urbano: 105074279, valor_rural: 5708917 },
    { label: 'MS', valor_urbano: 21987984, valor_rural: 1328670 },
    { label: 'MT', valor_urbano: 22813647, valor_rural: 1658000 },
    { label: 'PA', valor_urbano: 70420893, valor_rural: 2524156 },
    { label: 'PB', valor_urbano: 32658354, valor_rural: 4422215 },
    { label: 'PE', valor_urbano: 68482353, valor_rural: 6683249 },
    { label: 'PI', valor_urbano: 30064334, valor_rural: 1512000 },
    { label: 'PR', valor_urbano: 70049314, valor_rural: 3098533 },
    { label: 'RJ', valor_urbano: 82086921, valor_rural: 2815305 },
    { label: 'RN', valor_urbano: 24829989, valor_rural: 2600975 },
    { label: 'RO', valor_urbano: 406833, valor_rural: 60000 },
    { label: 'RR', valor_urbano: 13843089, valor_rural: 1065115 },
    { label: 'RS', valor_urbano: 68120272, valor_rural: 2142514 },
    { label: 'SC', valor_urbano: 25791959, valor_rural: 1965000 },
    { label: 'SE', valor_urbano: 20270960, valor_rural: 2259771 },
    { label: 'SP', valor_urbano: 282572896, valor_rural: 7607111 },
    { label: 'TO', valor_urbano: 17821454, valor_rural: 3111450 },
  ];

  // Data from data/section_1/executed_value_zone_by_uf_municipality.csv
  const municipalityData = [
    { label: 'AC', valor_urbano: 5952593, valor_rural: 634132 },
    { label: 'AL', valor_urbano: 22318108, valor_rural: 2847802 },
    { label: 'AM', valor_urbano: 28036650, valor_rural: 1707852 },
    { label: 'AP', valor_urbano: 6074779, valor_rural: 432310 },
    { label: 'BA', valor_urbano: 85888865, valor_rural: 14489558 },
    { label: 'CE', valor_urbano: 49410284, valor_rural: 8481036 },
    { label: 'DF', valor_urbano: 7349840, valor_rural: 306556 },
    { label: 'ES', valor_urbano: 23837389, valor_rural: 2011355 },
    { label: 'GO', valor_urbano: 47534591, valor_rural: 1984246 },
    { label: 'MA', valor_urbano: 46226330, valor_rural: 4870539 },
    { label: 'MG', valor_urbano: 150051640, valor_rural: 7614235 },
    { label: 'MS', valor_urbano: 18082851, valor_rural: 881492 },
    { label: 'MT', valor_urbano: 22139143, valor_rural: 1683118 },
    { label: 'PA', valor_urbano: 43680826, valor_rural: 6541440 },
    { label: 'PB', valor_urbano: 29878047, valor_rural: 3158894 },
    { label: 'PE', valor_urbano: 59716960, valor_rural: 6449664 },
    { label: 'PI', valor_urbano: 23356445, valor_rural: 2358354 },
    { label: 'PR', valor_urbano: 76275938, valor_rural: 3838879 },
    { label: 'RJ', valor_urbano: 97822413, valor_rural: 2085369 },
    { label: 'RN', valor_urbano: 23383872, valor_rural: 2173919 },
    { label: 'RO', valor_urbano: 7381471, valor_rural: 981223 },
    { label: 'RR', valor_urbano: 1107011, valor_rural: 440722 },
    { label: 'RS', valor_urbano: 75825552, valor_rural: 4731808 },
    { label: 'SC', valor_urbano: 49704723, valor_rural: 4089353 },
    { label: 'SE', valor_urbano: 15408782, valor_rural: 2485209 },
    { label: 'SP', valor_urbano: 258504559, valor_rural: 6677503 },
    { label: 'TO', valor_urbano: 10021004, valor_rural: 879294 },
  ];

  const stateFlags = Object.fromEntries(
    ['AC','AL','AM','AP','BA','CE','DF','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']
      .map((uf) => [uf, `/flags/states/${uf}.svg`])
  );

  const { Story } = defineMeta({
    title: 'Section 1/executedValueByZone',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
  });
</script>

<Story name="Proporção Urbano/Rural por UF (Governo Estadual)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={sortByRuralProportion(stateData)}
      keys={['valor_rural', 'valor_urbano']}
      labels={{ valor_urbano: 'Urbano', valor_rural: 'Rural' }}
      colors={redBlue}
      format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
      showTotalLabel={true}
    />
  {/snippet}
</Story>

<Story name="Proporção Urbano/Rural por UF (Municípios)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={sortByRuralProportion(municipalityData)}
      keys={['valor_rural', 'valor_urbano']}
      labels={{ valor_urbano: 'Urbano', valor_rural: 'Rural' }}
      colors={redBlue}
      format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
      showTotalLabel={true}
    />
  {/snippet}
</Story>

<Story name="Proporção Urbano/Rural por UF com Bandeiras (Governo Estadual)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={sortByRuralProportion(stateData)}
      keys={['valor_rural', 'valor_urbano']}
      labels={{ valor_urbano: 'Urbano', valor_rural: 'Rural' }}
      colors={redBlue}
      format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
      showTotalLabel={true}
      icons={stateFlags}
    />
  {/snippet}
</Story>

<Story name="Proporção Urbano/Rural por UF com Bandeiras (Municípios)">
  {#snippet template()}
    <HorizontalStackedBarChart
      data={sortByRuralProportion(municipalityData)}
      keys={['valor_rural', 'valor_urbano']}
      labels={{ valor_urbano: 'Urbano', valor_rural: 'Rural' }}
      colors={redBlue}
      format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
      showTotalLabel={true}
      icons={stateFlags}
    />
  {/snippet}
</Story>
