<script lang="ts">
	import BrazilChoropleth from '$lib/components/BrazilChoropleth.svelte';
	import DashboardFilterBar from '$lib/components/DashboardFilterBar.svelte';
	import BigNumberStat from '$lib/components/BigNumberStat.svelte';
	import { createDashboardFilters, VISAO_LABELS } from '$lib/stores/dashboardFilters.svelte';
	import {
		siglaToName,
		regionMap,
		regionAgg,
		rowsByVisao,
		nationalTotals,
		NUM_ESTADOS,
		NUM_MUNICIPIOS,
	} from '$lib/data/dashboard';

	const filters = createDashboardFilters();

	// ── Formatters ────────────────────────────────────────────────────────────
	const fmtBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency', currency: 'BRL',
			notation: 'compact', maximumFractionDigits: 1,
		}).format(v);
	const fmtBRLfull = (v: number) =>
		new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }).format(v);
	const fmtNum = (v: number) => v.toLocaleString('pt-BR');
	const fmtPct = (v: number) => v.toFixed(1).replace('.', ',') + '%';

	// ── Current rows for the active visão ───────────────────────────────────────
	const rows = $derived(rowsByVisao[filters.visao]);

	// ── Map values (keyed by sigla) ─────────────────────────────────────────────
	const mapValues = $derived.by(() => {
		const out: Record<string, number> = {};
		if (filters.visao === 'regioes') {
			for (const sigla of Object.keys(siglaToName)) {
				out[sigla] = regionAgg[regionMap[sigla]]?.valor ?? 0;
			}
		} else {
			for (const [sigla, row] of Object.entries(rows)) out[sigla] = row.valor;
		}
		return out;
	});

	// UFs in scope (for dimming). null = all in scope.
	const inScope = $derived.by(() => {
		const hasFilter = filters.uf !== 'Todas' || filters.regiao !== 'Todas';
		return hasFilter ? new Set(filters.filteredUFs) : null;
	});

	// ── Aggregated panel metrics over the scoped UFs ──────────────────────────────
	const scoped = $derived.by(() => {
		const ufs = filters.filteredUFs;
		let valor = 0, contemplados = 0, populacao = 0;
		for (const uf of ufs) {
			const r = rows[uf];
			if (!r) continue;
			valor += r.valor;
			contemplados += r.contemplados;
			populacao += r.populacao;
		}
		return { valor, contemplados, populacao };
	});

	const totalValor = $derived(nationalTotals[filters.visao].valor);
	const shareNacional = $derived(totalValor > 0 ? (scoped.valor / totalValor) * 100 : 0);
	const perCapita = $derived(scoped.populacao > 0 ? scoped.valor / scoped.populacao : 0);

	// Is the current scope the whole country?
	const isNacional = $derived(filters.uf === 'Todas' && filters.regiao === 'Todas');

	// ── "Número de entes" — exact where data allows, "—" otherwise ───────────────
	// `noun`/`adj` acompanham a seleção do filtro (ex.: "regiões contempladas").
	const entes = $derived.by((): { value: string; sub: string; noun: string; adj: string } => {
		const nUf = filters.filteredUFs.length;
		switch (filters.visao) {
			case 'estados':
				return { value: fmtNum(nUf), sub: nUf === 1 ? 'estado' : 'estados', noun: 'estados', adj: 'contemplados' };
			case 'regioes': {
				const n = filters.regiao === 'Todas' ? 5 : 1;
				return { value: fmtNum(n), sub: n === 1 ? 'região' : 'regiões', noun: 'regiões', adj: 'contempladas' };
			}
			case 'municipios':
				return isNacional
					? { value: fmtNum(NUM_MUNICIPIOS), sub: 'municípios', noun: 'municípios', adj: 'contemplados' }
					: { value: '—', sub: 'municípios (indisp. por recorte)', noun: 'municípios', adj: 'contemplados' };
			case 'uf':
			default:
				return isNacional
					? { value: fmtNum(NUM_ESTADOS + NUM_MUNICIPIOS), sub: `${NUM_ESTADOS} estados + ${fmtNum(NUM_MUNICIPIOS)} municípios`, noun: 'entes federativos', adj: 'contemplados' }
					: { value: fmtNum(nUf), sub: `${nUf} ${nUf === 1 ? 'estado' : 'estados'} + municípios`, noun: 'entes federativos', adj: 'contemplados' };
		}
	});

	// ── Scope label ───────────────────────────────────────────────────────────
	const scopeLabel = $derived.by(() => {
		if (filters.uf !== 'Todas') return siglaToName[filters.uf] ?? filters.uf;
		if (filters.regiao !== 'Todas') return `Região ${filters.regiao}`;
		return 'Brasil';
	});
