<script lang="ts">
	import HorizontalBarChartCustom from '$lib/components/HorizontalBarChartCustom.svelte';
	import DashboardFilterBar from '$lib/components/DashboardFilterBar.svelte';
	import { createDashboardFilters, VISAO_LABELS } from '$lib/stores/dashboardFilters.svelte';
	import { colorScales } from 'sniic-design-system';
	import { rowsByVisao, regionAgg, REGIOES } from '$lib/data/dashboard';

	const filters = createDashboardFilters();

	const fmtBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }).format(v);

	// ── Per capita bars (Gráfico 2), reactive to the visão ──────────────────────
	const bars = $derived.by(() => {
		if (filters.visao === 'regioes') {
			const regs = filters.regiao === 'Todas' ? REGIOES : [filters.regiao];
			return regs.map((r) => {
				const a = regionAgg[r];
				return { label: r, value: a.populacao > 0 ? a.valor / a.populacao : 0 };
			});
		}
		const rows = rowsByVisao[filters.visao];
		return filters.filteredUFs
			.map((uf) => {
				const row = rows[uf];
				if (!row) return null;
				return { label: uf, value: row.populacao > 0 ? row.valor / row.populacao : 0 };
			})
			.filter((d): d is { label: string; value: number } => d !== null);
	});

	const scopeLabel = $derived(filters.regiao !== 'Todas' ? `Região ${filters.regiao}` : 'Brasil');
</script>

<section class="section">
	<header class="sec-header">
		<p class="eyebrow">Gráfico 2</p>
		<h2>Valor per capita por estado</h2>
		<p class="lead">
			Valor executado dividido pela população. Use o filtro para alternar a visão
			(UF, estados, municípios ou regiões).
		</p>
	</header>

	<DashboardFilterBar {filters} showUf={false} />

	<div class="chart-card">
		<div class="scope-tag">{scopeLabel} · {VISAO_LABELS[filters.visao]}</div>
		<HorizontalBarChartCustom
			data={bars}
			color={colorScales.blue[2]}
			format={fmtBRL}
			xLabel="Valor per capita (R$)"
			margin={{ top: 20, right: 56, bottom: 48, left: 96 }}
			showFlags={filters.visao === 'uf' || filters.visao === 'estados'}
			labelColor="#000000"
			axisColor="#000000"
			outsideValueColor="#000000"
		/>
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
		max-width: 60ch;
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
