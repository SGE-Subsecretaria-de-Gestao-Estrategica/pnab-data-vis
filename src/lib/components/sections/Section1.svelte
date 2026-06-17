<script lang="ts">
	import DashboardFilters from '$lib/components/DashboardFilters.svelte';
	import DashboardCard from '$lib/components/DashboardCard.svelte';
	import ExecutedValueByStateMap from '$lib/components/ExecutedValueByStateMap.svelte';
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
	import { createFilters } from '$lib/stores/filters.svelte';
	import type { Visao, Regiao } from '$lib/stores/filters.svelte';
	import {
		BigNumber,
		TreemapChart,
		HorizontalBarChart,
		HorizontalStackedBarChart,
		colorScales,
		colorPairs,
		categorical8,
	} from 'sniic-design-system';
	import {
		siglaToName, regionMap,
		valorExecEstados, valorExecMunicipios, valorExecTotal,
		percExecEstados, percExecMunicipios,
		stateRows,
		states,
		percapitaData,
		porteTreemapData, porteRaw,
		capitalInteriorStackedData, capitalInteriorByUfData,
		specialTerritoriesMetrics,
		zoneData,
		percRuralQtde,
	} from '$lib/data/section1';
	import {
		percBenefCPF, percBenefCNPJ,
		percValorCPF, percValorCNPJ,
		totalBenefCPF, totalBenefCNPJ,
		benefVsValorData,
		faixaGroupedData,
		regiaoGroupedData,
		UF_BAND_KEYS, UF_BAND_LABELS,
		ufBandPercData, ufValorBandPercData,
	} from '$lib/data/section2';

	const filters = createFilters();

	function handleFilterChange(key: 'visao' | 'regiao' | 'uf', value: string) {
		if (key === 'visao') filters.visao = value as Visao;
		else if (key === 'regiao') filters.regiao = value as Regiao;
		else if (key === 'uf') filters.uf = value;
	}

	// Format helpers
	const fmtBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency', currency: 'BRL',
			notation: 'compact', maximumFractionDigits: 1,
		}).format(v);

	const fmtNum = (v: number) => v.toLocaleString('pt-BR');
	const fmtPct = (v: number) => v.toFixed(1).replace('.', ',') + '%';

	// ── Derived filtered data ───────────────────────────────────────────────────

	// Map data filtered by region/UF
	const filteredMapData = $derived(() => {
		const filtered = stateRows.filter((d) => filters.filteredUFs.includes(d.uf));
		return Object.fromEntries(
			filtered.map((d) => [siglaToName[d.uf], d])
		);
	});

	const filteredMapMetric = $derived(() => {
		if (filters.visao === 'estados') return 'valor_executado_rs';
		if (filters.visao === 'municipios') return 'valor_executado_rs';
		return 'valor_executado_rs';
	});

	// BigNumbers filtered
	const filteredTotals = $derived(() => {
		const filtered = stateRows.filter((d) => filters.filteredUFs.includes(d.uf));
		const totalVal = filtered.reduce((s, d) => s + d.valor_executado_rs, 0);
		const totalPop = filtered.reduce((s, d) => s + d.sum_populacao, 0);
		const totalContemp = filtered.reduce((s, d) => s + d.qtde_contemplados, 0);
		return { totalVal, totalPop, totalContemp, perCapita: totalPop > 0 ? totalVal / totalPop : 0 };
	});

	// Per capita ranking filtered
	const filteredPercapita = $derived(
		percapitaData.filter((d) => filters.filteredUFs.includes(d.uf))
	);

	// Capital/Interior filtered
	const filteredCapitalInterior = $derived(
		capitalInteriorByUfData.filter((d) => filters.filteredUFs.includes(d.label))
	);

	// Faixa valor por UF filtered
	const filteredFaixaUf = $derived(
		ufBandPercData.filter((d) => filters.filteredUFs.includes(d.label))
	);

	const filteredFaixaValorUf = $derived(
		ufValorBandPercData.filter((d) => filters.filteredUFs.includes(d.label))
	);

	// Zone data filtered
	const filteredZoneData = $derived(
		zoneData.filter((d) => filters.filteredUFs.includes(d.label))
	);

	// Map tab
	let mapMetricTab = $state(0);
	const MAP_METRICS = ['valor_executado_rs', 'qtde_contemplados', 'sum_populacao'] as const;
	const MAP_LABELS = ['Valor executado', 'Contemplados', 'População'];
	const MAP_FORMATS: ((v: number) => string)[] = [fmtBRL, fmtNum, fmtNum];

	// Faixa tab
	let faixaTab = $state(0);

	// Capital/Interior tab
	let capitalTab = $state(0);
