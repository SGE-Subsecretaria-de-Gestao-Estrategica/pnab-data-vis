<script lang="ts">
	import FaixaComparisonChart from '$lib/components/FaixaComparisonChart.svelte';
	import DashboardFilterBar from '$lib/components/DashboardFilterBar.svelte';
	import { createDashboardFilters, VISAO_LABELS } from '$lib/stores/dashboardFilters.svelte';
	import { colorScales } from 'sniic-design-system';
	import { faixaComparison, FAIXA_LABELS } from '$lib/data/faixa';

	const filters = createDashboardFilters();

	// Municipality-level faixa data doesn't exist — offer only the supported visões.
	const VISOES = ['uf', 'estados', 'regioes'] as const;

	const FAIXA_COLORS = [
		colorScales.blue[0],
		colorScales.blue[1],
		colorScales.blue[2],
		colorScales.blue[3],
		colorScales.blue[4],
	];

	const entities = $derived(
		faixaComparison(
			filters.visao === 'municipios' ? 'uf' : filters.visao,
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
		<p class="eyebrow">Gráfico 3</p>
		<h2>Distribuição por faixa de valor</h2>
		<p class="lead">
			Para cada ente federativo, duas barras: a participação de cada faixa de valor no
			<strong>valor executado</strong> e no <strong>número de pagamentos</strong>.
			Compare os entes entre si e com o Brasil.
		</p>
	</header>

	<DashboardFilterBar {filters} visoes={[...VISOES]} />

	<div class="chart-card">
		<div class="scope-tag">{scopeLabel} · {VISAO_LABELS[filters.visao]}</div>
		<FaixaComparisonChart
			entities={entities}
			faixaLabels={FAIXA_LABELS}
			colors={FAIXA_COLORS}
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
