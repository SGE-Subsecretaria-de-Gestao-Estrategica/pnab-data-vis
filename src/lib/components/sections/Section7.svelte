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

	// teal/amarelo se destacam bem sobre o roxo da seção.
	const cpfCnpjColors = [colorScales.teal[2], colorScales.yellow[2]]; // cpf, cnpj
</script>

<!-- Abertura da Seção 2 (público alcançado): título em "big number" sobre o roxo,
     espelhando a hero da Seção 1. -->
<section class="hero-band">
	<h1>
		QUEM ACESSOU OS RECURSOS DA POLÍTICA NACIONAL ALDIR BLANC?
	</h1>
</section>

<section class="section-band">
	<div class="section">
	<header class="sec-header">
		<h2>Beneficiários e recursos por tipo de documento</h2>
		<p class="lead">
			Participação de pessoas físicas (CPF) e pessoas jurídicas (CNPJ) no total de recursos recebidos e no número total de contemplados.
		</p>
	</header>

	<DashboardFilterBar
		{filters}
		visoes={['uf', 'estados', 'municipios']}
		showRegiao={false}
		showUf={false}
		labelColor="#000000"
	/>

	<div class="scope-tag">{VISAO_LABELS[filters.visao]}</div>

	<!-- ── Big numbers ─────────────────────────────────────────────────────── -->
	<div class="bn-grid">
		<div class="stat">
			<BigNumberStat value={fmtNum(data.totalContemplados)} label="contemplados" fontSize={44} shadowDepth={4} width={360} labelColor="#000000" shadowColor="#000000" />
		</div>
		<div class="stat">
			<BigNumberStat value={fmtBRL(data.totalValor)} label="valor executado" fontSize={44} shadowDepth={4} width={360} labelColor="#000000" shadowColor="#000000" />
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
			axisColor="#000000"
		/>
	</div>
	</div>
</section>

<style>
	/* Hero full-bleed roxo: abre a Seção 2 com o título em "big number"
	   (preenchimento branco + sombra 3D preta, igual aos números da seção). */
	.hero-band {
		min-height: 40vh;
		min-height: 40svh;
		display: flex;
		align-items: center;
		padding: 2rem 0;
		box-sizing: border-box;
		background: #265c4f;
	}

	.hero-band h1 {
		width: 100%;
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 2rem;
		box-sizing: border-box;
		font-size: clamp(1.6rem, 4vw, 3rem);
		font-weight: 800;
		line-height: 1.25;
		letter-spacing: -0.02em;
		text-align: left;
		/* Estilo "big number": preenchimento branco + sombra 3D preta extrudada,
		   replicando o contorno + degraus diagonais do componente BigNumber. */
		color: #ffffff;
		text-shadow:
			-2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000,
			0 -2px 0 #000, 0 2px 0 #000, -2px 0 0 #000, 2px 0 0 #000,
			1px 1px 0 #000, 2px 2px 0 #000, 3px 3px 0 #000, 4px 4px 0 #000,
			5px 5px 0 #000, 6px 6px 0 #000, 7px 7px 0 #000, 8px 8px 0 #000;
	}

	.section-band {
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
		max-width: 70ch;
	}

	.scope-tag {
		display: inline-block;
		font-size: 0.74rem;
		font-weight: 600;
		color: #1B1B1B;
		background: rgba(0, 0, 0, 0.06);
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
		.hero-band h1 {
			padding: 0 1rem;
		}
	}
</style>
