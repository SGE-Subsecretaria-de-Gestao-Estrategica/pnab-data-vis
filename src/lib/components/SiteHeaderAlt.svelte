<script lang="ts">
	import { blue } from 'sniic-design-system';

	// Tópicos do menu — cada um aponta para o id da seção correspondente.
	const sections = [
		{ id: 'sec-1', label: 'Valores gerais' },
		{ id: 'sec-1-percapita', label: 'Per capita' },
		{ id: 'sec-1-faixa', label: 'Faixa de valor' },
		{ id: 'sec-1-urbano-rural', label: 'Urbano e rural' },
		{ id: 'sec-1-capital-interior', label: 'Capital e interior' },
		{ id: 'sec-1-porte', label: 'Porte municipal' },
		{ id: 'sec-2', label: 'Tipo de documento' },
		{ id: 'sec-3', label: 'Gênero' },
		{ id: 'sec-4', label: 'Tipo de organização' },
		{ id: 'sec-5', label: 'Tipo de despesa' },
	];

	let menuOpen = $state(false);

	function go(id: string) {
		menuOpen = false;
		document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
	}
</script>

<header class="site-header" style:--accent={blue}>
	<div class="inner">
		<div class="brand">
			<h1 class="brand-title">
				<img
					class="brand-logo"
					src="/logos/logo-pnab-simples.svg"
					alt="Política Nacional Aldir Blanc"
				/>
			</h1>
			<p class="lead">
				O Painel de Dados SNIIC: Avaliação de Resultados da Aldir Blanc — Ciclo 1
				apresenta os principais resultados da pesquisa “Resultados do Primeiro Ciclo da
				Política Nacional Aldir Blanc de Fomento à Cultura: recursos distribuídos, agentes
				contemplados e ações fomentadas”. A ferramenta reúne gráficos interativos sobre a
				execução da política, permitindo a visualização dos dados por meio da aplicação de
				filtros pelos usuários.
			</p>
		</div>

		<!-- Desktop: tópicos à direita -->
		<nav class="topics" aria-label="Seções da pesquisa">
			{#each sections as s}
				<a href={'#' + s.id} onclick={(e) => { e.preventDefault(); go(s.id); }}>{s.label}</a>
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

	<!-- Mobile: menu abaixo do título -->
	{#if menuOpen}
		<nav id="mobile-menu" class="mobile-menu" aria-label="Seções da pesquisa">
			{#each sections as s}
				<a href={'#' + s.id} onclick={(e) => { e.preventDefault(); go(s.id); }}>{s.label}</a>
			{/each}
		</nav>
	{/if}
</header>

<style>
	.site-header {
		border-bottom: 1px solid #1a1a1a;
		background: #000000;
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

	/* Logo da PNAB no lugar do título. */
	.brand-title {
		margin: 0 0 1.5rem;
		line-height: 0;
	}

	.brand-logo {
		display: block;
		width: clamp(220px, 34vw, 380px);
		height: auto;
	}

	.lead {
		font-size: 1rem;
		color: #cccccc;
		line-height: 1.5;
		margin: 0.6rem 0 0;
		max-width: 46ch;
	}

	/* ── Tópicos (desktop) ── */
	.topics {
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 0.7rem;
	}

	.topics a {
		font-size: 0.95rem;
		font-weight: 600;
		color: #ffffff;
		text-decoration: none;
		white-space: nowrap;
		transition: color 0.15s ease;
	}

	.topics a:hover {
		color: var(--accent);
	}

	/* ── Toggle (mobile) ── */
	.menu-toggle {
		display: none;
		align-items: center;
		gap: 0.5rem;
		background: none;
		border: 1px solid #444444;
		padding: 0.45rem 0.8rem;
		cursor: pointer;
		color: #ffffff;
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

	.mobile-menu a {
		padding: 0.85rem 0;
		border-top: 1px solid #1f1f1f;
		font-size: 1.15rem;
		font-weight: 600;
		color: #ffffff;
		text-decoration: none;
	}
	.mobile-menu a:hover {
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
