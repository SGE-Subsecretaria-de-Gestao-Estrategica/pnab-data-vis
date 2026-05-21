<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DataTable } from 'sniic-design-system';

  // Data from data/section_1/executed_value_by_uf.csv
  const brl = (v) => `R$ ${parseFloat(v).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  const pct = (v) => `${parseFloat(v).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%`;

  const columns = [
    { key: 'uf', label: 'UF', align: 'left', width: 80 },
    { key: 'valor_executado_estado', label: 'Valor Executado Estado', align: 'right', width: 200 },
    { key: 'valor_executado_municipio', label: 'Valor Executado Município', align: 'right', width: 200 },
    { key: 'valor_executado_total_uf', label: 'Valor Executado Total UF', align: 'right', width: 200 },
    { key: 'perc_valor_executado_estado', label: '% Estado', align: 'right', width: 120 },
    { key: 'perc_valor_executado_municipio', label: '% Município', align: 'right', width: 120 },
    { key: 'valor_executado_perc', label: '% Total', align: 'right', width: 100 },
  ];

  const rawRows = [
    { uf: 'AC', valor_executado_estado: '17743059.01', valor_executado_municipio: '6586724.67', valor_executado_total_uf: '24329783.68', perc_valor_executado_estado: '72.93', perc_valor_executado_municipio: '27.07', valor_executado_perc: '0.85' },
    { uf: 'AL', valor_executado_estado: '35128148.39', valor_executado_municipio: '25166845.74', valor_executado_total_uf: '60294994.13', perc_valor_executado_estado: '58.26', perc_valor_executado_municipio: '41.74', valor_executado_perc: '2.12' },
    { uf: 'AM', valor_executado_estado: '44222860.52', valor_executado_municipio: '29899488.39', valor_executado_total_uf: '74122348.91', perc_valor_executado_estado: '59.66', perc_valor_executado_municipio: '40.34', valor_executado_perc: '2.60' },
    { uf: 'AP', valor_executado_estado: '17120298.32', valor_executado_municipio: '6513387.84', valor_executado_total_uf: '23633686.16', perc_valor_executado_estado: '72.44', perc_valor_executado_municipio: '27.56', valor_executado_perc: '0.83' },
    { uf: 'BA', valor_executado_estado: '76394220.84', valor_executado_municipio: '100514894.00', valor_executado_total_uf: '176909114.84', perc_valor_executado_estado: '43.18', perc_valor_executado_municipio: '56.82', valor_executado_perc: '6.22' },
    { uf: 'CE', valor_executado_estado: '78727917.79', valor_executado_municipio: '57895018.28', valor_executado_total_uf: '136622936.07', perc_valor_executado_estado: '57.62', perc_valor_executado_municipio: '42.38', valor_executado_perc: '4.80' },
    { uf: 'DF', valor_executado_estado: '21309243.88', valor_executado_municipio: '19861456.41', valor_executado_total_uf: '41170700.29', perc_valor_executado_estado: '51.76', perc_valor_executado_municipio: '48.24', valor_executado_perc: '1.45' },
    { uf: 'ES', valor_executado_estado: '29866850.17', valor_executado_municipio: '25863743.17', valor_executado_total_uf: '55730593.34', perc_valor_executado_estado: '53.59', perc_valor_executado_municipio: '46.41', valor_executado_perc: '1.96' },
    { uf: 'GO', valor_executado_estado: '55985604.87', valor_executado_municipio: '49518835.53', valor_executado_total_uf: '105504440.40', perc_valor_executado_estado: '53.06', perc_valor_executado_municipio: '46.94', valor_executado_perc: '3.71' },
    { uf: 'MA', valor_executado_estado: '63390851.19', valor_executado_municipio: '51530178.86', valor_executado_total_uf: '114921030.05', perc_valor_executado_estado: '55.16', perc_valor_executado_municipio: '44.84', valor_executado_perc: '4.04' },
    { uf: 'MG', valor_executado_estado: '110795695.10', valor_executado_municipio: '157760031.83', valor_executado_total_uf: '268555726.93', perc_valor_executado_estado: '41.26', perc_valor_executado_municipio: '58.74', valor_executado_perc: '9.44' },
    { uf: 'MS', valor_executado_estado: '23316653.57', valor_executado_municipio: '19035286.17', valor_executado_total_uf: '42351939.74', perc_valor_executado_estado: '55.05', perc_valor_executado_municipio: '44.95', valor_executado_perc: '1.49' },
    { uf: 'MT', valor_executado_estado: '24571646.22', valor_executado_municipio: '23822260.19', valor_executado_total_uf: '48393906.41', perc_valor_executado_estado: '50.77', perc_valor_executado_municipio: '49.23', valor_executado_perc: '1.70' },
    { uf: 'PA', valor_executado_estado: '73195925.77', valor_executado_municipio: '50865910.35', valor_executado_total_uf: '124061836.12', perc_valor_executado_estado: '59.00', perc_valor_executado_municipio: '41.00', valor_executado_perc: '4.36' },
    { uf: 'PB', valor_executado_estado: '37177439.73', valor_executado_municipio: '33051646.94', valor_executado_total_uf: '70229086.67', perc_valor_executado_estado: '52.94', perc_valor_executado_municipio: '47.06', valor_executado_perc: '2.47' },
    { uf: 'PE', valor_executado_estado: '75277246.24', valor_executado_municipio: '66231622.95', valor_executado_total_uf: '141508869.19', perc_valor_executado_estado: '53.20', perc_valor_executado_municipio: '46.80', valor_executado_perc: '4.97' },
    { uf: 'PI', valor_executado_estado: '31576333.77', valor_executado_municipio: '25714798.49', valor_executado_total_uf: '57291132.26', perc_valor_executado_estado: '55.12', perc_valor_executado_municipio: '44.88', valor_executado_perc: '2.01' },
    { uf: 'PR', valor_executado_estado: '73147845.91', valor_executado_municipio: '80127416.37', valor_executado_total_uf: '153275262.28', perc_valor_executado_estado: '47.72', perc_valor_executado_municipio: '52.28', valor_executado_perc: '5.39' },
    { uf: 'RJ', valor_executado_estado: '85881913.38', valor_executado_municipio: '100192361.59', valor_executado_total_uf: '186074274.97', perc_valor_executado_estado: '46.15', perc_valor_executado_municipio: '53.85', valor_executado_perc: '6.54' },
    { uf: 'RN', valor_executado_estado: '27951151.25', valor_executado_municipio: '26104858.85', valor_executado_total_uf: '54056010.10', perc_valor_executado_estado: '51.71', perc_valor_executado_municipio: '48.29', valor_executado_perc: '1.90' },
    { uf: 'RO', valor_executado_estado: '466832.92', valor_executado_municipio: '8362693.40', valor_executado_total_uf: '8829526.32', perc_valor_executado_estado: '5.29', perc_valor_executado_municipio: '94.71', valor_executado_perc: '0.31' },
    { uf: 'RR', valor_executado_estado: '14908203.20', valor_executado_municipio: '1552820.75', valor_executado_total_uf: '16461023.95', perc_valor_executado_estado: '90.57', perc_valor_executado_municipio: '9.43', valor_executado_perc: '0.58' },
    { uf: 'RS', valor_executado_estado: '70502784.62', valor_executado_municipio: '80648653.25', valor_executado_total_uf: '151151437.87', perc_valor_executado_estado: '46.64', perc_valor_executado_municipio: '53.36', valor_executado_perc: '5.31' },
    { uf: 'SC', valor_executado_estado: '27961958.44', valor_executado_municipio: '54160978.86', valor_executado_total_uf: '82122937.30', perc_valor_executado_estado: '34.05', perc_valor_executado_municipio: '65.95', valor_executado_perc: '2.89' },
    { uf: 'SE', valor_executado_estado: '22540730.32', valor_executado_municipio: '17894990.59', valor_executado_total_uf: '40435720.91', perc_valor_executado_estado: '55.74', perc_valor_executado_municipio: '44.26', valor_executado_perc: '1.42' },
    { uf: 'SP', valor_executado_estado: '290180006.82', valor_executado_municipio: '265662422.46', valor_executado_total_uf: '555842429.28', perc_valor_executado_estado: '52.21', perc_valor_executado_municipio: '47.79', valor_executado_perc: '19.53' },
    { uf: 'TO', valor_executado_estado: '21172903.86', valor_executado_municipio: '10941941.96', valor_executado_total_uf: '32114845.82', perc_valor_executado_estado: '65.93', perc_valor_executado_municipio: '34.07', valor_executado_perc: '1.13' },
  ];

  const rows = rawRows.map((d) => ({
    uf: d.uf,
    valor_executado_estado: brl(d.valor_executado_estado),
    valor_executado_municipio: brl(d.valor_executado_municipio),
    valor_executado_total_uf: brl(d.valor_executado_total_uf),
    perc_valor_executado_estado: pct(d.perc_valor_executado_estado),
    perc_valor_executado_municipio: pct(d.perc_valor_executado_municipio),
    valor_executado_perc: pct(d.valor_executado_perc),
  }));

  const { Story } = defineMeta({
    title: 'Section 1/DataTable',
    component: DataTable,
    tags: ['autodocs'],
  });
</script>

<Story name="Valor executado por UF">
  {#snippet template()}
    <svg width={1020} height={920}>
      <DataTable {columns} {rows} />
    </svg>
  {/snippet}
</Story>
