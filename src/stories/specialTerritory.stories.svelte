<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { BigNumber, DivergingBarChart, HorizontalStackedBarChart, colorPairs, colorScales } from 'sniic-design-system';

  // Data from data/section_1/special_territory_w_ibge_by_brazil.csv
  const ibgeData = [
    { territorio: 'Favela e Comunidade Urbana', valor: 138146185, perc_recurso: 4.85, perc_populacao: 8.0 },
    { territorio: 'Agrupamento quilombola',     valor: 7369210,   perc_recurso: 0.26, perc_populacao: 0.7 },
    { territorio: 'Agrupamento indígena',        valor: 5078944,   perc_recurso: 0.18, perc_populacao: 0.83 },
  ];

  // --- Option 1: BigNumber ---
  // Total % of resources reaching special territories (Favela + Quilombola + Indígena)
  const percRecursoEspecial = ibgeData.reduce((s, d) => s + d.perc_recurso, 0).toFixed(2); // 5.29
  const percPopulacaoEspecial = ibgeData.reduce((s, d) => s + d.perc_populacao, 0).toFixed(1); // 9.53

  // --- Option 2: DivergingBarChart ---
  // Normalize each territory so (leftPct + rightPct = 100) where:
  //   left  = share of population (% pop / (% pop + % recurso) * 100)
  //   right = share of resources
  // referenceValue = 50 means equal treatment (population share = resource share)
  const divergingData = ibgeData.map((d) => {
    const total = d.perc_populacao + d.perc_recurso;
    return {
      label: d.territorio,
      leftPct: (d.perc_populacao / total) * 100,
      rightPct: (d.perc_recurso / total) * 100,
    };
  });

  // --- Option 3: HorizontalStackedBarChart ---
  // Merged from values_by_special_territory_state.csv and values_by_special_territory_municipality.csv
  // Excludes "Não especial" — sorted by total value descending
  // shortLabel is used as categoryKey so long names don't overflow the fixed 50px left margin.
  // The chart SVG has overflow:visible, so padding-left on the wrapper gives room for label text.
  const stackedData = [
    { label: 'Favela e Comunidade Urbana',          shortLabel: 'Favela / Com. Urbana',   valor_estado: 83027141,  valor_municipio: 55119044  },
    { label: 'Setor com baixo patamar domiciliar',  shortLabel: 'Setor baixo patamar',    valor_estado: 12247531,  valor_municipio: 9604835   },
    { label: 'Não informado',                        shortLabel: 'Não informado',           valor_estado: 3331402,   valor_municipio: 15054200  },
    { label: 'Agrupamento quilombola',               shortLabel: 'Quilombola',              valor_estado: 4463173,   valor_municipio: 2906038   },
    { label: 'Agrupamento indígena',                 shortLabel: 'Indígena',                valor_estado: 3969151,   valor_municipio: 1109793   },
    { label: 'Quartel e base militar',               shortLabel: 'Quartel / Militar',       valor_estado: 350000,    valor_municipio: 130603    },
    { label: 'Agrovila do PA',                       shortLabel: 'Agrovila do PA',          valor_estado: 257631,    valor_municipio: 282888    },
    { label: 'Convento / hospital / ILPI / IACA',    shortLabel: 'Convento / ILPI / IACA',  valor_estado: 0,         valor_municipio: 152685    },
    { label: 'Unidade prisional',                    shortLabel: 'Unidade prisional',       valor_estado: 20000,     valor_municipio: 66969     },
    { label: 'Alojamento / acampamento',             shortLabel: 'Alojamento / Acampamento', valor_estado: 149200,   valor_municipio: 53308     },
  ].sort((a, b) => (b.valor_estado + b.valor_municipio) - (a.valor_estado + a.valor_municipio));

  const { Story } = defineMeta({
    title: 'Section 1/specialTerritory',
    component: BigNumber,
    tags: ['autodocs'],
  });
</script>

<!-- ===== Option 1: BigNumber ===== -->

