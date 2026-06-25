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
	import { white } from 'sniic-design-system';
</script>

<svelte:head>
	<title>PNAB - Painel de Dados</title>
</svelte:head>

<main style:background={white} style:--chart-bg={white}>
	<Section1 />
	<Section2 />
	<Section3 />
	<Section4 />
	<Section5 />
	<Section6 />
	<Section7 />
	<Section8 />
	<Section9 />
	<Section10 />
</main>

<style>
	main {
		width: 100%;
		min-height: 100vh;
	}
</style>
