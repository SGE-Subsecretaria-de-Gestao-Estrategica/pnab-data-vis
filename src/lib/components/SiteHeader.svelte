<script lang="ts">
	import { blue } from 'sniic-design-system';
	import { base } from '$app/paths';
	import TopTabs from './TopTabs.svelte';

	type Topic = { key: string; label: string; children: { id: string; label: string }[] };

	// Três seções da pesquisa (h1); as subseções são as frases dos h2 de cada bloco.
	const sections: Topic[] = [
		{
			key: 'territorios',
			label: 'COMO OS RECURSOS DA ALDIR BLANC FORAM DISTRIBUÍDOS NOS TERRITÓRIOS?',
			children: [
				{ id: 'sec-1', label: 'Valores gerais da pesquisa' },
				{ id: 'sec-1-percapita', label: 'Valor per capita por estado' },
				{ id: 'sec-1-faixa', label: 'Distribuição por faixa de valor' },
				{ id: 'sec-1-urbano-rural', label: 'Território urbano × rural por estado' },
				{ id: 'sec-1-capital-interior', label: 'Distribuição de recursos: capital, metropolitana e interior' },
				{ id: 'sec-1-porte', label: 'Distribuição do recurso por porte municipal' }
			]
		},
		{
			key: 'acesso',
			label: 'QUEM ACESSOU OS RECURSOS DA POLÍTICA NACIONAL ALDIR BLANC?',
			children: [
				{ id: 'sec-2', label: 'Beneficiários e recursos por tipo de documento' },
				{ id: 'sec-3', label: 'Distribuição por gênero' },
				{ id: 'sec-4', label: 'Contemplados PJ por tipo de organização' }
			]
		},
		{
			key: 'acoes',
			label: 'QUAIS AÇÕES CULTURAIS FORAM APOIADAS COM OS RECURSOS DA ALDIR BLANC?',
			children: [
				{ id: 'sec-5', label: 'Distribuição de recursos por tipo de despesa' }
			]
		}
	];

	let menuOpen = $state(false);
	let openGroup = $state<string | null>(null);

	function go(id: string) {
		menuOpen = false;
		openGroup = null;
		document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
	}

	function toggleGroup(key: string) {
		openGroup = openGroup === key ? null : key;
	}
</script>

