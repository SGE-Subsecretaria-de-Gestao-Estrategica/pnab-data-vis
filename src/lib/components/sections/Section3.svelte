<script lang="ts">
	import DashboardFilters from '$lib/components/DashboardFilters.svelte';
	import DashboardCard from '$lib/components/DashboardCard.svelte';
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import { createFilters } from '$lib/stores/filters.svelte';
	import type { Visao, Regiao } from '$lib/stores/filters.svelte';
	import {
		BigNumber,
		DonutChart,
		TreemapChart,
		HorizontalBarChart,
		colorScales,
	} from 'sniic-design-system';
	import {
		percContempladosCadunico, qtdContempladosCadunico,
		percFemCadunico, perc2554Cadunico,
		faixaEtariaSexoData, FAIXA_SEXO_KEYS, FAIXA_SEXO_LABELS,
		rendaDonutData, situacaoRendaDonutData,
		percUrbanoCadunico,
		domicilioTreemapData, porteTreemapData5,
		cadunicoUfData,
		valorGroupedData,
		percBolsaFamilia, percBpc,
		representacaoUfGroupedData,
	} from '$lib/data/section5';

	const filters = createFilters();

	function handleFilterChange(key: 'visao' | 'regiao' | 'uf', value: string) {
		if (key === 'visao') filters.visao = value as Visao;
		else if (key === 'regiao') filters.regiao = value as Regiao;
		else if (key === 'uf') filters.uf = value;
	}

	const fmtNum = (v: number) => v.toLocaleString('pt-BR');
	const fmtPct = (v: number) => v.toFixed(1).replace('.', ',') + '%';

	let rendaTab = $state(0);
	let geoTab = $state(0);

	const filteredCadunicoUf = $derived(
		cadunicoUfData.filter((d) => filters.filteredUFs.includes(d.label))
	);

	const filteredRepresentacaoUf = $derived(
		representacaoUfGroupedData.filter((d) => filters.filteredUFs.includes(d.label))
	);
</script>

<section id="section-3-intro" class="dashboard">
	<div class="dashboard-header">
		<h2>Agentes em Vulnerabilidade Social</h2>
		<p class="lead">Cruzamento com o CadUnico: {fmtPct(percContempladosCadunico)} dos contemplados PF estão cadastrados no CadUnico.</p>
	</div>

	<!-- Renda per capita -->
	<DashboardCard
		title="Renda per capita familiar"
		subtitle="Distribuição dos contemplados CadUnico por faixa de renda"
		tabs={['Renda per capita', 'Situação de renda']}
		activeTab={rendaTab}
		ontabchange={(i) => (rendaTab = i)}
	>
		{#if rendaTab === 0}
			<div class="donut-container">
				<DonutChart data={rendaDonutData} height={300} />
			</div>
		{:else}
			<div class="donut-container">
				<DonutChart data={situacaoRendaDonutData} height={300} />
			</div>
		{/if}
	</DashboardCard>

	<!-- Faixa etária × sexo -->
	<DashboardCard title="Faixa etária por sexo" subtitle="Distribuição dos contemplados CadUnico por idade e gênero">
		<HorizontalStackedBarChartCustom
			data={faixaEtariaSexoData}
			keys={[...FAIXA_SEXO_KEYS]}
			labels={FAIXA_SEXO_LABELS}
			colors={[colorScales.orange[2], colorScales.blue[2]]}
			height={280}
		/>
	</DashboardCard>

	<!-- Situação de domicílio e porte -->
	<DashboardCard
		title="Distribuição geográfica"
		subtitle="Situação de domicílio e porte dos municípios dos contemplados CadUnico"
		tabs={['Domicílio', 'Porte municipal']}
		activeTab={geoTab}
		ontabchange={(i) => (geoTab = i)}
	>
		{#if geoTab === 0}
			<TreemapChart data={domicilioTreemapData} height={280} />
		{:else}
			<TreemapChart data={porteTreemapData5} height={280} />
		{/if}
	</DashboardCard>

	<!-- Penetração por UF -->
	<DashboardCard title="Penetração do CadUnico por UF" subtitle="% dos contemplados da UF que estão no CadUnico">
		<HorizontalBarChart
			data={filteredCadunicoUf}
			format={(v: number) => fmtPct(v)}
			color={colorScales.teal[2]}
			height={Math.max(200, filteredCadunicoUf.length * 22)}
		/>
	</DashboardCard>

	<!-- Faixa de valor recebido -->
	<DashboardCard title="Faixa de valor recebido" subtitle="Comparação entre contemplados CadUnico e todos os contemplados PNAB">
		<div class="scroll-table">
			<table>
				<thead>
					<tr>
						<th>Faixa de valor</th>
						<th class="col-pct">% CadUnico</th>
						<th class="col-pct">% PNAB total</th>
					</tr>
				</thead>
				<tbody>
					{#each valorGroupedData as row}
						<tr>
							<td>{row.label}</td>
							<td class="col-pct">{fmtPct(row.values[0])}</td>
							<td class="col-pct ref">{fmtPct(row.values[1])}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</DashboardCard>

	<!-- Representação por UF -->
	<DashboardCard title="Representação CadUnico por UF" subtitle="% dos contemplados CadUnico vs % da população CadUnico nacional">
		<HorizontalBarChart
			data={filteredRepresentacaoUf.map((d) => ({ label: d.label, value: d.values[0] }))}
			format={(v: number) => fmtPct(v)}
			color={colorScales.orange[2]}
			height={Math.max(200, filteredRepresentacaoUf.length * 22)}
		/>
	</DashboardCard>
</section>

<style>
	.dashboard {
		max-width: 1200px;
		margin: 0 auto;
		padding: 3rem 2rem;
	}

	.dashboard-header {
		margin-bottom: 2rem;
	}

	.dashboard-header h2 {
		font-size: 1.75rem;
		font-weight: 800;
		color: #1B1B1B;
		margin: 0 0 0.5rem;
	}

	.lead {
		font-size: 1.05rem;
		color: #555;
		margin: 0;
		line-height: 1.5;
	}

	.metrics-row {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.metric {
		background: transparent;
		border-radius: 0.75rem;
		padding: 1rem 1.25rem;
		border: 1px solid rgba(0, 0, 0, 0.09);
	}

	.grid-2col {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
		margin-bottom: 1.5rem;
	}

	@media (max-width: 900px) {
		.grid-2col { grid-template-columns: 1fr; }
	}

	.donut-container {
		max-width: 340px;
		margin: 0 auto;
	}

	.scroll-table {
		max-height: 400px;
		overflow-y: auto;
	}

	.scroll-table table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.82rem;
	}

	.scroll-table th {
		text-align: left;
		font-weight: 600;
		color: #666;
		font-size: 0.72rem;
		text-transform: uppercase;
		padding: 0.5rem 0.5rem;
		border-bottom: 2px solid #e0e0e0;
		position: sticky;
		top: 0;
		background: white;
	}

	.scroll-table td {
		padding: 0.35rem 0.5rem;
		border-bottom: 1px solid #f0f0f0;
		color: #333;
	}

	.scroll-table tr:hover { background: #f8f8f8; }
	.ref { color: #999; }
	.col-pct { width: 5rem; text-align: right; }
</style>
