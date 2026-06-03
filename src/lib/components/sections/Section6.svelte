<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import { MarimekkoChart, categorical8 } from 'sniic-design-system';
	import {
		expensesChartData,
		expensesKeys,
		expensesLabels,
		expensesLegendItems,
		expensesGrandTotal,
	} from '$lib/data/section6';

	const formatBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency',
			currency: 'BRL',
			notation: 'compact',
			maximumFractionDigits: 1,
		}).format(v);

	const CHART_HEIGHT = 520;
	const MARGIN = { top: 16, right: 16, bottom: 16, left: 16 };
	const COLUMN_GAP = 2;
	const INNER_H = CHART_HEIGHT - MARGIN.top - MARGIN.bottom; // 520 - 16 - 16 = 488
	const MIN_LABEL_HEIGHT = 28;

	let wrapperEl: HTMLDivElement | undefined = $state();
	let containerWidth = $state(0);

	$effect(() => {
		if (!wrapperEl) return;
		containerWidth = wrapperEl.offsetWidth;
		const ro = new ResizeObserver(([e]) => { containerWidth = e.contentRect.width; });
		ro.observe(wrapperEl);
		return () => ro.disconnect();
	});

	function contrastColor(hex: string): string {
		const r = parseInt(hex.slice(1, 3), 16);
		const g = parseInt(hex.slice(3, 5), 16);
		const b = parseInt(hex.slice(5, 7), 16);
		return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.55 ? '#1a1a1a' : '#ffffff';
	}

	const overlayItems = $derived.by(() => {
		if (!containerWidth) return [];
		const innerW = containerWidth - MARGIN.left - MARGIN.right;
		const totalWidth = expensesChartData.reduce((s, d) => s + (d.total as number), 0); // sum of column totals = grand total
		const gapTotal = Math.max(0, expensesChartData.length - 1) * COLUMN_GAP;
		const availableW = innerW - gapTotal;

		const items: Array<{ label: string; pct: string; x: number; y: number; w: number; h: number; color: string; showLabel: boolean }> = [];
		let cumX = 0;

		for (const datum of expensesChartData) {
			const colW = (datum.total as number) / totalWidth * availableW;
			const segTotal = expensesKeys.reduce((s, k) => s + (Number(datum[k]) || 0), 0);
			let cumY = 0;

			for (let i = 0; i < expensesKeys.length; i++) {
				const key = expensesKeys[i];
				const value = Number(datum[key]) || 0;
				if (value === 0) { continue; }
				const h = (value / segTotal) * INNER_H;

				if (h >= MIN_LABEL_HEIGHT) {
					const legendItem = expensesLegendItems.find((l) => l.key === key);
					const realValue = legendItem?.valor ?? value;
					const pct = (realValue / expensesGrandTotal * 100).toLocaleString('pt-BR', {
						minimumFractionDigits: 1,
						maximumFractionDigits: 1,
					});
					const showLabel = h >= 60 && colW >= 150;
					items.push({
						label: legendItem?.label ?? key,
						pct,
						x: MARGIN.left + cumX,
						y: MARGIN.top + cumY,
						w: colW,
						h,
						color: categorical8[i] as string,
						showLabel,
					});
				}
				cumY += h;
			}
			cumX += colW + COLUMN_GAP;
		}
		return items;
	});
</script>

<ScrollSection id="section-6">
	<h2>6. Como os recursos foram distribuídos por tipo de despesa?</h2>

	<div class="chart-wrapper" bind:this={wrapperEl}>
		<!-- clip the built-in SVG legend bar that overflows below the chart -->
		<div style="overflow:hidden;height:{CHART_HEIGHT}px">
			<MarimekkoChart
				data={expensesChartData}
				keys={expensesKeys}
				labels={expensesLabels}
				height={CHART_HEIGHT}
				format={formatBRL}
				margin={MARGIN}
				pctFormat={() => ''}
			/>
		</div>

		<!-- category name overlay -->
		{#each overlayItems as item}
			<div
				class="seg-label"
				style="left:{item.x}px;top:{item.y}px;width:{item.w}px;height:{item.h}px"
			>
				<span class="seg-label-text" style="color:{contrastColor(item.color)}">
				<strong>{item.pct}%</strong>
				{#if item.showLabel}<br>{item.label}{/if}
			</span>
			</div>
		{/each}

		<table class="ref-table">
		<tbody>
			{#each expensesLegendItems as item}
				{@const colorIdx = expensesKeys.indexOf(item.key)}
				<tr>
					<td class="swatch-cell">
						<span class="swatch" style="background:{categorical8[colorIdx]}"></span>
					</td>
					<td class="label-cell">{item.label}</td>
					<td class="value-cell">
						{item.value}
						<span class="ci">({item.ci})</span>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
	</div>
</ScrollSection>


<style>
	.chart-wrapper {
		position: relative;
		width: 100%;
	}

	.seg-label {
		position: absolute;
		pointer-events: none;
		overflow: hidden;
	}

	.seg-label-text {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		left: 0;
		right: 0;
		text-align: center;
		font-family: 'Space Grotesk', system-ui, sans-serif;
		font-size: 0.72rem;
		font-weight: 400;
		line-height: 1.4;
		padding: 0 8px;
	}

	.seg-label-text strong {
		display: block;
		font-size: 0.9rem;
		font-weight: 700;
	}

	.ref-table {
		width: calc(100% - 32px);
		border-collapse: collapse;
		margin: 0.75rem 16px 0;
		font-family: 'Space Grotesk', system-ui, sans-serif;
		font-size: 0.8rem;
	}

	.ref-table tr + tr td {
		border-top: 1px solid var(--chart-fg-muted, #e0e0e0);
	}

	.swatch-cell {
		width: 20px;
		padding: 0.35rem 0.5rem 0.35rem 0;
		vertical-align: middle;
	}

	.swatch {
		display: inline-block;
		width: 12px;
		height: 12px;
		border-radius: 2px;
	}

	.label-cell {
		padding: 0.35rem 1rem 0.35rem 0;
	}

	.value-cell {
		padding: 0.35rem 0;
		font-weight: 600;
		text-align: right;
	}

	.ci {
		display: block;
		font-weight: 400;
		font-size: 0.7rem;
		color: var(--chart-fg-muted, #666);
		white-space: nowrap;
	}
</style>
