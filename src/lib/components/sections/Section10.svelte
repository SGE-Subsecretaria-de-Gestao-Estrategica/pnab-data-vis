<script lang="ts">
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import { categorical8, colorPairs } from 'sniic-design-system';
	// @ts-ignore — d3-hierarchy types resolved via design-system deps
	import { hierarchy, treemap as d3treemap } from 'd3-hierarchy';
	import {
		expensesLegendItems,
		expensesGrandTotal,
		fomentoDomainsRows,
		fomentoSubData,
		pncvSubData,
		tipoExecRegiaoData,
		tipoExecRegiaoKeys,
		tipoExecRegiaoLabels,
		pncvOuOutrosData,
		pncvOuOutrosKeys,
		pncvOuOutrosLabels,
		pncvNatJuridicaData,
		pncvNatJuridicaKeys,
		pncvNatJuridicaLabels,
		modalidadeObrasData,
		operacionalizacaoSubData,
	} from '$lib/data/section6';

	// ── Formatters ────────────────────────────────────────────────────────────
	const formatBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency', currency: 'BRL',
			notation: 'compact', maximumFractionDigits: 1,
		}).format(v);
	const fmtPct = (v: number) =>
		v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

	// ── Table row arrays ──────────────────────────────────────────────────────
	interface TableRow { label: string; valor: string; pct: string; ic: string }

	const categoriasRows: TableRow[] = expensesLegendItems.map((d) => ({
		label: d.label,
		valor: d.value,
		pct: fmtPct((d.valor / expensesGrandTotal) * 100),
		ic: d.ci,
	}));

	const toDetailRow = (d: { label: string; valor: number; pct: number; p025: number; p975: number }): TableRow => ({
		label: d.label,
		valor: formatBRL(d.valor),
		pct: fmtPct(d.pct),
		ic: `${formatBRL(d.p025)} – ${formatBRL(d.p975)}`,
	});

	const fomentoDetailRows = fomentoSubData.map(toDetailRow);
	const culturaVivaDetailRows = pncvSubData.map(toDetailRow);
	const obrasRows = modalidadeObrasData.map(toDetailRow);
	const operacRows = operacionalizacaoSubData.map(toDetailRow);

	// ── Treemap — Domínios de Fomento Cultural ────────────────────────────────
	const TW = 728;
	const TREEMAP_H = 480;
	const LEG_SEP = 28;
	const LEG_ROW_H = 44;
	const TOTAL_H = TREEMAP_H + LEG_SEP + fomentoDomainsRows.length * LEG_ROW_H + 8;
	const LEG_VAL_X = TW - 150;
	const LEG_PCT_X = TW - 4;

	const palette15 = [
		...categorical8,
		'#7ba0d4', '#f0956b', '#62a898', '#f9d878', '#c280a5', '#a8c860', '#de7872',
	];
	const domainColorMap = new Map(fomentoDomainsRows.map((r, i) => [r.name, palette15[i]]));

	function contrastColor(hex: string) {
		const r = parseInt(hex.slice(1, 3), 16);
		const g = parseInt(hex.slice(3, 5), 16);
		const b = parseInt(hex.slice(5, 7), 16);
		return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.55 ? '#1a1a1a' : '#ffffff';
	}

	const tmRoot = hierarchy({ children: fomentoDomainsRows })
		.sum((d: { value?: number }) => d.value ?? 0)
		.sort((a: { value?: number }, b: { value?: number }) => (b.value ?? 0) - (a.value ?? 0));
	d3treemap().size([TW, TREEMAP_H]).padding(2).paddingOuter(4)(tmRoot);
	const tmLeaves = tmRoot.leaves() as Array<{
		x0: number; x1: number; y0: number; y1: number;
		data: { name: string; value: number; pct: number };
	}>;
</script>

