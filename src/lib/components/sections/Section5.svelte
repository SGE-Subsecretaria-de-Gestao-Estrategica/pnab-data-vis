<script lang="ts">
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import DashboardFilterBar from '$lib/components/DashboardFilterBar.svelte';
	import { createDashboardFilters, VISAO_LABELS } from '$lib/stores/dashboardFilters.svelte';
	import { colorScales } from 'sniic-design-system';
	import { residenciaComparison, RESID_KEYS, RESID_LABELS } from '$lib/data/localResidencia';

	// Capital/metro/interior só existe por execução estadual — única visão disponível.
	const filters = createDashboardFilters('estados');

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
			? filters.uf2 !== 'Todas'
				? `${filters.uf} vs ${filters.uf2}`
				: filters.uf
			: filters.regiao !== 'Todas'
				? `Região ${filters.regiao}`
				: 'Brasil'
	);
</script>

<section class="section-band">
	<div class="section">
	<header class="sec-header">
		<h2>Distribuição de recursos: capital, metropolitana e interior</h2>
		<p class="lead">
			Participação de capital, região metropolitana e interior no valor executado,
			por ente federativo, com o Brasil como referência.
		</p>
	</header>

	<DashboardFilterBar {filters} showVisao={false} showCompare />

	<div class="chart-card">
		<div class="scope-tag">{scopeLabel} · {VISAO_LABELS[filters.visao]}</div>
		<HorizontalStackedBarChartCustom
			data={data}
			keys={[...RESID_KEYS]}
			labels={RESID_LABELS}
			colors={[colorScales.blue[2], colorScales.red[2], colorScales.purple[2]]}
			format={fmtPct}
			marginLeft={104}
			showFlags={filters.visao === 'estados'}
			axisColor="#000000"
			gridColor="#000000"
		/>
	</div>
	</div>
</section>

<style>
	.section-band {
		background: #f6c341;
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
		max-width: 64ch;
	}

	.chart-card {
		border-radius: 0;
		padding: 1.25rem 1.5rem 1rem;
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
