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
	const LABEL_CHAR_W = 7;     // px/char for the 12px arc labels (% + valor)
	const LABEL_GAP_FR = 0.06;  // distância do label fora do arco, fração do raio

	// Legend (horizontal row, centered below the donut)
	const LEGEND_H      = 40;   // vertical space reserved below the donut
	const SWATCH        = 13;   // legend color square size
	const SWATCH_GAP    = 7;    // gap between swatch and its label
	const ITEM_GAP      = 22;   // gap between legend items
	const LEGEND_CHAR_W = 7.2;  // px/char for the 12px legend labels

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);

	// Largest arc label (% ou valor absoluto) em px — reserva espaço lateral p/ não cortar
	const maxLabelW = $derived((() => {
		const t = data.reduce((s, d) => s + d.value, 0);
		let chars = 0;
		for (const d of data) {
			const perc = t > 0 ? `${((d.value / t) * 100).toFixed(1)}%` : '';
			chars = Math.max(chars, perc.length, format(d.value).length);
		}
		return chars * LABEL_CHAR_W;
	})());

	// Donut area = full container width (capped so it doesn't float in a huge
	// empty space), centered. Legend goes below, so no lateral reservation.
	const donutAreaW = $derived(Math.min(containerWidth, height * 1.5));
	// Raio máximo que cabe reservando os labels nas laterais (h) e topo/base (v)
	const outerRadius = $derived(
		Math.max(
			40,
			Math.min(
				(donutAreaW / 2 - maxLabelW) / (1 + LABEL_GAP_FR),
				(height / 2 - 26) / (1 + LABEL_GAP_FR)
			)
		)
	);
	const innerRadius = $derived(outerRadius * innerRadiusFraction);
	const cx          = $derived(containerWidth / 2);
	const cy          = $derived(height / 2);

	const svgWidth  = $derived(containerWidth);
	const svgHeight = $derived(height + LEGEND_H);

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
			.innerRadius(outerRadius * (1 + LABEL_GAP_FR))
			.outerRadius(outerRadius * (1 + LABEL_GAP_FR))
	);

	const arcs  = $derived(pieFn(data));
	const total = $derived(data.reduce((s, d) => s + d.value, 0));

	// Legend layout: items laid out left→right, whole row centered horizontally
	const legendItems = $derived.by(() => {
		const items = data.map((d: { label: string; value: number }, i: number) => {
			const w = SWATCH + SWATCH_GAP + d.label.length * LEGEND_CHAR_W;
			return { label: d.label, color: colors[i] ?? '#999', w };
		});
		const totalW = items.reduce((s, it) => s + it.w, 0) + Math.max(0, items.length - 1) * ITEM_GAP;
		let cursor = (containerWidth - totalW) / 2;
		return items.map((it) => {
			const x = cursor;
			cursor += it.w + ITEM_GAP;
			return { ...it, x };
		});
	});
	const legendY = $derived(height + LEGEND_H / 2);
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg
			width={svgWidth}
			height={svgHeight}
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

			<!-- Legend — horizontal row, centered below the donut -->
			<g transform="translate(0,{legendY})">
				{#each legendItems as item}
					<rect
						x={item.x}
						y={-SWATCH / 2}
						width={SWATCH}
						height={SWATCH}
						fill={item.color}
						shape-rendering="crispEdges"
					/>
					<text
						x={item.x + SWATCH + SWATCH_GAP}
						y={0}
						dy="0.35em"
						font-size="12"
						font-weight="600"
						fill="#1e293b"
					>{item.label}</text>
				{/each}
			</g>
		</svg>
	{/if}
</div>
