<script lang="ts">
	import DashboardFilterBar from '$lib/components/DashboardFilterBar.svelte';
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import { createDashboardFilters, VISAO_LABELS } from '$lib/stores/dashboardFilters.svelte';
	import { colorScales } from 'sniic-design-system';
	import BigNumberStat from '$lib/components/BigNumberStat.svelte';
	import {
		docByVisao,
		stackedData,
		docStackedKeys,
		docStackedLabels,
		type DocVisao,
	} from '$lib/data/section7';

	const filters = createDashboardFilters();

	// ── Formatters ────────────────────────────────────────────────────────────
	const fmtBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency', currency: 'BRL',
			notation: 'compact', maximumFractionDigits: 1,
		}).format(v);
	const fmtNum = (v: number) => v.toLocaleString('pt-BR');
	const fmtPct = (v: number) => v.toFixed(1).replace('.', ',') + '%';

	// ── Active visão ────────────────────────────────────────────────────────────
	const data = $derived(docByVisao[filters.visao as DocVisao]);
	const chartData = $derived(stackedData(data));

	const cpfCnpjColors = [colorScales.blue[2], colorScales.yellow[2]]; // cpf, cnpj
</script>

<section class="section-band">
	<div class="section">
	<header class="sec-header">
		<p class="eyebrow">Gráfico 7</p>
		<h2>Beneficiários e recursos por tipo de documento</h2>
		<p class="lead">
			Distribuição entre <strong>CPF</strong> (pessoas físicas) e <strong>CNPJ</strong>
			(pessoas jurídicas). As pessoas jurídicas concentram
			<strong>{fmtPct(data.cnpj.percValor)}</strong> dos recursos, mas representam apenas
			<strong>{fmtPct(data.cnpj.percContemplados)}</strong> dos contemplados — enquanto as
			pessoas físicas são <strong>{fmtPct(data.cpf.percContemplados)}</strong> dos contemplados
			com <strong>{fmtPct(data.cpf.percValor)}</strong> dos recursos.
		</p>
	</header>

	<DashboardFilterBar
		{filters}
		visoes={['uf', 'estados', 'municipios']}
		showRegiao={false}
		showUf={false}
		labelColor="#f0d8ec"
	/>

	<div class="scope-tag">{VISAO_LABELS[filters.visao]}</div>

	<!-- ── Big numbers ─────────────────────────────────────────────────────── -->
	<div class="bn-grid">
		<div class="stat">
			<BigNumberStat value={fmtNum(data.totalContemplados)} label="contemplados" fontSize={44} shadowDepth={4} width={360} labelColor="#f0d8ec" />
		</div>
		<div class="stat">
			<BigNumberStat value={fmtBRL(data.totalValor)} label="valor executado" fontSize={44} shadowDepth={4} width={360} labelColor="#f0d8ec" />
		</div>
	</div>

	<!-- ── Stacked bar (100%) ──────────────────────────────────────────────── -->
	<div class="chart-card">
		<HorizontalStackedBarChartCustom
			data={chartData}
			keys={[...docStackedKeys]}
			labels={docStackedLabels}
			colors={cpfCnpjColors}
			format={fmtPct}
			marginLeft={150}
			legendAlign="left"
			axisColor="#f0d8ec"
		/>
	</div>
	</div>
</section>

<style>
	.section-band {
		background: #a44c7f;
	}

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
		color: #f0d8ec;
		margin: 0 0 0.4rem;
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
		color: #f0d8ec;
		margin: 0;
		line-height: 1.5;
		max-width: 70ch;
	}

	.scope-tag {
		display: inline-block;
		font-size: 0.74rem;
		font-weight: 600;
		color: #f0d8ec;
		background: rgba(255, 255, 255, 0.14);
		padding: 0.3rem 0.7rem;
		border-radius: 0;
		margin-bottom: 1rem;
	}

	.bn-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.stat {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.2rem;
	}

	.chart-card {
		border-radius: 0;
		padding: 1.25rem 1.5rem 1rem;
	}

	@media (max-width: 720px) {
		.bn-grid {
			grid-template-columns: 1fr;
		}
		.sec-header h2 {
			font-size: 1.4rem;
		}
	}
</style>
