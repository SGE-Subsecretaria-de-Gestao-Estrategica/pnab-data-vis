<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { ProportionalAreaChart, StatesSilhouetteChart, RegionSilhouetteChart, categorical8 } from 'sniic-design-system';
  import { rankingData, regionAreaData, silhouetteStateData, silhouetteRegionData } from '$lib/data/section1';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency', currency: 'BRL',
      notation: 'compact', maximumFractionDigits: 0,
    }).format(v);

  const { Story } = defineMeta({
    title: 'Section 1/proportionalByState',
    component: ProportionalAreaChart,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Sentindo a concentração antes de calculá-la**

Às vezes, os números precisam virar forma para que o leitor realmente sinta o que está sendo dito.

Neste gráfico, a **área de cada círculo é proporcional ao valor executado** pelo estado. O resultado é imediato: a bolha de São Paulo domina o espaço visual de maneira que nenhuma barra ou tabela consegue transmitir com a mesma força.

A versão regional revela um segundo padrão: o Sudeste como um todo seria o maior círculo, mas o Nordeste — frequentemente invisível nos debates de investimento — aparece como o segundo maior bloco, à frente do Sul e do Centro-Oeste.

Este gráfico foi concebido para que o leitor *sinta* a concentração antes de processá-la numericamente.
          `,
        },
      },
    },
  });
</script>

<Story name="Área proporcional — Valor executado por estado">
  {#snippet template()}
    <ProportionalAreaChart
      data={rankingData}
      maxRadius={90}
      colors={categorical8}
      format={formatBRL}
      showLabels={true}
    />
  {/snippet}
</Story>

<Story name="Área proporcional — Valor executado por região">
  {#snippet template()}
    <ProportionalAreaChart
      data={regionAreaData}
      maxRadius={110}
      colors={categorical8}
      format={formatBRL}
      showLabels={true}
    />
  {/snippet}
</Story>

<Story name="Silhueta proporcional — Valor executado por estado">
  {#snippet template()}
    <StatesSilhouetteChart
      data={silhouetteStateData}
      maxSize={120}
      colors={categorical8}
      format={formatBRL}
      showLabels={true}
    />
  {/snippet}
</Story>

<Story name="Silhueta proporcional — Valor executado por região">
  {#snippet template()}
    <RegionSilhouetteChart
      data={silhouetteRegionData}
      maxSize={200}
      colors={categorical8}
      format={formatBRL}
      showLabels={true}
    />
  {/snippet}
</Story>
