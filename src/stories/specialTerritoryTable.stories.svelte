<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { DataTable } from 'sniic-design-system';
  import { specialTerritoriesMetrics } from '$lib/data/section1';

  const territoryNames = {
    'Favela e Comunidade Urbana': 'Favelas e Comunidades Urbanas',
    'Agrupamento quilombola':     'Agrupamentos quilombolas',
    'Agrupamento indígena':       'Agrupamentos indígenas',
  };

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(v);

  // @ts-ignore
  const formatPerc = (v) => `${v.toFixed(1)}%`;

  const columns = [
    { key: 'territorio',     label: 'Território',                                                    align: 'left',  width: 260 },
    { key: 'valor',          label: 'Valor (R$)',                                                    align: 'right', width: 190 },
    { key: 'perc_recurso',   label: '% dos recursos executados na Política',                         align: 'right', width: 130 },
    { key: 'perc_agentes',   label: '% de agentes contemplados na Política residente no território', align: 'right', width: 130 },
    { key: 'perc_populacao', label: '% da população total residente no território',                  align: 'right', width: 130 },
  ];

  // @ts-ignore
  const dataRows = specialTerritoriesMetrics.map((d) => ({
    territorio:     territoryNames[d.territorio] ?? d.territorio,
    valor:          formatBRL(d.valor),
    perc_recurso:   formatPerc(d.perc_recurso),
    perc_agentes:   formatPerc(d.perc_agentes),
    perc_populacao: formatPerc(d.perc_populacao),
  }));

  const totals = specialTerritoriesMetrics.reduce(
    (acc, d) => ({
      valor:          acc.valor + d.valor,
      perc_recurso:   acc.perc_recurso + d.perc_recurso,
      perc_agentes:   acc.perc_agentes + d.perc_agentes,
      perc_populacao: acc.perc_populacao + d.perc_populacao,
    }),
    { valor: 0, perc_recurso: 0, perc_agentes: 0, perc_populacao: 0 },
  );

  const rows = [
    ...dataRows,
    {
      territorio:     'Total',
      valor:          formatBRL(totals.valor),
      perc_recurso:   formatPerc(totals.perc_recurso),
      perc_agentes:   formatPerc(totals.perc_agentes),
      perc_populacao: formatPerc(totals.perc_populacao),
    },
  ];

  const { Story } = defineMeta({
    title: 'Section 1/specialTerritoryTable',
    component: DataTable,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Territórios especiais: recursos, agentes e população**

Comparação entre o valor executado, a participação nos recursos da política, a proporção de agentes contemplados e o peso demográfico de cada território especial.
          `,
        },
      },
    },
  });
</script>

<Story name="Tabela — Territórios Especiais">
  {#snippet template()}
    <div style="overflow-x: auto;">
      <svg width={840} height={260}>
        <DataTable {columns} {rows} headerColor="#4271b5" />
      </svg>
    </div>
  {/snippet}
</Story>
