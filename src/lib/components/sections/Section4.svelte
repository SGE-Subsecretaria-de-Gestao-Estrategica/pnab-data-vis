<script lang="ts">
	import DashboardCard from '$lib/components/DashboardCard.svelte';
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import {
		TreemapChart,
		HorizontalBarChart,
		BigNumber,
		colorScales,
	} from 'sniic-design-system';
	import {
		expensesGrandTotal,
		expensesLegendItems,
		fomentoDomainsTreemap, fomentoDomainsRows,
		fomentoSubData,
		pncvSubData,
		pncvOuOutrosData, pncvOuOutrosKeys, pncvOuOutrosLabels,
		tipoExecRegiaoData, tipoExecRegiaoKeys, tipoExecRegiaoLabels,
		pncvNatJuridicaData, pncvNatJuridicaKeys, pncvNatJuridicaLabels,
		modalidadeObrasData,
		operacionalizacaoSubData,
	} from '$lib/data/section6';

	const fmtBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency', currency: 'BRL',
			notation: 'compact', maximumFractionDigits: 1,
		}).format(v);
	const fmtPct = (v: number) => v.toFixed(1).replace('.', ',') + '%';

	const CAT_COLORS: Record<string, string> = {
		fomento: '#1351B4',
		cultura_viva: '#168821',
		subsidio: '#E5A000',
		obras: '#D94B2C',
		operacionalizacao: '#8B5CF6',
		vazio: '#9CA3AF',
		outros_cat: '#6B7280',
	};

	function getCatColor(key: string): string {
		return CAT_COLORS[key] ?? '#999';
	}

	let catTab = $state(0);
	let detailTab = $state(0);
</script>

