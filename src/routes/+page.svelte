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
	import SectionIntro from '$lib/components/sections/SectionIntro.svelte';
	import SectionFooter from '$lib/components/sections/SectionFooter.svelte';
	import SiteHeader from '$lib/components/SiteHeader.svelte';
	import SiteHeaderAlt from '$lib/components/SiteHeaderAlt.svelte';
	import { white } from 'sniic-design-system';

	// Alterna entre o cabeçalho padrão (claro) e a versão alternativa (fundo preto).
	// Botão flutuante no canto para comparar as duas versões.
</script>

<svelte:head>
	<title>PNAB - Painel de Dados</title>
</svelte:head>

<main style:background={white} style:--chart-bg={white}>
	<SiteHeader />
	<SectionIntro />

	<!-- Seção 1 — distribuição nos territórios: reúne os 6 blocos (valores gerais
	     → porte municipal). Cada bloco mantém sua própria âncora para o menu. -->
	<section id="sec-1" class="anchor section-group">
		<Section1 />
		<div id="sec-1-percapita" class="anchor"><Section2 /></div>
		<div id="sec-1-faixa" class="anchor"><Section3 /></div>
		<div id="sec-1-urbano-rural" class="anchor"><Section4 /></div>
		<div id="sec-1-capital-interior" class="anchor"><Section5 /></div>
		<div id="sec-1-porte" class="anchor"><Section6 /></div>
	</section>

	<div id="sec-2" class="anchor"><Section7 /></div>
	<div id="sec-3" class="anchor"><Section8 /></div>
	<div id="sec-4" class="anchor"><Section9 /></div>
	<div id="sec-5" class="anchor"><Section10 /></div>

	<SectionFooter />
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

	/* Seção 1 (blocos Section1→Section6) com o amarelo principal do SNIIC. */
	.section-group {
	}

	/* Botão temporário para comparar as duas versões de cabeçalho. */
	.header-switch {
		position: fixed;
		top: 1rem;
		right: 1rem;
		z-index: 1000;
		padding: 0.5rem 0.9rem;
		background: #000;
		color: #fff;
		border: 1px solid #fff;
		border-radius: 0;
		font-size: 0.8rem;
		font-weight: 700;
		cursor: pointer;
	}
</style>
