<script lang="ts">
	export interface BarDatum {
		label: string;
		value: number;
	}

	let {
		width = undefined,
		data = [] as BarDatum[],
		color = '#cb4034',
		format = (v: number) => v.toFixed(1) + '%',
		yLabel = '',
		height = 400,
		margin = { top: 30, right: 20, bottom: 60, left: 60 },
		yTicks = 5,
		insideLabelMinH = 30,
	}: {
		width?: number;
		data?: BarDatum[];
		color?: string;
		format?: (v: number) => string;
		yLabel?: string;
		height?: number;
		margin?: { top: number; right: number; bottom: number; left: number };
		yTicks?: number;
		insideLabelMinH?: number;
	} = $props();

	const FONT = "'Rawline', system-ui, sans-serif";
	const LABEL_FS = 12;
	const LABEL_LH = 13;

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);

	const innerW = $derived(Math.max(0, containerWidth - margin.left - margin.right));
	const innerH = $derived(Math.max(0, height - margin.top - margin.bottom));
	const baseline = $derived(margin.top + innerH);

	const nGroups = $derived(data.length);
	const groupSlotW = $derived(nGroups > 0 ? innerW / nGroups : 0);
	const barW = $derived(Math.max(4, groupSlotW * 0.6));

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

	const labelLines = $derived(data.map((d) => wrapText(d.label, maxChars)));
	const maxLabelLines = $derived(Math.max(1, ...labelLines.map((l) => l.length)));
	const labelAreaH = $derived(maxLabelLines * LABEL_LH + 10);

	const svgHeight = $derived(margin.top + innerH + labelAreaH + margin.bottom);

	const yMax = $derived(Math.max(...data.map((d) => d.value), 1));
	const yDomain = $derived(Math.ceil(yMax / 5) * 5);

	const tickStep = $derived(yDomain / yTicks);
	const tickValues = $derived(Array.from({ length: yTicks + 1 }, (_, i) => i * tickStep));
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={svgHeight} role="img" font-family={FONT}>
			<!-- Y-axis label -->
			{#if yLabel}
				<text
					x={-(margin.top + innerH / 2)}
					y={14}
					text-anchor="middle"
					font-size="12"
					fill="#888"
					transform="rotate(-90)"
				>{yLabel}</text>
			{/if}

			<!-- Grid lines + Y-axis ticks -->
			{#each tickValues as tick}
				{@const ty = baseline - (tick / yDomain) * innerH}
				<line
					x1={margin.left}
					y1={ty}
					x2={margin.left + innerW}
					y2={ty}
					stroke={tick === 0 ? '#d0d0d0' : '#e8e8e8'}
					stroke-width={tick === 0 ? 1 : 0.75}
					stroke-dasharray={tick === 0 ? 'none' : '3 3'}
				/>
				{#if tick > 0}
					<text
						x={margin.left - 6}
						y={ty}
						dy="0.35em"
						text-anchor="end"
						font-size="12"
						fill="#888"
					>{format(tick)}</text>
				{/if}
			{/each}

			<!-- Bars -->
			{#each data as d, i}
				{@const cx = margin.left + groupSlotW * i + groupSlotW / 2}
				{@const bx = cx - barW / 2}
				{@const barH = Math.max(0, (d.value / yDomain) * innerH)}
				{@const by = baseline - barH}
				{@const insideLabel = barH >= insideLabelMinH}

				<rect x={bx} y={by} width={barW} height={barH} fill={color} rx="2" />

				<!-- Value label: inside bar (rotated) if tall enough, else above -->
				{#if insideLabel}
					<text
						x={cx}
						y={by + barH / 2}
						text-anchor="middle"
						dominant-baseline="middle"
						font-size="12"
						font-weight="600"
						fill="#fffffe"
					>{format(d.value)}</text>
				{:else}
					<text
						x={cx}
						y={by - 4}
						text-anchor="middle"
						font-size="12"
						fill="#444"
					>{format(d.value)}</text>
				{/if}

				<!-- X-axis label (wrapped, uppercase) -->
				<text text-anchor="middle" font-size={LABEL_FS} fill="#555">
					{#each labelLines[i] as line, li}
						<tspan x={cx} y={baseline + 8 + (li + 1) * LABEL_LH}>{line}</tspan>
					{/each}
				</text>
			{/each}
		</svg>
	{/if}
</div>
