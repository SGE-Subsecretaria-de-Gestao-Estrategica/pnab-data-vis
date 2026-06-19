<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import ChoroplethMapLabeled from '$lib/components/ExecutedValueByStateMap.svelte';
  import { states } from '$lib/data/section1';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);

  // @ts-ignore
  const formatPercFix = (v) => `${v.toFixed(1)}%`;

  const { Story } = defineMeta({
    title: 'Section 1/Grafico 1',
    component: ChoroplethMapLabeled,
    tags: ['autodocs'],
  });
</script>

<Story name="Recurso Executado por Estado">
  {#snippet template()}
    <div style="font-family: 'Space Grotesk', system-ui, sans-serif;">
      <ChoroplethMapLabeled
        {states}
        metric="valor_executado_rs"
        label="Recurso executado (R$)"
        format={formatBRL}
        formatLine2={(row) => formatPercFix(row.valor_executado_perc * 100)}
        showSideLegend={true}
        legCols={2}
        mapFrac={0.72}
      />
    </div>
  {/snippet}
</Story>
