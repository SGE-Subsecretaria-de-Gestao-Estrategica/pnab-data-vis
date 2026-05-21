<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DivergingBarChart, colorPairs } from 'sniic-design-system';

  // Data from data/section_1/executed_value_by_uf.csv
  const rawRows = [
    { uf: 'AC', perc_valor_executado_estado: 72.93, perc_valor_executado_municipio: 27.07 },
    { uf: 'AL', perc_valor_executado_estado: 58.26, perc_valor_executado_municipio: 41.74 },
    { uf: 'AM', perc_valor_executado_estado: 59.66, perc_valor_executado_municipio: 40.34 },
    { uf: 'AP', perc_valor_executado_estado: 72.44, perc_valor_executado_municipio: 27.56 },
    { uf: 'BA', perc_valor_executado_estado: 43.18, perc_valor_executado_municipio: 56.82 },
    { uf: 'CE', perc_valor_executado_estado: 57.62, perc_valor_executado_municipio: 42.38 },
    { uf: 'DF', perc_valor_executado_estado: 51.76, perc_valor_executado_municipio: 48.24 },
    { uf: 'ES', perc_valor_executado_estado: 53.59, perc_valor_executado_municipio: 46.41 },
    { uf: 'GO', perc_valor_executado_estado: 53.06, perc_valor_executado_municipio: 46.94 },
    { uf: 'MA', perc_valor_executado_estado: 55.16, perc_valor_executado_municipio: 44.84 },
    { uf: 'MG', perc_valor_executado_estado: 41.26, perc_valor_executado_municipio: 58.74 },
    { uf: 'MS', perc_valor_executado_estado: 55.05, perc_valor_executado_municipio: 44.95 },
    { uf: 'MT', perc_valor_executado_estado: 50.77, perc_valor_executado_municipio: 49.23 },
    { uf: 'PA', perc_valor_executado_estado: 59.00, perc_valor_executado_municipio: 41.00 },
    { uf: 'PB', perc_valor_executado_estado: 52.94, perc_valor_executado_municipio: 47.06 },
    { uf: 'PE', perc_valor_executado_estado: 53.20, perc_valor_executado_municipio: 46.80 },
    { uf: 'PI', perc_valor_executado_estado: 55.12, perc_valor_executado_municipio: 44.88 },
    { uf: 'PR', perc_valor_executado_estado: 47.72, perc_valor_executado_municipio: 52.28 },
    { uf: 'RJ', perc_valor_executado_estado: 46.15, perc_valor_executado_municipio: 53.85 },
    { uf: 'RN', perc_valor_executado_estado: 51.71, perc_valor_executado_municipio: 48.29 },
    { uf: 'RO', perc_valor_executado_estado:  5.29, perc_valor_executado_municipio: 94.71 },
    { uf: 'RR', perc_valor_executado_estado: 90.57, perc_valor_executado_municipio:  9.43 },
    { uf: 'RS', perc_valor_executado_estado: 46.64, perc_valor_executado_municipio: 53.36 },
    { uf: 'SC', perc_valor_executado_estado: 34.05, perc_valor_executado_municipio: 65.95 },
    { uf: 'SE', perc_valor_executado_estado: 55.74, perc_valor_executado_municipio: 44.26 },
    { uf: 'SP', perc_valor_executado_estado: 52.21, perc_valor_executado_municipio: 47.79 },
    { uf: 'TO', perc_valor_executado_estado: 65.93, perc_valor_executado_municipio: 34.07 },
  ];

  const data = rawRows.map((d) => ({
    label: d.uf,
    leftPct: d.perc_valor_executado_estado,
    rightPct: d.perc_valor_executado_municipio,
  }));

  const { Story } = defineMeta({
    title: 'Section 1/executedValueByUfDiverging',
    component: DivergingBarChart,
    tags: ['autodocs'],
  });
</script>

<Story name="blueOrange">
  {#snippet template()}
    <DivergingBarChart
      {data}
      leftLabel="Estado"
      rightLabel="Município"
      referenceValue={50}
      referenceLabel=" "

      colors={colorPairs.blueOrange}
    />
  {/snippet}
</Story>

<Story name="bluePurple">
  {#snippet template()}
    <DivergingBarChart
      {data}
      leftLabel="Estado"
      rightLabel="Município"
      referenceValue={50}
      referenceLabel=" "

      colors={colorPairs.bluePurple}
    />
  {/snippet}
</Story>

<Story name="blueTeal">
  {#snippet template()}
    <DivergingBarChart
      {data}
      leftLabel="Estado"
      rightLabel="Município"
      referenceValue={50}
      referenceLabel=" "

      colors={colorPairs.blueTeal}
    />
  {/snippet}
</Story>

<Story name="tealYellow">
  {#snippet template()}
    <DivergingBarChart
      {data}
      leftLabel="Estado"
      rightLabel="Município"
      referenceValue={50}
      referenceLabel=" "

      colors={colorPairs.tealYellow}
    />
  {/snippet}
</Story>

<Story name="purpleYellow">
  {#snippet template()}
    <DivergingBarChart
      {data}
      leftLabel="Estado"
      rightLabel="Município"
      referenceValue={50}
      referenceLabel=" "

      colors={colorPairs.purpleYellow}
    />
  {/snippet}
</Story>

<Story name="limeRed">
  {#snippet template()}
    <DivergingBarChart
      {data}
      leftLabel="Estado"
      rightLabel="Município"
      referenceValue={50}
      referenceLabel=" "

      colors={colorPairs.limeRed}
    />
  {/snippet}
</Story>
