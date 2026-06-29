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

	// ── Treemap — Domínios de Fomento Cultural (responsivo ao container) ───────
	// Renderiza 1:1 (1 unidade do viewBox = 1px da tela), então os rótulos ficam
	// legíveis em qualquer largura; no mobile o layout fica mais alto (retrato)
	// para os 15 domínios não achatarem.
	let tmWidth = $state(0);
	const tmIsMobile = $derived(tmWidth > 0 && tmWidth < 560);
	const TW = $derived(Math.max(1, tmWidth));
	const TREEMAP_H = $derived(tmIsMobile ? TW * 1.5 : TW * 0.66);

	const palette15 = [
		...categorical8,
		'#7ba0d4', '#f0956b', '#62a898', '#f9d878', '#c280a5', '#a8c860', '#de7872',
	];
	const domainColorMap = new Map(fomentoDomainsRows.map((r, i) => [r.name, palette15[i]]));

	interface LegendRow extends TableRow { color: string }
	const fomentoLegendRows: LegendRow[] = fomentoDomainsRows.map((r, i) => ({
		color: palette15[i],
		label: r.name,
		valor: formatBRL(r.value),
		pct: fmtPct(r.pct),
		ic: `${formatBRL(r.p025)} – ${formatBRL(r.p975)}`,
	}));

	function contrastColor(hex: string) {
		const r = parseInt(hex.slice(1, 3), 16);
		const g = parseInt(hex.slice(3, 5), 16);
		const b = parseInt(hex.slice(5, 7), 16);
		return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.55 ? '#1a1a1a' : '#ffffff';
	}

	type TmLeaf = {
		x0: number; x1: number; y0: number; y1: number;
		data: { name: string; value: number; pct: number };
	};
	const tmLeaves = $derived.by(() => {
		const root = hierarchy({ children: fomentoDomainsRows })
			.sum((d: { value?: number }) => d.value ?? 0)
			.sort((a: { value?: number }, b: { value?: number }) => (b.value ?? 0) - (a.value ?? 0));
		d3treemap().size([TW, TREEMAP_H]).padding(2).paddingOuter(4)(root);
		return root.leaves() as TmLeaf[];
	});
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

