<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DataTable } from 'sniic-design-system';

  const columns = [
    { key: 'ente',           label: 'Ente',                          align: 'left',  width: 260 },
    { key: 'valor_repassado', label: 'Valor Repassado no Ciclo 1',   align: 'right', width: 240 },
    { key: 'valor_executado', label: 'Valor Executado até 31/12/25', align: 'right', width: 240 },
    { key: 'perc_executado',  label: '% Executado',                  align: 'right', width: 120 },
  ];

  const rows = [
    {
      ente:            'Estados e Distrito Federal',
      valor_repassado: 'R$ 1.510.000.000,00',
      valor_executado: 'R$ 1.466.894.326,10',
      perc_executado:  '97,1%',
    },
    {
      ente:            'Municípios e Distrito Federal',
      valor_repassado: 'R$ 1.490.000.000,00',
      valor_executado: 'R$ 1.407.543.234,58',
      perc_executado:  '94,5%',
    },
    {
      ente:            'Total',
      valor_repassado: 'R$ 3.000.000.000,00',
      valor_executado: 'R$ 2.874.437.560,68',
      perc_executado:  '95,8%',
    },
  ];

  const { Story } = defineMeta({
    title: 'Section 1/Tabela 1',
    component: DataTable,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Repasse e Execução — Ciclo 1 (por ente federativo)**

Síntese dos valores repassados e executados no Ciclo 1 da Política Nacional Aldir Blanc até 31/12/2025:

- **Estados e DF**: R$ 1,51 bi repassados → R$ 1,47 bi executados (97,1%)
- **Municípios e DF**: R$ 1,49 bi repassados → R$ 1,41 bi executados (94,5%)
- **Total**: R$ 3,00 bi repassados → R$ 2,87 bi executados (95,8%)

**Fonte**: BB Ágil — execução acumulada até 31/12/2025.
          `,
        },
      },
    },
  });
</script>

<Story name="Repasse e Execução — Totais por Ente">
  {#snippet template()}
    <div style="overflow-x: auto;">
      <svg width={900} height={200}>
        <DataTable {columns} {rows} headerColor="#4271b5" />
      </svg>
    </div>
  {/snippet}
</Story>
