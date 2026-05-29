<script lang="ts">
	export interface GroupedBarRow {
		label: string;
		values: number[]; // one value per series, same order as seriesLabels
	}

	let {
		data = [] as GroupedBarRow[],
		seriesLabels = [] as string[],
		colors = ['#2a9d8f', '#e9c46a'] as string[],
		format = (v: number) => v.toFixed(1) + '%',
		xLabel = '',
		margin = { top: 20, right: 90, bottom: 40, left: 50 },
		barHeight = 10,
		barPad = 4,
	}: {
		data: GroupedBarRow[];
		seriesLabels: string[];
		colors?: string[];
		format?: (v: number) => string;
		xLabel?: string;
		margin?: { top: number; right: number; bottom: number; left: number };
		barHeight?: number;
		barPad?: number;
	} = $props();

	let containerWidth = $state(0);

	const nSeries = $derived(seriesLabels.length);
	const groupHeight = $derived(nSeries * barHeight + (nSeries - 1) * barPad);
	const groupPad = 12;

	const svgHeight = $derived(
		margin.top + margin.bottom + data.length * (groupHeight + groupPad) - groupPad
	);

	const innerW = $derived(Math.max(0, containerWidth - margin.left - margin.right));

	const xMax = $derived(Math.max(...data.flatMap((d) => d.values), 1));

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

	function groupY(i: number): number {
		return margin.top + i * (groupHeight + groupPad);
	}
	function seriesY(si: number): number {
		return si * (barHeight + barPad);
	}
</script>

<div bind:clientWidth={containerWidth} style="width:100%;">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={svgHeight} role="img">
			<!-- grid lines -->
			{#each xTicks as tick}
				{@const x = margin.left + scaleX(tick)}
				<line
					x1={x}
					y1={margin.top - 6}
					x2={x}
					y2={svgHeight - margin.bottom}
					stroke="#e5e5e5"
					stroke-width="1"
				/>
				<text x={x} y={svgHeight - margin.bottom + 14} text-anchor="middle" font-size="11" fill="#666"
					>{format(tick)}</text
				>
			{/each}

			<!-- x axis label -->
			{#if xLabel}
				<text
					x={margin.left + innerW / 2}
					y={svgHeight - 4}
					text-anchor="middle"
					font-size="11"
					fill="#888">{xLabel}</text
				>
			{/if}

			<!-- groups -->
			{#each data as row, i}
				{@const gy = groupY(i)}

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
					{@const by = gy + seriesY(si)}
					<rect
						x={margin.left}
						y={by}
						width={barW}
						height={barHeight}
						fill={colors[si % colors.length]}
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
			{/each}

			<!-- legend -->
			{#each seriesLabels as label, si}
				{@const lx = margin.left + si * 200}
				<rect x={lx} y={6} width={12} height={10} fill={colors[si % colors.length]} rx="2" />
				<text x={lx + 16} y={13} font-size="11" fill="#444">{label}</text>
			{/each}
		</svg>
	{/if}
</div>
