<script lang="ts">
	import { pie, arc } from 'd3-shape';

	let {
		width = undefined,
		data = [] as { label: string; value: number }[],
		colors = [] as string[],
		centerLabel = '',
		centerValue = '',
		height = 360,
		format = (v: number) => v.toLocaleString(),
		radiusFraction = 0.42,
		innerRadiusFraction = 0.6,
	}: {
		width?: number;
		data?: { label: string; value: number }[];
		colors?: string[];
		centerLabel?: string;
		centerValue?: string;
		height?: number;
		format?: (v: number) => string;
		radiusFraction?: number;
		innerRadiusFraction?: number;
	} = $props();

	const FONT_FAMILY = "'Rawline', system-ui, sans-serif";
	const CHAR_W      = 7;
	const BOX_PAD     = 32;
	const LEGEND_GAP  = 16;

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);

	function labelColor(hex: string): string {
		const r = parseInt(hex.slice(1, 3), 16) / 255;
		const g = parseInt(hex.slice(3, 5), 16) / 255;
		const b = parseInt(hex.slice(5, 7), 16) / 255;
		const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
		return luminance > 0.65 ? '#1a1a1a' : '#fffffe';
	}

	// Legend: vertical box to the right, same height as chart
	const legendW     = $derived(Math.max(120, Math.max(...data.map((d) => d.label.length * CHAR_W)) + BOX_PAD));
	const legendItemH = $derived(height / data.length);

	// Donut area = capped at height * 1.5 so the donut doesn't float in a huge empty space
	const donutAreaW  = $derived(Math.min(containerWidth - legendW - LEGEND_GAP, height * 1.5));
	const outerRadius = $derived(Math.min(donutAreaW / 2, height / 2) * 0.78);
	const innerRadius = $derived(outerRadius * innerRadiusFraction);
	const cx          = $derived(donutAreaW / 2);
	const cy          = $derived(height / 2);

	// SVG width = actual content, not full container
	const svgWidth    = $derived(donutAreaW + LEGEND_GAP + legendW);

	// Pie arcs
	const pieFn = pie<{ label: string; value: number }>()
		.value((d) => d.value)
		.sort(null)
		.padAngle(0.015);

	const arcFn = $derived(
		arc<ReturnType<typeof pieFn>[number]>()
			.innerRadius(innerRadius)
			.outerRadius(outerRadius)
			.cornerRadius(2)
	);

	// Arc used only for centroid — placed just outside the slice
	const labelArcFn = $derived(
		arc<ReturnType<typeof pieFn>[number]>()
			.innerRadius(outerRadius * 1.15)
			.outerRadius(outerRadius * 1.15)
	);

	const arcs  = $derived(pieFn(data));
	const total = $derived(data.reduce((s, d) => s + d.value, 0));

	const legendX = $derived(donutAreaW + LEGEND_GAP);
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg
			width={svgWidth}
			height={height}
			role="img"
			aria-label="Donut chart"
			font-family={FONT_FAMILY}
		>
			<!-- Arcs -->
			<g transform="translate({cx},{cy})">
				{#each arcs as d, i}
					{@const [lx, ly] = labelArcFn.centroid(d)}
					{@const perc = total > 0 ? (d.data.value / total) * 100 : 0}
					{@const anchor = lx >= 0 ? 'start' : 'end'}
					<path
						d={arcFn(d) ?? ''}
						fill={colors[i] ?? '#ccc'}
					/>
					<!-- Arc label: percentage + absolute -->
					<text
						x={lx}
						y={ly}
						text-anchor={anchor}
						font-size="12"
						font-weight="700"
						fill="#1e293b"
					>{perc.toFixed(1)}%</text>
					<text
						x={lx}
						y={ly}
						dy="1.3em"
						text-anchor={anchor}
						font-size="12"
						fill="#64748b"
					>{format(d.data.value)}</text>
				{/each}

				<!-- Center label -->
				{#if centerValue}
					<text
						text-anchor="middle"
						dy="-0.3em"
						font-size="12"
						font-weight="700"
						fill="#1e293b"
					>{centerValue}</text>
				{/if}
				{#if centerLabel}
					<text
						text-anchor="middle"
						dy="1.1em"
						font-size="12"
						fill="#64748b"
					>{centerLabel}</text>
				{/if}
			</g>

			<!-- Legend — vertical box to the right, height = chart height -->
			<g transform="translate({legendX},0)">
				{#each data as item, i}
					<rect
						x={0}
						y={legendItemH * i}
						width={legendW}
						height={legendItemH}
						fill={colors[i] ?? '#999'}
						shape-rendering="crispEdges"
					/>
					<text
						x={legendW / 2}
						y={legendItemH * i + legendItemH / 2}
						dy="0.35em"
						text-anchor="middle"
						font-size="12"
						font-weight="600"
						fill={labelColor(colors[i] ?? '#999')}
					>{item.label}</text>
				{/each}

				<!-- Dividers between items -->
				{#each data.slice(0, data.length - 1) as _, i}
					<line
						x1={0}          y1={legendItemH * (i + 1)}
						x2={legendW}    y2={legendItemH * (i + 1)}
						stroke="#000000"
						stroke-width="0.5"
						shape-rendering="crispEdges"
					/>
				{/each}

				<!-- Border -->
				<rect
					x={0} y={0}
					width={legendW}
					height={height}
					fill="none"
					stroke="#000000"
					stroke-width="0.5"
					shape-rendering="crispEdges"
				/>
			</g>
		</svg>
	{/if}
</div>
