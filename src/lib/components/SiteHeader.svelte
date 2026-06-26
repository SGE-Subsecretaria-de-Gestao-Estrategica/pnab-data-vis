<script lang="ts">
	import { blue } from 'sniic-design-system';

	// "Big number" 3D look replicado em CSS para permitir uma cor por palavra e
	// alinhamento à esquerda (o componente BigNumber é monocromático e centralizado).
	// Uma das 4 principais cores do SNIIC para cada palavra do título.
	const titleWords = [
		{ text: 'Política', color: '#4271b5' }, // azul
		{ text: 'Nacional', color: '#ea662f' }, // laranja
		{ text: 'Aldir', color: '#317a68' }, // verde
		{ text: 'Blanc', color: '#a44c7f' }, // roxo
	];

	// Tópicos do menu — cada um aponta para o id da seção correspondente.
	const sections = [
		{ id: 'sec-1', label: 'Valores gerais' },
		{ id: 'sec-2', label: 'Per capita' },
		{ id: 'sec-3', label: 'Faixa de valor' },
		{ id: 'sec-4', label: 'Urbano e rural' },
		{ id: 'sec-5', label: 'Capital e interior' },
		{ id: 'sec-6', label: 'Porte municipal' },
		{ id: 'sec-7', label: 'Tipo de documento' },
		{ id: 'sec-8', label: 'Gênero' },
		{ id: 'sec-9', label: 'Tipo de organização' },
		{ id: 'sec-10', label: 'Tipo de despesa' },
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
				{#each titleWords as w}
					<span style:--c={w.color}>{w.text}</span>
				{/each}
			</h1>
			<p class="lead">
				Painel de dados sobre a execução da Política Nacional Aldir Blanc no território
				brasileiro.
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

	/* Título estilizado com o look 3D do BigNumber — uma cor por palavra. */
	.brand-title {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.04em;
		margin: 0 0 1.5rem;
		font-weight: 800;
		font-size: clamp(2.2rem, 5vw, 3.6rem);
		line-height: 1;
		letter-spacing: -0.01em;
	}

	.brand-title span {
		color: var(--c);
		paint-order: stroke fill;
		-webkit-text-stroke: 0.035em #000000;
		text-shadow:
			0.016em 0.016em 0 #000000,
			0.032em 0.032em 0 #000000,
			0.048em 0.048em 0 #000000,
			0.064em 0.064em 0 #000000;
	}

	.lead {
		font-size: 1rem;
		color: #555;
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
		font-size: 1.15rem;
		font-weight: 600;
		color: #000000;
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

	.mobile-menu a {
		padding: 0.85rem 0;
		border-top: 1px solid #eef1f6;
		font-size: 1.15rem;
		font-weight: 600;
		color: #333;
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
