<script lang="ts">
	export interface UfSexoRow {
		uf: string;
		aldirMasc: number; // 0-100
		aldirFem: number;  // 0-100
		ibgeMasc: number;  // 0-100
		ibgeFem: number;   // 0-100
	}

	let {
		data = [] as UfSexoRow[],
		colorMasc = '#4271b5',
		colorFem = '#a44c7f',
		barHeight = 14,
		pairGap = 3,
		groupGap = 10,
		margin = { top: 24, right: 20, bottom: 110, left: 130 },
	}: {
		data?: UfSexoRow[];
		colorMasc?: string;
		colorFem?: string;
		barHeight?: number;
		pairGap?: number;
		groupGap?: number;
		margin?: { top: number; right: number; bottom: number; left: number };
	} = $props();

	const FONT_FAMILY = "'Space Grotesk', system-ui, sans-serif";

	let containerWidth = $state(0);
	const innerW = $derived(Math.max(0, containerWidth - margin.left - margin.right));

	const groupH = $derived(barHeight * 2 + pairGap);
	const rowStep = $derived(groupH + groupGap);
	const totalContentH = $derived(data.length * rowStep - groupGap);
	const svgHeight = $derived(margin.top + totalContentH + margin.bottom);

	const scaleX = (v: number) => (v / 100) * innerW;

	const xTicks = [0, 25, 50, 75, 100];

	function textColor(hex: string, opacity = 1): string {
		const r = parseInt(hex.slice(1, 3), 16) / 255;
		const g = parseInt(hex.slice(3, 5), 16) / 255;
		const b = parseInt(hex.slice(5, 7), 16) / 255;
		// Adjust luminance for opacity blended over white
		const L = (0.2126 * r + 0.7152 * g + 0.0722 * b) * opacity + (1 - opacity);
		return L > 0.45 ? '#1a1a1a' : '#fffffe';
	}

	// Legend layout
	const LEGEND_BLOCK_H = 34;
	const LEGEND_CHAR_W  = 7.5;
	const LEGEND_PAD_X   = 16;
	const LEGEND_ROW_GAP = 2;

	const legendRows = $derived([
		[
			{ label: 'Masculino – contemplados',      color: colorMasc, opacity: 1    },
			{ label: 'Feminino – contempladas',        color: colorFem,  opacity: 1    },
		],
		[
			{ label: 'Masculino – População',  color: colorMasc, opacity: 0.35 },
			{ label: 'Feminino – População',   color: colorFem,  opacity: 0.35 },
		],
	]);
	const legendRowWidths = $derived(
		legendRows.map((row) => row.map((item) => item.label.length * LEGEND_CHAR_W + LEGEND_PAD_X * 2))
	);
	const LEGEND_Y = $derived(margin.top + totalContentH + 28);
</script>

