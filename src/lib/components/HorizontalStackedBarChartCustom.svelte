<script lang="ts">
	type DataRow = Record<string, string | number>;

	let {
		width = undefined,
		data = [] as DataRow[],
		keys = [] as string[],
		categoryKey = 'label',
		labels = {} as Record<string, string>,
		colors = [] as string[],
		format = (v: number) => v.toLocaleString(),
		rowHeight = 48,
		showTotalLabel = false,
		marginLeft = 180,
		legendAlign = 'left' as 'left' | 'center' | 'right',
		labelsAbove = false,
		yAxisFontSize = 12,
		hideSegmentLabelsFor = [] as string[],
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
		labelsAbove?: boolean;
		yAxisFontSize?: number;
		hideSegmentLabelsFor?: string[];
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
	const effectiveMarginLeft = $derived(labelsAbove ? ML_ABOVE : marginLeft);
	const innerWidth  = $derived(Math.max(0, containerWidth - effectiveMarginLeft - MR));

	// d3 scaleBand equivalent: padding(0.28) sets paddingInner = paddingOuter = 0.28
	const PAD = 0.15;
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

	const legendBoxWs = $derived(
		keys.map((key) => Math.max(60, (labels[key] ?? key).length * CHAR_W + BOX_PAD))
	);

	type LegendItem = { key: string; ki: number; w: number; x: number };
	const legendRows = $derived.by(() => {
		const result: LegendItem[][] = [];
		let cur: LegendItem[] = [];
		let rowW = 0;
		for (let ki = 0; ki < keys.length; ki++) {
			const w = legendBoxWs[ki];
			if (innerWidth > 0 && rowW + w > innerWidth && cur.length > 0) {
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

	const legendAvailW    = $derived(containerWidth - effectiveMarginLeft - MR);
	const legendY         = $derived(MT + innerHeight + XAXIS_H);
	const legendTotalH    = $derived(legendRows.length * LEGEND_ROW_H + Math.max(0, legendRows.length - 1) * LEGEND_GAP);
	const totalHeight     = $derived(MT + innerHeight + XAXIS_H + legendTotalH + 16);
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
			<g transform="translate({effectiveMarginLeft},{MT})">

				<!-- Vertical grid lines -->
				{#each ticks as tick}
					<line
						x1={tick.x} y1={0}
						x2={tick.x} y2={innerHeight}
						stroke="#e2e8f0"
						stroke-width="1"
						stroke-dasharray="3,3"
					/>
				{/each}

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

					<!-- Category label -->
					{#if labelsAbove}
						<text
							x={0}
							y={row.y - 6}
							font-size="12"
							font-weight="400"
							fill="#333333"
						>{row.label}</text>
					{:else}
						<text
							x={-8}
							y={row.midY}
							dy="0.35em"
							text-anchor="end"
							dominant-baseline="middle"
							font-size={yAxisFontSize}
							fill="#64748b"
						>{row.label}</text>
					{/if}

					{#if showTotalLabel}
						<text
							x={xScale(row.total) + 6}
							y={row.midY}
							dy="0.35em"
							dominant-baseline="middle"
							font-size="12"
							fill="#64748b"
						>{format(row.total)}</text>
					{/if}
				{/each}

				<!-- X-axis tick labels -->
				<g transform="translate(0,{innerHeight})">
					{#each ticks as tick, ti}
						<text
							x={tick.x}
							y={0}
							dy="1.2em"
							text-anchor={ti === 0 ? 'start' : ti === ticks.length - 1 ? 'end' : 'middle'}
							font-size="12"
							fill="#64748b"
						>{format(tick.v)}</text>
					{/each}
				</g>

			</g>

			<!-- Legend (multi-row, uses full container width) -->
			{#each legendRows as row, ri}
				{@const rowY = legendY + ri * (LEGEND_ROW_H + LEGEND_GAP)}
				{@const rowTotalW = row.reduce((s, item) => s + item.w, 0)}
				{@const legendOffsetX = legendAlign === 'right'
					? effectiveMarginLeft + innerWidth - rowTotalW
					: legendAlign === 'left'
					? effectiveMarginLeft
					: effectiveMarginLeft + Math.max(0, (innerWidth - rowTotalW) / 2)}
				<g transform="translate({legendOffsetX},{rowY})">
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
							x={item.x + 8}
							y={LEGEND_ROW_H / 2}
							dy="0.35em"
							font-size="12"
							font-weight="600"
							fill={labelColor(colors[item.ki] ?? '#999')}
						>{labels[item.key] ?? item.key}</text>
					{/each}
					{#each row.slice(0, row.length - 1) as item}
						<line
							x1={item.x + item.w} y1={0}
							x2={item.x + item.w} y2={LEGEND_ROW_H}
							stroke="#000000"
							stroke-width="0.5"
							shape-rendering="crispEdges"
						/>
					{/each}
					<rect
						fill="none"
						stroke="#000000"
						shape-rendering="crispEdges"
						x={0} y={0}
						width={rowTotalW}
						height={LEGEND_ROW_H}
						stroke-width="0.5"
					/>
				</g>
			{/each}
		</svg>
	{/if}
</div>