<section id="section-4" class="dashboard">
	<div class="dashboard-header">
		<h2>Classificação das Despesas</h2>
		<p class="lead">Como os recursos da PNAB foram utilizados? Estimativas com intervalos de confiança de 95%.</p>
	</div>

	<!-- Categorias de despesa -->
	<DashboardCard title="Categorias de despesa" subtitle="Valor estimado por categoria (com intervalo de confiança de 95%)">
		<div class="expense-table">
			<table>
				<thead>
					<tr>
						<th>Categoria</th>
						<th class="col-val">Valor estimado</th>
						<th class="col-ci">IC 95%</th>
					</tr>
				</thead>
				<tbody>
					{#each expensesLegendItems as item}
						<tr>
							<td>
								<span class="cat-dot" style:background={getCatColor(item.key)}></span>
								{item.label}
							</td>
							<td class="col-val">{item.value}</td>
							<td class="col-ci ref">{item.ci}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</DashboardCard>

	<!-- Domínios de Fomento Cultural -->
	<DashboardCard title="Domínios de Fomento Cultural" subtitle="Treemap dos domínios culturais financiados">
		<TreemapChart data={fomentoDomainsTreemap} height={350} />
	</DashboardCard>

	<!-- Subcategorias -->
	<DashboardCard
		title="Detalhamento por categoria"
		subtitle="Subcategorias de despesa"
		tabs={['Fomento Cultural', 'Cultura Viva (PNCV)']}
		activeTab={catTab}
		ontabchange={(i) => (catTab = i)}
	>
		{#if catTab === 0}
			<div class="sub-table">
				<table>
					<thead>
						<tr>
							<th>Subcategoria</th>
							<th class="col-val">Valor</th>
							<th class="col-pct">%</th>
						</tr>
					</thead>
					<tbody>
						{#each fomentoSubData as row}
							<tr>
								<td>{row.label}</td>
								<td class="col-val">{row.valorFormatted}</td>
								<td class="col-pct">{fmtPct(row.pct)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{:else}
			<div class="sub-table">
				<table>
					<thead>
						<tr>
							<th>Subcategoria</th>
							<th class="col-val">Valor</th>
							<th class="col-pct">%</th>
						</tr>
					</thead>
					<tbody>
						{#each pncvSubData as row}
							<tr>
								<td>{row.label}</td>
								<td class="col-val">{row.valorFormatted}</td>
								<td class="col-pct">{fmtPct(row.pct)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</DashboardCard>

	<!-- PNCV vs Outros -->
	<DashboardCard title="PNCV vs Outros investimentos" subtitle="Proporção por faixa de repasse municipal">
		<HorizontalStackedBarChartCustom
			data={pncvOuOutrosData}
			keys={[...pncvOuOutrosKeys]}
			labels={pncvOuOutrosLabels}
			colors={[colorScales.blue[2], colorScales.teal[2]]}
			height={160}
		/>
	</DashboardCard>

	<!-- Tipo de execução por região -->
	<DashboardCard title="Tipo de execução por região" subtitle="Ação Cultural, Bolsa e Premiação">
		<HorizontalStackedBarChartCustom
			data={tipoExecRegiaoData}
			keys={[...tipoExecRegiaoKeys]}
			labels={tipoExecRegiaoLabels}
			colors={[colorScales.blue[2], colorScales.orange[2], colorScales.lime[2]]}
			height={240}
		/>
	</DashboardCard>

	<!-- PNCV por natureza jurídica -->
	<DashboardCard title="PNCV por natureza do beneficiário" subtitle="Participação de CPF vs CNPJ nas modalidades PNCV">
		<HorizontalStackedBarChartCustom
			data={pncvNatJuridicaData}
			keys={[...pncvNatJuridicaKeys]}
			labels={pncvNatJuridicaLabels}
			colors={[colorScales.blue[2], colorScales.orange[2]]}
			height={120}
		/>
	</DashboardCard>

	<!-- Detalhamento adicional -->
	<DashboardCard
		title="Detalhamento adicional"
		subtitle="Obras e Operacionalização"
		tabs={['Obras e Reformas', 'Operacionalização']}
		activeTab={detailTab}
		ontabchange={(i) => (detailTab = i)}
	>
		{#if detailTab === 0}
			<div class="sub-table">
				<table>
					<thead>
						<tr>
							<th>Modalidade</th>
							<th class="col-val">Valor</th>
							<th class="col-pct">%</th>
						</tr>
					</thead>
					<tbody>
						{#each modalidadeObrasData as row}
							<tr>
								<td>{row.label}</td>
								<td class="col-val">{fmtBRL(row.valor)}</td>
								<td class="col-pct">{fmtPct(row.pct)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{:else}
			<div class="sub-table">
				<table>
					<thead>
						<tr>
							<th>Subcategoria</th>
							<th class="col-val">Valor</th>
							<th class="col-pct">%</th>
						</tr>
					</thead>
					<tbody>
						{#each operacionalizacaoSubData as row}
							<tr>
								<td>{row.label}</td>
								<td class="col-val">{fmtBRL(row.valor)}</td>
								<td class="col-pct">{fmtPct(row.pct)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
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

	.expense-table table,
	.sub-table table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.82rem;
	}

	.expense-table th,
	.sub-table th {
		text-align: left;
		font-weight: 600;
		color: #666;
		font-size: 0.72rem;
		text-transform: uppercase;
		padding: 0.5rem 0.5rem;
		border-bottom: 2px solid #e0e0e0;
	}

	.expense-table td,
	.sub-table td {
		padding: 0.4rem 0.5rem;
		border-bottom: 1px solid #f0f0f0;
		color: #333;
	}

	.expense-table tr:hover,
	.sub-table tr:hover {
		background: #f8f8f8;
	}

	.cat-dot {
		display: inline-block;
		width: 10px;
		height: 10px;
		border-radius: 50%;
		margin-right: 0.5rem;
		vertical-align: middle;
	}

	.col-val { text-align: right; width: 7rem; }
	.col-pct { text-align: right; width: 4rem; }
	.col-ci { text-align: right; width: 10rem; }
	.ref { color: #999; }
</style>
