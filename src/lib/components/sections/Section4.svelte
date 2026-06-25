<script lang="ts">
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import DashboardFilterBar from '$lib/components/DashboardFilterBar.svelte';
	import { createDashboardFilters, VISAO_LABELS } from '$lib/stores/dashboardFilters.svelte';
	import { colorScales } from 'sniic-design-system';
	import { rowsByVisao, regionAgg, REGIOES } from '$lib/data/dashboard';

	const filters = createDashboardFilters();

	const fmtPct = (v: number) => `${Math.round(v)}%`;

	type ZonaRow = { label: string; urbano: number; rural: number };

	function toPct(urbano: number, rural: number, label: string): ZonaRow {
		const total = urbano + rural || 1;
		return { label, urbano: (urbano / total) * 100, rural: (rural / total) * 100 };
	}

	// ── Urbano × Rural por entidade (% do valor), com linha Brasil ──────────────
	const data = $derived.by((): ZonaRow[] => {
		// "regioes" agrega a partir do nível uf (combinado).
		const source = filters.visao === 'regioes' ? rowsByVisao.uf : rowsByVisao[filters.visao];

		// Brasil = soma de todas as UFs da visão atual.
		let bu = 0, br = 0;
		for (const r of Object.values(source)) { bu += r.valorUrbano; br += r.valorRural; }
		const brasil = toPct(bu, br, 'Brasil');

		let entities: ZonaRow[];
		if (filters.visao === 'regioes') {
			const regs = filters.regiao === 'Todas' ? REGIOES : [filters.regiao];
			entities = regs.map((rg) => toPct(regionAgg[rg].valorUrbano, regionAgg[rg].valorRural, rg));
		} else {
			entities = filters.filteredUFs
				.map((uf) => source[uf])
				.filter((r): r is NonNullable<typeof r> => !!r)
				.map((r) => toPct(r.valorUrbano, r.valorRural, r.uf));
		}
		// Mais rural no topo (depois do Brasil).
		entities.sort((a, b) => b.rural - a.rural);
		return [brasil, ...entities];
	});

	const scopeLabel = $derived(
		filters.uf !== 'Todas'
			? filters.uf
			: filters.regiao !== 'Todas'
				? `Região ${filters.regiao}`
				: 'Brasil'
	);
</script>

<section class="section">
	<header class="sec-header">
		<p class="eyebrow">Gráfico 4</p>
		<h2>Território urbano × rural por estado</h2>
		<p class="lead">
			Participação das zonas urbana e rural no valor executado, por ente federativo,
			com o Brasil como referência. Use o filtro para alternar a visão.
		</p>
	</header>

	<DashboardFilterBar {filters} />

	<div class="chart-card">
		<div class="scope-tag">{scopeLabel} · {VISAO_LABELS[filters.visao]}</div>
		<HorizontalStackedBarChartCustom
			data={data}
			keys={['urbano', 'rural']}
			labels={{ urbano: 'Urbano', rural: 'Rural' }}
			colors={[colorScales.teal[2], colorScales.lime[2]]}
			format={fmtPct}
			marginLeft={104}
			showFlags={filters.visao === 'uf' || filters.visao === 'estados'}
			hideSegmentLabelsFor={[]}
		/>
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
		color: #1351B4;
		margin: 0 0 0.4rem;
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
		max-width: 64ch;
	}

	.chart-card {
		border: 1px solid rgba(0, 0, 0, 0.1);
		border-radius: 0.75rem;
		padding: 1.25rem 1.5rem 1rem;
		background: rgba(255, 255, 255, 0.45);
	}

	.scope-tag {
		display: inline-block;
		font-size: 0.74rem;
		font-weight: 600;
		color: #1351B4;
		background: rgba(19, 81, 180, 0.08);
		padding: 0.3rem 0.7rem;
		border-radius: 999px;
		margin-bottom: 1rem;
	}
</style>