{#snippet dataTable(rows: TableRow[])}
	<div class="table-wrap">
		<table>
			<thead>
				<tr>
					<th class="t-label">Categoria</th>
					<th class="t-num">Valor estimado</th>
					<th class="t-num">% do total</th>
					<th class="t-ic">IC 95%</th>
				</tr>
			</thead>
			<tbody>
				{#each rows as row}
					<tr>
						<td class="t-label">{row.label}</td>
						<td class="t-num t-strong">{row.valor}</td>
						<td class="t-num t-pct">{row.pct}</td>
						<td class="t-ic">{row.ic}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/snippet}

<section class="section">
	<header class="sec-header">
		<p class="eyebrow">Capítulo 6</p>
		<h2>Distribuição de recursos por tipo de despesa</h2>
		<p class="lead">
			Para onde foram os <strong>{formatBRL(expensesGrandTotal)}</strong> executados pela Aldir
			Blanc. Três categorias — Fomento Cultural, Política Nacional de Cultura Viva e Subsídio —
			concentram a maior parte do investimento.
		</p>
	</header>

	<!-- 1 · Tabela de categorias de despesa -->
	<div class="block">
		<h3 class="block-title">Categorias de despesa</h3>
		{@render dataTable(categoriasRows)}
	</div>

	<!-- 2 · Treemap de domínios de Fomento Cultural -->
	<div class="block">
		<h3 class="block-title">Domínios de Fomento Cultural</h3>
		<div class="chart-card">
			<svg
				viewBox={`0 0 ${TW} ${TOTAL_H}`}
				width="100%"
				font-family="'Rawline', system-ui, sans-serif"
				font-size="12"
				style="display:block"
				role="img"
				aria-label="Treemap dos domínios de Fomento Cultural"
			>
				<defs>
					{#each tmLeaves as leaf, i}
						{@const cw = leaf.x1 - leaf.x0}
						{@const ch = leaf.y1 - leaf.y0}
						<clipPath id="s10-tm-{i}">
							<rect x={leaf.x0 + 3} y={leaf.y0 + 3} width={Math.max(0, cw - 6)} height={Math.max(0, ch - 6)} />
						</clipPath>
					{/each}
				</defs>

				{#each tmLeaves as leaf, i}
					{@const w = leaf.x1 - leaf.x0}
					{@const h = leaf.y1 - leaf.y0}
					{@const cx = leaf.x0 + w / 2}
					{@const cy = leaf.y0 + h / 2}
					{@const color = domainColorMap.get(leaf.data.name) ?? categorical8[0]}
					{@const showBoth = w >= 90 && h >= 48}
					{@const isSmall = w < 45 || h < 20}
					<rect x={leaf.x0} y={leaf.y0} width={w} height={h} fill={color} shape-rendering="crispEdges" />
					<text
						x={cx} y={showBoth ? cy - 7 : cy}
						text-anchor="middle" dominant-baseline="middle"
						fill={contrastColor(color)} font-size={isSmall ? 8 : 12} font-weight="700"
						pointer-events="none" clip-path={isSmall ? undefined : `url(#s10-tm-${i})`}
					>{fmtPct(leaf.data.pct)}</text>
					{#if showBoth}
						<text
							x={cx} y={cy + 10}
							text-anchor="middle" dominant-baseline="middle"
							fill={contrastColor(color)} font-size="9"
							pointer-events="none" clip-path="url(#s10-tm-{i})"
						>{leaf.data.name}</text>
					{/if}
				{/each}

				<line x1={0} y1={TREEMAP_H + 12} x2={TW} y2={TREEMAP_H + 12} stroke="#e0e0e0" />
				<text x={LEG_VAL_X} y={TREEMAP_H + 24} text-anchor="end" fill="#666" font-size="10">Valor estimado (IC95%)</text>
				<text x={LEG_PCT_X} y={TREEMAP_H + 24} text-anchor="end" fill="#666" font-size="10">% do total</text>

				{#each fomentoDomainsRows as row, i}
					{@const ry = TREEMAP_H + LEG_SEP + 16 + i * LEG_ROW_H}
					{@const color = palette15[i]}
					{#if i > 0}
						<line x1={0} y1={ry - 6} x2={TW} y2={ry - 6} stroke="#e0e0e0" />
					{/if}
					<rect x={0} y={ry + 1} width={10} height={10} rx="2" fill={color} />
					<text x={18} y={ry + 6} dy="0.35em" fill="#1a1a1a">{row.name}</text>
					<text x={LEG_VAL_X} y={ry} dy="0.85em" text-anchor="end" fill="#111" font-weight="600">{formatBRL(row.value)}</text>
					<text x={LEG_VAL_X} y={ry + 16} dy="0.85em" text-anchor="end" fill="#666" font-size="10">IC95%: {formatBRL(row.p025)} – {formatBRL(row.p975)}</text>
					<text x={LEG_PCT_X} y={ry + 6} dy="0.35em" text-anchor="end" fill={color} font-size="13" font-weight="700">{fmtPct(row.pct)}</text>
				{/each}
			</svg>
		</div>
	</div>

	<!-- 3 · Detalhamento por categoria -->
	<div class="block">
		<h3 class="block-title">Detalhamento — Fomento Cultural</h3>
		{@render dataTable(fomentoDetailRows)}
	</div>
	<div class="block">
		<h3 class="block-title">Detalhamento — Política Nacional de Cultura Viva</h3>
		{@render dataTable(culturaVivaDetailRows)}
	</div>

	<!-- 4 · Tipo de execução por região -->
	<div class="block">
		<h3 class="block-title">Tipo de execução por região — Fomento Cultural</h3>
		<div class="chart-card">
			<HorizontalStackedBarChartCustom
				data={tipoExecRegiaoData}
				keys={[...tipoExecRegiaoKeys]}
				labels={tipoExecRegiaoLabels}
				colors={categorical8.slice(0, 3)}
				format={fmtPct}
				marginLeft={120}
				legendAlign="left"
			/>
		</div>
	</div>

	<!-- 5 · PNCV vs outros investimentos -->
	<div class="block">
		<h3 class="block-title">PNCV vs. outros investimentos — por faixa de repasse municipal</h3>
		<div class="chart-card">
			<HorizontalStackedBarChartCustom
				data={pncvOuOutrosData}
				keys={[...pncvOuOutrosKeys]}
				labels={pncvOuOutrosLabels}
				colors={[...colorPairs.bluePurple]}
				format={fmtPct}
				marginLeft={280}
				legendAlign="left"
			/>
		</div>
	</div>

	<!-- 6 · PNCV por natureza do beneficiário -->
	<div class="block">
		<h3 class="block-title">PNCV por natureza do beneficiário (CNPJ vs. CPF)</h3>
		<div class="chart-card">
			<HorizontalStackedBarChartCustom
				data={pncvNatJuridicaData}
				keys={[...pncvNatJuridicaKeys]}
				labels={pncvNatJuridicaLabels}
				colors={[...colorPairs.bluePurple]}
				format={fmtPct}
				marginLeft={120}
				legendAlign="left"
			/>
		</div>
	</div>

	<!-- 7 · Obras e operacionalização -->
	<div class="block">
		<h3 class="block-title">Obras, Reformas e Aquisição de Bens Culturais</h3>
		{@render dataTable(obrasRows)}
	</div>
	<div class="block">
		<h3 class="block-title">Operacionalização da Política</h3>
		{@render dataTable(operacRows)}
	</div>
</section>

<style>
	.section {
		max-width: 1200px;
		margin: 0 auto;
		padding: 1rem 2rem 5rem;
	}

	.sec-header {
		margin-bottom: 1.5rem;
	}

	.eyebrow {
		font-size: 0.72rem;
		font-weight: 700;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: #1351b4;
		margin: 0 0 0.4rem;
	}

	.sec-header h2 {
		font-size: 1.6rem;
		font-weight: 800;
		color: #1b1b1b;
		margin: 0 0 0.4rem;
		line-height: 1.15;
	}

	.lead {
		font-size: 0.98rem;
		color: #555;
		margin: 0;
		line-height: 1.5;
		max-width: 70ch;
	}

	.block {
		margin-top: 2.25rem;
	}

	.block-title {
		margin: 0 0 0.75rem;
		font-size: 1.05rem;
		font-weight: 700;
		color: #1b1b1b;
	}

	.chart-card {
		border: 1px solid rgba(0, 0, 0, 0.1);
		border-radius: 0.75rem;
		padding: 1.25rem 1.5rem 1rem;
		background: rgba(255, 255, 255, 0.45);
	}

	/* ── Tables ── */
	.table-wrap {
		border: 1px solid rgba(0, 0, 0, 0.1);
		border-radius: 0.75rem;
		overflow: hidden;
		background: rgba(255, 255, 255, 0.45);
	}

	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9rem;
	}

	thead th {
		text-align: left;
		font-size: 0.72rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		color: #666;
		padding: 0.7rem 0.9rem;
		border-bottom: 2px solid #cbd5e1;
		background: rgba(0, 0, 0, 0.015);
	}

	tbody td {
		padding: 0.65rem 0.9rem;
		border-top: 1px solid #e2e8f0;
		color: #1a1a1a;
		vertical-align: baseline;
	}

	tbody tr:first-child td {
		border-top: none;
	}

	.t-num {
		text-align: right;
		font-variant-numeric: tabular-nums;
		white-space: nowrap;
	}

	.t-strong {
		font-weight: 600;
		color: #111;
	}

	.t-pct {
		font-weight: 700;
		color: #1351b4;
	}

	.t-ic {
		text-align: right;
		color: #666;
		font-size: 0.8rem;
		white-space: nowrap;
	}

	.t-label {
		text-align: left;
	}

	@media (max-width: 720px) {
		.sec-header h2 { font-size: 1.4rem; }
		.t-ic { display: none; }
		thead th.t-ic { display: none; }
	}
</style>
