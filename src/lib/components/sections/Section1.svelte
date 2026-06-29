<script lang="ts">
	import BrazilChoropleth from '$lib/components/BrazilChoropleth.svelte';
	import DashboardFilterBar from '$lib/components/DashboardFilterBar.svelte';
	import BigNumberStat from '$lib/components/BigNumberStat.svelte';
	import { createDashboardFilters, VISAO_LABELS } from '$lib/stores/dashboardFilters.svelte';
	import {
		siglaToName,
		regionMap,
		regionAgg,
		rowsByVisao,
	} from '$lib/data/dashboard';

	const filters = createDashboardFilters();

	// ── Formatters ────────────────────────────────────────────────────────────
	const fmtBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency', currency: 'BRL',
			notation: 'compact', maximumFractionDigits: 1,
		}).format(v);
	const fmtBRLfull = (v: number) =>
		new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }).format(v);
	const fmtNum = (v: number) => v.toLocaleString('pt-BR');
	const fmtPct = (v: number) => v.toFixed(1).replace('.', ',') + '%';

	// ── Current rows for the active visão ───────────────────────────────────────
	const rows = $derived(rowsByVisao[filters.visao]);

	// ── Map values (keyed by sigla) ─────────────────────────────────────────────
	const mapValues = $derived.by(() => {
		const out: Record<string, number> = {};
		if (filters.visao === 'regioes') {
			for (const sigla of Object.keys(siglaToName)) {
				out[sigla] = regionAgg[regionMap[sigla]]?.valor ?? 0;
			}
		} else {
			for (const [sigla, row] of Object.entries(rows)) out[sigla] = row.valor;
		}
		return out;
	});

	// UFs in scope (for dimming). null = all in scope.
	const inScope = $derived.by(() => {
		const hasFilter = filters.uf !== 'Todas' || filters.regiao !== 'Todas';
		return hasFilter ? new Set(filters.filteredUFs) : null;
	});

	// ── Aggregated panel metrics over the scoped UFs ──────────────────────────────
	const scoped = $derived.by(() => {
		const ufs = filters.filteredUFs;
		let valor = 0, repassado = 0, contemplados = 0, populacao = 0, numMunicipios = 0;
		for (const uf of ufs) {
			const r = rows[uf];
			if (!r) continue;
			valor += r.valor;
			repassado += r.repassado;
			contemplados += r.contemplados;
			populacao += r.populacao;
			numMunicipios += r.numeroMunicipios;
		}
		return { valor, repassado, contemplados, populacao, numMunicipios };
	});

	// % executado = valor executado / valor repassado pelo MinC.
	// Repassado pode estar indisponível na fonte (0) → exibe "—".
	const hasRepassado = $derived(scoped.repassado > 0);
	const pctExecutado = $derived(hasRepassado ? (scoped.valor / scoped.repassado) * 100 : 0);

	// Is the current scope the whole country?
	const isNacional = $derived(filters.uf === 'Todas' && filters.regiao === 'Todas');

	// ── "Número de entes" — exact where data allows, "—" otherwise ───────────────
	// `noun`/`adj` acompanham a seleção do filtro (ex.: "regiões contempladas").
	const entes = $derived.by((): { value: string; sub: string; noun: string; adj: string } => {
		const nUf = filters.filteredUFs.length;
		switch (filters.visao) {
			case 'estados':
				return { value: fmtNum(nUf), sub: nUf === 1 ? 'estado' : 'estados', noun: 'estados', adj: 'contemplados' };
			case 'regioes': {
				const n = filters.regiao === 'Todas' ? 5 : 1;
				return { value: fmtNum(n), sub: n === 1 ? 'região' : 'regiões', noun: 'regiões', adj: 'contempladas' };
			}
			case 'municipios': {
				const nMun = scoped.numMunicipios;
				return { value: fmtNum(nMun), sub: nMun === 1 ? 'município' : 'municípios', noun: 'municípios', adj: 'contemplados' };
			}
			case 'uf':
			default: {
				const nMun = scoped.numMunicipios;
				return {
					value: fmtNum(nUf + nMun),
					sub: `${nUf} ${nUf === 1 ? 'estado' : 'estados'} + ${fmtNum(nMun)} ${nMun === 1 ? 'município' : 'municípios'}`,
					noun: 'entes federativos',
					adj: 'contemplados',
				};
			}
		}
	});

	// ── Scope label ───────────────────────────────────────────────────────────
	const scopeLabel = $derived.by(() => {
		if (filters.uf !== 'Todas') return siglaToName[filters.uf] ?? filters.uf;
		if (filters.regiao !== 'Todas') return `Região ${filters.regiao}`;
		return 'Brasil';
	});
</script>

<section class="hero-band">
	<h1>COMO OS RECURSOS DA ALDIR BLANC FORAM DISTRIBUÍDOS NOS TERRITÓRIOS?</h1>
</section>

