<script lang="ts">
	export interface VerticalGroupedBarRow {
		label: string;
		fullLabel?: string; // used for wrapped x-axis label (uppercased automatically)
		values: number[]; // one per series, same order as seriesLabels
		colors?: string[]; // per-row color override
	}

	let {
		data = [] as VerticalGroupedBarRow[],
		seriesLabels = [] as string[],
		colors = ['#cb4034', '#a44c7f', '#ea662f', '#ab4723'] as string[],
		format = (v: number) => v.toFixed(1) + '%',
		barWidth = 20,
		barPad = 4,
		innerH = 280,
		margin = { top: 20, right: 20, bottom: 10, left: 44 },
		yTicks = 5,
	}: {
		data: VerticalGroupedBarRow[];
		seriesLabels?: string[];
		colors?: string[];
		format?: (v: number) => string;
		barWidth?: number;
		barPad?: number;
		innerH?: number;
		margin?: { top: number; right: number; bottom: number; left: number };
		yTicks?: number;
	} = $props();

	let containerWidth = $state(0);

	const FONT = "'Space Grotesk', system-ui, sans-serif";
	const LABEL_FS = 10;
	const LABEL_LH = 13;
	const LEGEND_CHAR_W = 6.5;
	const LEGEND_PAD_X = 16;
	const LEGEND_BLOCK_H = 34;
	const LEGEND_ROW_GAP = 2;

	const nSeries = $derived(
		seriesLabels.length > 0
			? seriesLabels.length
			: Math.max(0, ...data.map((d) => d.values.length))
	);

	const groupBarW = $derived(nSeries * barWidth + Math.max(0, nSeries - 1) * barPad);
	const innerW = $derived(Math.max(0, containerWidth - margin.left - margin.right));
	const nGroups = $derived(data.length);
	const groupSlotW = $derived(nGroups > 0 ? innerW / nGroups : 0);

	// Estimate max chars per line from the slot width and font size
	const maxChars = $derived(Math.max(6, Math.floor(groupSlotW / (LABEL_FS * 0.62))));

	function wrapText(text: string, max: number): string[] {
		const words = text.toUpperCase().split(' ');
		const lines: string[] = [];
		let cur = '';
		for (const w of words) {
			const test = cur ? `${cur} ${w}` : w;
			if (test.length > max && cur) {
				lines.push(cur);
				cur = w;
			} else {
				cur = test;
			}
		}
		if (cur) lines.push(cur);
		return lines;
	}

	const labelLines = $derived(data.map((row) => wrapText(row.fullLabel ?? row.label, maxChars)));
	const maxLabelLines = $derived(Math.max(1, ...labelLines.map((l) => l.length)));
	const labelAreaH = $derived(maxLabelLines * LABEL_LH + 10);

	const legendItems = $derived(
		seriesLabels.map((label, i) => ({ label, color: colors[i % colors.length] }))
	);

	const legendNaturalW = $derived(
		legendItems.map((item) => item.label.length * LEGEND_CHAR_W + LEGEND_PAD_X * 2)
	);
	// Greedy row packing
	const legendRows = $derived((() => {
		if (legendItems.length === 0 || innerW === 0) return [] as number[][];
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
	const legendBlocksH = $derived(
		legendItems.length > 0
			? legendRows.length * LEGEND_BLOCK_H + Math.max(0, legendRows.length - 1) * LEGEND_ROW_GAP + 8
			: 0
	);
	const svgHeight = $derived(margin.top + innerH + labelAreaH + legendBlocksH + margin.bottom);

	const yMax = $derived(Math.max(...data.flatMap((d) => d.values), 1));
	const yDomain = $derived(Math.ceil(yMax / 5) * 5);

	const baseline = $derived(margin.top + innerH);

	const tickStep = $derived(yDomain / yTicks);
	const tickValues = $derived(
		Array.from({ length: yTicks + 1 }, (_, i) => i * tickStep)
	);

	const groupCenterX = $derived(
		data.map((_, i) => margin.left + groupSlotW * i + groupSlotW / 2)
	);

	const legendStartY = $derived(margin.top + innerH + labelAreaH + 8);
</script>

<div bind:clientWidth={containerWidth} style="width:100%;">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={svgHeight} role="img" font-family={FONT}>
			<!-- Legend (block style, bottom) -->
			{#if legendItems.length > 0}
				{#each legendRows as row, ri}
					{@const rowY = legendStartY + ri * (LEGEND_BLOCK_H + LEGEND_ROW_GAP)}
					{@const rowItems = row.map((idx) => ({ item: legendItems[idx], w: legendNaturalW[idx] }))}
					{@const rowTotalW = rowItems.reduce((s, r) => s + r.w, 0)}
					{@const rowOffsetX = margin.left + (innerW - rowTotalW) / 2}
					{#each rowItems as { item, w }, col}
						{@const bx = rowOffsetX + rowItems.slice(0, col).reduce((s, r) => s + r.w, 0)}
						<rect x={bx} y={rowY} width={w} height={LEGEND_BLOCK_H} fill={item.color} shape-rendering="crispEdges" />
						<text x={bx + w / 2} y={rowY + LEGEND_BLOCK_H / 2} dy="0.35em" text-anchor="middle" font-size="12" font-weight="600" fill="#fffffe">{item.label}</text>
						{#if col < rowItems.length - 1}
							<line x1={bx + w} y1={rowY} x2={bx + w} y2={rowY + LEGEND_BLOCK_H} stroke="rgba(0,0,0,0.25)" stroke-width="0.5" shape-rendering="crispEdges" />
						{/if}
					{/each}
					<rect fill="none" stroke="rgba(0,0,0,0.25)" stroke-width="0.5" shape-rendering="crispEdges" x={rowOffsetX} y={rowY} width={rowTotalW} height={LEGEND_BLOCK_H} />
				{/each}
			{/if}

			<!-- Grid lines + Y-axis labels -->
			{#each tickValues as tick}
				{@const ty = baseline - (tick / yDomain) * innerH}
				<line
					x1={margin.left}
					y1={ty}
					x2={margin.left + innerW}
					y2={ty}
					stroke={tick === 0 ? '#d0d0d0' : '#e8e8e8'}
					stroke-width={tick === 0 ? 1 : 0.75}
					stroke-dasharray={tick === 0 ? 'none' : '3 3'}
				/>
				{#if tick > 0}
					<text
						x={margin.left - 6}
						y={ty}
						dy="0.35em"
						text-anchor="end"
						font-size="9"
						fill="#888"
					>{format(tick)}</text>
				{/if}
			{/each}

			<!-- Groups -->
			{#each data as row, gi}
				{@const cx = groupCenterX[gi]}
				{@const gx = cx - groupBarW / 2}

				<!-- Bars and value labels -->
				{#each row.values as val, si}
					{@const bx = gx + si * (barWidth + barPad)}
					{@const barH = Math.max(0, (val / yDomain) * innerH)}
					{@const by = baseline - barH}
					{@const barColor = row.colors?.[si] ?? colors[si % colors.length]}

					<rect x={bx} y={by} width={barWidth} height={barH} fill={barColor} rx="2" />
					<text
						x={bx + barWidth / 2}
						y={by - 3}
						text-anchor="middle"
						font-size="10"
						fill="#444"
					>{format(val)}</text>
				{/each}

				<!-- X-axis label (wrapped, uppercase) -->
				<text text-anchor="middle" font-size={LABEL_FS} fill="#555">
					{#each labelLines[gi] as line, li}
						<tspan x={cx} y={baseline + 8 + (li + 1) * LABEL_LH}>{line}</tspan>
					{/each}
				</text>
			{/each}
		</svg>
	{/if}
</div>