</script>

<section class="dashboard">
	<header class="dash-header">
		<p class="eyebrow">PNAB · Painel de Dados</p>
		<h1>Valores gerais da pesquisa</h1>
		<p class="lead">
			Distribuição dos recursos da Política Nacional Aldir Blanc pelo território brasileiro.
			Use os filtros para alternar a visão e clique em um estado no mapa para detalhar.
		</p>
	</header>

	<!-- ── Filter bar ───────────────────────────────────────────────────────── -->
	<DashboardFilterBar {filters} />

	<!-- ── Main grid: metrics left, map right ───────────────────────────────── -->
	<div class="grid">
		<div class="panel">
			<div class="scope-tag">{scopeLabel} · {VISAO_LABELS[filters.visao]}</div>

			<!-- Headline: entes (rótulo acompanha a seleção do filtro) -->
			<BigNumberStat
				value={entes.value}
				label="{entes.noun} {entes.adj}"
				subtitle={entes.sub}
				fontSize={60}
				shadowDepth={6}
				width={460}
			/>

			<!-- Trio: recebido / executado / % nacional -->
			<div class="metric-trio">
				<div class="metric">
					<span class="metric-value">{fmtBRL(scoped.valor)}</span>
					<span class="metric-label">Valor executado</span>
				</div>
				<div class="metric">
					<span class="metric-value">{fmtPct(shareNacional)}</span>
					<span class="metric-label">do total nacional</span>
				</div>
				<div class="metric">
					<span class="metric-value">{fmtBRLfull(perCapita)}</span>
					<span class="metric-label">per capita</span>
				</div>
			</div>

			<!-- Contemplados -->
			<BigNumberStat value={fmtNum(scoped.contemplados)} label="contemplados (agentes / projetos)" fontSize={50} shadowDepth={5} width={460} />
		</div>

		<div class="map-wrap">
			<BrazilChoropleth
				values={mapValues}
				format={fmtBRL}
				metricLabel="Valor executado"
				selected={filters.visao === 'regioes' ? 'Todas' : filters.uf}
				inScope={inScope}
				onselect={(sigla) => filters.selectUf(sigla)}
			/>
			<p class="map-caption">Cor proporcional ao valor executado. Clique para detalhar.</p>
		</div>
	</div>
</section>

<style>
	.dashboard {
		max-width: 1200px;
		margin: 0 auto;
		padding: 3rem 2rem 5rem;
	}

	.dash-header {
		margin-bottom: 2rem;
	}

	.eyebrow {
		font-size: 0.72rem;
		font-weight: 700;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: #1351B4;
		margin: 0 0 0.5rem;
	}

	.dash-header h1 {
		font-size: 2rem;
		font-weight: 800;
		color: #1B1B1B;
		margin: 0 0 0.5rem;
		line-height: 1.15;
	}

	.lead {
		font-size: 1rem;
		color: #555;
		margin: 0;
		line-height: 1.5;
		max-width: 60ch;
	}

	/* ── Grid ── */
	.grid {
		display: grid;
		grid-template-columns: 1fr 1.05fr;
		gap: 2rem;
		align-items: start;
	}

	.panel {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.scope-tag {
		display: inline-block;
		align-self: flex-start;
		font-size: 0.74rem;
		font-weight: 600;
		color: #1351B4;
		background: rgba(19, 81, 180, 0.08);
		padding: 0.3rem 0.7rem;
		border-radius: 0;
	}

	/* ── Plain metrics (trio) ── */
	.metric {
		display: flex;
		flex-direction: column;
		align-items: center;
		text-align: center;
		gap: 0.1rem;
	}

	.metric-value {
		font-weight: 800;
		color: #1351B4;
		line-height: 1.05;
		font-size: 1.6rem;
		font-variant-numeric: tabular-nums;
	}

	.metric-label {
		font-size: 0.85rem;
		font-weight: 600;
		color: #555;
	}

	.metric-trio {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1rem 0.75rem;
	}

	/* ── Map ── */
	.map-wrap {
		position: sticky;
		top: 1rem;
	}

	.map-caption {
		text-align: center;
		font-size: 0.74rem;
		color: #888;
		margin: 0.5rem 0 0;
	}

	/* ── Responsive ── */
	@media (max-width: 860px) {
		.grid {
			grid-template-columns: 1fr;
		}
		.map-wrap {
			position: static;
			order: -1;
		}
		.dash-header h1 { font-size: 1.6rem; }
	}
</style>
