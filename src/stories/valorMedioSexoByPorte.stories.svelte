<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  // @ts-ignore
  import { colorScales } from 'sniic-design-system';
  import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
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

  const sexColors = [colorScales.blue[2], colorScales.yellow[2]];

  const { Story } = defineMeta({
    title: 'Section 3/valorMedioSexoByPorte',
    component: HorizontalGroupedBarChart,
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

<Story name="Barras horizontais agrupadas — Valor médio por sexo e porte municipal">
  {#snippet template()}
    <HorizontalGroupedBarChart
      data={valorMedioSexoPorteData}
      seriesLabels={valorMedioSexoSeriesLabels}
      colors={sexColors}
      format={formatBRL}
      barHeight={28}
      barPad={4}
      groupPad={14}
      rx={1}
      legendBottom={true}
      labelsInside={true}
      margin={{ top: 20, right: 70, bottom: 40, left: 110 }}
    />
  {/snippet}
</Story>
