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
    title: 'Section 1/executedValueByState',
    component: ChoroplethMapLabeled,
    tags: ['autodocs'],
  });
</script>

<Story name="Valor Executado por Estado">
  {#snippet template()}
    <div style="font-family: 'Space Grotesk', system-ui, sans-serif;">
      <ChoroplethMapLabeled
        {states}
        metric="valor_executado_rs"
        label="Valor executado"
        format={formatBRL}
        formatLine2={(row) => formatPercFix(row.valor_executado_perc * 100)}
        showSideLegend={true}
      />
    </div>
  {/snippet}
</Story>
