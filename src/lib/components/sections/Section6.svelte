<script lang="ts">
	import { categorical8 } from 'sniic-design-system';
	// @ts-ignore — d3-hierarchy ships its own types via the design system deps
	import { hierarchy, treemap as d3treemap } from 'd3-hierarchy';
	import { porteRaw, porteTreemapData } from '$lib/data/section1';

	// ── Fixed porte color palette (mesma usada nos demais gráficos de porte) ──────
	const PORTE_NAME_COLORS: Record<string, string> = {
		Grande: categorical8[0], // azul
		Médio: categorical8[4], // roxo
		'Pequeno I': categorical8[1], // laranja
		'Pequeno II': categorical8[2], // verde
	};

	const formatBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency',
			currency: 'BRL',
			notation: 'compact',
			maximumFractionDigits: 1,
		}).format(v);

	const formatPct = (v: number) =>
		`${v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;

	function contrastColor(hex: string) {
		const r = parseInt(hex.slice(1, 3), 16);
		const g = parseInt(hex.slice(3, 5), 16);
		const b = parseInt(hex.slice(5, 7), 16);
		return (0.299 * r + 0.587 * g + 0.114 * b) / 255 > 0.55 ? '#1a1a1a' : '#ffffff';
	}

	// ── Treemap layout — responsivo ao container ─────────────────────────────────
	// O SVG renderiza 1:1 (1 unidade do viewBox = 1px da tela), então os rótulos
	// usam tamanhos em px legíveis em qualquer largura. No mobile o layout fica
	// mais alto (retrato) para os blocos não achatarem e caberem os rótulos.
	let measuredWidth = $state(0);
	const isMobile = $derived(measuredWidth > 0 && measuredWidth < 560);
	const TM_W = $derived(Math.max(1, measuredWidth));
	const TM_H = $derived(isMobile ? TM_W * 1.25 : TM_W * 0.5);

	type Leaf = {
		x0: number; x1: number; y0: number; y1: number;
		data: { name: string; value: number };
	};
	const leaves = $derived.by(() => {
		const root = hierarchy({ children: porteTreemapData.children })
			.sum((d: { value?: number }) => d.value ?? 0)
			.sort((a: { value?: number }, b: { value?: number }) => (b.value ?? 0) - (a.value ?? 0));
		d3treemap().size([TM_W, TM_H]).padding(3).paddingOuter(4)(root);
		return root.leaves() as Leaf[];
	});

	const colorOf = (name: string) => PORTE_NAME_COLORS[name] ?? categorical8[0];

	// ── Legenda / dados auxiliares ────────────────────────────────────────────────
	const porteByName = new Map(porteRaw.map((d) => [d.porte, d]));
	const legendRows = $derived(
		leaves.map((l) => {
			const raw = porteByName.get(l.data.name);
			return {
				name: l.data.name,
				color: colorOf(l.data.name),
				value: raw?.valor_total ?? l.data.value,
				perc: raw?.perc_valor ?? 0,
				municipios: raw?.municipios ?? 0,
			};
		})
	);

	// Destaques para o texto introdutório (derivados dos dados, sem hard-code).
	const maior = [...porteRaw].sort((a, b) => b.perc_valor - a.perc_valor)[0];
	const pequenoI = porteByName.get('Pequeno I');
</script>

<section class="section">
	<header class="sec-header">
		<h3>Distribuição do recurso por porte municipal</h3>
		<p class="lead">
			Participação de cada porte populacional municipal no valor total executado por municípios.
		</p>
	</header>

	<div class="chart-card">
		<div class="tm-wrap" bind:clientWidth={measuredWidth}>
		{#if measuredWidth > 0}
		<svg
			viewBox={`0 0 ${TM_W} ${TM_H}`}
			width="100%"
			font-family="'Rawline', system-ui, sans-serif"
			style="display:block"
			role="img"
			aria-label="Treemap do valor executado por porte municipal"
		>
			<defs>
				{#each leaves as leaf, i}
					{@const cw = leaf.x1 - leaf.x0}
					{@const ch = leaf.y1 - leaf.y0}
					<clipPath id="s6-clip-{i}">
						<rect
							x={leaf.x0 + 3}
							y={leaf.y0 + 3}
							width={Math.max(0, cw - 6)}
							height={Math.max(0, ch - 6)}
						/>
					</clipPath>
				{/each}
			</defs>

			{#each leaves as leaf, i}
				{@const w = leaf.x1 - leaf.x0}
				{@const h = leaf.y1 - leaf.y0}
				{@const cx = leaf.x0 + w / 2}
				{@const cy = leaf.y0 + h / 2}
				{@const color = colorOf(leaf.data.name)}
				{@const raw = porteByName.get(leaf.data.name)}
				{@const showBoth = w >= 90 && h >= 56}
				{@const showVal = w >= 48 && h >= 24}
				<rect x={leaf.x0} y={leaf.y0} width={w} height={h} fill={color} shape-rendering="crispEdges" />
				{#if showBoth}
					<text
						x={cx}
						y={cy - 16}
						text-anchor="middle"
						dominant-baseline="middle"
						fill={contrastColor(color)}
						font-size="15"
						font-weight="700"
						pointer-events="none"
						clip-path="url(#s6-clip-{i})">{leaf.data.name}</text
					>
					<text
						x={cx}
						y={cy + 5}
						text-anchor="middle"
						dominant-baseline="middle"
						fill={contrastColor(color)}
						font-size="13"
						pointer-events="none"
						clip-path="url(#s6-clip-{i})">{formatBRL(leaf.data.value)}</text
					>
					{#if raw}
						<text
							x={cx}
							y={cy + 23}
							text-anchor="middle"
							dominant-baseline="middle"
							fill={contrastColor(color)}
							font-size="12"
							font-weight="700"
							pointer-events="none"
							clip-path="url(#s6-clip-{i})">{formatPct(raw.perc_valor)}</text
						>
					{/if}
				{:else if showVal}
					<text
						x={cx}
						y={cy}
						text-anchor="middle"
						dominant-baseline="middle"
						fill={contrastColor(color)}
						font-size="11"
						font-weight="700"
						pointer-events="none">{raw ? formatPct(raw.perc_valor) : ''}</text
					>
				{/if}
			{/each}
		</svg>
		{/if}
		</div>

		<ul class="legend">
			{#each legendRows as item}
				<li>
					<span class="swatch" style:background={item.color}></span>
					<span class="leg-name">{item.name}</span>
					<span class="leg-mun">{item.municipios.toLocaleString('pt-BR')} mun.</span>
					<span class="leg-val">{formatBRL(item.value)}</span>
					<span class="leg-pct" style:color={item.color}>{formatPct(item.perc)}</span>
				</li>
			{/each}
		</ul>
	</div>
</section>

<style>
	.section {
		max-width: 1200px;
		margin: 0 auto;
		padding: 4rem 2rem 5rem;
	}

	.sec-header {
		margin-bottom: 1.5rem;
	}

	.sec-header h3 {
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
		max-width: 64ch;
	}

	.chart-card {
		border-radius: 0;
		padding: 1.25rem 1.5rem 1rem;
	}

	.tm-wrap {
		width: 100%;
	}

	.legend {
		list-style: none;
		margin: 1rem 0 0;
		padding: 0;
	}

	.legend li {
		display: grid;
		grid-template-columns: 14px 1fr auto auto auto;
		align-items: center;
		gap: 0.75rem;
		padding: 0.5rem 0.25rem;
		border-top: 1px solid #e0e0e0;
		font-size: 0.88rem;
	}

	.legend li:first-child {
		border-top: none;
	}

	.swatch {
		width: 11px;
		height: 11px;
		border-radius: 0;
	}

	.leg-name {
		color: #1a1a1a;
		font-weight: 600;
	}

	.leg-mun {
		color: #888;
		font-size: 0.8rem;
		text-align: right;
	}

	.leg-val {
		color: #111;
		font-weight: 600;
		text-align: right;
		min-width: 6ch;
	}

	.leg-pct {
		font-weight: 700;
		text-align: right;
		min-width: 4.5ch;
	}

	/* No mobile, as 5 colunas estouram a largura — empilhamos em 2 linhas por item:
	   nome + % na primeira, nº de municípios + valor na segunda. */
	@media (max-width: 560px) {
		.legend li {
			grid-template-columns: 14px 1fr auto;
			column-gap: 0.6rem;
			row-gap: 0.15rem;
			font-size: 0.84rem;
		}
		.swatch {
			grid-column: 1;
			grid-row: 1;
		}
		.leg-name {
			grid-column: 2;
			grid-row: 1;
		}
		.leg-pct {
			grid-column: 3;
			grid-row: 1;
		}
		.leg-mun {
			grid-column: 2;
			grid-row: 2;
			text-align: left;
		}
		.leg-val {
			grid-column: 3;
			grid-row: 2;
		}
	}
</style>
