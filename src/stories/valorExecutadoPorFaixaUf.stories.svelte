<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  import { categorical8 } from 'sniic-design-system';

  // @ts-ignore
  import { ufValorBandPercData, UF_BAND_KEYS, UF_BAND_LABELS } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 2/Grafico 11',
    component: HorizontalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição dos Recursos Executados nas Unidades Federativas, por Faixa de Valor**

Cada barra representa uma UF e mostra como os recursos executados se distribuíram pelas faixas de valor. Os dados usam \`perc_valor_*\` (percentual do valor total), e não contagem de contemplados.

UFs estão ordenadas pela proporção de recursos nas faixas mais altas (≥ R$50k) de forma decrescente.

**Fonte**: \`aggregate_faixa_valor_ju_wide_by_uf.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Distribuição dos Recursos por Faixa de Valor — por UF">
  {#snippet template()}
    <HorizontalStackedBarChartCustom
      data={ufValorBandPercData}
      keys={[...UF_BAND_KEYS]}
      labels={UF_BAND_LABELS}
      colors={categorical8}
      format={formatPct}
      rowHeight={28}
      marginLeft={40}
    />
  {/snippet}
</Story>
