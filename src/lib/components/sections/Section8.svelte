<script lang="ts">
	import DonutChartWithLegend from '$lib/components/DonutChartWithLegend.svelte';
	import PyramidChartCustom from '$lib/components/PyramidChartCustom.svelte';
	import { colorScales } from 'sniic-design-system';
	import {
		totalPF,
		valorTotalPF,
		sexoQuantityDonutData,
		sexoValueDonutData,
		sexoPropFeminino,
		sexoPropMasculino,
		pyramidData,
		pyramidValueData,
	} from '$lib/data/section3';

	// ── Metric filter ─────────────────────────────────────────────────────────
	type Metric = 'contemplados' | 'valor';
	let metric = $state<Metric>('contemplados');

	// ── Formatters ────────────────────────────────────────────────────────────
	const fmtBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency', currency: 'BRL',
			notation: 'compact', maximumFractionDigits: 1,
		}).format(v);
	const fmtNum = (v: number) => v.toLocaleString('pt-BR');
	const fmtPct = (v: number) => (v * 100).toFixed(1).replace('.', ',') + '%';

	// ── Derived chart inputs ──────────────────────────────────────────────────
	const isValor = $derived(metric === 'valor');
	const donutData = $derived(isValor ? sexoValueDonutData : sexoQuantityDonutData);
	const pyData = $derived(isValor ? pyramidValueData : pyramidData);
	const fmt = $derived(isValor ? fmtBRL : fmtNum);

	const centerValue = $derived(isValor ? fmtBRL(valorTotalPF) : fmtNum(totalPF));
	const centerLabel = $derived(isValor ? 'valor executado' : 'agentes');

	// Feminino = azul, Masculino = amarelo (mesmo padrão dos demais gráficos de sexo)
	const donutColors = [colorScales.blue[2], colorScales.yellow[2]]; // [Feminino, Masculino]
	const pyramidColors: [string, string] = [colorScales.yellow[2], colorScales.blue[2]]; // [Masc, Fem]
</script>

<section class="section">
	<header class="sec-header">
		<p class="eyebrow">Gráfico 8</p>
		<h2>Distribuição por gênero</h2>
		<p class="lead">
			Perfil dos agentes culturais pessoa física contemplados pela Aldir Blanc. As mulheres
			representam <strong>{fmtPct(sexoPropFeminino)}</strong> dos contemplados e os homens
			<strong>{fmtPct(sexoPropMasculino)}</strong>. Alterne entre número de contemplados e valor
			executado.
		</p>
	</header>

	<!-- ── Metric filter ───────────────────────────────────────────────────── -->
	<div class="filter-bar" role="group" aria-label="Métrica">
		<span class="filter-label">Métrica</span>
		<div class="seg">
			<button class="seg-btn" class:active={metric === 'contemplados'} onclick={() => (metric = 'contemplados')}>
				Nº de contemplados
			</button>
			<button class="seg-btn" class:active={metric === 'valor'} onclick={() => (metric = 'valor')}>
				Valor executado
			</button>
		</div>
	</div>

	<div class="grid">
		<div class="chart-card">
			<h3 class="chart-title">Contemplados por sexo</h3>
			<DonutChartWithLegend
				data={donutData}
				colors={donutColors}
				centerValue={centerValue}
				centerLabel={centerLabel}
				format={fmt}
				height={360}
			/>
		</div>

		<div class="chart-card">
			<h3 class="chart-title">Pirâmide etária por sexo</h3>
			<PyramidChartCustom
				data={pyData}
				leftLabel="Masculino"
				rightLabel="Feminino"
				colors={pyramidColors}
				format={fmt}
				height={400}
				centerGap={96}
			/>
		</div>
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

	.filter-bar {
		display: flex;
		align-items: center;
		gap: 0.85rem;
		padding: 1rem 1.25rem;
		background: rgba(19, 81, 180, 0.04);
		border: 1px solid rgba(19, 81, 180, 0.12);
		border-radius: 0.75rem;
		margin-bottom: 1.75rem;
	}

	.filter-label {
		font-size: 0.68rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: #666;
	}

	.seg {
		display: inline-flex;
		border: 1px solid #ccc;
		border-radius: 0.5rem;
		overflow: hidden;
		background: white;
	}

	.seg-btn {
		font-family: inherit;
		font-size: 0.85rem;
		font-weight: 500;
		padding: 0.45rem 0.95rem;
		border: none;
		background: white;
		color: #555;
		cursor: pointer;
	}

	.seg-btn + .seg-btn {
		border-left: 1px solid #ccc;
	}

	.seg-btn.active {
		background: #1351b4;
		color: white;
		font-weight: 600;
	}

	.seg-btn:hover:not(.active) {
		background: rgba(19, 81, 180, 0.06);
	}

	.grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
		align-items: start;
	}

	.chart-card {
		border: 1px solid rgba(0, 0, 0, 0.1);
		border-radius: 0.75rem;
		padding: 1.25rem 1.5rem 1rem;
		background: rgba(255, 255, 255, 0.45);
	}

	.chart-title {
		margin: 0 0 0.75rem;
		font-size: 1rem;
		font-weight: 700;
		color: #1b1b1b;
	}

	@media (max-width: 860px) {
		.grid {
			grid-template-columns: 1fr;
		}
		.sec-header h2 {
			font-size: 1.4rem;
		}
	}
</style>
