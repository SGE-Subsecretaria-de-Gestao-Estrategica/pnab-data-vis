<script lang="ts">
	import { base } from '$app/paths';
	import { FLAG_RATIO, FLAG_GAP, FLAG_BORDER_COLOR, FLAG_BORDER_WIDTH, hasFlag, flagId, flagTitle, flagAwareLabel, truncateToWidth } from '$lib/chartStandards';
	import { createMediaQuery } from '$lib/utils/media.svelte';
	import type { FaixaEntity } from '$lib/data/faixa';

	// No mobile a legenda é centralizada na área de barras.
	const isMobile = createMediaQuery('(max-width: 768px)');

	interface Props {
		entities: FaixaEntity[];
		faixaLabels: string[];
		colors: string[];
		width?: number;
		showFlags?: boolean;
		flagSize?: number;
		flagBorder?: boolean;
		flagBasePath?: string;
		/** Sobrescreve a cor dos rótulos textuais (entidades, sub-rótulos, legenda). */
		axisColor?: string;
	}

	let {
		entities,
		faixaLabels,
		colors,
		width = undefined,
		showFlags = false,
		flagSize = 20,
		flagBorder = true,
		flagBasePath = `${base}/flags/states`,
		axisColor = undefined,
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

	// Legenda no padrão dos gráficos 4/5: caixas coloridas contíguas com o rótulo
	// dentro de cada caixa (texto em contraste automático).
	const LEG_CHAR_W = 8;    // largura estimada por caractere
	const LEG_BOX_PAD = 20;  // padding horizontal interno da caixa
	const LEG_ROW_H = 28;    // altura de cada linha da legenda
	const LEG_GAP = 2;       // espaço entre linhas da legenda
	const LEG_TOP = 12;      // espaço acima da legenda

	const flagW = flagSize * FLAG_RATIO;
	// Entity label column: sigla text, plus a flag column when showing flags.
	const LBL_W = showFlags ? SIGLA_W + flagW + FLAG_GAP : 48;

	const BLOCK_H = BAR_H * 2 + BAR_GAP;

	let measuredWidth = $state(0);
	const containerWidth = $derived(width ?? measuredWidth);
	const barAreaW = $derived(Math.max(0, containerWidth - LBL_W - SUB_W - MR));

	const blocks = $derived(
		entities.map((e, i) => ({ entity: e, y: blocksTop + i * (BLOCK_H + BLOCK_GAP) }))
	);

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

	// Caixas dimensionadas ao próprio rótulo (mín. 60px), nunca mais largas que a
	// área de barras, quebrando em múltiplas linhas quando não couber tudo numa só.
	const legendBoxWs = $derived(
		faixaLabels.map((lbl) => {
			const natural = Math.max(60, lbl.length * LEG_CHAR_W + LEG_BOX_PAD);
			return barAreaW > 0 ? Math.min(natural, barAreaW) : natural;
		})
	);

	type LegendItem = { i: number; w: number; x: number };
	const legendRows = $derived.by(() => {
		const rows: LegendItem[][] = [];
		let cur: LegendItem[] = [];
		let rowW = 0;
		for (let i = 0; i < faixaLabels.length; i++) {
			const w = legendBoxWs[i];
			if (barAreaW > 0 && rowW + w > barAreaW && cur.length > 0) {
				rows.push(cur);
				cur = [];
				rowW = 0;
			}
			cur.push({ i, w, x: rowW });
			rowW += w;
		}
		if (cur.length > 0) rows.push(cur);
		return rows;
	});

	const legendTotalH = $derived(
		legendRows.length * LEG_ROW_H + Math.max(0, legendRows.length - 1) * LEG_GAP
	);

	// Legenda no topo; os blocos das entidades começam abaixo dela.
	const legendTop = MT;
	const blocksTop = $derived(MT + legendTotalH + LEG_TOP);
	const chartH = $derived(blocksTop + entities.length * (BLOCK_H + BLOCK_GAP) + 4);
</script>

<div bind:clientWidth={measuredWidth} style="width:{width ? width + 'px' : '100%'};">
	{#if containerWidth > 0}
		<svg width={containerWidth} height={chartH} font-family={FONT} role="img" aria-label="Distribuição por faixa de valor">
			{#each blocks as { entity, y }}
				{@const valSegs = segments(entity.valor)}
				{@const qtdSegs = segments(entity.qtd)}

				<!-- State flag (when the entity is a UF) -->
				{#if showFlags && hasFlag(entity.label)}
					<image
						href="{flagBasePath}/{flagId(entity.label)}.svg"
						x={2}
						y={y + BLOCK_H / 2 - flagSize / 2}
						width={flagW}
						height={flagSize}
						preserveAspectRatio="xMidYMid meet"
					>
						<title>{flagTitle(entity.label)}</title>
					</image>
					{#if flagBorder}
						<rect
							x={2}
							y={y + BLOCK_H / 2 - flagSize / 2}
							width={flagW}
							height={flagSize}
							fill="none"
							stroke={FLAG_BORDER_COLOR}
							stroke-width={FLAG_BORDER_WIDTH}
						/>
					{/if}
				{/if}

				<!-- Entity label, vertically centered on the block -->
				<text
					x={LBL_W - 8}
					y={y + BLOCK_H / 2}
					dy="0.35em"
					text-anchor="end"
					font-size="12"
					font-weight={entity.isBrasil ? 700 : 600}
					fill={entity.isBrasil ? '#1351B4' : (axisColor ?? '#334155')}
				>{flagAwareLabel(entity.label, showFlags)}</text>

				<!-- Sub-labels -->
				<text x={LBL_W + SUB_W - 8} y={y + BAR_H / 2} dy="0.35em" text-anchor="end" font-size="11" fill={axisColor ?? '#94a3b8'}>valor</text>
				<text x={LBL_W + SUB_W - 8} y={y + BAR_H + BAR_GAP + BAR_H / 2} dy="0.35em" text-anchor="end" font-size="11" fill={axisColor ?? '#94a3b8'}>pgto.</text>

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
					<line x1={LBL_W} y1={y + BLOCK_H + BLOCK_GAP / 2} x2={containerWidth - MR} y2={y + BLOCK_H + BLOCK_GAP / 2} stroke="#000000" stroke-width="1" stroke-dasharray="3 3" />
				{/if}
			{/each}

			<!-- Legend: caixas coloridas contíguas com rótulo dentro (padrão gráficos 4/5) -->
			{#each legendRows as row, ri}
				{@const rowTotalW = row.reduce((s, item) => s + item.w, 0)}
				{@const legendOffsetX = isMobile.matches ? (containerWidth - rowTotalW) / 2 - (LBL_W + SUB_W) : 0}
				<g transform={`translate(${LBL_W + SUB_W + legendOffsetX}, ${legendTop + ri * (LEG_ROW_H + LEG_GAP)})`}>
					{#each row as item}
						<rect
							x={item.x}
							y={0}
							width={item.w}
							height={LEG_ROW_H}
							fill={colors[item.i] ?? '#999'}
							shape-rendering="crispEdges"
						/>
						<text
							x={isMobile.matches ? item.x + item.w / 2 : item.x + 8}
							y={LEG_ROW_H / 2}
							dy="0.35em"
							text-anchor={isMobile.matches ? 'middle' : 'start'}
							font-size="12"
							font-weight="600"
							fill={labelColor(colors[item.i] ?? '#999')}
							pointer-events="none"
						>{truncateToWidth(faixaLabels[item.i], item.w - 16, 12)}</text>
					{/each}
				</g>
			{/each}
		</svg>
	{/if}
</div>
