<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  // @ts-ignore
  import { colorPairs } from 'sniic-design-system';
  import VerticalGroupedBarChart from '$lib/components/VerticalGroupedBarChart.svelte';
  // @ts-ignore
  import { valorMedioSexoPorteData, valorMedioSexoSeriesLabels } from '$lib/data/section3';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(v);

  const sexColors = [colorPairs.bluePurple[1], colorPairs.bluePurple[0]];

  const { Story } = defineMeta({
    title: 'Section 3/valorMedioSexoByPorte',
    component: VerticalGroupedBarChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Valor médio recebido por sexo e porte municipal**

Em todas as faixas de porte populacional, os agentes culturais do sexo masculino receberam, em média, valores superiores aos do sexo feminino. A maior diferença proporcional ocorre nos municípios de **Pequeno porte I**, onde as agentes do sexo feminino receberam em média **R$2,7 mil** frente a **R$3,4 mil** dos agentes do sexo masculino.

Nos **Entes Estatais** os valores médios são os mais elevados, refletindo o perfil institucional das entidades atendidas diretamente por estados.
          `,
        },
      },
    },
  });
</script>

<Story name="Barras verticais agrupadas — Valor médio por sexo e porte municipal">
  {#snippet template()}
    <VerticalGroupedBarChart
      data={valorMedioSexoPorteData}
      seriesLabels={valorMedioSexoSeriesLabels}
      colors={sexColors}
      format={formatBRL}
      barWidth={36}
      barPad={14}
      innerH={300}
      margin={{ top: 20, right: 20, bottom: 10, left: 72 }}
    />
  {/snippet}
</Story>
