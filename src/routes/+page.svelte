<script lang="ts">
	import Section1 from '$lib/components/sections/Section1.svelte';
	import Section2 from '$lib/components/sections/Section2.svelte';
	import Section3 from '$lib/components/sections/Section3.svelte';
	import Section4 from '$lib/components/sections/Section4.svelte';
	import Section5 from '$lib/components/sections/Section5.svelte';
	import Section6 from '$lib/components/sections/Section6.svelte';
	import Section7 from '$lib/components/sections/Section7.svelte';
</script>

<svelte:head>
	<title>PNAB - Visualizacao de Dados</title>
</svelte:head>

<main>
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
	}
</style>
