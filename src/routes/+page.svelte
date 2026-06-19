<script lang="ts">
	import Section1 from '$lib/components/sections/Section1.svelte';
	import Section2 from '$lib/components/sections/Section2.svelte';
	import Section3 from '$lib/components/sections/Section3.svelte';
	import Section4 from '$lib/components/sections/Section4.svelte';
	import { cream, white } from 'sniic-design-system';

	type BgColor = 'cream' | 'white';
	const bgColors: Record<BgColor, string> = { cream, white };

	let activeBg = $state<BgColor>('cream');

	const sections = [
		{ id: 'section-1-intro', label: '1. Distribuição Territorial' },
		{ id: 'section-2-intro', label: '2. Perfil dos Agentes' },
		{ id: 'section-3-intro', label: '3. Vulnerabilidade Social' },
		{ id: 'section-4', label: '4. Classificação das Despesas' },
	];

	function scrollTo(id: string) {
		document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}
</script>

<svelte:head>
	<title>PNAB - Painel de Dados</title>
</svelte:head>

<div class="controls">
	<div class="bg-switcher">
		{#each Object.keys(bgColors) as key}
			<button
				class="swatch"
				class:active={activeBg === key}
				style:background={bgColors[key as BgColor]}
				onclick={() => (activeBg = key as BgColor)}
				aria-label="Fundo {key}"
			></button>
		{/each}
	</div>
	<nav class="section-nav">
		{#each sections as { id, label }}
			<button onclick={() => scrollTo(id)}>{label}</button>
		{/each}
	</nav>
</div>

<main style:background={bgColors[activeBg]} style:--chart-bg={bgColors[activeBg]}>
	<Section1 />
	<Section2 />
	<Section3 />
	<Section4 />
</main>

<style>
	main {
		width: 100%;
		min-height: 100vh;
		transition: background 0.3s ease;
	}

	.controls {
		position: fixed;
		top: 1rem;
		right: 1rem;
		z-index: 100;
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 0.5rem;
	}

	.bg-switcher {
		display: flex;
		gap: 0.5rem;
		padding: 0.4rem;
		background: rgba(0, 0, 0, 0.06);
		border-radius: 999px;
		backdrop-filter: blur(4px);
	}

	.section-nav {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		padding: 0.5rem 0.6rem;
		background: rgba(0, 0, 0, 0.06);
		border-radius: 0.75rem;
		backdrop-filter: blur(4px);
	}

	.section-nav button {
		background: none;
		border: none;
		cursor: pointer;
		font-family: 'Rawline', system-ui, sans-serif;
		font-size: 0.72rem;
		text-align: right;
		color: #333;
		padding: 0.2rem 0.4rem;
		border-radius: 0.4rem;
		opacity: 0.7;
		transition: opacity 0.15s, background 0.15s;
		white-space: nowrap;
	}

	.section-nav button:hover {
		opacity: 1;
		background: rgba(0, 0, 0, 0.07);
	}

	.swatch {
		width: 1.5rem;
		height: 1.5rem;
		border-radius: 50%;
		border: 2px solid transparent;
		cursor: pointer;
		padding: 0;
		transition: border-color 0.2s;
		box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.15);
	}

	.swatch.active {
		border-color: #333;
	}
</style>
