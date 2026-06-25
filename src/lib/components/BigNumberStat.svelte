<script lang="ts">
	import { BigNumber } from 'sniic-design-system';

	// Standard "big number" style shared across all sections: white fill with a
	// blue shadow (the design-system 3D look), no card chrome. Only size/content
	// varies per usage — the colors are fixed here so the look stays consistent.
	let {
		value,
		label,
		subtitle = undefined,
		fontSize = 44,
		width = 360,
		shadowDepth = 4,
	}: {
		value: string;
		label: string;
		subtitle?: string;
		fontSize?: number;
		width?: number;
		shadowDepth?: number;
	} = $props();
</script>

<div class="bn-stat">
	<BigNumber
		{value}
		{label}
		{subtitle}
		{fontSize}
		{width}
		{shadowDepth}
		color="#ffffff"
		shadowColor="#1351B4"
		labelColor="#555555"
		subtitleColor="#888888"
	/>
</div>

<style>
	.bn-stat :global(svg) {
		width: 100%;
		height: auto;
		display: block;
	}
</style>
