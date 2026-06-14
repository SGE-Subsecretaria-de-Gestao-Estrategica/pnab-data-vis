<script lang="ts">
	type DataRow = Record<string, string | number>;

	let {
		data = [] as DataRow[],
		keys = [] as string[],
		categoryKey = 'label',
		labels = {} as Record<string, string>,
		colors = [] as string[],
		format = (v: number) => v.toLocaleString(),
		rowHeight = 52,
		showTotalLabel = false,
		marginLeft = 180,
		legendAlign = 'center' as 'left' | 'center' | 'right',
	}: {
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
	} = $props();

	let containerWidth = $state(0);

	const FONT_FAMILY = "'Space Grotesk', system-ui, sans-serif";

	function labelColor(hex: string): string {
		const r = parseInt(hex.slice(1, 3), 16) / 255;
		const g = parseInt(hex.slice(3, 5), 16) / 255;
		const b = parseInt(hex.slice(5, 7), 16) / 255;
		const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
		return luminance > 0.65 ? '#1a1a1a' : '#fffffe';
	}

	// Fixed margins (bottom is computed dynamically based on legend height)
	const MT = 16, MR = 28;
	const innerWidth  = $derived(Math.max(0, containerWidth - marginLeft - MR));

	// d3 scaleBand equivalent: padding(0.28) sets paddingInner = paddingOuter = 0.28
	const PAD = 0.28;
	const n = $derived(data.length);
	const innerHeight = $derived(n * rowHeight);
	const step      = $derived(n > 0 ? innerHeight / (n - PAD + PAD * 2) : rowHeight);
	const bandwidth = $derived(step * (1 - PAD));
	const bandY     = (i: number) => i * step + PAD * step;

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
	const CHAR_W       = 6;
	const BOX_PAD      = 16;
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

	const legendAvailW    = $derived(containerWidth - MR);
	const legendY         = $derived(MT + innerHeight + 22);
	const legendTotalH    = $derived(legendRows.length * LEGEND_ROW_H + Math.max(0, legendRows.length - 1) * LEGEND_GAP);
	const totalHeight     = $derived(MT + innerHeight + 22 + legendTotalH + 16);
</script>

<div bind:clientWidth={containerWidth} style="width: 100%;">
	{#if containerWidth > 0}
		<svg
			width={containerWidth}
			height={totalHeight}
			role="img"
			aria-label="Chart"
			font-family={FONT_FAMILY}
			style="overflow: visible;"
		>
			<g transform="translate({marginLeft},{MT})">

				<!-- Vertical grid lines -->
				{#each ticks as tick}
					<line
						x1={tick.x} y1={0}
						x2={tick.x} y2={innerHeight}
						stroke="var(--chart-grid, #e2e8f0)"
						stroke-width="1"
						stroke-dasharray="3,3"
					/>
				{/each}

				<!-- Bars + labels -->
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
							{#if seg.w > 28}
								<text
									x={seg.x + 6}
									y={row.midY}
									dy="0.35em"
									font-size="12.48"
									font-weight="700"
									fill={labelColor(seg.color)}
									text-anchor="start"
									pointer-events="none"
								>{format(seg.value)}</text>
							{/if}
						{/if}
					{/each}

					<!-- Category label (left axis) -->
					<text
						x={-8}
						y={row.midY}
						dy="0.35em"
						text-anchor="end"
						dominant-baseline="middle"
						font-size="11"
						fill="var(--chart-fg, #64748b)"
					>{row.label}</text>

					{#if showTotalLabel}
						<text
							x={xScale(row.total) + 6}
							y={row.midY}
							dy="0.35em"
							dominant-baseline="middle"
							font-size="11"
							fill="var(--chart-fg, #64748b)"
						>{format(row.total)}</text>
					{/if}
				{/each}

				<!-- X-axis tick labels -->
				<g transform="translate(0,{innerHeight})">
					{#each ticks as tick}
						<text
							x={tick.x}
							y={0}
							dy="1.2em"
							text-anchor="middle"
							font-size="10"
							fill="var(--chart-fg, #64748b)"
						>{format(tick.v)}</text>
					{/each}
				</g>

			</g>

			<!-- Legend (multi-row, uses full container width) -->
			{#each legendRows as row, ri}
				{@const rowY = legendY + ri * (LEGEND_ROW_H + LEGEND_GAP)}
				{@const rowTotalW = row.reduce((s, item) => s + item.w, 0)}
				{@const legendOffsetX = legendAlign === 'right'
					? marginLeft + innerWidth - rowTotalW
					: legendAlign === 'left'
					? marginLeft
					: marginLeft + Math.max(0, (innerWidth - rowTotalW) / 2)}
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
							font-size="10"
							font-weight="600"
							fill={labelColor(colors[item.ki] ?? '#999')}
						>{labels[item.key] ?? item.key}</text>
					{/each}
					{#each row.slice(0, row.length - 1) as item}
						<line
							x1={item.x + item.w} y1={0}
							x2={item.x + item.w} y2={LEGEND_ROW_H}
							stroke="var(--chart-fg-strong, #000000)"
							stroke-width="0.5"
							shape-rendering="crispEdges"
						/>
					{/each}
					<rect
						fill="none"
						stroke="var(--chart-fg-strong, #000000)"
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
