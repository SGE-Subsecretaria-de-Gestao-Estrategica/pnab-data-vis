<script lang="ts">
	import { base } from '$app/paths';
	import { CHART_ROW_HEIGHT, BAR_FILL, FLAG_RATIO, FLAG_GAP, FLAG_BORDER_COLOR, FLAG_BORDER_WIDTH, hasFlag, flagId, flagTitle, flagAwareLabel, truncateToWidth } from '$lib/chartStandards';

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
		rowHeight = CHART_ROW_HEIGHT,
		nTicks = 5,
		margin = { top: 20, right: 40, bottom: 40, left: 120 },
		showFlags = false,
		flagSize = 22,
		flagBorder = true,
		flagBasePath = `${base}/flags/states`,
		labelColor = '#64748b',
		axisColor = '#888',
		outsideValueColor = '#334155',
	}: {
		width?: number;
		data?: BarDatum[];
		color?: string;
		format?: (v: number) => string;
		xLabel?: string;
		rowHeight?: number;
		nTicks?: number;
		margin?: { top: number; right: number; bottom: number; left: number };
		showFlags?: boolean;
		flagSize?: number;
		flagBorder?: boolean;
		flagBasePath?: string;
		/** Cor dos rótulos de categoria (eixo Y). */
		labelColor?: string;
		/** Cor dos textos do eixo X (ticks + xLabel). */
		axisColor?: string;
		/** Cor dos rótulos de valor exibidos fora da barra (barras curtas). */
		outsideValueColor?: string;
	} = $props();

	const FONT = "'Rawline', system-ui, sans-serif";
	const LABEL_PAD = 6;
	const LABEL_FS = 12;
	// Minimum bar pixel width needed to fit a label inside
	const MIN_INSIDE_PX = 44;

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);

	const sorted = $derived([...data].sort((a, b) => b.value - a.value));

	// ── Responsive left column ──────────────────────────────────────────────
	// Always fill the device width: cap the label column to a fraction of the
	// container so a fixed `margin.left` never starves the bars on mobile.
	const MIN_LABEL = 40;
	const MAX_LEFT_FRAC = 0.34;
	const flagW = $derived(flagSize * FLAG_RATIO);
	const flagSpace = $derived(showFlags ? flagW + FLAG_GAP : 0);
	// Snug the column to the widest label (short for siglas, wider for names),
	// bounded by the requested margin and a fraction of the device width.
	const longestLabelPx = $derived(
		sorted.reduce((m, d) => Math.max(m, String(d.label).length), 0) * LABEL_FS * 0.6 + 12,
	);
	const labelColW = $derived(
		Math.min(margin.left, longestLabelPx, Math.max(MIN_LABEL, containerWidth * MAX_LEFT_FRAC)),
	);
	const effLeft = $derived(labelColW + flagSpace);
	const labelAvail = $derived(labelColW - 8);

	const innerW = $derived(Math.max(0, containerWidth - effLeft - margin.right));
	const innerH = $derived(sorted.length * rowHeight);
	const svgHeight = $derived(margin.top + innerH + margin.bottom);

	const maxVal = $derived(Math.max(...sorted.map((d) => d.value), 1));

	// nice step: round a raw interval to a "nice" number (1, 2, 2.5, 5 × 10^n)
	function niceStep(range: number, count: number): number {
		if (range <= 0) return 1;
		const raw = range / count;
		const exp = Math.floor(Math.log10(raw));
		const base = Math.pow(10, exp);
		const f = raw / base;
		const nf = f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10;
		return nf * base;
	}

	// Domain ends exactly at the largest value so the longest (first) bar fills
	// the full available width. Gridlines/legend ticks sit at nice round steps
	// within [0, maxVal], so the axis adapts to whatever the visão filter selects.
	const xScale = $derived((v: number) => (v / maxVal) * innerW);

	const tickValues = $derived.by(() => {
		const step = niceStep(maxVal, nTicks);
		const ticks: number[] = [];
		for (let t = 0; t <= maxVal + step * 1e-6; t += step) ticks.push(t);
		return ticks;
	});

	const barH = $derived(Math.max(4, rowHeight * BAR_FILL));
	const barOffset = $derived((rowHeight - barH) / 2);
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={svgHeight} role="img" font-family={FONT}>
			<g transform="translate({effLeft},{margin.top})">
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

					<rect x={0} y={by} width={bw} height={barH} fill={color} rx="0" />

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
							fill={outsideValueColor}
						>{formatted}</text>
					{/if}
				{/each}

				<!-- X-axis ticks + labels -->
				<g class="x-axis" transform="translate(0,{innerH})">
					{#each tickValues as tick}
						{@const tx = xScale(tick)}
						<line x1={tx} y1={0} x2={tx} y2={4} stroke="#aaa" stroke-width="0.75" />
						<text
							x={tx}
							y={8}
							dy="0.71em"
							text-anchor="middle"
							font-size="12"
							fill={axisColor}
							font-family={FONT}
						>{format(tick)}</text>
					{/each}
					{#if xLabel}
						<text
							x={innerW / 2}
							y={38}
							text-anchor="middle"
							font-size="12"
							fill={axisColor}
							font-family={FONT}
						>{xLabel}</text>
					{/if}
				</g>
			</g>

			<!-- Y-axis labels (+ state flags) in the left column -->
			{#each sorted as d, i}
				{@const ty = margin.top + i * rowHeight + rowHeight / 2}
				{#if showFlags && hasFlag(d.label)}
					<image
						href="{flagBasePath}/{flagId(d.label)}.svg"
						x={2}
						y={ty - flagSize / 2}
						width={flagW}
						height={flagSize}
						preserveAspectRatio="xMidYMid meet"
					>
						<title>{flagTitle(d.label)}</title>
					</image>
					{#if flagBorder}
						<rect
							x={2}
							y={ty - flagSize / 2}
							width={flagW}
							height={flagSize}
							fill="none"
							stroke={FLAG_BORDER_COLOR}
							stroke-width={FLAG_BORDER_WIDTH}
						/>
					{/if}
				{/if}
				<text
					x={effLeft - 8}
					y={ty}
					dy="0.35em"
					text-anchor="end"
					font-size="12"
					font-family={FONT}
					fill={labelColor}
				>{truncateToWidth(flagAwareLabel(d.label, showFlags), labelAvail, 12)}</text>
			{/each}
		</svg>
	{/if}
</div>

<style>
	/* No mobile, os rótulos do eixo X se sobrepõem e ficam ilegíveis — ocultamos. */
	@media (max-width: 720px) {
		.x-axis {
			display: none;
		}
	}
</style>
