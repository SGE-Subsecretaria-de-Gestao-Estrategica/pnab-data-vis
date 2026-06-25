<script lang="ts">
	import { base } from '$app/paths';
	import { siglaToName } from '$lib/data/dashboard';
	import { FLAG_RATIO, FLAG_GAP, isState } from '$lib/chartStandards';
	import type { FaixaEntity } from '$lib/data/faixa';

	interface Props {
		entities: FaixaEntity[];
		faixaLabels: string[];
		colors: string[];
		width?: number;
		showFlags?: boolean;
		flagSize?: number;
		flagBasePath?: string;
	}

	let {
		entities,
		faixaLabels,
		colors,
		width = undefined,
		showFlags = false,
		flagSize = 20,
		flagBasePath = `${base}/flags/states`,
	}: Props = $props();

	const FONT = "'Rawline', system-ui, sans-serif";

	// Layout constants
	const SIGLA_W = 30;      // sigla text column
	const SUB_W = 50;        // "valor" / "pgto." sub-label column
	const MR = 12;           // right margin
	const BAR_H = 30;        // height of each stacked bar
	const BAR_GAP = 5;       // gap between the two bars of one entity
	const BLOCK_GAP = 16;    // gap between entities
	const MT = 8;            // top margin
	const LEGEND_H = 40;     // legend area height

	const flagW = flagSize * FLAG_RATIO;
	// Entity label column: sigla text, plus a flag column when showing flags.
	const LBL_W = showFlags ? SIGLA_W + flagW + FLAG_GAP : 48;

	const BLOCK_H = BAR_H * 2 + BAR_GAP;

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);
	const barAreaW = $derived(Math.max(0, containerWidth - LBL_W - SUB_W - MR));

	const blocks = $derived(
		entities.map((e, i) => ({ entity: e, y: MT + i * (BLOCK_H + BLOCK_GAP) }))
	);

	const chartH = $derived(MT + entities.length * (BLOCK_H + BLOCK_GAP) + LEGEND_H);

	function labelColor(hex: string): string {
		const r = parseInt(hex.slice(1, 3), 16) / 255;
		const g = parseInt(hex.slice(3, 5), 16) / 255;
		const b = parseInt(hex.slice(5, 7), 16) / 255;
		return 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.6 ? '#1a1a1a' : '#ffffff';
	}

	// Cumulative segments for a 100%-stacked bar.
	function segments(pcts: number[]) {
		let cursor = 0;
		return pcts.map((pct, i) => {
			const w = (pct / 100) * barAreaW;
			const seg = { i, pct, x: cursor, w, color: colors[i] ?? '#999' };
			cursor += w;
			return seg;
		});
	}

	const legendBoxW = $derived(
		Math.min(150, Math.max(72, barAreaW / Math.max(1, faixaLabels.length)))
	);
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={chartH} font-family={FONT} role="img" aria-label="Distribuição por faixa de valor">
			{#each blocks as { entity, y }}
				{@const valSegs = segments(entity.valor)}
				{@const qtdSegs = segments(entity.qtd)}

				<!-- State flag (when the entity is a UF) -->
				{#if showFlags && isState(entity.label)}
					<image
						href="{flagBasePath}/{entity.label.toUpperCase()}.svg"
						x={2}
						y={y + BLOCK_H / 2 - flagSize / 2}
						width={flagW}
						height={flagSize}
						preserveAspectRatio="xMidYMid meet"
					>
						<title>{siglaToName[entity.label.toUpperCase()] ?? entity.label}</title>
					</image>
				{/if}

				<!-- Entity label, vertically centered on the block -->
				<text
					x={LBL_W - 8}
					y={y + BLOCK_H / 2}
					dy="0.35em"
					text-anchor="end"
					font-size="12"
					font-weight={entity.isBrasil ? 700 : 600}
					fill={entity.isBrasil ? '#1351B4' : '#334155'}
				>{entity.label}</text>

				<!-- Sub-labels -->
				<text x={LBL_W + SUB_W - 8} y={y + BAR_H / 2} dy="0.35em" text-anchor="end" font-size="11" fill="#94a3b8">valor</text>
				<text x={LBL_W + SUB_W - 8} y={y + BAR_H + BAR_GAP + BAR_H / 2} dy="0.35em" text-anchor="end" font-size="11" fill="#94a3b8">pgto.</text>

				<!-- Valor bar (top) -->
				<g transform={`translate(${LBL_W + SUB_W}, ${y})`}>
					{#each valSegs as s}
						{#if s.w > 0}
							<rect x={s.x} y={0} width={s.w} height={BAR_H} fill={s.color} shape-rendering="crispEdges" />
							{#if s.w > 30}
								<text x={s.x + s.w / 2} y={BAR_H / 2} dy="0.35em" text-anchor="middle" font-size="12" font-weight="700" fill={labelColor(s.color)} pointer-events="none">{Math.round(s.pct)}%</text>
							{/if}
						{/if}
					{/each}
				</g>

				<!-- Pagamentos bar (bottom) -->
				<g transform={`translate(${LBL_W + SUB_W}, ${y + BAR_H + BAR_GAP})`}>
					{#each qtdSegs as s}
						{#if s.w > 0}
							<rect x={s.x} y={0} width={s.w} height={BAR_H} fill={s.color} shape-rendering="crispEdges" />
							{#if s.w > 30}
								<text x={s.x + s.w / 2} y={BAR_H / 2} dy="0.35em" text-anchor="middle" font-size="12" font-weight="700" fill={labelColor(s.color)} pointer-events="none">{Math.round(s.pct)}%</text>
							{/if}
						{/if}
					{/each}
				</g>

				{#if entity.isBrasil}
					<line x1={LBL_W} y1={y + BLOCK_H + BLOCK_GAP / 2} x2={containerWidth - MR} y2={y + BLOCK_H + BLOCK_GAP / 2} stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3 3" />
				{/if}
			{/each}

			<!-- Legend -->
			<g transform={`translate(${LBL_W + SUB_W}, ${MT + entities.length * (BLOCK_H + BLOCK_GAP) + 6})`}>
				{#each faixaLabels as lbl, i}
					{@const lx = i * legendBoxW}
					<rect x={lx} y={4} width={12} height={12} rx={2} fill={colors[i] ?? '#999'} />
					<text x={lx + 17} y={10} dy="0.35em" font-size="11" fill="#475569">{lbl}</text>
				{/each}
			</g>
		</svg>
	{/if}
</div>
