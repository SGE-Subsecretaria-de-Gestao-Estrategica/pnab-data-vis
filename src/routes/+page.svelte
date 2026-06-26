<script lang="ts">
	import Section1 from '$lib/components/sections/Section1.svelte';
	import Section2 from '$lib/components/sections/Section2.svelte';
	import Section3 from '$lib/components/sections/Section3.svelte';
	import Section4 from '$lib/components/sections/Section4.svelte';
	import Section5 from '$lib/components/sections/Section5.svelte';
	import Section6 from '$lib/components/sections/Section6.svelte';
	import Section7 from '$lib/components/sections/Section7.svelte';
	import Section8 from '$lib/components/sections/Section8.svelte';
	import Section9 from '$lib/components/sections/Section9.svelte';
	import Section10 from '$lib/components/sections/Section10.svelte';
	import SiteHeader from '$lib/components/SiteHeader.svelte';
	import { white } from 'sniic-design-system';
</script>

<svelte:head>
	<title>PNAB - Painel de Dados</title>
</svelte:head>

<main style:background={white} style:--chart-bg={white}>
	<SiteHeader />
	<div id="sec-1" class="anchor"><Section1 /></div>
	<div id="sec-2" class="anchor"><Section2 /></div>
	<div id="sec-3" class="anchor"><Section3 /></div>
	<div id="sec-4" class="anchor"><Section4 /></div>
	<div id="sec-5" class="anchor"><Section5 /></div>
	<div id="sec-6" class="anchor"><Section6 /></div>
	<div id="sec-7" class="anchor"><Section7 /></div>
	<div id="sec-8" class="anchor"><Section8 /></div>
	<div id="sec-9" class="anchor"><Section9 /></div>
	<div id="sec-10" class="anchor"><Section10 /></div>
</main>

<style>
	main {
		width: 100%;
		min-height: 100vh;
		/* Contém o sliver horizontal dos blocos full-bleed (100vw) sem virar
		   container de scroll — `clip` não força overflow-y, preservando o sticky. */
		overflow-x: clip;
	}

	/* Espaço para o scroll suave não esconder o topo da seção. */
	.anchor {
		scroll-margin-top: 1rem;
	}
</style>
