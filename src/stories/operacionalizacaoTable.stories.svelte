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
    <div style="font-family: 'Space Grotesk', system-ui, sans-serif; font-size: 13px; max-width: 760px; padding: 16px;">
      <table style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr style="border-bottom: 2px solid #cbd5e1;">
            <th style="padding: 6px 12px 6px 0; text-align: left; font-size: 11px; color: #666; white-space: nowrap; font-weight: 600;">Categoria</th>
            <th style="padding: 6px 0 6px 16px; text-align: right; font-size: 11px; color: #666; white-space: nowrap; font-weight: 600;">Valor estimado</th>
            <th style="padding: 6px 0 6px 16px; text-align: right; font-size: 11px; color: #666; white-space: nowrap; font-weight: 600;">IC 95%</th>
            <th style="padding: 6px 0 6px 16px; text-align: right; font-size: 11px; color: #666; white-space: nowrap; font-weight: 600;">% do total</th>
          </tr>
        </thead>
        <tbody>
          {#each operacionalizacaoSubData as row, i}
            <tr style={i > 0 ? 'border-top: 1px solid #e2e8f0;' : ''}>
              <td style="padding: 7px 12px 7px 0;">{row.label}</td>
              <td style="padding: 7px 0 7px 16px; text-align: right; font-weight: 600; white-space: nowrap;">{formatBRL(row.valor)}</td>
              <td style="padding: 7px 0 7px 16px; text-align: right; white-space: nowrap; color: #666; font-size: 11px;">{formatBRL(row.p025)} – {formatBRL(row.p975)}</td>
              <td style="padding: 7px 0 7px 16px; text-align: right; font-weight: 600; white-space: nowrap; color: {colorScales.blue[2]};">{row.pct.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/snippet}
</Story>
