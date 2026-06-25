<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DataTable } from 'sniic-design-system';
  import { porteMeanData } from '$lib/data/section1';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(v);

  // @ts-ignore
  const formatInt = (v) => new Intl.NumberFormat('pt-BR').format(v);

  const porteLabels = {
    'Pequeno I':  'Pequeno Porte I',
    'Pequeno II': 'Pequeno Porte II',
    'Médio':      'Médio Porte',
    'Grande':     'Grande Porte',
  };
  const porteOrder = ['Pequeno I', 'Pequeno II', 'Médio', 'Grande'];

  const columns = [
    { key: 'porte', label: 'Porte de Município', align: 'left', width: 200 },
    { key: 'n_municipios', label: 'Nº de Municípios no Brasil', align: 'right', width: 220 },
    { key: 'recurso_total', label: 'Recurso Total Executado', align: 'right', width: 220 },
    { key: 'media_recurso', label: 'Média de Recurso Executado por Município', align: 'right', width: 300 },
  ];

  const rows = [...porteMeanData]
    .sort((a, b) => porteOrder.indexOf(a.label) - porteOrder.indexOf(b.label))
    .map((d) => ({
      // @ts-ignore
      porte:         porteLabels[d.label] ?? d.label,
      n_municipios:  formatInt(d.municipios),
      recurso_total: formatBRL(d.valor_total),
      media_recurso: formatBRL(d.valor_medio_municipio),
    }));

  const { Story } = defineMeta({
    title: 'Section 1/Tabela 2',
    component: DataTable,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Recurso executado por porte de município**

Distribuição dos recursos da PNAB pelos quatro portes populacionais de municípios, com total executado e média por município.
          `,
        },
      },
    },
  });
</script>

<Story name="Valor executado por porte">
  {#snippet template()}
    <div style="overflow-x: auto;">
      <svg width={980} height={220}>
        <DataTable {columns} {rows} />
      </svg>
    </div>
  {/snippet}
</Story>
