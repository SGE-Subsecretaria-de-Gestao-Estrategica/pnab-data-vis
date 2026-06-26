<script lang="ts">
	import DashboardFilterBar from '$lib/components/DashboardFilterBar.svelte';
	import HorizontalBarChartCustom from '$lib/components/HorizontalBarChartCustom.svelte';
	import { createDashboardFilters } from '$lib/stores/dashboardFilters.svelte';
	import { colorScales } from 'sniic-design-system';
	import { orgScope } from '$lib/data/section9';
	import { siglaToName } from '$lib/data/dashboard';

	const filters = createDashboardFilters();

	const fmtNum = (v: number) => v.toLocaleString('pt-BR');
	const fmtPct = (v: number) => v.toFixed(1).replace('.', ',') + '%';

	const scope = $derived(orgScope(filters.visao, filters.filteredUFs));
	const hasData = $derived(scope.total > 0);

	const scopeLabel = $derived.by(() => {
		if (filters.uf !== 'Todas') return siglaToName[filters.uf] ?? filters.uf;
		if (filters.regiao !== 'Todas') return `Região ${filters.regiao}`;
		return 'Brasil';
	});
	const topOrg = $derived(scope.bars[0]);
</script>

<section class="section-band">
	<div class="section">
	<header class="sec-header">
		<h2>Contemplados PJ por tipo de organização</h2>
		<p class="lead">
			Distribuição das pessoas jurídicas contempladas pela Aldir Blanc por natureza jurídica.
			{#if hasData && topOrg}
				No escopo <strong>{scopeLabel}</strong>, <strong>{topOrg.label}</strong> lidera com
				<strong>{fmtNum(topOrg.value)}</strong> contemplados ({fmtPct(topOrg.perc)}).
			{/if}
		</p>
	</header>

	<DashboardFilterBar {filters} labelColor="#fff4e9" />

	{#if hasData}
		<div class="scope-tag">{scopeLabel} · {scope.total.toLocaleString('pt-BR')} contemplados PJ</div>

		<div class="chart-card">
			<HorizontalBarChartCustom
				data={scope.bars}
				color={colorScales.teal[2]}
				format={fmtNum}
				xLabel="Contemplados"
				margin={{ top: 20, right: 56, bottom: 40, left: 256 }}
				labelColor="#fff4e9"
				axisColor="#fff4e9"
				outsideValueColor="#fff4e9"
			/>
		</div>
	{:else}
		<div class="empty">
			<p>
				Não há contemplados de pessoa jurídica no recorte
				<strong>{scopeLabel}</strong> para esta visão. Ajuste os filtros acima.
			</p>
		</div>
	{/if}
	</div>
</section>

<style>
	.section-band {
		background: #883a67;
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
		color: #ffffff;
		margin: 0 0 0.4rem;
		line-height: 1.15;
	}

	.lead {
		font-size: 0.98rem;
		color: #fff4e9;
		margin: 0;
		line-height: 1.5;
		max-width: 70ch;
	}

	.scope-tag {
		display: inline-block;
		font-size: 0.74rem;
		font-weight: 600;
		color: #fff4e9;
		background: rgba(255, 255, 255, 0.14);
		padding: 0.3rem 0.7rem;
		border-radius: 0;
		margin-bottom: 1rem;
	}

	.chart-card {
		border-radius: 0;
		padding: 1.25rem 1.5rem 1rem;
	}

	.empty {
		border: 1px dashed rgba(255, 255, 255, 0.45);
		border-radius: 0;
		padding: 1.5rem;
		background: rgba(255, 255, 255, 0.08);
	}

	.empty p {
		margin: 0;
		font-size: 0.92rem;
		color: #fff4e9;
		line-height: 1.5;
		max-width: 60ch;
	}

	@media (max-width: 720px) {
		.sec-header h2 {
			font-size: 1.4rem;
		}
	}
</style>