<section class="dashboard-band">
	<div class="dashboard">
	<header class="dash-header">
		<p class="lead">
			Distribuição dos recursos da Política Nacional Aldir Blanc (ciclo 1) pelo território brasileiro. Use os filtros para alterar a visualização e clique em um estado no mapa para detalhar. 
		</p>
		<p class="lead note">
			*O “Valor Repassado (R$)” não leva em consideração os rendimentos da conta
		</p>
	</header>

	<h2>Valores gerais da pesquisa</h2>

	<!-- ── Filter bar ───────────────────────────────────────────────────────── -->
	<DashboardFilterBar {filters} />

	<!-- ── Main grid: metrics left, map right ───────────────────────────────── -->
	<div class="grid">
		<div class="panel">
			<div class="scope-tag">{scopeLabel} · {VISAO_LABELS[filters.visao]}</div>

			<div class="stat-grid">
			<!-- Headline: contemplados + texto -->
			<div class="stat-row stat-contemplados">
				<BigNumberStat value={fmtNum(scoped.contemplados)} label="contemplados" fontSize={60} shadowDepth={6} width={340} shadowColor="#000000" labelColor="#1B1B1B" subtitleColor="#1B1B1B" />
			</div>

			<!-- Valor executado em destaque (big number) -->
			<div class="stat-row stat-executado">
				<BigNumberStat
					value={fmtBRL(scoped.valor)}
					label="valor executado"
					fontSize={50}
					shadowDepth={5}
					width={340}
					shadowColor="#000000"
					labelColor="#1B1B1B"
					subtitleColor="#1B1B1B"
				/>
			</div>

			<!-- Valor repassado pelo MinC (big number) -->
			<div class="stat-row stat-repassado">
				<BigNumberStat
					value={hasRepassado ? fmtBRL(scoped.repassado) : '—'}
					label="valor repassado pelo MinC"
					fontSize={44}
					shadowDepth={5}
					width={340}
					shadowColor="#000000"
					labelColor="#1B1B1B"
					subtitleColor="#1B1B1B"
				/>
			</div>

			<!-- % executado / repassado (big number) -->
			<div class="stat-row stat-pct">
				<BigNumberStat
					value={hasRepassado ? fmtPct(pctExecutado) : '—'}
					label="executado / repassado"
					fontSize={44}
					shadowDepth={5}
					width={340}
					shadowColor="#000000"
					labelColor="#1B1B1B"
					subtitleColor="#1B1B1B"
				/>
			</div>

			<!-- Entes federativos (rótulo acompanha a seleção do filtro) + texto -->
			<div class="stat-row stat-entes">
				<BigNumberStat
					value={entes.value}
					label="{entes.noun} {entes.adj}"
					subtitle={entes.sub}
					fontSize={50}
					shadowDepth={5}
					width={340}
					shadowColor="#000000"
					labelColor="#1B1B1B"
					subtitleColor="#1B1B1B"
				/>
			</div>
			</div>
		</div>

		<div class="map-wrap">
			<BrazilChoropleth
				values={mapValues}
				format={fmtBRL}
				metricLabel="Valor executado"
				selected={filters.visao === 'regioes' ? 'Todas' : filters.uf}
				inScope={inScope}
				onselect={(sigla) => filters.selectUf(sigla)}
			/>
			<p class="map-caption">Cor proporcional ao valor executado. Clique para detalhar.</p>
		</div>
	</div>
	</div>
</section>

<style>
	/* Hero full-bleed: a pergunta-título ocupa toda a viewport antes do painel. */
	.hero-band {
		min-height: 40vh;
		min-height: 40svh;
		display: flex;
		align-items: center;
		padding: 2rem 0;
		box-sizing: border-box;
		background: #1351B4;
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

	/* Faixa full-bleed com o amarelo principal do SNIIC. */
	.dashboard-band {
	}

	.dashboard {
		max-width: 1200px;
		margin: 0 auto;
		padding: 3rem 2rem 5rem;
	}

	.dash-header {
		margin-bottom: 2rem;
	}

	.lead {
		font-size: 1rem;
		color: #1B1B1B;
		margin: 0;
		line-height: 1.5;
		max-width: 60ch;
	}

	.lead + .lead {
		margin-top: 0.75rem;
	}

	.lead.note {
		font-size: 0.875rem;
		color: #1B1B1B;
		font-style: italic;
	}

	/* ── Grid ── */
	.grid {
		display: grid;
		grid-template-columns: 1.35fr 1fr;
		gap: 2rem;
		align-items: start;
	}

	.panel {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		min-width: 0;
	}

	/* ── Big numbers em grid (desktop): headline em destaque + 2×2 abaixo ── */
	.stat-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1.5rem 1.75rem;
		align-items: start;
	}

	/* O número de contemplados é a manchete: ocupa as duas colunas. */
	.stat-contemplados {
		grid-column: 1 / -1;
	}

	.stat-row {
		min-width: 0;
	}

	.panel-text {
		display: flex;
		flex-direction: column;
		gap: 0.85rem;
	}

	.panel-text p {
		margin: 0;
		font-size: 0.92rem;
		line-height: 1.6;
		color: #1B1B1B;
		font-weight: 400;
		text-align: justify;
	}

	.scope-tag {
		display: inline-block;
		align-self: flex-start;
		font-size: 0.74rem;
		font-weight: 600;
		color: #1B1B1B;
		background: rgba(19, 81, 180, 0.08);
		padding: 0.3rem 0.7rem;
		border-radius: 0;
	}

	/* ── Map ── */
	.map-wrap {
		position: sticky;
		top: 1rem;
	}

	.map-caption {
		text-align: center;
		font-size: 0.74rem;
		color: #1B1B1B;
		margin: 0.5rem 0 0;
	}

	/* ── Responsive ── */
	@media (max-width: 860px) {
		.grid {
			grid-template-columns: 1fr;
			row-gap: 1rem;
		}
		/* Achata painel e grid de big numbers para que cada bloco possa ser
		   reordenado individualmente em relação ao mapa. */
		.panel,
		.stat-grid {
			display: contents;
		}
		.stat-contemplados { order: -2; }
		.map-wrap {
			position: static;
			order: -1;
		}
		.scope-tag { order: 0; }
		.stat-executado { order: 1; }
		.stat-repassado { order: 2; }
		.stat-pct { order: 3; }
		.stat-entes { order: 4; }
	}

	/* Telas estreitas (ex.: 320px): reduz o respiro lateral. */
	@media (max-width: 520px) {
		.dashboard {
			padding: 2rem 1rem 3rem;
		}
		.hero-band h1 {
			padding: 0 1rem;
		}
	}
</style>
