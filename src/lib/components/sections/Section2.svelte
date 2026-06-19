<script lang="ts">
	import DashboardFilters from '$lib/components/DashboardFilters.svelte';
	import DashboardCard from '$lib/components/DashboardCard.svelte';
	import PyramidChartCustom from '$lib/components/PyramidChartCustom.svelte';
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import { createFilters } from '$lib/stores/filters.svelte';
	import type { Visao, Regiao } from '$lib/stores/filters.svelte';
	import {
		BigNumber,
		DonutChart,
		HorizontalBarChart,
		TreemapChart,
		colorScales,
	} from 'sniic-design-system';
	import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
	import {
		totalBeneficiarios,
		pfPjDonutData,
		totalPF,
		valorTotalPF, valorTotalPJ,
		sexoQuantityDonutData,
		sexoPropMasculino, sexoPropFeminino,
		pyramidData,
		naturezaJuridicaData,
		top20CnaesQtdTableData,
		sexoUfComparisonData,
	} from '$lib/data/section3';
	import {
		totalComVinculo, totalSemVinculo,
		percComVinculo, percSemVinculo,
		racaCorBarData,
		racaCorTreemapData,
		escolaridadeComparisonGroupedData,
		sexoComparisonStackedData, sexoComparisonStackedKeys, sexoComparisonStackedLabels,
		regionComparisonGroupedData,
		cboRaisTop20,
	} from '$lib/data/section4';

	const filters = createFilters();

	function handleFilterChange(key: 'visao' | 'regiao' | 'uf', value: string) {
		if (key === 'visao') filters.visao = value as Visao;
		else if (key === 'regiao') filters.regiao = value as Regiao;
		else if (key === 'uf') filters.uf = value;
	}

	const fmtBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency', currency: 'BRL',
			notation: 'compact', maximumFractionDigits: 1,
		}).format(v);
	const fmtNum = (v: number) => v.toLocaleString('pt-BR');
	const fmtPct = (v: number) => v.toFixed(1).replace('.', ',') + '%';

	let empTab = $state(0);

	const filteredSexoUf = $derived(
		sexoUfComparisonData.filter((d) => filters.filteredUFs.includes(d.uf))
	);
</script>

