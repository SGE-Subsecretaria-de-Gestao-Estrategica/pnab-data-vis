<script lang="ts">
	export interface BarDatum {
		label: string;
		value: number;
	}

	let {
		width = undefined,
		data = [] as BarDatum[],
		color = '#4271b5',
		format = (v: number) => String(v),
		xLabel = '',
		rowHeight = 32,
		nTicks = 5,
		margin = { top: 20, right: 40, bottom: 40, left: 120 },
	}: {
		width?: number;
		data?: BarDatum[];
		color?: string;
		format?: (v: number) => string;
		xLabel?: string;
		rowHeight?: number;
		nTicks?: number;
		margin?: { top: number; right: number; bottom: number; left: number };
	} = $props();

	const FONT = "'Rawline', system-ui, sans-serif";
	const LABEL_PAD = 6;
	const LABEL_FS = 12;
	// Minimum bar pixel width needed to fit a label inside
	const MIN_INSIDE_PX = 44;

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);

	const sorted = $derived([...data].sort((a, b) => b.value - a.value));
	const innerW = $derived(Math.max(0, containerWidth - margin.left - margin.right));
	const innerH = $derived(sorted.length * rowHeight);
	const svgHeight = $derived(margin.top + innerH + margin.bottom);

	const maxVal = $derived(Math.max(...sorted.map((d) => d.value), 1));
	// nice ceiling: round up to a "nice" number (1, 2, 2.5, 5 × 10^n)
	function niceCeil(x: number): number {
		if (x <= 0) return 1;
		const exp = Math.floor(Math.log10(x));
		const base = Math.pow(10, exp);
		const f = x / base;
		const nf = f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10;
		return nf * base;
	}
	const niceMax = $derived(niceCeil(maxVal));

	const xScale = $derived((v: number) => (v / niceMax) * innerW);

	const tickValues = $derived(
		Array.from({ length: nTicks + 1 }, (_, i) => (niceMax / nTicks) * i),
	);

	const barH = $derived(Math.max(4, rowHeight * 0.65));
	const barOffset = $derived((rowHeight - barH) / 2);
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={svgHeight} role="img" font-family={FONT}>
			<g transform="translate({margin.left},{margin.top})">
				<!-- Vertical grid lines -->
				{#each tickValues as tick}
					{@const tx = xScale(tick)}
					<line
						x1={tx}
						y1={0}
						x2={tx}
						y2={innerH}
						stroke={tick === 0 ? '#d0d0d0' : '#e8e8e8'}
						stroke-width={tick === 0 ? 1 : 0.75}
						stroke-dasharray={tick === 0 ? 'none' : '3 3'}
					/>
				{/each}

				<!-- Bars -->
				{#each sorted as d, i}
					{@const by = i * rowHeight + barOffset}
					{@const bw = xScale(d.value)}
					{@const labelInside = bw >= MIN_INSIDE_PX}
					{@const formatted = format(d.value)}

					<rect x={0} y={by} width={bw} height={barH} fill={color} rx="1" />

					{#if labelInside}
						<text
							x={bw - LABEL_PAD}
							y={by + barH / 2}
							dy="0.35em"
							text-anchor="end"
							font-size={LABEL_FS}
							font-weight="600"
							font-family={FONT}
							fill="#ffffff"
						>{formatted}</text>
					{:else}
						<text
							x={bw + LABEL_PAD}
							y={by + barH / 2}
							dy="0.35em"
							text-anchor="start"
							font-size={LABEL_FS}
							font-weight="500"
							font-family={FONT}
							fill="#334155"
						>{formatted}</text>
					{/if}
				{/each}

				<!-- X-axis ticks + labels -->
				<g transform="translate(0,{innerH})">
					{#each tickValues as tick}
						{@const tx = xScale(tick)}
						<line x1={tx} y1={0} x2={tx} y2={4} stroke="#aaa" stroke-width="0.75" />
						<text
							x={tx}
							y={8}
							dy="0.71em"
							text-anchor="middle"
							font-size="12"
							fill="#888"
							font-family={FONT}
						>{format(tick)}</text>
					{/each}
					{#if xLabel}
						<text
							x={innerW / 2}
							y={38}
							text-anchor="middle"
							font-size="12"
							fill="#888"
							font-family={FONT}
						>{xLabel}</text>
					{/if}
				</g>
			</g>

			<!-- Y-axis labels (left margin) -->
			{#each sorted as d, i}
				{@const ty = margin.top + i * rowHeight + rowHeight / 2}
				<text
					x={margin.left - 8}
					y={ty}
					dy="0.35em"
					text-anchor="end"
					font-size="12"
					font-family={FONT}
					fill="#64748b"
				>{d.label}</text>
			{/each}
		</svg>
	{/if}
</div>
