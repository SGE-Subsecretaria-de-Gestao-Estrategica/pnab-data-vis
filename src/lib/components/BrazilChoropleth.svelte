<script lang="ts">
	import { geoMercator, geoPath } from 'd3-geo';
	import { scaleSequential } from 'd3-scale';
	import { interpolateRgbBasis } from 'd3-interpolate';
	import { colorScales, getContrastColor } from 'sniic-design-system';
	import { loadBrazilGeoJSON } from '$lib/geo';

	const FONT_FAMILY = "'Rawline', system-ui, sans-serif";

	interface Props {
		/** Value keyed by UF sigla (e.g. { SP: 123, RJ: 45 }). */
		values: Record<string, number>;
		/** Format a value for the tooltip. */
		format?: (v: number) => string;
		/** Currently selected sigla (highlighted). 'Todas' / undefined = none. */
		selected?: string;
		/** Optional set of siglas that are "in scope" — others are dimmed. */
		inScope?: Set<string> | null;
		/** Click handler — receives the UF sigla. */
		onselect?: (sigla: string) => void;
		metricLabel?: string;
	}

	let {
		values,
		format = (v) => v.toLocaleString('pt-BR'),
		selected = 'Todas',
		inScope = null,
		onselect,
		metricLabel = '',
	}: Props = $props();

	let geojson = $state<any>(null);
	let containerEl: HTMLDivElement | undefined = $state();
	let width = $state(520);
	let hovered = $state<string | null>(null);

	$effect(() => {
		if (!containerEl) return;
		width = containerEl.clientWidth;
		const ro = new ResizeObserver(([e]) => { width = e.contentRect.width; });
		ro.observe(containerEl);
		return () => ro.disconnect();
	});

	$effect(() => {
		loadBrazilGeoJSON().then((g: any) => { geojson = g; });
	});

	const mapH = $derived(Math.round(width * 0.92));

	const maxVal = $derived(Math.max(...Object.values(values), 1));
	const colorScale = $derived(
		scaleSequential<string>()
			.domain([0, maxVal])
			.interpolator(interpolateRgbBasis(colorScales.blue))
	);

	const projection = $derived.by(() => {
		if (!geojson || width <= 0) return null;
		return geoMercator().fitSize([width, mapH], geojson);
	});
	const pathFn = $derived(projection ? geoPath(projection) : null);

	function siglaOf(f: any): string {
		return f.properties.sigla as string;
	}
	function valueOf(f: any): number {
		return values[siglaOf(f)] ?? 0;
	}
	function dimmed(sigla: string): boolean {
		return !!inScope && !inScope.has(sigla);
	}

	const hoveredRow = $derived.by(() => {
		if (!hovered) return null;
		return { sigla: hovered, value: values[hovered] ?? 0 };
	});
</script>

<div bind:this={containerEl} class="choropleth">
	{#if geojson && pathFn && width > 0}
		<svg width={width} height={mapH} font-family={FONT_FAMILY} role="group" aria-label="Mapa do Brasil por UF">
			{#each geojson.features as f (f.properties.name)}
				{@const d = pathFn(f)}
				{@const sigla = siglaOf(f)}
				{@const val = valueOf(f)}
				{@const isSel = selected === sigla}
				{@const isDim = dimmed(sigla)}
				{#if d}
					<path
						{d}
						fill={val > 0 ? colorScale(val) : '#e5e7eb'}
						stroke={isSel ? '#1B1B1B' : 'white'}
						stroke-width={isSel ? 2 : 0.6}
						opacity={isDim ? 0.25 : 1}
						class="state"
						class:clickable={!!onselect}
						role="button"
						tabindex="0"
						aria-label={`${sigla}: ${format(val)}`}
						onclick={() => onselect?.(sigla)}
						onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onselect?.(sigla); } }}
						onmouseenter={() => (hovered = sigla)}
						onmouseleave={() => (hovered = null)}
					/>
				{/if}
			{/each}

			<!-- Sigla labels at centroids -->
			{#each geojson.features as f (f.properties.name + '-lbl')}
				{@const c = pathFn.centroid(f)}
				{@const sigla = siglaOf(f)}
				{@const val = valueOf(f)}
				{#if isFinite(c[0]) && isFinite(c[1]) && !dimmed(sigla)}
					<text
						x={c[0]}
						y={c[1]}
						text-anchor="middle"
						dy="0.35em"
						font-size="9.5"
						font-weight="700"
						fill={val > 0 ? getContrastColor(colorScale(val)) : '#6b7280'}
						pointer-events="none"
					>{sigla}</text>
				{/if}
			{/each}
		</svg>

		{#if hoveredRow}
			<div class="tooltip">
				<strong>{hoveredRow.sigla}</strong>
				{#if metricLabel}<span class="t-label">{metricLabel}</span>{/if}
				<span class="t-value">{format(hoveredRow.value)}</span>
			</div>
		{/if}
	{:else}
		<div class="loading" style:height={`${mapH}px`}>Carregando mapa…</div>
	{/if}
</div>

<style>
	.choropleth {
		position: relative;
		width: 100%;
	}

	svg {
		display: block;
		width: 100%;
		height: auto;
	}

	.state {
		transition: opacity 0.15s, fill 0.2s;
	}

	.state.clickable {
		cursor: pointer;
	}

	.state.clickable:hover {
		fill-opacity: 0.85;
		stroke: #1B1B1B;
		stroke-width: 1.2;
	}

	.state:focus {
		outline: none;
	}

	.state:focus-visible {
		outline: none;
		stroke: #1351B4;
		stroke-width: 2;
	}

	.tooltip {
		position: absolute;
		top: 0.5rem;
		left: 0.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.1rem;
		padding: 0.5rem 0.75rem;
		background: rgba(27, 27, 27, 0.92);
		color: white;
		border-radius: 0;
		font-family: 'Rawline', system-ui, sans-serif;
		pointer-events: none;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
	}

	.tooltip strong {
		font-size: 0.95rem;
	}

	.tooltip .t-label {
		font-size: 0.65rem;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		opacity: 0.7;
	}

	.tooltip .t-value {
		font-size: 0.9rem;
		font-weight: 600;
	}

	.loading {
		display: flex;
		align-items: center;
		justify-content: center;
		color: #999;
		font-family: 'Rawline', system-ui, sans-serif;
		font-size: 0.85rem;
	}
</style>