<section id="section-2-intro" class="dashboard">
	<div class="dashboard-header">
		<h2>Perfil dos Agentes Culturais</h2>
		<p class="lead">Quem são os {fmtNum(totalBeneficiarios)} agentes culturais que acessaram a PNAB?</p>
	</div>

	<div class="grid-2col">
		<!-- PF vs PJ donut -->
		<DashboardCard title="Pessoa Física vs Jurídica" subtitle="Distribuição dos agentes contemplados por tipo">
			<div class="donut-container">
				<DonutChart data={pfPjDonutData} height={280} />
			</div>
		</DashboardCard>

		<!-- Pirâmide etária -->
		<DashboardCard title="Pirâmide etária por sexo" subtitle="Distribuição dos contemplados PF por faixa etária e gênero">
			<PyramidChartCustom
				data={pyramidData}
				leftLabel="Masculino"
				rightLabel="Feminino"
				colors={[colorScales.yellow[2], colorScales.blue[2]]}
				height={320}
			/>
		</DashboardCard>
	</div>

	<!-- Sexo por UF -->
	<DashboardCard title="Distribuição de gênero por UF" subtitle="Comparação entre PNAB e IBGE por estado">
		<div class="scroll-table">
			<table>
				<thead>
					<tr>
						<th>UF</th>
						<th>Masc. PNAB</th>
						<th>Fem. PNAB</th>
						<th>Masc. IBGE</th>
						<th>Fem. IBGE</th>
					</tr>
				</thead>
				<tbody>
					{#each filteredSexoUf as d}
						<tr>
							<td class="uf-cell">{d.uf}</td>
							<td>{fmtPct(d.aldirMasc)}</td>
							<td>{fmtPct(d.aldirFem)}</td>
							<td class="ref">{fmtPct(d.ibgeMasc)}</td>
							<td class="ref">{fmtPct(d.ibgeFem)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</DashboardCard>

	<!-- Natureza jurídica -->
	<DashboardCard title="Natureza jurídica (PJ)" subtitle="Distribuição dos contemplados PJ por tipo de organização">
		<HorizontalBarChart
			data={naturezaJuridicaData}
			format={(v: number) => fmtPct(v)}
			color={colorScales.teal[2]}
			height={240}
		/>
	</DashboardCard>

	<!-- Vínculo formal -->
	<DashboardCard
		title="Vínculo formal de trabalho"
		subtitle="Perfil dos contemplados com vínculo formal (RAIS 2022-2024)"
		tabs={['Por região', 'Por raça/cor', 'Por escolaridade']}
		activeTab={empTab}
		ontabchange={(i) => (empTab = i)}
	>
		{#if empTab === 0}
			<HorizontalGroupedBarChart
				data={regionComparisonGroupedData}
				seriesLabels={['Contemplados PNAB', 'Vínculos RAIS 2024']}
				colors={[colorScales.yellow[2], colorScales.blue[2]]}
				format={(v: number) => fmtPct(v)}
				margin={{ top: 20, right: 80, bottom: 40, left: 120 }}
				barHeight={20}
				groupPad={24}
				rx={0}
				crispEdges={true}
				labelsInside={true}
				legendBottom={true}
			/>
		{:else if empTab === 1}
			<TreemapChart data={racaCorTreemapData} height={280} />
		{:else}
			<HorizontalGroupedBarChart
				data={escolaridadeComparisonGroupedData}
				seriesLabels={['PNAB', 'Total trabalhadores formais']}
				colors={[colorScales.yellow[2], colorScales.blue[2]]}
				format={(v: number) => fmtPct(v)}
				margin={{ top: 20, right: 80, bottom: 40, left: 260 }}
				barHeight={20}
				rx={0}
				crispEdges={true}
				labelsInside={true}
				legendBottom={true}
			/>
		{/if}
	</DashboardCard>

	<DashboardCard title="Gênero no vínculo formal" subtitle="PNAB vs Brasil (RAIS)">
		<HorizontalStackedBarChartCustom
			data={sexoComparisonStackedData}
			keys={[...sexoComparisonStackedKeys]}
			labels={sexoComparisonStackedLabels}
			colors={[colorScales.yellow[2], colorScales.blue[2]]}
			labelsAbove={true}
		/>
	</DashboardCard>

	<!-- Top CNAEs -->
	<DashboardCard title="Principais atividades econômicas (CNAE)" subtitle="Top 20 atividades dos contemplados PJ, ordenadas por quantidade">
		<div class="scroll-table">
			<table>
				<thead>
					<tr>
						<th class="col-pos">#</th>
						<th>Atividade</th>
						<th class="col-pct">% Qtde</th>
						<th class="col-pct">% Valor</th>
					</tr>
				</thead>
				<tbody>
					{#each top20CnaesQtdTableData as row}
						<tr>
							<td class="col-pos">{row.posicao}</td>
							<td>{row.descricao}</td>
							<td class="col-pct">{row.percQuantidadeFormatted}</td>
							<td class="col-pct">{row.percValorFormatted}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</DashboardCard>

	<!-- Top CBOs -->
	<DashboardCard title="Principais ocupações formais (CBO/RAIS)" subtitle="Top 20 ocupações entre contemplados com vínculo formal">
		<div class="scroll-table">
			<table>
				<thead>
					<tr>
						<th class="col-pos">#</th>
						<th>Ocupação</th>
						<th class="col-pct">% Valor</th>
					</tr>
				</thead>
				<tbody>
					{#each cboRaisTop20 as row}
						<tr>
							<td class="col-pos">{row.posicao}</td>
							<td>{row.descricao}</td>
							<td class="col-pct">{row.percFormatted}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
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
		max-width: 320px;
		margin: 0 auto;
	}

	.scroll-table {
		max-height: 500px;
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
	.uf-cell { font-weight: 600; }
	.ref { color: #999; }
	.col-pos { width: 2rem; text-align: center; color: #999; }
	.col-pct { width: 5rem; text-align: right; }
</style>
