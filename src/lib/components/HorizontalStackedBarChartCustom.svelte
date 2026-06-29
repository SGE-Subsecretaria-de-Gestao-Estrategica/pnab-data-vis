<script lang="ts">
	import { base } from '$app/paths';
	import { CHART_ROW_HEIGHT, BAR_FILL, FLAG_RATIO, FLAG_GAP, FLAG_BORDER_COLOR, FLAG_BORDER_WIDTH, hasFlag, flagId, flagTitle, flagAwareLabel, truncateToWidth } from '$lib/chartStandards';
	import { createMediaQuery } from '$lib/utils/media.svelte';

	// No mobile a legenda é sempre centralizada, independente de `legendAlign`.
	const isMobile = createMediaQuery('(max-width: 768px)');

	type DataRow = Record<string, string | number>;

	let {
		width = undefined,
		data = [] as DataRow[],
		keys = [] as string[],
		categoryKey = 'label',
		labels = {} as Record<string, string>,
		colors = [] as string[],
		format = (v: number) => v.toLocaleString(),
		rowHeight = CHART_ROW_HEIGHT,
		showTotalLabel = false,
		marginLeft = 180,
		legendAlign = 'left' as 'left' | 'center' | 'right',
		legendInset = false,
		labelsAbove = false,
		yAxisFontSize = 12,
		hideSegmentLabelsFor = [] as string[],
		showFlags = false,
		flagSize = 22,
		flagBorder = true,
		flagBasePath = `${base}/flags/states`,
		axisColor = '#64748b',
		gridColor = '#e2e8f0',
	}: {
		width?: number;
		data?: DataRow[];
		keys?: string[];
		categoryKey?: string;
		labels?: Record<string, string>;
		colors?: string[];
		format?: (v: number) => string;
		rowHeight?: number;
		showTotalLabel?: boolean;
		marginLeft?: number;
		legendAlign?: 'left' | 'center' | 'right';
		/** Alinha a borda esquerda da legenda ao início das barras (área do gráfico),
		    em vez de à coluna de rótulos do eixo Y. Ignorado no mobile (centralizado). */
		legendInset?: boolean;
		labelsAbove?: boolean;
		yAxisFontSize?: number;
		hideSegmentLabelsFor?: string[];
		showFlags?: boolean;
		flagSize?: number;
		flagBorder?: boolean;
		flagBasePath?: string;
		/** Cor dos rótulos de eixo (categorias Y, ticks X e total). */
		axisColor?: string;
		/** Cor das linhas de grade/referência verticais (tracejadas). */
		gridColor?: string;
	} = $props();

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);

	const FONT_FAMILY = "'Rawline', system-ui, sans-serif";

	function labelColor(hex: string): string {
		const r = parseInt(hex.slice(1, 3), 16) / 255;
		const g = parseInt(hex.slice(3, 5), 16) / 255;
		const b = parseInt(hex.slice(5, 7), 16) / 255;
		const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
		return luminance > 0.65 ? '#1a1a1a' : '#fffffe';
	}

	// Fixed margins (bottom is computed dynamically based on legend height)
	const MT = 16, MR = 28, ML_ABOVE = 8;
	const LABEL_ABOVE_H = 20; // extra height per row when labelsAbove
	const XAXIS_H = 28; // space for x-axis tick labels below bars

	// ── Responsive left column ──────────────────────────────────────────────
	// Cap the label column to a fraction of the container so a fixed
	// `marginLeft` never starves the bars on mobile — charts always fill width.
	const MIN_LABEL = 40;
	const MAX_LEFT_FRAC = 0.34;
	const flagW = $derived(flagSize * FLAG_RATIO);
	const flagSpace = $derived(showFlags && !labelsAbove ? flagW + FLAG_GAP : 0);
	// Snug the column to the widest label (short for siglas, wider for names),
	// bounded by the requested margin and a fraction of the device width.
	const longestLabelPx = $derived(
		data.reduce((m, row) => Math.max(m, String(row[categoryKey] ?? '').length), 0) * yAxisFontSize * 0.6 + 12,
	);
	const labelColW = $derived(
		labelsAbove
			? ML_ABOVE
			: Math.min(marginLeft, longestLabelPx, Math.max(MIN_LABEL, containerWidth * MAX_LEFT_FRAC)),
	);
	const effectiveMarginLeft = $derived(labelColW + flagSpace);
	const labelAvail = $derived(labelColW - 8);
	const innerWidth  = $derived(Math.max(0, containerWidth - effectiveMarginLeft - MR));

	// paddingInner = 1 - BAR_FILL keeps bar thickness identical to the single-bar chart.
	const PAD = 1 - BAR_FILL;
	const effectiveRowHeight = $derived(labelsAbove ? rowHeight + LABEL_ABOVE_H : rowHeight);
	const n = $derived(data.length);
	const innerHeight = $derived(n * effectiveRowHeight);
	const step      = $derived(n > 0 ? innerHeight / (n - PAD + PAD * 2) : effectiveRowHeight);
	const bandwidth = $derived(labelsAbove ? (step * (1 - PAD)) - LABEL_ABOVE_H : step * (1 - PAD));
	const bandY     = (i: number) => i * step + PAD * step + (labelsAbove ? LABEL_ABOVE_H : 0);

	// X scale: linear 0..maxRowTotal → 0..innerWidth, 5 nice ticks
	const maxRowTotal = $derived(
		data.length > 0
			? Math.max(...data.map((row) => keys.reduce((s, k) => s + (Number(row[k]) || 0), 0)))
			: 1
	);
	const xScale = $derived((v: number) => (v / maxRowTotal) * innerWidth);
	const TICK_COUNT = 5;
	const ticks = $derived(
		Array.from({ length: TICK_COUNT + 1 }, (_, i) => {
			const v = (maxRowTotal / TICK_COUNT) * i;
			return { v, x: xScale(v) };
		})
	);

	// Stacked rows
	const rows = $derived(
		data.map((row, i) => {
			let cursor = 0;
			const segments = keys.map((key, ki) => {
				const value = Number(row[key]) || 0;
				const w = xScale(value);
				const seg = { key, value, x: cursor, w, color: colors[ki] ?? '#999' };
				cursor += w;
				return seg;
			});
			const total = keys.reduce((s, k) => s + (Number(row[k]) || 0), 0);
			const y   = bandY(i);
			const midY = y + bandwidth / 2;
			return { label: String(row[categoryKey]), y, midY, segments, total };
		})
	);

	// Legend: each box sized to fit its text (min 60px), wraps to multiple rows if needed
	const CHAR_W       = 8;
	const BOX_PAD      = 20;
	const LEGEND_ROW_H = 34;
	const LEGEND_GAP   = 2;

	// By default the legend spans the full component width (aligning with the
	// y-axis labels). With `legendInset` its left edge starts at the bars instead,
	// so the legend lines up with the chart area. Always full-width on mobile.
	const legendX0 = $derived(legendInset && !isMobile.matches ? effectiveMarginLeft : 0);
	const legendW = $derived(Math.max(0, containerWidth - MR - legendX0));

	// Box fits its label, but never wider than the available legend area, so a
	// long label (ex.: "Região metropolitana") can't overflow on narrow screens.
	const legendBoxWs = $derived(
		keys.map((key) => {
			const natural = Math.max(60, (labels[key] ?? key).length * CHAR_W + BOX_PAD);
			return legendW > 0 ? Math.min(natural, legendW) : natural;
		})
	);

	type LegendItem = { key: string; ki: number; w: number; x: number };
	const legendRows = $derived.by(() => {
		const result: LegendItem[][] = [];
		let cur: LegendItem[] = [];
		let rowW = 0;
		for (let ki = 0; ki < keys.length; ki++) {
			const w = legendBoxWs[ki];
			if (legendW > 0 && rowW + w > legendW && cur.length > 0) {
				result.push(cur);
				cur = [];
				rowW = 0;
			}
			cur.push({ key: keys[ki], ki, w, x: rowW });
			rowW += w;
		}
		if (cur.length > 0) result.push(cur);
		return result;
	});

	const LEGEND_CHART_GAP = 12; // espaço entre a legenda (topo) e o início do gráfico
	const legendTotalH    = $derived(legendRows.length * LEGEND_ROW_H + Math.max(0, legendRows.length - 1) * LEGEND_GAP);
	// Legenda no topo; o gráfico começa abaixo dela.
	const legendY         = $derived(MT);
	const chartTop        = $derived(MT + legendTotalH + LEGEND_CHART_GAP);
	const totalHeight     = $derived(chartTop + innerHeight + XAXIS_H + 8);
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg
			width={containerWidth}
			height={totalHeight}
			role="img"
			aria-label="Chart"
			font-family={FONT_FAMILY}
			style="overflow: visible;"
		>
			<g transform="translate({effectiveMarginLeft},{chartTop})">

				<!-- Vertical grid lines -->
				{#if !isMobile.matches}
					{#each ticks as tick}
						<line
							x1={tick.x} y1={0}
							x2={tick.x} y2={innerHeight}
							stroke={gridColor}
							stroke-width="1"
							stroke-dasharray="3,3"
						/>
					{/each}
				{/if}

				<!-- Bars + labels (all rects first, then all labels on top so
				     a label overflowing into the next segment isn't painted over) -->
				{#each rows as row}
					{#each row.segments as seg}
						{#if seg.w > 0}
							<rect
								x={seg.x}
								y={row.y}
								width={seg.w}
								height={bandwidth}
								fill={seg.color}
								shape-rendering="crispEdges"
							/>
						{/if}
					{/each}
					{#each row.segments as seg}
						{#if seg.w > 28 && !hideSegmentLabelsFor.includes(row.label)}
							<text
								x={seg.x + 6}
								y={row.midY}
								dy="0.35em"
								font-size="12"
								font-weight="700"
								fill={labelColor(seg.color)}
								text-anchor="start"
								pointer-events="none"
							>{format(seg.value)}</text>
						{/if}
					{/each}

					<!-- Category label (+ state flag) -->
					{#if labelsAbove}
						<text
							x={0}
							y={row.y - 6}
							font-size="12"
							font-weight="400"
							fill="#333333"
						>{row.label}</text>
					{:else}
						{#if showFlags && hasFlag(row.label)}
							<image
								href="{flagBasePath}/{flagId(row.label)}.svg"
								x={-effectiveMarginLeft + 2}
								y={row.midY - flagSize / 2}
								width={flagW}
								height={flagSize}
								preserveAspectRatio="xMidYMid meet"
							>
								<title>{flagTitle(row.label)}</title>
							</image>
							{#if flagBorder}
								<rect
									x={-effectiveMarginLeft + 2}
									y={row.midY - flagSize / 2}
									width={flagW}
									height={flagSize}
									fill="none"
									stroke={FLAG_BORDER_COLOR}
									stroke-width={FLAG_BORDER_WIDTH}
								/>
							{/if}
						{/if}
						<text
							x={-8}
							y={row.midY}
							dy="0.35em"
							text-anchor="end"
							dominant-baseline="middle"
							font-size={yAxisFontSize}
							fill={axisColor}
						>{truncateToWidth(flagAwareLabel(row.label, showFlags), labelAvail, yAxisFontSize)}</text>
					{/if}

					{#if showTotalLabel}
						<text
							x={xScale(row.total) + 6}
							y={row.midY}
							dy="0.35em"
							dominant-baseline="middle"
							font-size="12"
							fill={axisColor}
						>{format(row.total)}</text>
					{/if}
				{/each}

				<!-- X-axis tick labels -->
				<g class="x-axis" transform="translate(0,{innerHeight})">
					{#each ticks as tick, ti}
						<text
							x={tick.x}
							y={0}
							dy="1.2em"
							text-anchor={ti === 0 ? 'start' : ti === ticks.length - 1 ? 'end' : 'middle'}
							font-size="12"
							fill={axisColor}
						>{format(tick.v)}</text>
					{/each}
				</g>

			</g>

			<!-- Legend (multi-row, uses full container width) -->
			{#each legendRows as row, ri}
				{@const rowY = legendY + ri * (LEGEND_ROW_H + LEGEND_GAP)}
				{@const rowTotalW = row.reduce((s, item) => s + item.w, 0)}
				{@const legendOffsetX = isMobile.matches
					? Math.max(0, (legendW - rowTotalW) / 2)
					: legendAlign === 'right'
					? Math.max(0, legendW - rowTotalW)
					: legendAlign === 'left'
					? 0
					: Math.max(0, (legendW - rowTotalW) / 2)}
				<g transform="translate({legendX0 + legendOffsetX},{rowY})">
					{#each row as item}
						<rect
							x={item.x}
							y={0}
							width={item.w}
							height={LEGEND_ROW_H}
							fill={colors[item.ki] ?? '#999'}
							shape-rendering="crispEdges"
						/>
						<text
							x={isMobile.matches ? item.x + item.w / 2 : item.x + 8}
							y={LEGEND_ROW_H / 2}
							dy="0.35em"
							text-anchor={isMobile.matches ? 'middle' : 'start'}
							font-size="12"
							font-weight="600"
							fill={labelColor(colors[item.ki] ?? '#999')}
						>{truncateToWidth(labels[item.key] ?? item.key, item.w - 16, 12)}</text>
					{/each}
				</g>
			{/each}
		</svg>
	{/if}
</div>

<style>
	/* No mobile, os rótulos do eixo X se sobrepõem e ficam ilegíveis — ocultamos. */
	@media (max-width: 720px) {
		.x-axis {
			display: none;
		}
	}
</style>