{#snippet legendTable(rows: LegendRow[])}
	<div class="table-wrap">
		<table>
			<thead>
				<tr>
					<th class="t-label">Domínio</th>
					<th class="t-num">Valor estimado</th>
					<th class="t-num">% do total</th>
					<th class="t-ic">IC 95%</th>
				</tr>
			</thead>
			<tbody>
				{#each rows as row}
					<tr>
						<td class="t-label">
							<span class="swatch" style="background:{row.color}"></span>{row.label}
						</td>
						<td class="t-num t-strong">{row.valor}</td>
						<td class="t-num t-pct">{row.pct}</td>
						<td class="t-ic">{row.ic}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/snippet}

<!-- Abertura da Seção 3 (ações apoiadas): título em "big number" sobre o teal,
     espelhando as heros das seções 1 e 2. -->
<section class="hero-band">
	<h1>QUAIS AÇÕES CULTURAIS FORAM APOIADAS COM OS RECURSOS DA ALDIR BLANC?</h1>
</section>

<section class="section-band">
	<div class="section">
	<header class="sec-header">
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
		<div class="chart-card chart-card--frame">
			<div class="tm-wrap" bind:clientWidth={tmWidth}>
			{#if tmWidth > 0}
			<svg
				viewBox={`0 0 ${TW} ${TREEMAP_H}`}
				width="100%"
				font-family="'Rawline', system-ui, sans-serif"
				font-size="14"
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
					{@const showBoth = w >= 90 && h >= 54}
					{@const isSmall = w < 45 || h < 22}
					<rect x={leaf.x0} y={leaf.y0} width={w} height={h} fill={color} shape-rendering="crispEdges" />
					<text
						x={cx} y={showBoth ? cy - 9 : cy}
						text-anchor="middle" dominant-baseline="middle"
						fill={contrastColor(color)} font-size={isSmall ? 11 : 17} font-weight="700"
						pointer-events="none" clip-path={isSmall ? undefined : `url(#s10-tm-${i})`}
					>{fmtPct(leaf.data.pct)}</text>
					{#if showBoth}
						<text
							x={cx} y={cy + 13}
							text-anchor="middle" dominant-baseline="middle"
							fill={contrastColor(color)} font-size="12"
							pointer-events="none" clip-path="url(#s10-tm-{i})"
						>{leaf.data.name}</text>
					{/if}
				{/each}
			</svg>
			{/if}
			</div>
		</div>
		<div class="treemap-legend">
			{@render legendTable(fomentoLegendRows)}
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
				colors={[categorical8[4], categorical8[1], categorical8[3]]}
				format={fmtPct}
				marginLeft={120}
				legendAlign="left"
				axisColor="#000000"
			/>
		</div>
	</div>

	<!-- 5 · PNCV vs outros investimentos -->
	<div class="block block--yellow">
		<div class="block-inner">
			<h3 class="block-title">PNCV vs. outros investimentos — por faixa de repasse municipal</h3>
			<div class="chart-card">
				<HorizontalStackedBarChartCustom
					data={pncvOuOutrosData}
					keys={[...pncvOuOutrosKeys]}
					labels={pncvOuOutrosLabels}
					colors={[...colorPairs.purpleYellow].reverse()}
					format={fmtPct}
					marginLeft={280}
					legendAlign="left"
					axisColor="#000000"
				/>
			</div>
		</div>
	</div>

	<!-- 6 · PNCV por natureza do beneficiário -->
	<div class="block block--yellow">
		<div class="block-inner">
			<h3 class="block-title">PNCV por natureza do beneficiário (CNPJ vs. CPF)</h3>
			<div class="chart-card">
				<HorizontalStackedBarChartCustom
					data={pncvNatJuridicaData}
					keys={[...pncvNatJuridicaKeys]}
					labels={pncvNatJuridicaLabels}
					colors={[...colorPairs.purpleYellow].reverse()}
					format={fmtPct}
					marginLeft={120}
					legendAlign="left"
					axisColor="#000000"
				/>
			</div>
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
	</div>
</section>

<style>
	/* Hero full-bleed teal: abre a Seção 3 com o título em "big number"
	   (preenchimento branco + sombra 3D preta), igual às heros anteriores. */
	.hero-band {
		min-height: 40vh;
		min-height: 40svh;
		display: flex;
		align-items: center;
		padding: 2rem 0;
		box-sizing: border-box;
		background: #773561;
	}

	.hero-band h1 {
		width: 100%;
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 2rem;
		box-sizing: border-box;
		font-size: clamp(1.6rem, 4vw, 3rem);
		font-weight: 800;
		line-height: 1.25;
		letter-spacing: -0.02em;
		text-align: left;
		/* Estilo "big number": preenchimento branco + sombra 3D preta extrudada,
		   replicando o contorno + degraus diagonais do componente BigNumber. */
		color: #ffffff;
		text-shadow:
			-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000,
			0 -2px 0 #000, 0 2px 0 #000, -2px 0 0 #000, 2px 0 0 #000,
			1px 1px 0 #000, 2px 2px 0 #000, 3px 3px 0 #000, 4px 4px 0 #000,
			5px 5px 0 #000, 6px 6px 0 #000, 7px 7px 0 #000, 8px 8px 0 #000;
	}

	/* Seção 3 inteira sobre o teal (full-bleed). */
	.section-band {
	}

	.section {
		max-width: 1200px;
		margin: 0 auto;
		padding: 4rem 2rem 5rem;
	}

	.sec-header {
		margin-bottom: 1.5rem;
	}

	.sec-header h2 {
		font-size: 1.6rem;
		font-weight: 800;
		color: #1B1B1B;
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

	/* Blocos amarelos consecutivos se tocam (sem espaço entre eles). */
	.block--yellow + .block--yellow {
		margin-top: 0;
	}

	.block--yellow {
		background: transparent;
		/* Full-bleed: escapa do container central de 1200px e ocupa toda a largura. */
		width: 100vw;
		position: relative;
		left: 50%;
		margin-left: -50vw;
		padding: 2.5rem 0;
	}

	.block--yellow .block-inner {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 2rem;
	}

	.block-title {
		margin: 0 0 0.75rem;
		font-size: 1.05rem;
		font-weight: 700;
		color: #1B1B1B;
	}

	.chart-card {
		border-radius: 0;
		padding: 1.25rem 1.5rem 1rem;
	}

	/* Treemap é colorido e sem borda: uma moldura branca (card + padding) o separa
	   do teal e evita o look "esquisito" de blocos coloridos colados ao fundo. */
	.chart-card--frame {
		background: #ffffff;
		padding: 1.25rem;
	}

	.tm-wrap {
		width: 100%;
	}

	/* ── Tables ── */
	.table-wrap {
		border: 1px solid rgba(0, 0, 0, 0.1);
		border-radius: 0;
		/* Scroll horizontal interno: no mobile, em vez de cortar/esconder colunas,
		   a tabela rola lateralmente mantendo todas as colunas visíveis. */
		overflow-x: auto;
		-webkit-overflow-scrolling: touch;
		/* Tabelas em card branco sólido para legibilidade sobre o teal. */
		background: #ffffff;
	}

	table {
		width: 100%;
		/* Largura mínima para que as colunas não fiquem espremidas; abaixo dela
		   o .table-wrap exibe scroll horizontal. */
		min-width: 32rem;
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

	.treemap-legend {
		margin-top: 0.75rem;
	}

	.swatch {
		display: inline-block;
		width: 0.7rem;
		height: 0.7rem;
		border-radius: 0;
		margin-right: 0.55rem;
		vertical-align: -0.05rem;
		flex: none;
	}

	@media (max-width: 720px) {
		.sec-header h2 { font-size: 1.4rem; }
		.hero-band h1 { padding: 0 1rem; }
	}
</style>