<Story name="BigNumber - % recursos em territórios especiais">
  {#snippet template()}
    <BigNumber
      value={percRecursoEspecial}
      suffix="%"
      label="dos recursos chegaram a Favelas, Quilombos e Territórios Indígenas"
      fontSize={96}
    />
  {/snippet}
</Story>

<Story name="BigNumber - % população em territórios especiais">
  {#snippet template()}
    <BigNumber
      value={percPopulacaoEspecial}
      suffix="%"
      label="da população vive em Favelas, Quilombos e Territórios Indígenas"
      fontSize={96}
    />
  {/snippet}
</Story>

<Story name="BigNumber - Favela: % recursos">
  {#snippet template()}
    <BigNumber
      value="4,85"
      suffix="%"
      label="dos recursos chegaram a Favelas e Comunidades Urbanas"
      fontSize={96}
    />
  {/snippet}
</Story>

<Story name="BigNumber - Favela: % população">
  {#snippet template()}
    <BigNumber
      value="8,0"
      suffix="%"
      label="da população vive em Favelas e Comunidades Urbanas"
      fontSize={96}
    />
  {/snippet}
</Story>

<!-- ===== Option 2: DivergingBarChart (equity gap) ===== -->
<!--
  Each bar shows what share of (population + resources combined) is population vs resources.
  referenceValue=50 = "equal treatment" (population share = resource share).
  All territories lean left (population > resources) → underserved.
-->

<Story name="DivergingBarChart - Lacuna de equidade (blueTeal)">
  {#snippet template()}
    <div style="padding-left: 30px;">
      <DivergingBarChart
        data={divergingData}
        leftLabel="% população no território"
        rightLabel="% do total de recursos"
        referenceValue={50}
        referenceLabel="Equidade"
        colors={colorPairs.blueTeal}
      />
    </div>
  {/snippet}
</Story>

<Story name="DivergingBarChart - Lacuna de equidade (blueOrange)">
  {#snippet template()}
    <div style="padding-left: 30px;">
      <DivergingBarChart
        data={divergingData}
        leftLabel="% população no território"
        rightLabel="% do total de recursos"
        referenceValue={50}
        referenceLabel="Equidade"
        colors={colorPairs.blueOrange}
      />
    </div>
  {/snippet}
</Story>

<Story name="DivergingBarChart - Lacuna de equidade (purpleYellow)">
  {#snippet template()}
    <div style="padding-left: 30px;">
      <DivergingBarChart
        data={divergingData}
        leftLabel="% população no território"
        rightLabel="% do total de recursos"
        referenceValue={50}
        referenceLabel="Equidade"
        colors={colorPairs.purpleYellow}
      />
    </div>
  {/snippet}
</Story>

<!-- ===== Option 3: HorizontalStackedBarChart (Estado vs Município) ===== -->

<Story name="HorizontalStackedBarChart - Estado vs Município (valor absoluto)">
  {#snippet template()}
    <!-- padding-left gives room for label text that overflows the chart's fixed 50px left margin -->
    <div style="padding-left: 100px;">
      <HorizontalStackedBarChart
        data={stackedData}
        keys={['valor_estado', 'valor_municipio']}
        categoryKey="shortLabel"
        labels={{ valor_estado: 'Governo Estadual', valor_municipio: 'Governo Municipal' }}
        colors={[colorScales.blue[2], colorScales.red[2]]}
        format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
        showTotalLabel={true}
      />
    </div>
  {/snippet}
</Story>

<Story name="HorizontalStackedBarChart - Estado vs Município (teal/orange)">
  {#snippet template()}
    <div style="padding-left: 100px;">
      <HorizontalStackedBarChart
        data={stackedData}
        keys={['valor_estado', 'valor_municipio']}
        categoryKey="shortLabel"
        labels={{ valor_estado: 'Governo Estadual', valor_municipio: 'Governo Municipal' }}
        colors={[colorScales.teal[2], colorScales.orange[2]]}
        format={(v) => `R$ ${(v / 1e6).toFixed(1)}M`}
        showTotalLabel={true}
      />
    </div>
  {/snippet}
</Story>
