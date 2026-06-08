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
		margin = { top: 20, right: 20, bottom: 10, left: 20 },
	}: {
		data: VerticalGroupedBarRow[];
		seriesLabels?: string[];
		colors?: string[];
		format?: (v: number) => string;
		barWidth?: number;
		barPad?: number;
		innerH?: number;
		margin?: { top: number; right: number; bottom: number; left: number };
	} = $props();

	let containerWidth = $state(0);

	const FONT = "'Space Grotesk', system-ui, sans-serif";
	const LABEL_FS = 10;
	const LABEL_LH = 13;
	const LEGEND_ITEM_GAP = 20;
	const LEGEND_H = 28;
	const LEGEND_CHAR_W = 6.5;

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
	const legendExtraH = $derived(legendItems.length > 0 ? LEGEND_H : 0);
	const svgHeight = $derived(margin.top + innerH + labelAreaH + legendExtraH + margin.bottom);

	const yMax = $derived(Math.max(...data.flatMap((d) => d.values), 1));
	const yDomain = $derived(Math.ceil(yMax / 5) * 5);

	const baseline = $derived(margin.top + innerH);

	const groupCenterX = $derived(
		data.map((_, i) => margin.left + groupSlotW * i + groupSlotW / 2)
	);

	const legendItemWidths = $derived(
		legendItems.map((item) => 12 + 5 + item.label.length * LEGEND_CHAR_W)
	);
	const legendTotalW = $derived(
		legendItemWidths.reduce((s, w) => s + w, 0) +
			Math.max(0, legendItems.length - 1) * LEGEND_ITEM_GAP
	);
	const legendItemX = $derived(
		legendItemWidths.reduce<number[]>((acc, w, i) => {
			acc.push(
				i === 0
					? (containerWidth - legendTotalW) / 2
					: acc[i - 1] + legendItemWidths[i - 1] + LEGEND_ITEM_GAP
			);
			return acc;
		}, [])
	);
	const legendY = $derived(margin.top + innerH + labelAreaH + 10);
</script>

<div bind:clientWidth={containerWidth} style="width:100%;">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={svgHeight} role="img" font-family={FONT}>
			<!-- Legend (centered, bottom) -->
			{#if legendItems.length > 0}
				{#each legendItems as item, li}
					{@const lx = legendItemX[li]}
					<rect x={lx} y={legendY} width={12} height={10} fill={item.color} rx="2" />
					<text x={lx + 17} y={legendY + 9} font-size="11" fill="#444">{item.label}</text>
				{/each}
			{/if}

			<!-- Baseline -->
			<line
				x1={margin.left}
				y1={baseline}
				x2={margin.left + innerW}
				y2={baseline}
				stroke="#d0d0d0"
				stroke-width="1"
			/>

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
