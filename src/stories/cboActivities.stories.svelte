<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { HorizontalBarChart, colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { top20CboData } from '$lib/data/section3';

  // @ts-ignore
  const formatNum = (v) => v.toLocaleString('pt-BR');

  const { Story } = defineMeta({
    title: 'Section 3/cboActivities',
    component: HorizontalBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Top 20 atividades econômicas dos contemplados com vínculo formal**

Entre os agentes culturais contemplados que possuem vínculo formal de trabalho (RAIS), as ocupações mais frequentes revelam um perfil heterogêneo — com destaque para funções administrativas, de ensino e de gestão pública.

A lista evidencia que o setor cultural formal no Brasil vai muito além das artes em sentido estrito, incluindo profissões de suporte administrativo e educacional que sustentam o ecossistema cultural.

**Fonte**: \`aggregate_cbo_rais.csv\` (cruzamento PNAB × RAIS).
          `,
        },
      },
    },
  });
</script>

<Story name="Top 20 atividades econômicas (CBO/RAIS)">
  {#snippet template()}
    <HorizontalBarChart
      data={top20CboData}
      color={colorScales.teal[2]}
      format={formatNum}
      xLabel="Quantidade de vínculos formais"
      margin={{ top: 20, right: 60, bottom: 40, left: 320 }}
    />
  {/snippet}
</Story>
