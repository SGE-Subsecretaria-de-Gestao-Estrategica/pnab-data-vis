<script lang="ts">
	interface Row {
		label: string;
		left: number;
		right: number;
	}

	let {
		width = undefined,
		data = [] as Row[],
		leftLabel = 'Masculino',
		rightLabel = 'Feminino',
		colors = ['#4271b5', '#7b4fa0'] as [string, string],
		format = (v: number) => v.toLocaleString(),
		height = 420,
		centerGap = 96,
	}: {
		width?: number;
		data: Row[];
		leftLabel?: string;
		rightLabel?: string;
		colors?: [string, string];
		format?: (v: number) => string;
		height?: number;
		centerGap?: number;
	} = $props();

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);

	const margin = { top: 16, right: 16, bottom: 68, left: 16 };
	const FONT_PAD = 4;
	const PLOT_BOTTOM_RESERVE = 28;

	// Texto dentro da barra: escuro em barras claras (ex.: amarelo), claro em escuras.
	function labelColor(hex: string): string {
		const r = parseInt(hex.slice(1, 3), 16) / 255;
		const g = parseInt(hex.slice(3, 5), 16) / 255;
		const b = parseInt(hex.slice(5, 7), 16) / 255;
		const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
		return luminance > 0.6 ? '#1a1a1a' : '#ffffff';
	}

	const iw = $derived(containerWidth - margin.left - margin.right);
	const ih = $derived(height - margin.top - margin.bottom);
	const plotH = $derived(ih - PLOT_BOTTOM_RESERVE);
	const cx = $derived(iw / 2);
	const hw = $derived((iw - centerGap) / 2);
	const maxVal = $derived(data.length > 0 ? Math.max(...data.map((d) => Math.max(d.left, d.right))) : 1);

	const BAND_PAD = 0.12;
	const bw = $derived(plotH / (data.length + (data.length - 1) * BAND_PAD));
	const bg = $derived(bw * BAND_PAD);

	const rows = $derived(
		data.map((d, i) => {
			const y = i * (bw + bg);
			const lw = (d.left / maxVal) * hw;
			const rw = (d.right / maxVal) * hw;
			const lx = cx - centerGap / 2 - lw;
			const rx = cx + centerGap / 2;
			const midY = y + bw / 2;
			const fs = 12;
			const lt = format(d.left);
			const rt = format(d.right);
			const leftFits = lw >= FONT_PAD + lt.length * fs * 0.62 + FONT_PAD;
			const rightFits = rw >= FONT_PAD + rt.length * fs * 0.62 + FONT_PAD;
			return { label: d.label, y, lw, rw, lx, rx, midY, fs, lt, rt, leftFits, rightFits };
		})
	);

	const axisLabelY = $derived(plotH + 20);
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg
			width={containerWidth}
			{height}
			aria-label="Population pyramid"
			style="overflow: visible; font-family: 'Rawline', system-ui, sans-serif;"
		>
			<g transform="translate({margin.left}, {margin.top})">
				{#each rows as row}
					<!-- Left bar -->
					<g aria-label="{row.label} {leftLabel}: {row.lt}">
						<rect
							x={row.lx}
							y={row.y}
							width={row.lw}
							height={bw}
							fill={colors[0]}
							shape-rendering="crispEdges"
						/>
						{#if row.leftFits}
							<text
								x={row.lx + row.lw / 2}
								y={row.midY}
								dy="0.35em"
								font-size={row.fs}
								font-weight="700"
								fill={labelColor(colors[0])}
								text-anchor="middle"
								pointer-events="none"
							>{row.lt}</text>
						{:else if row.lw > 0}
							<text
								x={row.lx - FONT_PAD}
								y={row.midY}
								dy="0.35em"
								font-size={row.fs}
								font-weight="700"
								fill={colors[0]}
								text-anchor="end"
								pointer-events="none"
							>{row.lt}</text>
						{/if}
					</g>

					<!-- Right bar -->
					<g aria-label="{row.label} {rightLabel}: {row.rt}">
						<rect
							x={row.rx}
							y={row.y}
							width={row.rw}
							height={bw}
							fill={colors[1]}
							shape-rendering="crispEdges"
						/>
						{#if row.rightFits}
							<text
								x={row.rx + row.rw / 2}
								y={row.midY}
								dy="0.35em"
								font-size={row.fs}
								font-weight="700"
								fill={labelColor(colors[1])}
								text-anchor="middle"
								pointer-events="none"
							>{row.rt}</text>
						{:else if row.rw > 0}
							<text
								x={row.rx + row.rw + FONT_PAD}
								y={row.midY}
								dy="0.35em"
								font-size={row.fs}
								font-weight="700"
								fill={colors[1]}
								text-anchor="start"
								pointer-events="none"
							>{row.rt}</text>
						{/if}
					</g>

					<!-- Center label -->
					<text
						x={cx}
						y={row.midY}
						dy="0.35em"
						font-size="12"
						font-weight="600"
						text-anchor="middle"
						fill="#000000"
					>{row.label}</text>
				{/each}

				<!-- Axis labels -->
				<text
					x={0}
					y={axisLabelY}
					font-size="12"
					text-anchor="start"
					fill="#000000"
				>← {leftLabel}</text>
				<text
					x={iw}
					y={axisLabelY}
					font-size="12"
					text-anchor="end"
					fill="#000000"
				>{rightLabel} →</text>
			</g>
		</svg>
	{/if}
</div>
