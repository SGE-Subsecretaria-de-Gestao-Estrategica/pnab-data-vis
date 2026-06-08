<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { colorScales } from 'sniic-design-system';
  // @ts-ignore
  import { fomentoSubData } from '$lib/data/section6';

  const W = 760;
  const M = { top: 24, right: 16, bottom: 48, left: 260 };
  const ROW_H = 32;
  const ROW_GAP = 20;
  const LEG_SEP = 28;
  const LEG_ROW_H = 44;
  const SWATCH = 10;
  const COLOR = colorScales.blue[2];
  const FONT = "'Space Grotesk', system-ui, sans-serif";

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(v);

  // @ts-ignore
  function niceMax(v) {
    const mag = Math.pow(10, Math.floor(Math.log10(v)));
    return Math.ceil(v / mag) * mag;
  }

  const maxVal = Math.max(...fomentoSubData.map((d) => d.valor));
  const nMax = niceMax(maxVal);
  const innerW = W - M.left - M.right;
  const n = fomentoSubData.length;
  const barsH = n * ROW_H + (n - 1) * ROW_GAP;
  const chartH = M.top + barsH + M.bottom;
  const legendH = LEG_SEP + n * LEG_ROW_H + 8;
  const totalH = chartH + legendH;
  const axisY = M.top + barsH;

  const TICKS = [0, 0.25, 0.5, 0.75, 1].map((t) => t * nMax);
  // @ts-ignore
  const scaleX = (v) => (v / nMax) * innerW;
  // @ts-ignore
  const barY = (i) => M.top + i * (ROW_H + ROW_GAP);

  // Legend column anchors
  const LEG_VAL_X = W - 140;  // value text right-aligned here
  const LEG_PCT_X = W - 4;    // pct text right-aligned here

  // Align legend left edge with the visual start of the longest y-axis label.
  // Labels are right-anchored at M.left-12; Space Grotesk 12px ≈ 6.8px/char.
  const AVG_CHAR_W = 6.8;
  const maxLabelChars = Math.max(...fomentoSubData.map((d) => d.label.length));
  const LEG_LEFT = Math.max(0, M.left - 12 - maxLabelChars * AVG_CHAR_W);

  const { Story } = defineMeta({
    title: 'Section 6/fomentoSubcategorias',
    component: {},
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
    <svg width={W} height={totalH} font-family={FONT} font-size="12">

      <!-- grid lines -->
      {#each TICKS as tick}
        {@const tx = M.left + scaleX(tick)}
        <line x1={tx} y1={M.top} x2={tx} y2={axisY}
          stroke="var(--chart-grid, #e2e8f0)" stroke-dasharray="4 3" />
      {/each}

      <!-- bars -->
      {#each fomentoSubData as item, i}
        {@const bw = scaleX(item.valor)}
        {@const by = barY(i)}
        {@const cy = by + ROW_H / 2}

        <!-- category label (left) -->
        <text x={M.left - 12} y={cy} dy="0.35em"
          text-anchor="end" fill="var(--chart-fg, #1a1a1a)" font-size="12">
          {item.label}
        </text>

        <!-- bar -->
        <rect x={M.left} y={by} width={bw} height={ROW_H}
          fill={COLOR} shape-rendering="crispEdges" />

        <!-- value label (right of bar) -->
        <text x={M.left + bw + 8} y={cy} dy="0.35em"
          text-anchor="start" fill="var(--chart-fg-strong, #111)" font-size="12" font-weight="600">
          {item.valorFormatted}
        </text>
      {/each}

      <!-- x axis line -->
      <line x1={M.left} y1={axisY} x2={M.left + innerW} y2={axisY}
        stroke="var(--chart-fg-muted, #94a3b8)" />

      <!-- x axis ticks + labels -->
      {#each TICKS as tick}
        {@const tx = M.left + scaleX(tick)}
        <line x1={tx} y1={axisY} x2={tx} y2={axisY + 5}
          stroke="var(--chart-fg-muted, #94a3b8)" />
        <text x={tx} y={axisY + 18} text-anchor="middle"
          fill="var(--chart-fg-muted, #666)" font-size="11">
          {formatBRL(tick)}
        </text>
      {/each}

      <!-- x axis label -->
      <text x={M.left + innerW / 2} y={axisY + 38}
        text-anchor="middle" fill="var(--chart-fg-muted, #666)" font-size="11">
        Valor estimado (R$)
      </text>

      <!-- legend separator -->
      <line x1={LEG_LEFT} y1={chartH + 12} x2={W} y2={chartH + 12}
        stroke="var(--chart-fg-muted, #e0e0e0)" />

      <!-- legend column headers -->
      <text x={LEG_VAL_X} y={chartH + 24}
        text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">
        Valor estimado (IC95%)
      </text>
      <text x={LEG_PCT_X} y={chartH + 24}
        text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">
        % do total
      </text>

      <!-- legend rows -->
      {#each fomentoSubData as item, i}
        {@const ry = chartH + LEG_SEP + 16 + i * LEG_ROW_H}

        <!-- row separator -->
        {#if i > 0}
          <line x1={LEG_LEFT} y1={ry - 6} x2={W} y2={ry - 6}
            stroke="var(--chart-fg-muted, #e0e0e0)" />
        {/if}

        <!-- swatch -->
        <rect x={LEG_LEFT} y={ry + 1} width={SWATCH} height={SWATCH} rx="2"
          fill={COLOR} />

        <!-- label -->
        <text x={LEG_LEFT + SWATCH + 8} y={ry + SWATCH / 2} dy="0.35em"
          fill="var(--chart-fg, #1a1a1a)" font-size="12">
          {item.label}
        </text>

        <!-- absolute value -->
        <text x={LEG_VAL_X} y={ry} dy="0.85em"
          text-anchor="end" fill="var(--chart-fg-strong, #111)" font-size="12" font-weight="600">
          {item.valorFormatted}
        </text>
        <!-- CI -->
        <text x={LEG_VAL_X} y={ry + 16} dy="0.85em"
          text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">
          IC95%: {formatBRL(item.p025)} – {formatBRL(item.p975)}
        </text>

        <!-- pct -->
        <text x={LEG_PCT_X} y={ry + SWATCH / 2} dy="0.35em"
          text-anchor="end" fill={COLOR} font-size="13" font-weight="700">
          {item.pct.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%
        </text>
      {/each}

    </svg>
  {/snippet}
</Story>
