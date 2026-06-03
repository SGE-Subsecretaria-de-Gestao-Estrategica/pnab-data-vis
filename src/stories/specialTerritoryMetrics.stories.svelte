<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalStackedBarChart, categorical8 } from 'sniic-design-system';
  import { specialTerritoriesMetrics } from '$lib/data/section1';

  // @ts-ignore
  const formatPerc = (v) => `${v.toFixed(1)}%`;

  const stByName = {};
  specialTerritoriesMetrics.forEach((d) => { stByName[d.territorio] = d; });
  const stFav  = stByName['Favela e Comunidade Urbana'] || { perc_populacao: 0, perc_recurso: 0, perc_agentes: 0 };
  const stQui  = stByName['Agrupamento quilombola']     || { perc_populacao: 0, perc_recurso: 0, perc_agentes: 0 };
  const stInd  = stByName['Agrupamento indígena']       || { perc_populacao: 0, perc_recurso: 0, perc_agentes: 0 };

  const stKeys   = ['favela', 'quilombola', 'indigena'];
  const stLabels = { favela: 'Favela / Com. Urbana', quilombola: 'Quilombola', indigena: 'Indígena' };
  const stStackedData = [
    {
      cat: '% da população',
      favela:     stFav.perc_populacao,
      quilombola: stQui.perc_populacao,
      indigena:   stInd.perc_populacao,
    },
    {
      cat: '% dos recursos',
      favela:     stFav.perc_recurso,
      quilombola: stQui.perc_recurso,
      indigena:   stInd.perc_recurso,
    },
    {
      cat: '% dos agentes',
      favela:     stFav.perc_agentes,
      quilombola: stQui.perc_agentes,
      indigena:   stInd.perc_agentes,
    },
  ];

  const { Story } = defineMeta({
    title: 'Section 1/specialTerritoryMetrics',
    component: HorizontalStackedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Sub-representação nos territórios especiais**

Comparação entre % da população, % dos recursos executados e % dos agentes contemplados
para Favelas e Comunidades Urbanas, Quilombolas e Territórios Indígenas.

Em todos os territórios, a fatia da **população** supera a fatia de **recursos** e de **agentes contemplados** — evidenciando um padrão sistemático de sub-representação.
          `,
        },
      },
    },
  });
</script>

<Story name="Métricas por território especial">
  {#snippet template()}
    <div style="padding-left: 100px;">
      <HorizontalStackedBarChart
        data={stStackedData}
        keys={stKeys}
        categoryKey="cat"
        labels={stLabels}
        colors={categorical8}
        format={formatPerc}
        showTotalLabel={true}
      />
    </div>
  {/snippet}
</Story>
