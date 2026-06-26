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

<section class="section">
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
	/>

	<div class="scope-tag">{VISAO_LABELS[filters.visao]}</div>

	<!-- ── Big numbers ─────────────────────────────────────────────────────── -->
	<div class="bn-grid">
		<div class="stat">
			<BigNumberStat value={fmtNum(data.totalContemplados)} label="contemplados" fontSize={44} shadowDepth={4} width={360} />
			<span class="bn-split">
				<span style:color={cpfCnpjColors[0]}>CPF {fmtNum(data.cpf.contemplados)}</span>
				<span style:color={cpfCnpjColors[1]}>CNPJ {fmtNum(data.cnpj.contemplados)}</span>
			</span>
		</div>
		<div class="stat">
			<BigNumberStat value={fmtBRL(data.totalValor)} label="valor executado" fontSize={44} shadowDepth={4} width={360} />
			<span class="bn-split">
				<span style:color={cpfCnpjColors[0]}>CPF {fmtBRL(data.cpf.valor)}</span>
				<span style:color={cpfCnpjColors[1]}>CNPJ {fmtBRL(data.cnpj.valor)}</span>
			</span>
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
		color: #1351b4;
		margin: 0 0 0.4rem;
	}

	.sec-header h2 {
		font-size: 1.6rem;
		font-weight: 800;
		color: #1b1b1b;
		margin: 0 0 0.4rem;
		line-height: 1.15;
	}

	.lead {
		font-size: 0.98rem;
		color: #555;
		margin: 0;
		line-height: 1.5;
		max-width: 70ch;
	}

	.scope-tag {
		display: inline-block;
		font-size: 0.74rem;
		font-weight: 600;
		color: #1351b4;
		background: rgba(19, 81, 180, 0.08);
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

	.bn-split {
		display: flex;
		gap: 1rem;
		margin-top: 0.35rem;
		font-size: 0.78rem;
		font-weight: 700;
		font-variant-numeric: tabular-nums;
	}

	.chart-card {
		border: 1px solid rgba(0, 0, 0, 0.1);
		border-radius: 0;
		padding: 1.25rem 1.5rem 1rem;
		background: rgba(255, 255, 255, 0.45);
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
