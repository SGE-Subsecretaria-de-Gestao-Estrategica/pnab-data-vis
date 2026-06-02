<script lang="ts">
	export interface GroupedBarRow {
		label: string;
		values: number[]; // one value per series, same order as seriesLabels
		colors?: string[]; // per-row color override (same order as values)
		isSeparator?: boolean; // renders as a region header with no bars
	}

	let {
		data = [] as GroupedBarRow[],
		seriesLabels = [] as string[],
		colors = ['#2a9d8f', '#e9c46a'] as string[],
		legendItems = undefined as { label: string; color: string; secondLabel?: string; secondColor?: string; groupLabel?: string }[] | undefined,
		format = (v: number) => v.toFixed(1) + '%',
		xLabel = '',
		margin = { top: 20, right: 90, bottom: 40, left: 50 },
		barHeight = 10,
		barPad = 4,
		legendBottom = false,
	}: {
		data: GroupedBarRow[];
		seriesLabels: string[];
		colors?: string[];
		legendItems?: { label: string; color: string; secondLabel?: string; secondColor?: string; groupLabel?: string }[];
		format?: (v: number) => string;
		xLabel?: string;
		margin?: { top: number; right: number; bottom: number; left: number };
		barHeight?: number;
		barPad?: number;
		legendBottom?: boolean;
	} = $props();

	let containerWidth = $state(0);

	const FONT_FAMILY = "'Space Grotesk', system-ui, sans-serif";

	// Derive nSeries from data when seriesLabels is not provided
	const nSeries = $derived(
		seriesLabels.length > 0
			? seriesLabels.length
			: Math.max(0, ...data.filter((d) => !d.isSeparator).map((d) => d.values.length))
	);
	const groupHeight = $derived(nSeries * barHeight + Math.max(0, nSeries - 1) * barPad);
	const groupPad = 6;
	const separatorH = 16;

	// Compute row Y positions accounting for separator rows
	const rowPositions = $derived(
		(() => {
			let y = margin.top;
			return data.map((row) => {
				const pos = y;
				y += row.isSeparator ? separatorH : groupHeight + groupPad;
				return pos;
			});
		})()
	);

	const totalContentH = $derived(
		data.reduce((sum, row) => sum + (row.isSeparator ? separatorH : groupHeight + groupPad), 0)
	);

	const hasGroupLabels = $derived(legendItems?.some((i) => i.groupLabel) ?? false);
	const legendH = $derived(34 + 8 + (hasGroupLabels ? 16 : 0)); // blocks + optional group label row

	const svgHeight = $derived(
		margin.top + totalContentH + margin.bottom + (legendBottom ? legendH : 0)
	);

	const innerW = $derived(Math.max(0, containerWidth - margin.left - margin.right));

	const xMax = $derived(
		Math.max(...data.filter((d) => !d.isSeparator).flatMap((d) => d.values), 1)
	);

	// nice-ish domain: round up to next multiple of 10
	const xDomain = $derived(Math.ceil(xMax / 10) * 10);

	function scaleX(v: number): number {
		return (v / xDomain) * innerW;
	}

	const tickCount = 5;
	const tickStep = $derived(xDomain / tickCount);
	const xTicks = $derived(
		Array.from({ length: tickCount + 1 }, (_, i) => Math.round(i * tickStep * 10) / 10)
	);

	const legendStartY = $derived(margin.top + totalContentH + (xLabel ? 40 : 28));
</script>