</script>

<section id="section-1-intro" class="dashboard">
	<div class="dashboard-header">
		<h2>Distribuição Territorial dos Recursos</h2>
		<p class="lead">Como os R$ {fmtBRL(valorExecTotal)} da PNAB foram distribuídos pelo território brasileiro?</p>
	</div>

	<!-- Map — full width -->
	<DashboardCard
		title="Mapa de distribuição por UF"
		subtitle="Valor total executado por estado (estado + municípios)"
		tabs={MAP_LABELS}
		activeTab={mapMetricTab}
		ontabchange={(i) => (mapMetricTab = i)}
	>
		<ExecutedValueByStateMap
			states={filteredMapData()}
			metric={MAP_METRICS[mapMetricTab]}
			label={MAP_LABELS[mapMetricTab]}
			format={MAP_FORMATS[mapMetricTab]}
			formatLine2={mapMetricTab === 0 ? (row) => fmtPct(row.valor_executado_perc * 100) : undefined}
			showSideLegend={true}
		/>
	</DashboardCard>

	<!-- Per capita — full width -->
	<DashboardCard title="Valor per capita por UF" subtitle="Valor executado dividido pela população da UF">
		<HorizontalBarChart
			data={filteredPercapita.map((d) => ({ label: d.uf, value: d.valor_percapita_uf }))}
			format={fmtBRL}
			color={colorScales.blue[2]}
			height={Math.max(300, filteredPercapita.length * 22)}
		/>
	</DashboardCard>

	<!-- Faixa de valor — full width -->
	<DashboardCard
		title="Distribuição por faixa de valor"
		subtitle="Percentual de contemplados e recursos por faixa de pagamento, por UF"
		tabs={['% de contemplados', '% do valor']}
		activeTab={faixaTab}
		ontabchange={(i) => (faixaTab = i)}
	>
		{#if faixaTab === 0}
			<HorizontalStackedBarChartCustom
				data={filteredFaixaUf}
				keys={[...UF_BAND_KEYS]}
				labels={UF_BAND_LABELS}
				colors={[colorScales.blue[0], colorScales.blue[1], colorScales.blue[2], colorScales.blue[3], colorScales.blue[4]]}
				height={Math.max(300, filteredFaixaUf.length * 24)}
			/>
		{:else}
			<HorizontalStackedBarChartCustom
				data={filteredFaixaValorUf}
				keys={[...UF_BAND_KEYS]}
				labels={UF_BAND_LABELS}
				colors={[colorScales.blue[0], colorScales.blue[1], colorScales.blue[2], colorScales.blue[3], colorScales.blue[4]]}
				height={Math.max(300, filteredFaixaValorUf.length * 24)}
			/>
		{/if}
	</DashboardCard>

	<!-- Capital / Interior — full width -->
	<DashboardCard
		title="Capital, Metropolitana e Interior"
		subtitle="Distribuição de recursos e contemplados por localização"
		tabs={['Visão Brasil', 'Por UF']}
		activeTab={capitalTab}
		ontabchange={(i) => (capitalTab = i)}
	>
		{#if capitalTab === 0}
			<HorizontalStackedBarChartCustom
				data={capitalInteriorStackedData}
				keys={['capital', 'metropolitana', 'interior']}
				labels={{ capital: 'Capital', metropolitana: 'Metropolitana', interior: 'Interior' }}
				colors={[colorScales.orange[2], colorScales.teal[2], colorScales.lime[2]]}
				height={140}
			/>
		{:else}
			<HorizontalStackedBarChartCustom
				data={filteredCapitalInterior}
				keys={['capital', 'metropolitana', 'interior']}
				labels={{ capital: 'Capital', metropolitana: 'Metropolitana', interior: 'Interior' }}
				colors={[colorScales.orange[2], colorScales.teal[2], colorScales.lime[2]]}
				height={Math.max(200, filteredCapitalInterior.length * 24)}
			/>
		{/if}
	</DashboardCard>

	<!-- Porte municipal treemap — full width -->
	<DashboardCard title="Distribuição por porte municipal" subtitle="Valor total executado por tamanho do município">
		<TreemapChart data={porteTreemapData} height={360} />
	</DashboardCard>

	<!-- Urbano vs Rural — full width -->
	<DashboardCard title="Urbano vs Rural" subtitle="Distribuição por zona de residência dos contemplados">
		<div class="rural-highlight">
			<BigNumber value={fmtPct(percRuralQtde)} label="dos contemplados vivem em zona rural" />
		</div>
		<HorizontalStackedBarChart
			data={filteredZoneData.map((d) => ({
				label: d.label,
				urbano: d.valor_urbano / (d.valor_urbano + d.valor_rural) * 100,
				rural: d.valor_rural / (d.valor_urbano + d.valor_rural) * 100,
			}))}
			keys={['urbano', 'rural']}
			labels={{ urbano: 'Urbano', rural: 'Rural' }}
			colors={[colorScales.teal[2], colorScales.lime[2]]}
			height={Math.max(200, filteredZoneData.length * 22)}
		/>
	</DashboardCard>

	<!-- CPF vs CNPJ — full width -->
	<DashboardCard title="Pessoa Física vs Jurídica" subtitle="Distribuição de beneficiários e recursos por tipo de documento">
		<div class="cpf-cnpj-grid">
			<div class="mini-metric">
				<span class="mini-value">{fmtPct(percBenefCPF)}</span>
				<span class="mini-label">Beneficiários CPF</span>
			</div>
			<div class="mini-metric">
				<span class="mini-value">{fmtPct(percBenefCNPJ)}</span>
				<span class="mini-label">Beneficiários CNPJ</span>
			</div>
			<div class="mini-metric">
				<span class="mini-value">{fmtPct(percValorCPF)}</span>
				<span class="mini-label">Valor para CPF</span>
			</div>
			<div class="mini-metric">
				<span class="mini-value">{fmtPct(percValorCNPJ)}</span>
				<span class="mini-label">Valor para CNPJ</span>
			</div>
		</div>
		<HorizontalStackedBarChartCustom
			data={benefVsValorData}
			keys={['cpf', 'cnpj']}
			labels={{ cpf: 'CPF (Pessoa Física)', cnpj: 'CNPJ (Pessoa Jurídica)' }}
			colors={[colorScales.blue[2], colorScales.orange[2]]}
			height={120}
		/>
	</DashboardCard>

	<!-- Territórios especiais — full width -->
	<DashboardCard title="Territórios especiais" subtitle="Participação dos territórios especiais na distribuição de recursos">
		<div class="special-table">
			<table>
				<thead>
					<tr>
						<th>Território</th>
						<th>% Recurso</th>
						<th>% Agentes</th>
						<th>% Pop.</th>
					</tr>
				</thead>
				<tbody>
					{#each specialTerritoriesMetrics as t}
						<tr>
							<td>{t.shortLabel}</td>
							<td>{fmtPct(t.perc_recurso)}</td>
							<td>{fmtPct(t.perc_agentes)}</td>
							<td>{fmtPct(t.perc_populacao)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</DashboardCard>

	<!-- Agentes por região — full width -->
	<DashboardCard title="Agentes culturais vs população por região" subtitle="Comparação entre a distribuição de agentes contemplados e a distribuição da população">
		<HorizontalGroupedBarChart
			data={regiaoGroupedData}
			seriesLabels={['% agentes contemplados', '% população']}
			colors={[colorPairs.purpleYellow[0], colorPairs.purpleYellow[1]]}
			format={(v: number) => fmtPct(v)}
			margin={{ top: 30, right: 90, bottom: 60, left: 140 }}
			barHeight={22}
			barPad={6}
			rx={0}
			legendBottom={true}
			labelsInside={true}
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



	.cpf-cnpj-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.75rem;
		margin-bottom: 1rem;
	}

	.mini-metric {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 0.5rem;
		background: transparent;
		border-radius: 0.5rem;
		border: 1px solid rgba(0, 0, 0, 0.07);
	}

	.mini-value {
		font-size: 1.3rem;
		font-weight: 700;
		color: #1351B4;
	}

	.mini-label {
		font-size: 0.72rem;
		color: #666;
		text-align: center;
	}

	.special-table table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.82rem;
	}

	.special-table th {
		text-align: left;
		font-weight: 600;
		color: #666;
		font-size: 0.72rem;
		text-transform: uppercase;
		padding: 0.5rem 0.75rem;
		border-bottom: 2px solid #e0e0e0;
	}

	.special-table td {
		padding: 0.4rem 0.75rem;
		border-bottom: 1px solid #f0f0f0;
		color: #333;
	}

	.special-table tr:hover {
		background: #f8f8f8;
	}

	.rural-highlight {
		margin-bottom: 1rem;
		text-align: center;
	}

</style>
