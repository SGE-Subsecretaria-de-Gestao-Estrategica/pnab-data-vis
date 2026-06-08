<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { categorical8 } from 'sniic-design-system';
  import VerticalStackedBarChartCustom from '$lib/components/VerticalStackedBarChartCustom.svelte';
  // @ts-ignore
  import { portePagamentosData, UF_BAND_KEYS, UF_BAND_LABELS } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 2/valueRangeByPorte',
    component: VerticalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição dos pagamentos por porte de município**

Cada barra representa um porte de município, mostrando como os pagamentos se distribuem por faixa de valor dentro de cada categoria. Os rótulos percentuais estão exibidos diretamente dentro de cada segmento.

Municípios de **grande porte** concentram proporcionalmente mais pagamentos nas faixas mais altas — reflexo do peso de CNPJs e entidades culturais nessas cidades. Municípios **Pequenos I** têm a maior fatia nas faixas mais baixas (até R$2k e R$2–10k), indicando que o programa alcança um perfil de beneficiário com menor porte financeiro formal.

**Fonte**: \`values_by_population_size.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Faixa de valor por porte de município">
  {#snippet template()}
    <VerticalStackedBarChartCustom
      data={portePagamentosData}
      keys={[...UF_BAND_KEYS]}
      labels={UF_BAND_LABELS}
      colors={categorical8}
      format={formatPct}
      normalize={true}
      height={420}
    />
  {/snippet}
</Story>
