<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { categorical8 } from 'sniic-design-system';
  import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
  // @ts-ignore
  import { regiaoContempladosFaixaData, UF_BAND_KEYS, UF_BAND_LABELS } from '$lib/data/section2';

  // @ts-ignore
  const formatPct = (v) =>
    v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

  const { Story } = defineMeta({
    title: 'Section 2/regiaoContempladosFaixa',
    component: HorizontalStackedBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição de contemplados por faixa de valor × região**

Cada barra representa uma região do Brasil e totaliza 100%, permitindo comparar o **perfil de distribuição das faixas de valor** entre Norte, Nordeste, Centro-Oeste, Sudeste e Sul.

Regiões com maior participação nas faixas mais altas (acima de R$50 mil) tendem a concentrar agentes culturais com maior volume individual de recursos recebidos. O contraste entre regiões revela desigualdades estruturais no acesso às faixas superiores de pagamento.

**Fonte**: execução estadual agregada por região (\`aggregate_faixa_valor_ju_wide_by_uf.csv\`).
          `,
        },
      },
    },
  });
</script>

<Story name="Contemplados por faixa de valor — por região">
  {#snippet template()}
    <div style="padding: 16px;">
      <HorizontalStackedBarChartCustom
        data={regiaoContempladosFaixaData}
        keys={[...UF_BAND_KEYS]}
        labels={UF_BAND_LABELS}
        colors={categorical8}
        format={formatPct}
        rowHeight={48}
        marginLeft={120}
      />
    </div>
  {/snippet}
</Story>
