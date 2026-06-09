<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DataTable } from 'sniic-design-system';

  const columns = [
    { key: 'indicador', label: 'Indicador', align: 'left', width: 340 },
    { key: 'estados', label: 'Estados', align: 'center', width: 160 },
    { key: 'municipios', label: 'Municípios', align: 'center', width: 160 },
  ];

  const rows = [
    { indicador: 'Número de contemplados',                          estados: '22.050',          municipios: '144.836'       },
    { indicador: 'Ticket médio dos pagamentos',                     estados: 'R$ 52.711',        municipios: 'R$ 7.839'      },
    { indicador: 'Concentração dos contemplados, por faixa de valor', estados: 'De 10 a 50 mil', municipios: 'De 2 a 10 mil' },
    { indicador: 'Concentração do recurso executado, por faixa de valor', estados: 'Acima de 200 mil', municipios: 'De 10 a 50 mil' },
  ];

  const { Story } = defineMeta({
    title: 'Section 2/resumoEstadosMunicipios',
    component: DataTable,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Tabela-resumo comparativa: Estados vs Municípios**

Síntese dos principais indicadores de execução financeira comparando os dois níveis de esfera pública:

- **Número de contemplados**: estados (22.050) vs municípios (144.836)
- **Ticket médio**: estados concentram pagamentos muito maiores (R$52.711 vs R$7.839)
- **Concentração por faixa**: estados lideram na faixa R$10–50k (contemplados) e acima de R$200k (valor); municípios na faixa R$2–10k e R$10–50k respectivamente

**Fonte**: execução estadual e municipal agregada por faixa de valor.
          `,
        },
      },
    },
  });
</script>

<Story name="Tabela resumo — Estados vs Municípios">
  {#snippet template()}
    <div style="overflow-x: auto;">
      <svg width={700} height={220}>
        <DataTable {columns} {rows} />
      </svg>
    </div>
  {/snippet}
</Story>
