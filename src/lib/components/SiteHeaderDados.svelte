<script lang="ts">
	import { blue } from 'sniic-design-system';
	import { base } from '$app/paths';
	import TopTabs from './TopTabs.svelte';

	// Itens do menu = títulos dos acordeões da página /dados-abertos.
	// Cada id corresponde ao <details> equivalente no +page.svelte.
	const items: { id: string; label: string }[] = [
		{ id: 'acc-obtencao', label: 'Obtenção e Tratamento dos Dados' },
		{ id: 'acc-dicionario', label: 'Dicionário de Dados' },
		{ id: 'acc-citar', label: 'Como citar a utilização dos dados disponibilizados' },
	];

	let menuOpen = $state(false);

	function go(id: string) {
		menuOpen = false;
		const el = document.getElementById(id);
		if (!el) return;
		// Abre o acordeão antes de rolar até ele.
		if (el instanceof HTMLDetailsElement) el.open = true;
		el.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}
</script>

<header class="site-header" style:--accent={blue}>
	<div class="inner">
		<div class="brand">
			<h1 class="brand-title">
				Dados Abertos — Política Nacional Aldir Blanc de Fomento à Cultura (Ciclo I)
			</h1>
			<p class="lead">
				Esta seção de Dados Abertos disponibiliza a base consolidada dos agentes culturais contemplados no Ciclo I da Política Nacional Aldir Blanc de Fomento à Cultura (PNAB). Os dados integram o processo de reestruturação do Sistema Nacional de Informações e Indicadores Culturais (SNIIC) e fundamentaram a pesquisa “Resultados do Primeiro Ciclo da Política Nacional Aldir Blanc de Fomento à Cultura: recursos distribuídos, agentes contemplados e ações fomentadas”. Sua divulgação em formato aberto assegura a transparência ativa, a reprodutibilidade das análises e a credibilidade dos resultados, permitindo que a sociedade debata a política pública com base em evidências.
			</p>
		</div>

		<!-- Desktop: menu à direita com os títulos das seções desta página -->
		<nav class="topics" aria-label="Conteúdo desta página">
			<span class="topics-title">Nesta página</span>
			{#each items as it}
				<a
					class="topic-link"
					href={'#' + it.id}
					onclick={(e) => {
						e.preventDefault();
						go(it.id);
					}}
				>
					<span>{it.label}</span>
					<span class="chev" aria-hidden="true"></span>
				</a>
			{/each}
		</nav>

		<!-- Mobile: botão que abre o menu -->
		<button
			class="menu-toggle"
			aria-expanded={menuOpen}
			aria-controls="mobile-menu-dados"
			onclick={() => (menuOpen = !menuOpen)}
		>
			<span class="menu-toggle-label">{menuOpen ? 'Fechar' : 'Nesta página'}</span>
			<span class="menu-toggle-icon" class:open={menuOpen} aria-hidden="true"></span>
		</button>
	</div>

	<!-- Mobile: menu abaixo do título -->
	{#if menuOpen}
		<nav id="mobile-menu-dados" class="mobile-menu" aria-label="Conteúdo desta página">
			{#each items as it}
				<a
					class="m-link"
					href={'#' + it.id}
					onclick={(e) => {
						e.preventDefault();
						go(it.id);
					}}>{it.label}</a
				>
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

<TopTabs active="dados" />

<style>
	.site-header {
		border-bottom: 1px solid #e5e9f0;
		background: #ffffff;
	}

	.inner {
		max-width: 1200px;
		margin: 0 auto;
		padding: 4rem 2rem;
		min-height: 46vh;
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 2rem;
	}

	/* ── Brand / título ── */
	.brand {
		flex-shrink: 0;
		max-width: 560px;
	}

	.brand-title {
		margin: 0 0 1.5rem;
		font-size: clamp(1.5rem, 2.4vw, 2.1rem);
		font-weight: 700;
		line-height: 1.25;
		color: #1b1b1b;
	}

	.lead {
		font-size: 1rem;
		color: #555;
		line-height: 1.5;
		margin: 0.6rem 0 0;
		max-width: 52ch;
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

	/* ── Menu (desktop) ── */
	.topics {
		display: flex;
		flex-direction: column;
		align-items: stretch;
		gap: 0.15rem;
		width: 320px;
		flex-shrink: 0;
	}

	.topics-title {
		font-size: 0.75rem;
		font-weight: 700;
		letter-spacing: 0.05em;
		text-transform: uppercase;
		color: #8a93a6;
		margin-bottom: 0.4rem;
	}

	.topic-link {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 0.6rem;
		width: 100%;
		padding: 0.6rem 0;
		border-top: 1px solid #eef1f6;
		text-align: left;
		cursor: pointer;
		font-size: 0.9rem;
		font-weight: 700;
		line-height: 1.25;
		color: #000000;
		text-decoration: none;
		text-transform: uppercase;
		transition: color 0.15s ease;
	}
	.topic-link:last-child {
		border-bottom: 1px solid #eef1f6;
	}

	.topic-link:hover {
		color: var(--accent);
	}

	/* Seta indicadora */
	.chev {
		flex-shrink: 0;
		margin-top: 0.25rem;
		width: 8px;
		height: 8px;
		border-right: 2px solid currentColor;
		border-bottom: 2px solid currentColor;
		transform: rotate(-45deg);
		opacity: 0.6;
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
	.menu-toggle-icon::before {
		top: -5px;
	}
	.menu-toggle-icon::after {
		top: 5px;
	}
	.menu-toggle-icon.open {
		background: transparent;
	}
	.menu-toggle-icon.open::before {
		transform: translateY(5px) rotate(45deg);
	}
	.menu-toggle-icon.open::after {
		transform: translateY(-5px) rotate(-45deg);
	}

	/* ── Menu (mobile) ── */
	.mobile-menu {
		display: none;
		flex-direction: column;
		padding: 0 2rem 1.25rem;
		max-width: 1200px;
		margin: 0 auto;
	}

	.m-link {
		padding: 0.85rem 0;
		border-top: 1px solid #eef1f6;
		font-size: 1.05rem;
		font-weight: 700;
		line-height: 1.25;
		color: #1b1b1b;
		text-decoration: none;
		text-transform: uppercase;
	}
	.m-link:hover {
		color: var(--accent);
	}

	/* ── Responsivo ── */
	@media (max-width: 860px) {
		.inner {
			padding: 3rem 1.5rem;
			min-height: auto;
			align-items: center;
			gap: 1rem;
		}
		.brand {
			flex: 1 1 auto;
			min-width: 0;
			max-width: 100%;
		}
		.topics {
			display: none;
		}
		.menu-toggle {
			display: inline-flex;
			flex-shrink: 0;
		}
		.mobile-menu {
			display: flex;
		}
	}
</style>
