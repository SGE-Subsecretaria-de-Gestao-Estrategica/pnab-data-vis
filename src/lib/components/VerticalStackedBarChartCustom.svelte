<script lang="ts">
	type DataRow = Record<string, string | number>;

	let {
		width = undefined,
		data = [] as DataRow[],
		keys = [] as string[],
		categoryKey = 'label',
		labels = {} as Record<string, string>,
		colors = [] as string[],
		format = (v: number) => `${v.toFixed(1)}%`,
		height: chartHeight = 420,
		normalize = true,
	}: {
		width?: number;
		data?: DataRow[];
		keys?: string[];
		categoryKey?: string;
		labels?: Record<string, string>;
		colors?: string[];
		format?: (v: number) => string;
		height?: number;
		normalize?: boolean;
	} = $props();

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);

	const FONT_FAMILY = "'Rawline', system-ui, sans-serif";
	const MARGIN = { top: 16, right: 24, bottom: 80, left: 50 };

	const innerW = $derived(Math.max(0, containerWidth - MARGIN.left - MARGIN.right));
	const innerH = $derived(Math.max(0, chartHeight - MARGIN.top - MARGIN.bottom));

	// Band x-scale (mirrors D3 scaleBand with padding(0.25))
	const PAD = 0.25;
	const n = $derived(data.length);
	const step = $derived(n > 0 ? innerW / (n + PAD) : 0);
	const bandwidth = $derived(step * (1 - PAD));
	const bandX = (i: number) => step * (PAD + i);

	// Y-scale: linear [0, yMax] → [innerH, 0]
	const yMax = $derived(
		normalize
			? 100
			: Math.max(1, ...data.map((row) => keys.reduce((s, k) => s + (Number(row[k]) || 0), 0)))
	);
	const yScale = (v: number) => innerH * (1 - v / yMax);

	function labelColor(hex: string): string {
		if (!hex.startsWith('#') || hex.length < 7) return '#fff';
		const r = parseInt(hex.slice(1, 3), 16) / 255;
		const g = parseInt(hex.slice(3, 5), 16) / 255;
		const b = parseInt(hex.slice(5, 7), 16) / 255;
		const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
		return lum > 0.55 ? '#1a1a1a' : '#fffffe';
	}

	// Stacked segments per category
	const rows = $derived(
		data.map((row, i) => {
			const rowTotal = keys.reduce((s, k) => s + (Number(row[k]) || 0), 0) || 1;
			const scale = normalize ? 100 / rowTotal : 1;
			let cursor = 0;
			const segments = keys.map((key, ki) => {
				const raw = Number(row[key]) || 0;
				const val = raw * scale;
				const y1 = cursor + val;
				const seg = {
					key,
					value: raw,
					y0: cursor,
					y1,
					color: colors[ki] ?? '#999',
				};
				cursor = y1;
				return seg;
			});
			return { label: String(row[categoryKey]), i, segments };
		})
	);

	// Y-axis ticks
	const Y_TICKS = 5;
	const yTicks = $derived(
		Array.from({ length: Y_TICKS + 1 }, (_, i) => {
			const v = (yMax / Y_TICKS) * i;
			return { v, y: yScale(v) };
		})
	);

	// Legend
	const CHAR_W = 7;
	const BOX_PAD = 24;
	const legendBoxWs = $derived(
		keys.map((key) => Math.max(60, (labels[key] ?? key).length * CHAR_W + BOX_PAD))
	);
	const legendBoxX = (ki: number) => legendBoxWs.slice(0, ki).reduce((s, w) => s + w, 0);
	const legendTotalW = $derived(legendBoxWs.reduce((s, w) => s + w, 0));
	const legendY = $derived(innerH + 48);
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg
			width={containerWidth}
			height={chartHeight}
			role="img"
			aria-label="Stacked bar chart"
			font-family={FONT_FAMILY}
			style="overflow: visible;"
		>
			<g transform="translate({MARGIN.left},{MARGIN.top})">

				<!-- Horizontal grid lines -->
				{#each yTicks as tick}
					<line
						x1={0} y1={tick.y}
						x2={innerW} y2={tick.y}
						stroke="#e2e8f0"
						stroke-width="1"
						stroke-dasharray="3,3"
					/>
				{/each}

				<!-- Bars + in-bar labels -->
				{#each rows as row}
					{@const bx = bandX(row.i)}
					{#each row.segments as seg}
						{@const barY = yScale(seg.y1)}
						{@const barH = yScale(seg.y0) - yScale(seg.y1)}
						{#if barH > 0}
							<rect
								x={bx}
								y={barY}
								width={bandwidth}
								height={barH}
								fill={seg.color}
								shape-rendering="crispEdges"
							/>
							{#if barH >= 14}
								<text
									x={bx + bandwidth / 2}
									y={barY + barH / 2}
									dy="0.35em"
									text-anchor="middle"
									font-size="12"
									font-weight="600"
									fill={labelColor(seg.color)}
									pointer-events="none"
								>{format(seg.value)}</text>
							{/if}
						{/if}
					{/each}

					<!-- X-axis category label -->
					<text
						x={bx + bandwidth / 2}
						y={innerH + 12}
						dy="0.9em"
						text-anchor="middle"
						font-size="12"
						fill="#64748b"
					>{row.label}</text>
				{/each}

				<!-- Y-axis ticks -->
				{#each yTicks as tick}
					<text
						x={-8}
						y={tick.y}
						dy="0.35em"
						text-anchor="end"
						font-size="12"
						fill="#64748b"
					>{normalize ? `${tick.v.toFixed(0)}%` : String(tick.v)}</text>
				{/each}

				<!-- Legend -->
				<g transform="translate({(innerW - legendTotalW) / 2},{legendY})">
					{#each keys as key, ki}
						<rect
							x={legendBoxX(ki)}
							y={0}
							width={legendBoxWs[ki]}
							height={30}
							fill={colors[ki] ?? '#999'}
							shape-rendering="crispEdges"
						/>
						<text
							x={legendBoxX(ki) + 10}
							y={15}
							dy="0.35em"
							font-size="12"
							font-weight="600"
							fill={labelColor(colors[ki] ?? '#999')}
						>{labels[key] ?? key}</text>
					{/each}
					{#each keys.slice(0, keys.length - 1) as _, ki}
						<line
							x1={legendBoxX(ki + 1)} y1={0}
							x2={legendBoxX(ki + 1)} y2={30}
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
						width={legendTotalW}
						height={30}
						stroke-width="0.5"
					/>
				</g>

			</g>
		</svg>
	{/if}
</div>
