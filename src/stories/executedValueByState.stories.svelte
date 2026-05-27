<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import ChoroplethMapLabeled from '$lib/components/ExecutedValueByStateMap.svelte';
  import { states } from '$lib/data/section1';
  import { SvgExportDecorator } from 'sniic-design-system';

  // @ts-ignore
  const formatPerc = (v) =>
    v.toLocaleString('pt-BR', { style: 'percent', minimumFractionDigits: 1, maximumFractionDigits: 1 });

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);

  // @ts-ignore
  const formatLine2 = (row) => formatPerc(row.valor_executado_perc);

  const { Story } = defineMeta({
    title: 'Section 1/executedValueByState',
    component: ChoroplethMapLabeled,
    tags: ['autodocs'],
  decorators: [() => ({ Component: SvgExportDecorator })],
    parameters: {
      docs: {
        description: {
          component: `
**Estado a estado: a concentração fica evidente**

Dentro das regiões, a desigualdade se aprofunda. **São Paulo sozinho absorveu quase 20%** de todo o orçamento executado pelo PNAB. Minas Gerais ficou em segundo com 7,6%. Rio de Janeiro, Ceará e Bahia completam o topo.

No mapa, a intensidade da cor mapeia diretamente o valor executado — e o contraste entre o estado mais escuro e os mais claros ilustra o abismo entre os extremos: SP recebeu **622 vezes mais** do que Rondônia (R$ 290 milhões contra R$ 467 mil).

A pergunta que esse mapa levanta: essa concentração é justa, ou apenas reflete o tamanho populacional de cada estado?
          `,
        },
      },
    },
  });
</script>

<Story name="Valor Executado por Estado">
  {#snippet template()}
    <ChoroplethMapLabeled
      {states}
      metric="valor_executado_rs"
      label="Valor executado"
      format={formatBRL}
    />
  {/snippet}
</Story>