<header class="site-header" style:--accent={blue}>
	<div class="inner">
		<div class="brand">
			<h1 class="brand-title">
				Painel de Dados SNIIC: Avaliação de Resultados da Política Nacional Aldir Blanc de Fomento à Cultura
			</h1>
			<p class="lead">
				Este Painel de Dados SNIIC disponibiliza os principais números da pesquisa “Resultados do Primeiro Ciclo da Política Nacional Aldir Blanc de Fomento à Cultura: recursos distribuídos, agentes contemplados e ações fomentadas”. Por meio de gráficos interativos e filtros de consulta, a ferramenta possibilita a visualização e a análise dos dados sobre a execução do Ciclo 1 da política em diferentes recortes e perspectivas. Os microdados também estão descritos e disponíveis na aba "Dados abertos".
			</p>
		</div>

		<!-- Desktop: seções à direita, submenu abre abaixo do título ao clicar -->
		<nav class="topics" aria-label="Seções da pesquisa">
			{#each sections as s}
				<div class="topic-group" class:open={openGroup === s.key}>
					<button
						class="topic-parent"
						aria-expanded={openGroup === s.key}
						onclick={() => toggleGroup(s.key)}
					>
						<span>{s.label}</span>
						<span class="chev" class:open={openGroup === s.key} aria-hidden="true"></span>
					</button>
					{#if openGroup === s.key}
						<div class="submenu">
							{#each s.children as c}
								<a href={'#' + c.id} onclick={(e) => { e.preventDefault(); go(c.id); }}>{c.label}</a>
							{/each}
						</div>
					{/if}
				</div>
			{/each}
		</nav>

		<!-- Mobile: botão que abre o menu -->
		<button
			class="menu-toggle"
			aria-expanded={menuOpen}
			aria-controls="mobile-menu"
			onclick={() => (menuOpen = !menuOpen)}
		>
			<span class="menu-toggle-label">{menuOpen ? 'Fechar' : 'Seções'}</span>
			<span class="menu-toggle-icon" class:open={menuOpen} aria-hidden="true"></span>
		</button>
	</div>

	<!-- Mobile: menu abaixo do título, com subseções expansíveis -->
	{#if menuOpen}
		<nav id="mobile-menu" class="mobile-menu" aria-label="Seções da pesquisa">
			{#each sections as s}
				<div class="m-group">
					<button
						class="m-parent"
						aria-expanded={openGroup === s.key}
						onclick={() => toggleGroup(s.key)}
					>
						<span>{s.label}</span>
						<span class="chev" class:open={openGroup === s.key} aria-hidden="true"></span>
					</button>
					{#if openGroup === s.key}
						<div class="m-sub">
							{#each s.children as c}
								<a href={'#' + c.id} onclick={(e) => { e.preventDefault(); go(c.id); }}>{c.label}</a>
							{/each}
						</div>
					{/if}
				</div>
			{/each}
		</nav>
	{/if}

	<div class="brand-logo-wrap">
		<img
			class="brand-logo"
			src="{base}/logos/aldir_horizontal_color.png"
			alt="Política Nacional Aldir Blanc"
		/>
	</div>
</header>

<TopTabs active="painel" />

<style>
	.site-header {
		border-bottom: 1px solid #e5e9f0;
		background: #ffffff;
	}

	.inner {
		max-width: 1200px;
		margin: 0 auto;
		padding: 5rem 2rem;
		min-height: 60vh;
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 2rem;
	}

	/* ── Brand / título ── */
	.brand {
		flex-shrink: 0;
		max-width: 540px;
	}

	.brand-title {
		margin: 0 0 1.5rem;
		font-size: clamp(1.5rem, 2.4vw, 2.1rem);
		font-weight: 700;
		line-height: 1.25;
		color: #1B1B1B;
	}

	.brand-logo-wrap {
		display: flex;
		justify-content: center;
		padding: 0 2rem 3rem;
		max-width: 1200px;
		margin: 0 auto;
	}

	.brand-logo {
		display: block;
		width: clamp(280px, 42vw, 480px);
		height: auto;
	}

	.lead {
		font-size: 1rem;
		color: #555;
		line-height: 1.5;
		margin: 0.6rem 0 0;
		max-width: 46ch;
	}

	/* ── Seções (desktop) ── */
	.topics {
		display: flex;
		flex-direction: column;
		align-items: stretch;
		gap: 0.5rem;
		width: 320px;
		flex-shrink: 0;
	}

	.topic-group {
		display: flex;
		flex-direction: column;
	}

	.topic-parent {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 0.6rem;
		width: 100%;
		background: none;
		border: none;
		padding: 0.5rem 0;
		text-align: left;
		cursor: pointer;
		font-size: 0.9rem;
		font-weight: 700;
		line-height: 1.25;
		color: #000000;
		transition: color 0.15s ease;
	}

	.topic-parent:hover,
	.topic-group.open .topic-parent {
		color: var(--accent);
	}

	/* ── Submenu (abre abaixo, inline) ── */
	.submenu {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		padding: 0.3rem 0 0.6rem 0.9rem;
		border-left: 2px solid #e5e9f0;
		margin-left: 0.2rem;
	}

	.submenu a {
		font-size: 0.88rem;
		font-weight: 500;
		line-height: 1.3;
		color: #333;
		text-decoration: none;
		transition: color 0.15s ease;
	}

	.submenu a:hover {
		color: var(--accent);
	}

	/* Seta indicadora (gira ao abrir) */
	.chev {
		flex-shrink: 0;
		margin-top: 0.25rem;
		width: 8px;
		height: 8px;
		border-right: 2px solid currentColor;
		border-bottom: 2px solid currentColor;
		transform: rotate(45deg);
		transition: transform 0.15s ease;
		opacity: 0.6;
	}
	.chev.open {
		transform: rotate(-135deg);
	}

	/* ── Toggle (mobile) ── */
	.menu-toggle {
		display: none;
		align-items: center;
		gap: 0.5rem;
		background: none;
		border: 1px solid #d5dceb;
		padding: 0.45rem 0.8rem;
		cursor: pointer;
		color: var(--accent);
		font-size: 0.85rem;
		font-weight: 700;
	}

	.menu-toggle-icon {
		position: relative;
		width: 16px;
		height: 2px;
		background: currentColor;
		transition: background 0.15s ease;
	}
	.menu-toggle-icon::before,
	.menu-toggle-icon::after {
		content: '';
		position: absolute;
		left: 0;
		width: 16px;
		height: 2px;
		background: currentColor;
		transition: transform 0.15s ease;
	}
	.menu-toggle-icon::before { top: -5px; }
	.menu-toggle-icon::after { top: 5px; }
	.menu-toggle-icon.open { background: transparent; }
	.menu-toggle-icon.open::before { transform: translateY(5px) rotate(45deg); }
	.menu-toggle-icon.open::after { transform: translateY(-5px) rotate(-45deg); }

	/* ── Menu (mobile) ── */
	.mobile-menu {
		display: none;
		flex-direction: column;
		padding: 0 2rem 1.25rem;
		max-width: 1200px;
		margin: 0 auto;
	}

	.m-parent {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 0.6rem;
		width: 100%;
		padding: 0.85rem 0;
		border: none;
		border-top: 1px solid #eef1f6;
		font-size: 1.05rem;
		font-weight: 700;
		line-height: 1.25;
		color: #1B1B1B;
		background: none;
		text-align: left;
		cursor: pointer;
	}
	.m-parent:hover {
		color: var(--accent);
	}

	.m-sub {
		display: flex;
		flex-direction: column;
		padding: 0 0 0.6rem 1rem;
		border-left: 2px solid #eef1f6;
		margin: 0 0 0.4rem 0.2rem;
	}
	.m-sub a {
		padding: 0.55rem 0;
		font-size: 1rem;
		font-weight: 500;
		line-height: 1.3;
		color: #555;
		text-decoration: none;
	}
	.m-sub a:hover {
		color: var(--accent);
	}

	/* ── Responsivo ── */
	@media (max-width: 860px) {
		.inner {
			padding: 3rem 1.5rem;
			min-height: 45vh;
			align-items: center;
			gap: 1rem;
		}
		.brand {
			/* Permite encolher para não empurrar o botão para fora da viewport. */
			flex: 1 1 auto;
			min-width: 0;
			max-width: 100%;
		}
		.menu-toggle {
			flex-shrink: 0;
		}
		.topics {
			display: none;
		}
		.menu-toggle {
			display: inline-flex;
		}
		.mobile-menu {
			display: flex;
		}
	}
</style>
