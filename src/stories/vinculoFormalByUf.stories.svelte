<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { StatesSilhouetteChart, HorizontalBarChart, colorScales, categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import { ufSilhouetteData, ufRankingData } from '$lib/data/section4';

  // @ts-ignore
  const formatN = (v) => v.toLocaleString('pt-BR');
  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 4/vinculoFormalByUf',
    component: StatesSilhouetteChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição estadual do emprego formal no setor cultural**

Em volume absoluto, **SP, MG e BA** lideram em beneficiários com vínculo formal. Normalizado pelo total de cada estado, o ranking muda: **Amapá** e **Acre** sobem ao topo — estados onde a infraestrutura cultural formal, embora pequena, é proporcionalmente mais representada.
          `,
        },
      },
    },
  });
</script>

<Story name="Silhueta — Beneficiários com vínculo formal por UF">
  {#snippet template()}
    <StatesSilhouetteChart
      data={ufSilhouetteData}
      maxSize={120}
      colors={categorical8}
      format={formatN}
      showLabels={true}
    />
  {/snippet}
</Story>

<Story name="Ranking — % com vínculo formal por UF">
  {#snippet template()}
    <HorizontalBarChart
      data={ufRankingData}
      color={colorScales.lime[2]}
      format={formatPct}
      xLabel="% beneficiários com vínculo formal"
      margin={{ top: 20, right: 60, bottom: 40, left: 50 }}
    />
  {/snippet}
</Story>