<div bind:clientWidth={containerWidth} style="width:100%;">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={svgHeight} role="img" font-family={FONT_FAMILY}>

			<!-- grid lines -->
			{#each xTicks as tick}
				{@const x = margin.left + scaleX(tick)}
				<line
					x1={x} y1={margin.top - 6}
					x2={x} y2={margin.top + totalContentH}
					stroke={tick === 50 ? '#bbb' : '#e5e5e5'}
					stroke-width="1"
					stroke-dasharray={tick === 50 ? '4,3' : undefined}
				/>
				<text x={x} y={margin.top + totalContentH + 14} text-anchor="middle" font-size="11" fill="#666"
					>{tick}%</text>
			{/each}

			<!-- UF groups -->
			{#each data as row, i}
				{@const gy = margin.top + i * rowStep}
				{@const aldirY = gy}
				{@const ibgeY = gy + barHeight + pairGap}
				{@const midGroupY = gy + groupH / 2}

				<!-- UF label (centered on the pair) -->
				<text
					x={margin.left - 78}
					y={midGroupY}
					dominant-baseline="middle"
					font-size="11"
					font-weight="700"
					fill="#333"
				>{row.uf}</text>

				<!-- sub-labels -->
				<text
					x={margin.left - 6}
					y={aldirY + barHeight / 2}
					dominant-baseline="middle"
					text-anchor="end"
					font-size="9"
					fill="#555"
				>PNAB</text>
				<text
					x={margin.left - 6}
					y={ibgeY + barHeight / 2}
					dominant-baseline="middle"
					text-anchor="end"
					font-size="9"
					fill="#999"
				>População</text>

				<!-- Aldir Blanc bar (full opacity) -->
				{@const aMascW = scaleX(row.aldirMasc)}
				{@const aFemW  = scaleX(row.aldirFem)}
				<rect x={margin.left}          y={aldirY} width={aMascW} height={barHeight} fill={colorMasc} />
				<rect x={margin.left + aMascW} y={aldirY} width={aFemW}  height={barHeight} fill={colorFem} />
				{#if aMascW > 36}
					<text x={margin.left + 5} y={aldirY + barHeight / 2} dominant-baseline="middle" font-size="10" font-weight="600" fill={textColor(colorMasc)}>
						{row.aldirMasc.toFixed(1)}%
					</text>
				{/if}
				{#if aFemW > 36}
					<text x={margin.left + aMascW + 5} y={aldirY + barHeight / 2} dominant-baseline="middle" font-size="10" font-weight="800" fill={textColor(colorFem)}>
						{row.aldirFem.toFixed(1)}%
					</text>
				{/if}

				<!-- IBGE bar (muted) -->
				{@const iMascW = scaleX(row.ibgeMasc)}
				{@const iFemW  = scaleX(row.ibgeFem)}
				<rect x={margin.left}          y={ibgeY} width={iMascW} height={barHeight} fill={colorMasc} opacity="0.35" />
				<rect x={margin.left + iMascW} y={ibgeY} width={iFemW}  height={barHeight} fill={colorFem}  opacity="0.35" />
				{#if iMascW > 36}
					<text x={margin.left + 5} y={ibgeY + barHeight / 2} dominant-baseline="middle" font-size="10" fill={textColor(colorMasc, 0.35)}>
						{row.ibgeMasc.toFixed(1)}%
					</text>
				{/if}
				{#if iFemW > 36}
					<text x={margin.left + iMascW + 5} y={ibgeY + barHeight / 2} dominant-baseline="middle" font-size="10" fill={textColor(colorFem, 0.35)}>
						{row.ibgeFem.toFixed(1)}%
					</text>
				{/if}
			{/each}

			<!-- legend: 4 blocos em 2 linhas -->
			{#each legendRows as row, ri}
				{@const rowY = LEGEND_Y + ri * (LEGEND_BLOCK_H + LEGEND_ROW_GAP)}
				{@const widths = legendRowWidths[ri]}
				{@const rowTotalW = widths.reduce((s, w) => s + w, 0)}
				{@const rowStartX = (containerWidth - rowTotalW) / 2}
				{#each row as item, ci}
					{@const bx = rowStartX + widths.slice(0, ci).reduce((s, w) => s + w, 0)}
					{@const w = widths[ci]}
					<rect x={bx} y={rowY} width={w} height={LEGEND_BLOCK_H} fill={item.color} opacity={item.opacity} shape-rendering="crispEdges" />
					<text x={bx + LEGEND_PAD_X} y={rowY + LEGEND_BLOCK_H / 2} dy="0.35em" font-size="12" font-weight="600" fill={textColor(item.color, item.opacity)}>{item.label}</text>
					{#if ci < row.length - 1}
						<line x1={bx + w} y1={rowY} x2={bx + w} y2={rowY + LEGEND_BLOCK_H} stroke="rgba(0,0,0,0.25)" stroke-width="0.5" shape-rendering="crispEdges" />
					{/if}
				{/each}
				<rect fill="none" stroke="rgba(0,0,0,0.25)" stroke-width="0.5" shape-rendering="crispEdges" x={rowStartX} y={rowY} width={rowTotalW} height={LEGEND_BLOCK_H} />
			{/each}

		</svg>
	{/if}
</div>
