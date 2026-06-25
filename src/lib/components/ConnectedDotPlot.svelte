<script lang="ts">
	export interface DotRow {
		label: string;
		values: number[]; // [series_a, series_b]
		isSeparator?: boolean;
	}

	const FONT = "'Rawline', system-ui, sans-serif";

	function labelColor(hex: string): string {
		const r = parseInt(hex.slice(1, 3), 16) / 255;
		const g = parseInt(hex.slice(3, 5), 16) / 255;
		const b = parseInt(hex.slice(5, 7), 16) / 255;
		const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
		return luminance > 0.55 ? '#1a1a1a' : '#fffffe';
	}

	let {
		width = undefined,
		data = [] as DotRow[],
		seriesLabels = [] as string[],
		colors = ['#e76f51', '#2a9d8f'] as string[],
		format = (v: number) => v.toFixed(1) + '%',
		margin = { top: 20, right: 56, bottom: 56, left: 44 },
		rowHeight = 28,
		separatorHeight = 28,
		dotRadius = 5,
	}: {
		width?: number;
		data?: DotRow[];
		seriesLabels?: string[];
		colors?: string[];
		format?: (v: number) => string;
		margin?: { top: number; right: number; bottom: number; left: number };
		rowHeight?: number;
		separatorHeight?: number;
		dotRadius?: number;
	} = $props();

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);

	const innerW = $derived(Math.max(0, containerWidth - margin.left - margin.right));

	const dataRows = $derived(data.filter((d) => !d.isSeparator));

	const xMax = $derived(
		Math.max(...dataRows.flatMap((d) => d.values), 1)
	);
	const xDomain = $derived(Math.ceil(xMax / 5) * 5);

	function scaleX(v: number): number {
		return (v / xDomain) * innerW;
	}

	// y position of center of each row
	const rowCenters = $derived(
		(() => {
			let y = 0;
			return data.map((row) => {
				const cy = y + (row.isSeparator ? separatorHeight : rowHeight) / 2;
				y += row.isSeparator ? separatorHeight : rowHeight;
				return cy;
			});
		})()
	);

	const totalInnerH = $derived(
		data.reduce((s, d) => s + (d.isSeparator ? separatorHeight : rowHeight), 0)
	);

	const LEGEND_GAP_TOP = 2;
	const svgH = $derived(margin.top + totalInnerH + margin.bottom + (seriesLabels.length >= 2 ? LEGEND_ROW_H + LEGEND_GAP_TOP + 2 : 0));

	// Ticks
	const N_TICKS = 5;
	const tickStep = $derived(xDomain / N_TICKS);
	const ticks = $derived(
		Array.from({ length: N_TICKS + 1 }, (_, i) => i * tickStep)
	);

	const LEGEND_ROW_H = 34;
	const LEGEND_CHAR_W = 7;
	const LEGEND_BOX_PAD = 16;

	const legendItemW = $derived(
		seriesLabels.map((label) => Math.max(60, label.length * LEGEND_CHAR_W + LEGEND_BOX_PAD))
	);

	// Minimum pixel gap between two dots before we hide labels to avoid overlap
	const MIN_LABEL_GAP = 30;
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg
			width={containerWidth}
			height={svgH}
			font-family={FONT}
			role="img"
			aria-label="Dot plot comparativo por UF"
		>
			<g transform="translate({margin.left},{margin.top})">

				<!-- Grid lines -->
				{#each ticks as tick}
					{@const tx = scaleX(tick)}
					<line
						x1={tx} y1={0}
						x2={tx} y2={totalInnerH}
						stroke={tick === 0 ? '#aaa' : '#e5e5e5'}
						stroke-width={tick === 0 ? 1 : 1}
					/>
				{/each}

				<!-- Rows -->
				{#each data as row, i}
					{@const cy = rowCenters[i]}

					{#if row.isSeparator}
						<text
							x={12}
							y={cy}
							dy="0.35em"
							font-size="12"
							font-weight="700"
							fill="#555"
							letter-spacing="0.04em"
						>{row.label}</text>
					{:else}
						{@const v0 = row.values[0] ?? 0}
						{@const v1 = row.values[1] ?? 0}
						{@const x0 = scaleX(v0)}
						{@const x1 = scaleX(v1)}
						{@const xLeft = Math.min(x0, x1)}
						{@const xRight = Math.max(x0, x1)}
						{@const gapPx = xRight - xLeft}

						<!-- UF label -->
						<text
							x={-6}
							y={cy}
							dy="0.35em"
							text-anchor="end"
							font-size="12"
							fill="#333"
						>{row.label}</text>

						<!-- Connecting line, colored by direction -->
						<line
							x1={xLeft} y1={cy}
							x2={xRight} y2={cy}
							stroke={v0 >= v1 ? colors[0] : colors[1]}
							stroke-width="1.5"
							opacity="0.45"
						/>

						<!-- Dot series 1 (values[1]) — draw first so series 0 is on top -->
						<circle cx={x1} cy={cy} r={dotRadius} fill={colors[1]} />

						<!-- Dot series 0 (values[0]) -->
						<circle cx={x0} cy={cy} r={dotRadius} fill={colors[0]} />

						<!-- Value labels: show outside the pair, hide if too close -->
						{#if gapPx >= MIN_LABEL_GAP}
							<!-- left dot label -->
							<text
								x={xLeft - dotRadius - 3}
								y={cy - 6}
								text-anchor="middle"
								font-size="12"
								font-weight="600"
								fill={x0 <= x1 ? colors[0] : colors[1]}
							>{format(x0 <= x1 ? v0 : v1)}</text>

							<!-- right dot label -->
							<text
								x={xRight + dotRadius + 3}
								y={cy - 6}
								text-anchor="middle"
								font-size="12"
								font-weight="600"
								fill={x0 > x1 ? colors[0] : colors[1]}
							>{format(x0 > x1 ? v0 : v1)}</text>
						{:else}
							<!-- dots too close: show combined label to the right with per-series colors -->
							<text x={xRight + dotRadius + 4} y={cy} dy="0.35em" font-size="12" font-weight="600">
								<tspan fill={colors[0]}>{format(v0)}</tspan>
								<tspan fill="#888"> / </tspan>
								<tspan fill={colors[1]}>{format(v1)}</tspan>
							</text>
						{/if}
					{/if}
				{/each}

				<!-- X axis -->
				<g transform="translate(0,{totalInnerH})">
					{#each ticks as tick}
						{@const tx = scaleX(tick)}
						<line x1={tx} y1={0} x2={tx} y2={5} stroke="#bbb" stroke-width="0.75" />
						<text
							x={tx}
							y={8}
							dy="0.71em"
							text-anchor="middle"
							font-size="12"
							fill="#888"
						>{format(tick)}</text>
					{/each}
				</g>
			</g>

			<!-- Legend: left-aligned, no gap between items, matches HorizontalStackedBarChartCustom pattern -->
			{#if seriesLabels.length >= 2}
				{@const rowTotalW = legendItemW.reduce((s, w) => s + w, 0)}
				{@const legendY = margin.top + totalInnerH + margin.bottom + LEGEND_GAP_TOP}
				{@const legendX = Math.max(2, (containerWidth - rowTotalW) / 2)}

				<g transform="translate({legendX},{legendY})">
					{#each seriesLabels as label, i}
						{@const bx = legendItemW.slice(0, i).reduce((s, w) => s + w, 0)}
						{@const w = legendItemW[i]}
						<rect x={bx} y={0} width={w} height={LEGEND_ROW_H} fill={colors[i]} shape-rendering="crispEdges" />
						<text x={bx + 8} y={LEGEND_ROW_H / 2} dy="0.35em" font-size="12" font-weight="600" fill={labelColor(colors[i])} font-family={FONT}>{label}</text>
					{/each}
					<!-- Separators between items -->
					{#each seriesLabels.slice(0, -1) as _, i}
						{@const sx = legendItemW.slice(0, i + 1).reduce((s, w) => s + w, 0)}
						<line x1={sx} y1={0} x2={sx} y2={LEGEND_ROW_H} stroke="#000" stroke-width="0.5" shape-rendering="crispEdges" />
					{/each}
					<!-- Outer border -->
					<rect x={0} y={0} width={rowTotalW} height={LEGEND_ROW_H} fill="none" stroke="#000" stroke-width="0.5" shape-rendering="crispEdges" />
				</g>
			{/if}
		</svg>
	{/if}
</div>
