<script lang="ts">
	import Section1 from '$lib/components/sections/Section1.svelte';
	import Section2 from '$lib/components/sections/Section2.svelte';
	import Section3 from '$lib/components/sections/Section3.svelte';
	import Section4 from '$lib/components/sections/Section4.svelte';
	import Section5 from '$lib/components/sections/Section5.svelte';
	import Section6 from '$lib/components/sections/Section6.svelte';
	import Section7 from '$lib/components/sections/Section7.svelte';
	import { cream, white } from 'sniic-design-system';

	type BgColor = 'cream' | 'white';
	const bgColors: Record<BgColor, string> = { cream, white };

	let activeBg = $state<BgColor>('cream');
</script>

<svelte:head>
	<title>PNAB - Visualizacao de Dados</title>
</svelte:head>

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

<main style:background={bgColors[activeBg]} style:--chart-bg={bgColors[activeBg]}>
	<Section1 />
	<Section2 />
	<Section3 />
	<Section4 />
	<Section5 />
	<Section6 />
	<Section7 />
</main>

<style>
	main {
		width: 100%;
		min-height: 100vh;
		transition: background 0.3s ease;
	}

	.bg-switcher {
		position: fixed;
		top: 1rem;
		right: 1rem;
		z-index: 100;
		display: flex;
		gap: 0.5rem;
		padding: 0.4rem;
		background: rgba(0, 0, 0, 0.06);
		border-radius: 999px;
		backdrop-filter: blur(4px);
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
