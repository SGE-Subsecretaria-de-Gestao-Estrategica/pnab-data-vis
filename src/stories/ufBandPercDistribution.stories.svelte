<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { categorical8 } from 'sniic-design-system';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  // @ts-ignore
  import { ufBandPercData, UF_BAND_KEYS, UF_BAND_LABELS } from '$lib/data/section2';

  // @ts-ignore
  const formatPctFixed = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 2/Grafico 13',
    component: HorizontalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição dos Contemplados por Faixa de Valor nas Unidades Federativas**

Cada barra representa uma UF e totaliza 100%, permitindo comparar o **perfil de distribuição das faixas de valor** entre os estados e o Distrito Federal. As UFs estão ordenadas pela proporção de contemplados nas faixas mais altas (acima de R$50 mil).

**Fonte**: \`aggregate_faixa_valor_ju_wide_by_uf.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Contemplados por faixa de valor — por UF">
  {#snippet template()}
    <div style="padding: 16px;">
      <HorizontalStackedBarChartCustom
        data={ufBandPercData}
        keys={[...UF_BAND_KEYS]}
        labels={UF_BAND_LABELS}
        colors={categorical8}
        format={formatPctFixed}
        rowHeight={36}
        marginLeft={40}
      />
    </div>
  {/snippet}
</Story>
