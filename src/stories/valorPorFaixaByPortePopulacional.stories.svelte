<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { categorical8 } from 'sniic-design-system';
  import VerticalStackedBarChartCustom from '$lib/components/VerticalStackedBarChartCustom.svelte';
  // @ts-ignore
  import { porteValorPercData, UF_BAND_KEYS, UF_BAND_LABELS } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 2/valorPorFaixaByPortePopulacional',
    component: VerticalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**% do valor pago por faixa de valor e porte de município**

Cada barra representa um porte de município, mostrando como o **valor total pago** se distribui pelas faixas de valor dentro de cada categoria. Os rótulos percentuais estão exibidos diretamente dentro de cada segmento.

Municípios de **grande porte** concentram proporcionalmente mais recursos nas faixas mais altas (acima de R$200k e R$50–200k), enquanto municípios de **pequeno porte I** direcionam a maior fatia do valor para a faixa de R$2–10k.

**Fonte**: \`faixa_valor_porte_populacional.csv\`.
          `,
        },
      },
    },
  });
</script>

<Story name="Valor pago por faixa e porte de município">
  {#snippet template()}
    <VerticalStackedBarChartCustom
      data={porteValorPercData}
      keys={[...UF_BAND_KEYS]}
      labels={UF_BAND_LABELS}
      colors={categorical8}
      format={formatPct}
      normalize={true}
      height={420}
    />
  {/snippet}
</Story>
