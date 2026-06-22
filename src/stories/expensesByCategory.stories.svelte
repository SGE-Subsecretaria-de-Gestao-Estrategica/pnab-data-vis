<script module>
  // @ts-ignore
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { categorical8 } from 'sniic-design-system';
  // @ts-ignore
  import {
    expensesChartData,
    expensesKeys,
    expensesLegendItems,
    expensesGrandTotal,
  } from '$lib/data/section6';

  const CHART_W      = 900;
  const CHART_HEIGHT = 520;
  const MARGIN       = { top: 16, right: 16, bottom: 16, left: 16 };
  const COLUMN_GAP   = 2;
  const INNER_H      = CHART_HEIGHT - MARGIN.top - MARGIN.bottom; // 488
  const MIN_LABEL_H  = 28;

  const LEG_SEP      = 20;
  const LEG_HEADER_H = 24;
  const LEG_ROW_H    = 44;
  const legY         = CHART_HEIGHT + LEG_SEP;
  const TOTAL_H      = legY + LEG_HEADER_H + expensesLegendItems.length * LEG_ROW_H + 8;
  const LEG_VAL_X    = CHART_W - 150;
  const LEG_PCT_X    = CHART_W - 4;

  const FONT = "'Rawline', system-ui, sans-serif";

  const LARGE_LABEL_KEYS = new Set(['fomento', 'cultura_viva', 'obras', 'subsidio']);

  // @ts-ignore
  const formatBRL = (v) =>
    new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(v);

  // @ts-ignore
  function contrastColor(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.55 ? '#1a1a1a' : '#ffffff';
  }

  // Pre-compute all segment positions (fixed 900px width, no reactive state needed)
  const innerW     = CHART_W - MARGIN.left - MARGIN.right;
  const totalWidth = expensesChartData.reduce((s, /** @type {any} */ d) => s + d.total, 0);
  const availableW = innerW - Math.max(0, expensesChartData.length - 1) * COLUMN_GAP;

  /** @type {Array<{key:string;label:string;pct:string;x:number;y:number;w:number;h:number;color:string;showPct:boolean;showLabel:boolean}>} */
  const segments = [];
  let cumX = 0;
  for (const datum of expensesChartData) {
    const colW    = (datum.total / totalWidth) * availableW;
    const segTotal = expensesKeys.reduce((s, k) => s + (Number(/** @type {any} */ (datum)[k]) || 0), 0);
    let cumY = 0;
    for (let i = 0; i < expensesKeys.length; i++) {
      const key   = expensesKeys[i];
      const value = Number(/** @type {any} */ (datum)[key]) || 0;
      if (value === 0) continue;
      const h          = (value / segTotal) * INNER_H;
      const legendItem = expensesLegendItems.find((l) => l.key === key);
      const realValue  = legendItem?.valor ?? value;
      const pct        = (realValue / expensesGrandTotal * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
      segments.push({
        key,
        label:     legendItem?.label ?? key,
        pct,
        x:         MARGIN.left + cumX,
        y:         MARGIN.top + cumY,
        w:         colW,
        h,
        color:     categorical8[i],
        showPct:   h >= MIN_LABEL_H,
        showLabel: h >= 60 && colW >= 150,
      });
      cumY += h;
    }
    cumX += colW + COLUMN_GAP;
  }

  const { Story } = defineMeta({
    title: 'Section 6/Grafico 34',
    component: {},
    tags: ['autodocs'],
    parameters: {
      docs: {
        description: {
          component: `
**Distribuição dos recursos por tipo de despesa**

As três principais categorias — Fomento Cultural, Política Nacional de Cultura Viva e Subsídio e Manutenção de Espaços — concentram cerca de **88,4%** do total investido.

Os demais investimentos somam aproximadamente **R$ 154,6M**, distribuídos entre obras e reformas, operacionalização da política e outros gastos.
          `,
        },
      },
    },
  });
</script>

<Story name="Despesas por Categoria — Marimekko">
  {#snippet template()}
    <svg width={CHART_W} height={TOTAL_H} font-family={FONT} font-size="12" style="display:block">

      <!-- chart segment rects + labels -->
      {#each segments as seg}
        <rect x={seg.x} y={seg.y} width={seg.w} height={seg.h} fill={seg.color} shape-rendering="crispEdges" />
        {#if seg.showPct}
          <text
            x={seg.x + seg.w / 2}
            y={seg.y + seg.h / 2 + (seg.showLabel ? -8 : 0)}
            text-anchor="middle"
            dominant-baseline="middle"
            fill={contrastColor(seg.color)}
            font-size="14"
            font-weight="700"
            pointer-events="none"
          >{seg.pct}%</text>
        {/if}
        {#if seg.showLabel}
          <text
            x={seg.x + seg.w / 2}
            y={seg.y + seg.h / 2 + 10}
            text-anchor="middle"
            dominant-baseline="middle"
            fill={contrastColor(seg.color)}
            font-size={LARGE_LABEL_KEYS.has(seg.key) ? "13" : "10"}
            pointer-events="none"
          >{seg.label}</text>
        {/if}
      {/each}

      <!-- legend separator -->
      <line x1={0} y1={legY} x2={CHART_W} y2={legY} stroke="#e0e0e0" />

      <!-- legend column headers -->
      <text x={LEG_VAL_X} y={legY + LEG_HEADER_H - 8} text-anchor="end" fill="#666" font-size="10">Valor estimado (IC95%)</text>
      <text x={LEG_PCT_X} y={legY + LEG_HEADER_H - 8} text-anchor="end" fill="#666" font-size="10">% do total</text>

      <!-- legend rows -->
      {#each expensesLegendItems as item, i}
        {@const colorIdx = expensesKeys.indexOf(item.key)}
        {@const color    = categorical8[colorIdx]}
        {@const ry       = legY + LEG_HEADER_H + 16 + i * LEG_ROW_H}
        {@const itemPct  = (item.valor / expensesGrandTotal * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}
        {#if i > 0}
          <line x1={0} y1={ry - 6} x2={CHART_W} y2={ry - 6} stroke="#e0e0e0" />
        {/if}
        <rect x={MARGIN.left} y={ry + 1} width={10} height={10} rx="2" fill={color} />
        <text x={MARGIN.left + 18} y={ry + 6}  dy="0.35em" fill="#1a1a1a">{item.label}</text>
        <text x={LEG_VAL_X} y={ry}      dy="0.85em" text-anchor="end" fill="#111" font-weight="600">{item.value}</text>
        <text x={LEG_VAL_X} y={ry + 16} dy="0.85em" text-anchor="end" fill="#666" font-size="10">{item.ci}</text>
        <text x={LEG_PCT_X} y={ry + 6}  dy="0.35em" text-anchor="end" fill={color} font-size="13" font-weight="700">{itemPct}%</text>
      {/each}

    </svg>
  {/snippet}
</Story>
