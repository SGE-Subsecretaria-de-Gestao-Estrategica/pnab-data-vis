<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DataTable } from 'sniic-design-system';

  const columns = [
    { key: 'porte', label: 'Porte de Município', align: 'left', width: 200 },
    { key: 'n_municipios', label: 'Nº de Municípios no Brasil', align: 'right', width: 220 },
    { key: 'recurso_total', label: 'Recurso Total Executado', align: 'right', width: 220 },
    { key: 'media_recurso', label: 'Média de Recurso Executado por Município', align: 'right', width: 300 },
  ];

  const rows = [
    { porte: 'Pequeno Porte I',  n_municipios: '3.401', recurso_total: 'R$ 266.445.332,42', media_recurso: 'R$ 78.343,23'    },
    { porte: 'Pequeno Porte II', n_municipios: '1.030', recurso_total: 'R$ 234.896.275,23', media_recurso: 'R$ 228.054,63'   },
    { porte: 'Médio Porte',      n_municipios: '334',   recurso_total: 'R$ 161.197.608,53', media_recurso: 'R$ 482.627,57'   },
    { porte: 'Grande Porte',     n_municipios: '332',   recurso_total: 'R$ 732.942.051,71', media_recurso: 'R$ 2.207.656,78' },
  ];

  const { Story } = defineMeta({
    title: 'Section 1/executedValueByPorte',
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