<div bind:clientWidth={containerWidth} style="width:100%;">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={svgHeight} role="img" font-family={FONT_FAMILY}>
			<!-- grid lines -->
			{#each xTicks as tick}
				{@const x = margin.left + scaleX(tick)}
				<line
					x1={x}
					y1={margin.top - 6}
					x2={x}
					y2={margin.top + totalContentH}
					stroke="#e5e5e5"
					stroke-width="1"
				/>
				<text x={x} y={margin.top + totalContentH + 14} text-anchor="middle" font-size="11" fill="#666"
					>{format(tick)}</text
				>
			{/each}

			<!-- x axis label -->
			{#if xLabel}
				<text
					x={margin.left + innerW / 2}
					y={margin.top + totalContentH + 28}
					text-anchor="middle"
					font-size="11"
					fill="#888">{xLabel}</text
				>
			{/if}

			<!-- groups -->
			{#each data as row, i}
				{@const gy = rowPositions[i]}

				{#if row.isSeparator}
					<!-- Region header -->
					<text
						x={margin.left}
						y={gy + separatorH / 2}
						dominant-baseline="middle"
						font-size="11"
						font-weight="700"
						fill="#444">{row.label}</text
					>
				{:else}
					<!-- row label -->
					<text
						x={margin.left - 6}
						y={gy + groupHeight / 2}
						text-anchor="end"
						dominant-baseline="middle"
						font-size="11"
						fill="#333">{row.label}</text
					>

					{#each row.values as val, si}
						{@const barW = scaleX(val)}
						{@const by = gy + si * (barHeight + barPad)}
						{@const barColor = row.colors?.[si] ?? colors[si % colors.length]}
						<rect
							x={margin.left}
							y={by}
							width={barW}
							height={barHeight}
							fill={barColor}
							rx="2"
						/>
						<!-- value label -->
						<text
							x={margin.left + barW + 4}
							y={by + barHeight / 2}
							dominant-baseline="middle"
							font-size="10"
							fill="#444">{format(val)}</text
						>
					{/each}
				{/if}
			{/each}

			<!-- legend -->
			{#if legendBottom}
				{@const items = legendItems ?? seriesLabels.map((l, i) => ({ label: l, color: colors[i % colors.length] }))}
				{@const blockW = innerW / items.length}
				{@const blockOffsetY = hasGroupLabels ? 16 : 0}
				<g transform="translate({margin.left},{legendStartY})">
					{#each items as item, li}
						<!-- Group label above block -->
						{#if item.groupLabel}
							<text
								x={li * blockW + blockW / 2}
								y={0}
								dy="0.8em"
								text-anchor="middle"
								font-size="11"
								font-weight="600"
								fill="var(--chart-fg, #64748b)"
							>{item.groupLabel}</text>
						{/if}
						{#if item.secondLabel && item.secondColor}
							<!-- Split block -->
							<rect x={li * blockW} y={blockOffsetY} width={blockW / 2} height={34} fill={item.color} shape-rendering="crispEdges" />
							<rect x={li * blockW + blockW / 2} y={blockOffsetY} width={blockW / 2} height={34} fill={item.secondColor} shape-rendering="crispEdges" />
							<text x={li * blockW + blockW / 4} y={blockOffsetY + 17} dy="0.35em" text-anchor="middle" font-size="11" font-weight="600" fill="#fffffe">{item.label}</text>
							<text x={li * blockW + blockW * 3 / 4} y={blockOffsetY + 17} dy="0.35em" text-anchor="middle" font-size="11" font-weight="600" fill="#fffffe">{item.secondLabel}</text>
							<line x1={li * blockW + blockW / 2} y1={blockOffsetY} x2={li * blockW + blockW / 2} y2={blockOffsetY + 34} stroke="rgba(255,255,255,0.4)" stroke-width="1" shape-rendering="crispEdges" />
						{:else}
							<!-- Single-color block -->
							<rect x={li * blockW} y={blockOffsetY} width={blockW} height={34} fill={item.color} shape-rendering="crispEdges" />
							<text x={li * blockW + 10} y={blockOffsetY + 17} dy="0.35em" font-size="12" font-weight="600" fill="#fffffe">{item.label}</text>
						{/if}
					{/each}
					{#each items.slice(0, items.length - 1) as _, li}
						<line
							x1={(li + 1) * blockW} y1={blockOffsetY}
							x2={(li + 1) * blockW} y2={blockOffsetY + 34}
							stroke="var(--chart-fg-strong, #000000)"
							stroke-width="0.5"
							shape-rendering="crispEdges"
						/>
					{/each}
					<rect
						fill="none"
						stroke="var(--chart-fg-strong, #000000)"
						stroke-width="0.5"
						shape-rendering="crispEdges"
						x={0} y={blockOffsetY}
						width={blockW * items.length} height={34}
					/>
				</g>
			{:else}
				{#each seriesLabels as label, si}
					{@const lx = margin.left + si * 200}
					<rect x={lx} y={6} width={12} height={10} fill={colors[si % colors.length]} rx="2" />
					<text x={lx + 16} y={13} font-size="11" fill="#444">{label}</text>
				{/each}
			{/if}
		</svg>
	{/if}
</div>
