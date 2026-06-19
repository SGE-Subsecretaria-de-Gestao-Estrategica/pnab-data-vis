<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorPairs } from 'sniic-design-system';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  // @ts-ignore
  import { faixaEtariaSexoData, FAIXA_SEXO_KEYS, FAIXA_SEXO_LABELS } from '$lib/data/section5';

  const { Story } = defineMeta({
    title: 'Section 5/cadunicoFaixaSexo',
    component: HorizontalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição por sexo em cada faixa etária — CadÚnico**

Nas faixas de **25 a 64 anos** as mulheres são maioria entre os contemplados inscritos no CadÚnico. Apenas na faixa mais jovem (15–24 anos) os homens representam mais da metade. Cada barra soma 100%, mostrando a proporção feminino/masculino dentro de cada faixa etária.

**Fonte**: \`aggregate_cadunico_faixa_etaria_by_sexo.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="HorizontalStackedBarChart — faixa etaria por sexo (bluePurple)">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={faixaEtariaSexoData}
      keys={[...FAIXA_SEXO_KEYS]}
      labels={FAIXA_SEXO_LABELS}
      colors={[colorPairs.bluePurple[0], colorPairs.bluePurple[1]]}
      format={(v) => `${v.toFixed(1)}%`}
      rowHeight={44}
      showTotalLabel={false}
      marginLeft={110}
    />
  {/snippet}
</Story>

<Story name="HorizontalStackedBarChart — faixa etaria por sexo (blueOrange)">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={faixaEtariaSexoData}
      keys={[...FAIXA_SEXO_KEYS]}
      labels={FAIXA_SEXO_LABELS}
      colors={[colorPairs.bluePurple[0], colorPairs.bluePurple[1]]}
      format={(v) => `${v.toFixed(1)}%`}
      rowHeight={44}
      showTotalLabel={false}
      marginLeft={110}
    />
  {/snippet}
</Story>
