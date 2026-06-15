<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  // @ts-ignore
  import { operacionalizacaoSubData } from '$lib/data/section6';
  import { colorScales } from 'sniic-design-system';

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(v);

  const W = 760;
  const ROW_H = 36;
  const HEADER_H = 32;
  const SVG_H = HEADER_H + operacionalizacaoSubData.length * ROW_H + 4;
  const FONT = "'Space Grotesk', system-ui, sans-serif";

  const { Story } = defineMeta({
    title: 'Section 6/operacionalizacaoTable',
    component: {},
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Categorias de Operacionalização da Política**

Valor estimado por categoria de despesa de Operacionalização da Política, com intervalo de confiança de 95% e participação percentual no total geral.
          `,
        },
      },
    },
  });
</script>

<Story name="Operacionalização da Política — Categorias">
  {#snippet template()}
    <svg width={W} height={SVG_H} font-family={FONT} font-size="12" style="display:block">
      <!-- header -->
      <text x={4} y={20} fill="#666" font-size="11" font-weight="600">Subcategoria</text>
      <text x={W - 260} y={20} text-anchor="end" fill="#666" font-size="11" font-weight="600">Valor estimado</text>
      <text x={W - 100} y={20} text-anchor="end" fill="#666" font-size="11" font-weight="600">IC 95%</text>
      <text x={W - 4} y={20} text-anchor="end" fill="#666" font-size="11" font-weight="600">% do total</text>
      <line x1={0} y1={HEADER_H - 2} x2={W} y2={HEADER_H - 2} stroke="#cbd5e1" stroke-width="2" />

      {#each operacionalizacaoSubData as row, i}
        {@const ry = HEADER_H + i * ROW_H + 22}
        {#if i > 0}
          <line x1={0} y1={ry - 16} x2={W} y2={ry - 16} stroke="#e2e8f0" />
        {/if}
        <text x={4} y={ry} fill="#1a1a1a" font-size="12">{row.label}</text>
        <text x={W - 260} y={ry} text-anchor="end" fill="#111" font-weight="600">{formatBRL(row.valor)}</text>
        <text x={W - 100} y={ry} text-anchor="end" fill="#666" font-size="11">{formatBRL(row.p025)} – {formatBRL(row.p975)}</text>
        <text x={W - 4} y={ry} text-anchor="end" fill={colorScales.teal[2]} font-weight="700">{row.pct.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%</text>
      {/each}
    </svg>
  {/snippet}
</Story>
