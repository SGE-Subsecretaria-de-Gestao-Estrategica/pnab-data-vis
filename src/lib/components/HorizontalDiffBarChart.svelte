<script lang="ts">
	export interface DiffRow {
		label: string;
		diff?: number;
		isSeparator?: boolean;
	}

	const FONT = "'Space Grotesk', system-ui, sans-serif";

	function labelColor(hex: string): string {
		const r = parseInt(hex.slice(1, 3), 16) / 255;
		const g = parseInt(hex.slice(3, 5), 16) / 255;
		const b = parseInt(hex.slice(5, 7), 16) / 255;
		const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
		return luminance > 0.55 ? '#1a1a1a' : '#fffffe';
	}

	let {
		data = [] as DiffRow[],
		colorPositive = '#1351B4',
		colorNegative = '#cb4034',
		format = (v: number) => (v > 0 ? '+' : '') + v.toFixed(1) + '%',
		rowHeight = 34,
		separatorHeight = 28,
		margin = { top: 16, right: 80, bottom: 48, left: 50 },
		xLabel = '',
		zeroLabel = '0%',
	}: {
		data?: DiffRow[];
		colorPositive?: string;
		colorNegative?: string;
		format?: (v: number) => string;
		rowHeight?: number;
		separatorHeight?: number;
		margin?: { top: number; right: number; bottom: number; left: number };
		xLabel?: string;
		zeroLabel?: string;
	} = $props();

	let containerWidth = $state(0);

	const innerW = $derived(Math.max(0, containerWidth - margin.left - margin.right));

	// absolute max diff for symmetric scale
	const maxAbs = $derived(
		Math.max(
			...data.filter((d) => !d.isSeparator).map((d) => Math.abs(d.diff ?? 0)),
			1
		)
	);
	const niceMax = $derived(Math.ceil(maxAbs / 5) * 5);

	// x=0 is at center of innerW
	const cx = $derived(innerW / 2);
	const xScale = $derived((v: number) => cx + (v / niceMax) * cx);

	// total height: sum of row heights
	const totalInnerH = $derived(
		data.reduce((s, d) => s + (d.isSeparator ? separatorHeight : rowHeight), 0)
	);
	const svgH = $derived(margin.top + totalInnerH + margin.bottom);

	// pre-compute y positions
	const rows = $derived(
		data.reduce(
			(acc, d) => {
				const prev = acc.at(-1);
				const y = prev ? prev.y + prev.h : 0;
				const h = d.isSeparator ? separatorHeight : rowHeight;
				acc.push({ ...d, y, h });
				return acc;
			},
			[] as (DiffRow & { y: number; h: number })[]
		)
	);

	// tick values: symmetric around 0
	const N_TICKS = 4;
	const ticks = $derived(
		Array.from({ length: N_TICKS * 2 + 1 }, (_, i) => {
			const v = -niceMax + (niceMax / N_TICKS) * i;
			return { v, x: xScale(v) };
		})
	);

	const barH = $derived(rowHeight * 0.72);
	const barOff = $derived((rowHeight - barH) / 2);
	const MIN_LABEL_PX = 30;

	const LEGEND_H = 34;
	const LEGEND_GAP = 8;
	const LEGEND_BOX_W = 120;
	const legendY = $derived(margin.top + totalInnerH + margin.bottom - LEGEND_H - 4);
	const legendTotalW = $derived(LEGEND_BOX_W * 2 + LEGEND_GAP);
	const legendX = $derived(margin.left + cx - legendTotalW / 2);
</script>

