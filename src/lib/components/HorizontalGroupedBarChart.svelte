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
		groupPad: groupPadProp = 6,
		legendBottom = false,
		rx = 2,
		labelsInside = false,
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
		groupPad?: number;
		legendBottom?: boolean;
		rx?: number;
		labelsInside?: boolean;
	} = $props();

	function labelColor(hex: string): string {
		const r = parseInt(hex.slice(1, 3), 16) / 255;
		const g = parseInt(hex.slice(3, 5), 16) / 255;
		const b = parseInt(hex.slice(5, 7), 16) / 255;
		const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
		return luminance > 0.35 ? '#1a1a1a' : '#fffffe';
	}

	let containerWidth = $state(0);

	const FONT_FAMILY = "'Space Grotesk', system-ui, sans-serif";

	// Derive nSeries from data when seriesLabels is not provided
	const nSeries = $derived(
		seriesLabels.length > 0
			? seriesLabels.length
			: Math.max(0, ...data.filter((d) => !d.isSeparator).map((d) => d.values.length))
	);
	const groupHeight = $derived(nSeries * barHeight + Math.max(0, nSeries - 1) * barPad);
	const groupPad = groupPadProp;
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

	// Legend block layout: pack items into rows using full containerWidth so cells always fit their text
	const LEGEND_CHAR_W = 7.5;
	const LEGEND_PAD_X = 16;
	const LEGEND_BLOCK_H = 34;
	const LEGEND_ROW_GAP = 2;

	const legendAllItems = $derived(
		legendItems ?? seriesLabels.map((l, i) => ({ label: l, color: colors[i % colors.length] }))
	);

	// DOM-measured text widths; fall back to char estimate before first measurement
	let legendTextEls = $state<(SVGTextElement | null)[]>([]);
	let legendText2Els = $state<(SVGTextElement | null)[]>([]);
	let measuredLegendW = $state<number[]>([]);

	$effect(() => {
		if (!legendBottom || legendTextEls.length === 0) return;
		const ws = legendAllItems.map((item, i) => {
			const el = legendTextEls[i];
			if (!el) return 0;
			const w1 = Math.ceil(el.getComputedTextLength());
			if (item.secondLabel) {
				const el2 = legendText2Els[i];
				const w2 = el2 ? Math.ceil(el2.getComputedTextLength()) : 0;
				return Math.max(w1, w2) * 2 + LEGEND_PAD_X * 2;
			}
			return w1 + LEGEND_PAD_X * 2;
		});
		if (ws.some((w) => w > 0)) measuredLegendW = ws;
	});

	const legendNaturalW = $derived(
		legendAllItems.map((item, i) => {
			const m = measuredLegendW[i];
			if (m && m > 0) return m;
			return Math.max(item.label.length, item.secondLabel?.length ?? 0) * LEGEND_CHAR_W + LEGEND_PAD_X * 2;
		})
	);
	// Greedy row packing against innerW
	const legendRows = $derived((() => {
		if (!legendBottom || innerW === 0) return [] as number[][];
		const rows: number[][] = [[]];
		let rowW = 0;
		legendNaturalW.forEach((w, i) => {
			if (rows[rows.length - 1].length > 0 && rowW + w > innerW) {
				rows.push([]);
				rowW = 0;
			}
			rows[rows.length - 1].push(i);
			rowW += w;
		});
		return rows;
	})());

	const legendH = $derived(
		legendBottom
			? legendRows.length * LEGEND_BLOCK_H + Math.max(0, legendRows.length - 1) * LEGEND_ROW_GAP + 8
			: 34 + 8 + (hasGroupLabels ? 16 : 0)
	);

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

	// Accumulated x offsets for top legend items based on actual label widths
	const legendTopOffsets = $derived(
		seriesLabels.reduce<number[]>((acc, label, i) => {
			const prev = i === 0 ? 0 : acc[i - 1] + seriesLabels[i - 1].length * LEGEND_CHAR_W + 32;
			acc.push(prev);
			return acc;
		}, [])
	);
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
							rx={rx}
						/>
						<!-- value label -->
						{#if labelsInside}
							{@const labelText = format(val)}
							{@const minW = labelText.length * 7 + 10}
							{#if barW >= minW}
								<text
									x={margin.left + barW - 6}
									y={by + barHeight / 2}
									text-anchor="end"
									dominant-baseline="middle"
									font-size="11"
									font-weight="600"
									fill="#fffffe">{labelText}</text
								>
							{:else}
								<text
									x={margin.left + barW + 4}
									y={by + barHeight / 2}
									dominant-baseline="middle"
									font-size="10"
									fill="#444">{labelText}</text
								>
							{/if}
						{:else}
							<text
								x={margin.left + barW + 4}
								y={by + barHeight / 2}
								dominant-baseline="middle"
								font-size="10"
								fill="#444">{format(val)}</text
							>
						{/if}
					{/each}
				{/if}
			{/each}

			<!-- hidden text measurement group for legend widths -->
			{#if legendBottom}
				<g visibility="hidden" aria-hidden="true" pointer-events="none">
					{#each legendAllItems as item, i}
						<text bind:this={legendTextEls[i]} font-size="12" font-weight="600">{item.label}</text>
						{#if item.secondLabel}
							<text bind:this={legendText2Els[i]} font-size="12" font-weight="600">{item.secondLabel}</text>
						{/if}
					{/each}
				</g>
			{/if}

			<!-- legend -->
			{#if legendBottom}
				{#each legendRows as row, ri}
					{@const rowY = legendStartY + ri * (LEGEND_BLOCK_H + LEGEND_ROW_GAP)}
					{@const rowItems = row.map((idx) => ({ item: legendAllItems[idx], w: legendNaturalW[idx] }))}
					{@const rowTotalW = rowItems.reduce((s, r) => s + r.w, 0)}
					{@const rowOffsetX = margin.left + (innerW - rowTotalW) / 2}
					{#each rowItems as { item, w }, col}
						{@const bx = rowOffsetX + rowItems.slice(0, col).reduce((s, r) => s + r.w, 0)}
						{#if item.secondLabel && item.secondColor}
							<rect x={bx} y={rowY} width={w / 2} height={LEGEND_BLOCK_H} fill={item.color} shape-rendering="crispEdges" />
							<rect x={bx + w / 2} y={rowY} width={w / 2} height={LEGEND_BLOCK_H} fill={item.secondColor} shape-rendering="crispEdges" />
							<text x={bx + w / 4} y={rowY + LEGEND_BLOCK_H / 2} dy="0.35em" text-anchor="middle" font-size="11" font-weight="600" fill="#fffffe">{item.label}</text>
							<text x={bx + w * 3 / 4} y={rowY + LEGEND_BLOCK_H / 2} dy="0.35em" text-anchor="middle" font-size="11" font-weight="600" fill="#fffffe">{item.secondLabel}</text>
							<line x1={bx + w / 2} y1={rowY} x2={bx + w / 2} y2={rowY + LEGEND_BLOCK_H} stroke="rgba(255,255,255,0.4)" stroke-width="1" shape-rendering="crispEdges" />
						{:else}
							<rect x={bx} y={rowY} width={w} height={LEGEND_BLOCK_H} fill={item.color} shape-rendering="crispEdges" />
							<text x={bx + LEGEND_PAD_X} y={rowY + LEGEND_BLOCK_H / 2} dy="0.35em" font-size="12" font-weight="600" fill="#fffffe">{item.label}</text>
						{/if}
						{#if col < rowItems.length - 1}
							<line x1={bx + w} y1={rowY} x2={bx + w} y2={rowY + LEGEND_BLOCK_H} stroke="rgba(0,0,0,0.25)" stroke-width="0.5" shape-rendering="crispEdges" />
						{/if}
					{/each}
					<rect fill="none" stroke="rgba(0,0,0,0.25)" stroke-width="0.5" shape-rendering="crispEdges" x={rowOffsetX} y={rowY} width={rowTotalW} height={LEGEND_BLOCK_H} />
				{/each}
			{:else}
				{#each seriesLabels as label, si}
					{@const lx = margin.left + legendTopOffsets[si]}
					<rect x={lx} y={6} width={12} height={10} fill={colors[si % colors.length]} rx="2" />
					<text x={lx + 16} y={13} font-size="11" fill="#444">{label}</text>
				{/each}
			{/if}
		</svg>
	{/if}
</div>
