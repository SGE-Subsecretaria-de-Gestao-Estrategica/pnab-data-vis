<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import HorizontalBarChartCustom from '$lib/components/HorizontalBarChartCustom.svelte';
  // @ts-ignore
  import { fomentoSubData } from '$lib/data/section6';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(v);

  const chartData = fomentoSubData.map((d) => ({ label: d.label, value: d.valor }));

  const { Story } = defineMeta({
    title: 'Section 6/fomentoSubcategorias',
    component: HorizontalBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Subcategorias de Fomento Cultural**

Distribuição dos recursos dentro da categoria Fomento Cultural, mostrando valores absolutos estimados e participação percentual no total geral.
          `,
        },
      },
    },
  });
</script>

<Story name="Subcategorias de Fomento Cultural">
  {#snippet template()}
    <HorizontalBarChartCustom
      data={chartData}
      color={colorScales.blue[2]}
      format={formatBRL}
      xLabel="Valor estimado (R$)"
      margin={{ top: 20, right: 120, bottom: 40, left: 260 }}
      rowHeight={52}
    />
  {/snippet}
</Story>