<div bind:clientWidth={containerWidth} style="width: 100%;">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={svgH} font-family={FONT} role="img" aria-label="Diferença PNAB vs RAIS por UF">
			<g transform="translate({margin.left},{margin.top})">

				<!-- Grid lines -->
				{#each ticks as tick}
					<line
						x1={tick.x} y1={0}
						x2={tick.x} y2={totalInnerH}
						stroke={Math.abs(tick.v) < 0.001 ? '#aaa' : '#e2e8f0'}
						stroke-width={Math.abs(tick.v) < 0.001 ? 1.5 : 1}
						stroke-dasharray={Math.abs(tick.v) < 0.001 ? 'none' : '3 3'}
					/>
				{/each}

				<!-- Rows -->
				{#each rows as row}
					{#if row.isSeparator}
						<!-- Region label -->
						<text
							x={cx}
							y={row.y + separatorHeight * 0.72}
							text-anchor="middle"
							font-size="12"
							font-weight="700"
							fill="#444"
							letter-spacing="0.04em"
						>{row.label}</text>
					{:else}
						{@const diff = row.diff ?? 0}
						{@const barX = diff >= 0 ? cx : xScale(diff)}
						{@const barW = Math.abs(xScale(diff) - cx)}
						{@const by = row.y + barOff}
						{@const col = diff >= 0 ? colorPositive : colorNegative}
						{@const labelX = diff >= 0 ? xScale(diff) + 5 : xScale(diff) - 5}
						{@const anchor = diff >= 0 ? 'start' : 'end'}
						{@const showInside = barW >= MIN_LABEL_PX}

						<rect x={barX} y={by} width={barW} height={barH} fill={col} shape-rendering="crispEdges" />

						<text
							x={showInside ? (diff >= 0 ? xScale(diff) - 5 : xScale(diff) + 5) : labelX}
							y={by + barH / 2}
							dy="0.35em"
							text-anchor={showInside ? (diff >= 0 ? 'end' : 'start') : anchor}
							font-size="10"
							font-weight="600"
							fill={showInside ? labelColor(col) : '#333'}
						>{format(diff)}</text>

						<!-- UF label -->
						<text
							x={cx - 6}
							y={row.y + rowHeight / 2}
							dy="0.35em"
							text-anchor="end"
							font-size="11"
							fill="#555"
						>{row.label}</text>
					{/if}
				{/each}

				<!-- X-axis -->
				<g transform="translate(0,{totalInnerH})">
					{#each ticks as tick, ti}
						<line x1={tick.x} y1={0} x2={tick.x} y2={5} stroke="#bbb" stroke-width="0.75" />
						<text
							x={tick.x}
							y={8}
							dy="0.71em"
							text-anchor={ti === 0 ? 'start' : ti === ticks.length - 1 ? 'end' : 'middle'}
							font-size="9"
							fill="#888"
						>{Math.abs(tick.v) < 0.001 ? zeroLabel : format(tick.v)}</text>
					{/each}
					{#if xLabel}
						<text x={cx} y={30} text-anchor="middle" font-size="10" fill="#888">{xLabel}</text>
					{/if}
				</g>

			</g>
			<!-- Legend -->
			<g transform="translate({legendX - margin.left},{legendY - margin.top})">
				<rect x={0} y={0} width={LEGEND_BOX_W} height={LEGEND_H} fill={colorPositive} shape-rendering="crispEdges" />
				<text x={8} y={LEGEND_H / 2} dy="0.35em" font-size="11" font-weight="600" fill={labelColor(colorPositive)}>PNAB &gt; RAIS</text>
				<rect x={LEGEND_BOX_W + LEGEND_GAP} y={0} width={LEGEND_BOX_W} height={LEGEND_H} fill={colorNegative} shape-rendering="crispEdges" />
				<text x={LEGEND_BOX_W + LEGEND_GAP + 8} y={LEGEND_H / 2} dy="0.35em" font-size="11" font-weight="600" fill={labelColor(colorNegative)}>PNAB &lt; RAIS</text>
				<rect x={0} y={0} width={legendTotalW} height={LEGEND_H} fill="none" stroke="rgba(0,0,0,0.2)" stroke-width="0.5" shape-rendering="crispEdges" />
				<line x1={LEGEND_BOX_W} y1={0} x2={LEGEND_BOX_W} y2={LEGEND_H} stroke="rgba(0,0,0,0.2)" stroke-width="0.5" shape-rendering="crispEdges" />
			</g>

		</svg>
	{/if}
</div>
