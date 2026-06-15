<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import { HorizontalStackedBarChart, categorical8, colorScales } from 'sniic-design-system';
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	// eslint-disable-next-line @typescript-eslint/ban-ts-comment
	// @ts-ignore
	import { hierarchy, treemap as d3treemap } from 'd3-hierarchy';
	import {
		expensesChartData,
		expensesKeys,
		expensesLegendItems,
		expensesGrandTotal,
		fomentoDomainsRows,
		pncvOuOutrosData,
		pncvOuOutrosKeys,
		pncvOuOutrosLabels,
		tipoExecRegiaoData,
		tipoExecRegiaoKeys,
		tipoExecRegiaoLabels,
		pncvNatJuridicaData,
		pncvNatJuridicaKeys,
		pncvNatJuridicaLabels,
		operacionalizacaoSubData,
		modalidadeObrasData,
	} from '$lib/data/section6';

	const formatBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency',
			currency: 'BRL',
			notation: 'compact',
			maximumFractionDigits: 1,
		}).format(v);

	const formatPct = (v: number) =>
		v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

	const pncvOuOutrosColors = [colorScales.teal[2], colorScales.blue[2]] as string[];
	const tipoExecColors = [colorScales.blue[2], colorScales.teal[2], colorScales.orange[2]] as string[];
	const natJuridicaColors = [colorScales.blue[2], colorScales.orange[2]] as string[];

	const TREEMAP_H = 480;
	const TREEMAP_LEG_SEP = 28;
	const TREEMAP_LEG_ROW_H = 44;
	const TREEMAP_SVG_H = TREEMAP_H + TREEMAP_LEG_SEP + fomentoDomainsRows.length * TREEMAP_LEG_ROW_H + 8;

	const domainColorMap = new Map(
		fomentoDomainsRows.map((r, i) => [r.name, categorical8[i % categorical8.length] as string]),
	);
	
	let containerWidth = $state(0);

	const treemapW = $derived((containerWidth - 32) || 728);

	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	type TLeaf = { x0: number; y0: number; x1: number; y1: number; data: typeof fomentoDomainsRows[0] };

	const treemapLeaves = $derived.by((): TLeaf[] => {
		if (!treemapW) return [];
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		const root = (hierarchy as any)({ children: fomentoDomainsRows })
			.sum((d: { value?: number }) => d.value ?? 0)
			.sort((a: { value?: number }, b: { value?: number }) => (b.value ?? 0) - (a.value ?? 0));
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		(d3treemap as any)()
			.size([treemapW, TREEMAP_H])
			.padding(2)
			.paddingOuter(4)(root);
		return root.leaves();
	});

	const CHART_HEIGHT = 520;
	const MARGIN = { top: 16, right: 16, bottom: 16, left: 16 };
	const COLUMN_GAP = 2;
	const INNER_H = CHART_HEIGHT - MARGIN.top - MARGIN.bottom; // 520 - 16 - 16 = 488
	const MIN_LABEL_HEIGHT = 28;

	const LEG_SEP = 20;
	const LEG_HEADER_H = 24;
	const LEG_ROW_H = 44;
	const legY = CHART_HEIGHT + LEG_SEP;
	const totalSvgH = legY + LEG_HEADER_H + expensesLegendItems.length * LEG_ROW_H + 8;

	// Fallback width so the SVG is always non-empty (needed for SVG export before ResizeObserver fires)
	const CHART_W = $derived(containerWidth || 760);

	let wrapperEl: HTMLDivElement | undefined = $state();

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

	const allSegments = $derived.by(() => {
		const innerW = CHART_W - MARGIN.left - MARGIN.right;
		const totalWidth = expensesChartData.reduce((s, d) => s + (d.total as number), 0);
		const gapTotal = Math.max(0, expensesChartData.length - 1) * COLUMN_GAP;
		const availableW = innerW - gapTotal;

		const items: Array<{ key: string; label: string; pct: string; x: number; y: number; w: number; h: number; color: string; showPct: boolean; showLabel: boolean }> = [];
		let cumX = 0;

		for (const datum of expensesChartData) {
			const colW = (datum.total as number) / totalWidth * availableW;
			const segTotal = expensesKeys.reduce((s, k) => s + (Number(datum[k]) || 0), 0);
			let cumY = 0;

			for (let i = 0; i < expensesKeys.length; i++) {
				const key = expensesKeys[i];
				const value = Number(datum[key]) || 0;
				if (value === 0) continue;
				const h = (value / segTotal) * INNER_H;

				const legendItem = expensesLegendItems.find((l) => l.key === key);
				const realValue = legendItem?.valor ?? value;
				const pct = (realValue / expensesGrandTotal * 100).toLocaleString('pt-BR', {
					minimumFractionDigits: 1,
					maximumFractionDigits: 1,
				});
				items.push({
					key,
					label: legendItem?.label ?? key,
					pct,
					x: MARGIN.left + cumX,
					y: MARGIN.top + cumY,
					w: colW,
					h,
					color: categorical8[i] as string,
					showPct: h >= MIN_LABEL_HEIGHT,
					showLabel: h >= 60 && colW >= 150,
				});
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
		<svg
			class="expenses-svg"
			width={CHART_W}
			height={totalSvgH}
			font-family="'Space Grotesk', system-ui, sans-serif"
			font-size="12"
		>
			<!-- chart segment rects + labels -->
			{#each allSegments as seg}
				<rect x={seg.x} y={seg.y} width={seg.w} height={seg.h} fill={seg.color} shape-rendering="crispEdges" />
				{#if seg.showPct}
					<text
						x={seg.x + seg.w / 2}
						y={seg.y + seg.h / 2 + (seg.showLabel ? -8 : 0)}
						text-anchor="middle"
						dominant-baseline="middle"
						fill={contrastColor(seg.color)}
						font-size="14"
						font-weight="700"
						pointer-events="none"
					>{seg.pct}%</text>
				{/if}
				{#if seg.showLabel}
					<text
						x={seg.x + seg.w / 2}
						y={seg.y + seg.h / 2 + 10}
						text-anchor="middle"
						dominant-baseline="middle"
						fill={contrastColor(seg.color)}
						font-size="10"
						pointer-events="none"
					>{seg.label}</text>
				{/if}
			{/each}

			<!-- legend separator -->
			<line x1={0} y1={legY} x2={CHART_W} y2={legY} stroke="var(--chart-fg-muted, #e0e0e0)" />

			<!-- legend column headers -->
			<text x={CHART_W - 150} y={legY + LEG_HEADER_H - 8} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">Valor estimado (IC95%)</text>
			<text x={CHART_W - 4}   y={legY + LEG_HEADER_H - 8} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">% do total</text>

			<!-- legend rows -->
			{#each expensesLegendItems as item, i}
				{@const colorIdx = expensesKeys.indexOf(item.key)}
				{@const color = categorical8[colorIdx] as string}
				{@const ry = legY + LEG_HEADER_H + 16 + i * LEG_ROW_H}
				{@const itemPct = (item.valor / expensesGrandTotal * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}
				{#if i > 0}
					<line x1={0} y1={ry - 6} x2={CHART_W} y2={ry - 6} stroke="var(--chart-fg-muted, #e0e0e0)" />
				{/if}
				<rect x={MARGIN.left} y={ry + 1} width={10} height={10} rx="2" fill={color} />
				<text x={MARGIN.left + 18} y={ry + 6} dy="0.35em" fill="var(--chart-fg, #1a1a1a)">{item.label}</text>
				<text x={CHART_W - 150} y={ry}      dy="0.85em" text-anchor="end" fill="var(--chart-fg-strong, #111)" font-weight="600">{item.value}</text>
				<text x={CHART_W - 150} y={ry + 16} dy="0.85em" text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">{item.ci}</text>
				<text x={CHART_W - 4}   y={ry + 6}  dy="0.35em" text-anchor="end" fill={color} font-size="13" font-weight="700">{itemPct}%</text>
			{/each}
		</svg>
	</div>

	<h3>Operacionalização da Política — Subcategorias</h3>
	<p class="chart-caption">Valor estimado por subcategoria de despesa de Operacionalização da Política, com intervalo de confiança de 95%.</p>

	{@const opRowH = 36}
	{@const opHeaderH = 32}
	{@const opSvgH = opHeaderH + operacionalizacaoSubData.length * opRowH + 4}
	<svg class="data-table-svg" width={CHART_W} height={opSvgH} font-family="'Space Grotesk', system-ui, sans-serif" font-size="12">
		<!-- header -->
		<text x={4} y={20} fill="var(--chart-fg-muted, #666)" font-size="11" font-weight="600">Subcategoria</text>
		<text x={CHART_W - 260} y={20} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="11" font-weight="600">Valor estimado</text>
		<text x={CHART_W - 100} y={20} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="11" font-weight="600">IC 95%</text>
		<text x={CHART_W - 4} y={20} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="11" font-weight="600">% do total</text>
		<line x1={0} y1={opHeaderH - 2} x2={CHART_W} y2={opHeaderH - 2} stroke="var(--chart-fg-muted, #cbd5e1)" stroke-width="2" />

		{#each operacionalizacaoSubData as row, i}
			{@const ry = opHeaderH + i * opRowH + 22}
			{#if i > 0}
				<line x1={0} y1={ry - 16} x2={CHART_W} y2={ry - 16} stroke="var(--chart-fg-muted, #e2e8f0)" />
			{/if}
			<text x={4} y={ry} fill="var(--chart-fg, #1a1a1a)" font-size="12">{row.label}</text>
			<text x={CHART_W - 260} y={ry} text-anchor="end" fill="var(--chart-fg-strong, #111)" font-weight="600">{formatBRL(row.valor)}</text>
			<text x={CHART_W - 100} y={ry} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="11">{formatBRL(row.p025)} – {formatBRL(row.p975)}</text>
			<text x={CHART_W - 4} y={ry} text-anchor="end" fill={colorScales.teal[2]} font-weight="700">{row.pct.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%</text>
		{/each}
	</svg>

	<h3>Obras, Reformas e Aquisição de Bens Culturais — Por Modalidade</h3>
	<p class="chart-caption">Valor estimado por modalidade de Obras, Reformas e Aquisição de Bens Culturais, com intervalo de confiança de 95%.</p>

	{@const obRowH = 36}
	{@const obHeaderH = 32}
	{@const obSvgH = obHeaderH + modalidadeObrasData.length * obRowH + 4}
	<svg class="data-table-svg" width={CHART_W} height={obSvgH} font-family="'Space Grotesk', system-ui, sans-serif" font-size="12">
		<!-- header -->
		<text x={4} y={20} fill="var(--chart-fg-muted, #666)" font-size="11" font-weight="600">Modalidade</text>
		<text x={CHART_W - 400} y={20} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="11" font-weight="600">Valor Estimado</text>
		<text x={CHART_W - 260} y={20} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="11" font-weight="600">% Estimado</text>
		<text x={CHART_W - 4} y={20} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="11" font-weight="600">Intervalo de Confiança</text>
		<line x1={0} y1={obHeaderH - 2} x2={CHART_W} y2={obHeaderH - 2} stroke="var(--chart-fg-muted, #cbd5e1)" stroke-width="2" />

		{#each modalidadeObrasData as row, i}
			{@const ry = obHeaderH + i * obRowH + 22}
			{#if i > 0}
				<line x1={0} y1={ry - 16} x2={CHART_W} y2={ry - 16} stroke="var(--chart-fg-muted, #e2e8f0)" />
			{/if}
			<text x={4} y={ry} fill="var(--chart-fg, #1a1a1a)" font-size="12">{row.label}</text>
			<text x={CHART_W - 400} y={ry} text-anchor="end" fill="var(--chart-fg-strong, #111)" font-weight="600">{formatBRL(row.valor)}</text>
			<text x={CHART_W - 260} y={ry} text-anchor="end" fill={colorScales.teal[2]} font-weight="700">{row.pct.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%</text>
			<text x={CHART_W - 4} y={ry} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="11">IC95% {formatBRL(row.p025)} – {formatBRL(row.p975)}</text>
		{/each}
	</svg>

	<h3>PNCV vs. Outros — Participação por faixa de repasse</h3>
	<p class="chart-caption">Participação percentual do valor estimado entre PNCV e demais despesas, por faixa de repasse municipal.</p>

	<HorizontalStackedBarChartCustom
		data={pncvOuOutrosData}
		keys={[...pncvOuOutrosKeys]}
		labels={pncvOuOutrosLabels}
		colors={pncvOuOutrosColors}
		format={formatPct}
		showTotalLabel={false}
		marginLeft={220}
	/>

	<h3>Distribuição por Modalidade e Natureza Jurídica — PNCV</h3>
	<p class="chart-caption">Participação percentual entre CNPJ e CPF dentro de cada modalidade da Política Nacional de Cultura Viva.</p>

	<div style="padding-left: 220px;">
		<HorizontalStackedBarChart
			data={pncvNatJuridicaData}
			keys={[...pncvNatJuridicaKeys]}
			labels={pncvNatJuridicaLabels}
			colors={natJuridicaColors}
			format={formatPct}
			showTotalLabel={false}
		/>
	</div>

	<h3>Tipo de Execução por Região — Fomento Cultural</h3>
	<p class="chart-caption">Participação percentual do valor estimado por tipo de execução (Ação Cultural, Bolsa e Premiação) em cada região.</p>

	<div style="padding-left: 220px;">
		<HorizontalStackedBarChart
			data={tipoExecRegiaoData}
			keys={[...tipoExecRegiaoKeys]}
			labels={tipoExecRegiaoLabels}
			colors={tipoExecColors}
			format={formatPct}
			showTotalLabel={false}
		/>
	</div>

	<h3>Distribuição por Domínio — Fomento Cultural</h3>
	<p class="chart-caption">Valor estimado investido por domínio cultural no âmbito do Fomento Cultural.</p>

	<svg class="treemap-svg" width={treemapW} height={TREEMAP_SVG_H} font-family="'Space Grotesk', system-ui, sans-serif" font-size="12">
		<defs>
			{#each treemapLeaves as leaf, i}
				{@const cw = leaf.x1 - leaf.x0}
				{@const ch = leaf.y1 - leaf.y0}
				<clipPath id="tm-clip-{i}">
					<rect x={leaf.x0 + 3} y={leaf.y0 + 3} width={Math.max(0, cw - 6)} height={Math.max(0, ch - 6)} />
				</clipPath>
			{/each}
		</defs>

		<!-- treemap cells -->
		{#each treemapLeaves as leaf, i}
			{@const w = leaf.x1 - leaf.x0}
			{@const h = leaf.y1 - leaf.y0}
			{@const cx = leaf.x0 + w / 2}
			{@const cy = leaf.y0 + h / 2}
			{@const color = domainColorMap.get(leaf.data.name) ?? (categorical8[0] as string)}
			{@const showBoth = w >= 90 && h >= 48}
			{@const showPct = w >= 45 && h >= 20}
			<rect x={leaf.x0} y={leaf.y0} width={w} height={h} fill={color} shape-rendering="crispEdges" />
			{#if showPct}
				<text
					x={cx}
					y={showBoth ? cy - 7 : cy}
					text-anchor="middle"
					dominant-baseline="middle"
					fill={contrastColor(color)}
					font-size="12"
					font-weight="700"
					pointer-events="none"
					clip-path="url(#tm-clip-{i})"
				>{leaf.data.pct.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%</text>
				{#if showBoth}
					<text
						x={cx}
						y={cy + 10}
						text-anchor="middle"
						dominant-baseline="middle"
						fill={contrastColor(color)}
						font-size="9"
						pointer-events="none"
						clip-path="url(#tm-clip-{i})"
					>{leaf.data.name}</text>
				{/if}
			{/if}
		{/each}

		<!-- legend separator -->
		<line x1={0} y1={TREEMAP_H + 12} x2={treemapW} y2={TREEMAP_H + 12} stroke="var(--chart-fg-muted, #e0e0e0)" />

		<!-- legend column headers -->
		<text x={treemapW - 150} y={TREEMAP_H + 24} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">Valor estimado (IC95%)</text>
		<text x={treemapW - 4}   y={TREEMAP_H + 24} text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">% do total</text>

		<!-- legend rows -->
		{#each fomentoDomainsRows as row, i}
			{@const ry = TREEMAP_H + TREEMAP_LEG_SEP + 16 + i * TREEMAP_LEG_ROW_H}
			{@const color = categorical8[i % categorical8.length] as string}
			{#if i > 0}
				<line x1={0} y1={ry - 6} x2={treemapW} y2={ry - 6} stroke="var(--chart-fg-muted, #e0e0e0)" />
			{/if}
			<rect x={0} y={ry + 1} width={10} height={10} rx="2" fill={color} />
			<text x={18} y={ry + 6} dy="0.35em" fill="var(--chart-fg, #1a1a1a)">{row.name}</text>
			<text x={treemapW - 150} y={ry}      dy="0.85em" text-anchor="end" fill="var(--chart-fg-strong, #111)" font-weight="600">{formatBRL(row.value)}</text>
			<text x={treemapW - 150} y={ry + 16} dy="0.85em" text-anchor="end" fill="var(--chart-fg-muted, #666)" font-size="10">IC95%: {formatBRL(row.p025)} – {formatBRL(row.p975)}</text>
			<text x={treemapW - 4}   y={ry + 6}  dy="0.35em" text-anchor="end" fill={color} font-size="13" font-weight="700">{row.pct.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%</text>
		{/each}
	</svg>
</ScrollSection>


<style>
	h3 {
		font-family: 'Space Grotesk', system-ui, sans-serif;
		font-size: 1rem;
		font-weight: 600;
		margin: 2rem 0 0.25rem;
	}

	.chart-caption {
		font-family: 'Space Grotesk', system-ui, sans-serif;
		font-size: 0.8rem;
		color: var(--chart-fg-muted, #666);
		margin: 0 0 1rem;
	}

	.treemap-svg {
		display: block;
		margin: 0 16px;
	}

	.chart-wrapper {
		position: relative;
		width: 100%;
	}

	.expenses-svg {
		display: block;
	}

	.data-table-svg {
		display: block;
		margin: 0 0 1.5rem;
	}

</style>
