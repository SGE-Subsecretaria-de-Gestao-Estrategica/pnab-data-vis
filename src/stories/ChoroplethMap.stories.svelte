<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { ChoroplethMap } from 'sniic-design-system';

  const siglaToName = {
    AC: 'Acre', AL: 'Alagoas', AM: 'Amazonas', AP: 'Amapá',
    BA: 'Bahia', CE: 'Ceará', DF: 'Distrito Federal', ES: 'Espírito Santo',
    GO: 'Goiás', MA: 'Maranhão', MG: 'Minas Gerais', MS: 'Mato Grosso do Sul',
    MT: 'Mato Grosso', PA: 'Pará', PB: 'Paraíba', PE: 'Pernambuco',
    PI: 'Piauí', PR: 'Paraná', RJ: 'Rio de Janeiro', RN: 'Rio Grande do Norte',
    RO: 'Rondônia', RR: 'Roraima', RS: 'Rio Grande do Sul', SC: 'Santa Catarina',
    SE: 'Sergipe', SP: 'São Paulo', TO: 'Tocantins',
  };

  const csvRows = [
    { uf: 'AC', valor_executado_rs: 17743059.01,  valor_executado_perc: 0.012232253546716629 },
    { uf: 'AL', valor_executado_rs: 35128148.39,  valor_executado_perc: 0.024217719024154084 },
    { uf: 'AM', valor_executado_rs: 44222860.52,  valor_executado_perc: 0.03048771027232946 },
    { uf: 'AP', valor_executado_rs: 17120298.32,  valor_executado_perc: 0.011802915705101221 },
    { uf: 'BA', valor_executado_rs: 76394220.84,  valor_executado_perc: 0.052666988160952034 },
    { uf: 'CE', valor_executado_rs: 78727917.79,  valor_executado_perc: 0.05427586365291261 },
    { uf: 'DF', valor_executado_rs: 21309243.88,  valor_executado_perc: 0.01469081931599683 },
    { uf: 'ES', valor_executado_rs: 29866850.17,  valor_executado_perc: 0.020590524086930635 },
    { uf: 'GO', valor_executado_rs: 55985604.87,  valor_executado_perc: 0.03859707130265207 },
    { uf: 'MA', valor_executado_rs: 63390851.19,  valor_executado_perc: 0.04370232685701153 },
    { uf: 'MG', valor_executado_rs: 110795695.1,  valor_executado_perc: 0.07638373031302391 },
    { uf: 'MS', valor_executado_rs: 23316653.57,  valor_executado_perc: 0.016074748901440724 },
    { uf: 'MT', valor_executado_rs: 24571646.22,  valor_executado_perc: 0.0169399541789193 },
    { uf: 'PA', valor_executado_rs: 73195925.77,  valor_executado_perc: 0.050462049531632004 },
    { uf: 'PB', valor_executado_rs: 37177439.73,  valor_executado_perc: 0.02563052226444329 },
    { uf: 'PE', valor_executado_rs: 75277246.24,  valor_executado_perc: 0.051896933994714865 },
    { uf: 'PI', valor_executado_rs: 31576333.77,  valor_executado_perc: 0.0217690602580254 },
    { uf: 'PR', valor_executado_rs: 73147845.91,  valor_executado_perc: 0.05042890276490597 },
    { uf: 'RJ', valor_executado_rs: 85881913.38,  valor_executado_perc: 0.05920790428241467 },
    { uf: 'RN', valor_executado_rs: 27951151.25,  valor_executado_perc: 0.01926982088150229 },
    { uf: 'RO', valor_executado_rs: 466832.92,    valor_executado_perc: 0.0003218395789686369 },
    { uf: 'RR', valor_executado_rs: 14908203.2,   valor_executado_perc: 0.010277873807757356 },
    { uf: 'RS', valor_executado_rs: 70502784.62,  valor_executado_perc: 0.04860536938615488 },
    { uf: 'SC', valor_executado_rs: 27961958.44,  valor_executado_perc: 0.019277271473203142 },
    { uf: 'SE', valor_executado_rs: 22540730.32,  valor_executado_perc: 0.015539819162355535 },
    { uf: 'SP', valor_executado_rs: 290180006.82, valor_executado_perc: 0.2000531822393009 },
    { uf: 'TO', valor_executado_rs: 21172903.86,  valor_executado_perc: 0.014596825056480222 },
  ];

  const states = Object.fromEntries(csvRows.map((d) => [siglaToName[d.uf], d]));

  const formatPerc = (v) =>
    v.toLocaleString('pt-BR', { style: 'percent', minimumFractionDigits: 1, maximumFractionDigits: 1 });

  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);

  const { Story } = defineMeta({
    title: 'Section 1/ChoroplethMap',
    component: ChoroplethMap,
    tags: ['autodocs'],
  });
</script>

<Story name="% do Valor Executado por Estado">
  {#snippet template()}
    <ChoroplethMap
      {states}
      metric="valor_executado_perc"
      label="% do valor total executado"
      format={formatPerc}
    />
  {/snippet}
</Story>

<Story name="Valor Executado (R$) por Estado">
  {#snippet template()}
    <ChoroplethMap
      {states}
      metric="valor_executado_rs"
      label="Valor executado (R$)"
      format={formatBRL}
    />
  {/snippet}
</Story>
