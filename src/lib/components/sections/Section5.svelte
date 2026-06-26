<script lang="ts">
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import DashboardFilterBar from '$lib/components/DashboardFilterBar.svelte';
	import { createDashboardFilters, VISAO_LABELS } from '$lib/stores/dashboardFilters.svelte';
	import { colorScales } from 'sniic-design-system';
	import { residenciaComparison, RESID_KEYS, RESID_LABELS } from '$lib/data/localResidencia';

	// Capital/metro/interior só existe por execução estadual — visões disponíveis.
	const filters = createDashboardFilters('estados');
	const VISOES = ['estados', 'regioes'] as const;

	const fmtPct = (v: number) => `${Math.round(v)}%`;

	const data = $derived(
		residenciaComparison(
			filters.visao === 'regioes' ? 'regioes' : 'estados',
			filters.filteredUFs,
			filters.regiao
		)
	);

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
		<p class="eyebrow">Gráfico 5</p>
		<h2>Distribuição de recursos: capital, metropolitana e interior</h2>
		<p class="lead">
			Participação de capital, região metropolitana e interior no valor executado,
			por ente federativo, com o Brasil como referência.
		</p>
	</header>

	<DashboardFilterBar {filters} visoes={[...VISOES]} />

	<div class="chart-card">
		<div class="scope-tag">{scopeLabel} · {VISAO_LABELS[filters.visao]}</div>
		<HorizontalStackedBarChartCustom
			data={data}
			keys={[...RESID_KEYS]}
			labels={RESID_LABELS}
			colors={[colorScales.orange[2], colorScales.teal[2], colorScales.lime[2]]}
			format={fmtPct}
			marginLeft={104}
			showFlags={filters.visao === 'estados'}
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
		border-radius: 0;
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
		border-radius: 0;
		margin-bottom: 1rem;
	}
</style>
