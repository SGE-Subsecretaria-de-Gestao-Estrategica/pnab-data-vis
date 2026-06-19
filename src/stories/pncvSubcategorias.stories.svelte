<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  import HorizontalBarChartCustom from '$lib/components/HorizontalBarChartCustom.svelte';
  // @ts-ignore
  import { pncvSubData } from '$lib/data/section6';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(v);

  const chartData = pncvSubData.map((d) => ({ label: d.label, value: d.valor }));

  const { Story } = defineMeta({
    title: 'Section 6/pncvSubcategorias',
    component: HorizontalBarChartCustom,
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Subcategorias da Política Nacional de Cultura Viva (PNCV)**

Distribuição dos recursos dentro da categoria PNCV, mostrando valores absolutos estimados e participação percentual no total geral.
          `,
        },
      },
    },
  });
</script>

<Story name="Subcategorias de PNCV">
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
