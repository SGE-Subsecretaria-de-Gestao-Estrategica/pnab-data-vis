<script lang="ts">
	interface Props {
		outerFem: number;
		outerMasc: number;
		innerFem: number;
		innerMasc: number;
		colorFem?: string;
		colorMasc?: string;
		formatOuter?: (v: number) => string;
		formatInner?: (v: number) => string;
	}

	let {
		outerFem,
		outerMasc,
		innerFem,
		innerMasc,
		colorFem = '#a44c7f',
		colorMasc = '#4271b5',
		formatOuter = (v: number) =>
			new Intl.NumberFormat('pt-BR', {
				style: 'currency',
				currency: 'BRL',
				notation: 'compact',
				maximumFractionDigits: 1,
			}).format(v),
		formatInner = (v: number) => v.toLocaleString('pt-BR'),
	}: Props = $props();

	// ── Layout ─────────────────────────────────────────────────────────────────
	const W = 660;
	const H = 415;
	const CX = 330;
	const CY = 195;
	const PAD = 0.03;

	const OUTER_OR = 158;
	const OUTER_IR = 122;
	const INNER_OR = 108;
	const INNER_IR = 70;

	const FONT = "'Rawline', system-ui, sans-serif";

	// Annotation box layout
	const BOX_W      = 155;
	const BOX_H      = 54;
	const BOX_GAP    = 10;
	const RIGHT_BOX_X = CX + OUTER_OR + 12;
	const LEFT_BOX_X  = CX - OUTER_OR - 12 - BOX_W;
	const BOX_Y_UPPER = CY - BOX_H - BOX_GAP / 2;
	const BOX_Y_LOWER = CY + BOX_GAP / 2;

	// ── Segment computation ───────────────────────────────────────────────────
	// Masculino FIRST → clockwise from top → right side (blue)
	// Feminino SECOND → continues clockwise → left side (pink)
	interface Seg {
		label: string;
		value: number;
		perc: number;
		start: number;
		end: number;
		mid: number;
		color: string;
	}

	function buildSegs(fem: number, masc: number, cFem: string, cMasc: string): Seg[] {
		const total = fem + masc;
		const fp = fem / total;
		const mp = masc / total;
		const s0 = -Math.PI / 2;
		return [
			{
				label: 'Masculino',
				value: masc,
				perc: mp,
				start: s0 + PAD / 2,
				end: s0 + mp * 2 * Math.PI - PAD / 2,
				mid: s0 + mp * Math.PI,
				color: cMasc,
			},
			{
				label: 'Feminino',
				value: fem,
				perc: fp,
				start: s0 + mp * 2 * Math.PI + PAD / 2,
				end: s0 + 2 * Math.PI - PAD / 2,
				mid: s0 + mp * 2 * Math.PI + fp * Math.PI,
				color: cFem,
			},
		];
	}

	function annularPath(or_: number, ir: number, a0: number, a1: number): string {
		const large = a1 - a0 > Math.PI ? 1 : 0;
		const ox0 = CX + or_ * Math.cos(a0), oy0 = CY + or_ * Math.sin(a0);
		const ox1 = CX + or_ * Math.cos(a1), oy1 = CY + or_ * Math.sin(a1);
		const ix0 = CX + ir * Math.cos(a1), iy0 = CY + ir * Math.sin(a1);
		const ix1 = CX + ir * Math.cos(a0), iy1 = CY + ir * Math.sin(a0);
		return `M${ox0},${oy0} A${or_},${or_} 0 ${large} 1 ${ox1},${oy1} L${ix0},${iy0} A${ir},${ir} 0 ${large} 0 ${ix1},${iy1} Z`;
	}

	function percFmt(p: number): string {
		return (
			(p * 100).toLocaleString('pt-BR', {
				minimumFractionDigits: 1,
				maximumFractionDigits: 1,
			}) + '%'
		);
	}

	// ── Derived ──────────────────────────────────────────────────────────────
	const outerSegs = $derived(buildSegs(outerFem, outerMasc, colorFem, colorMasc));
	const innerSegs = $derived(buildSegs(innerFem, innerMasc, colorFem, colorMasc));
	const innerTotal = $derived(innerFem + innerMasc);

	// [0] = Masculino (right), [1] = Feminino (left)
	const innerMascPx = $derived(CX + INNER_OR * Math.cos(innerSegs[0].mid));
	const innerMascPy = $derived(CY + INNER_OR * Math.sin(innerSegs[0].mid));
	const outerMascPx = $derived(CX + OUTER_OR * Math.cos(outerSegs[0].mid));
	const outerMascPy = $derived(CY + OUTER_OR * Math.sin(outerSegs[0].mid));
	const innerFemPx  = $derived(CX + INNER_OR * Math.cos(innerSegs[1].mid));
	const innerFemPy  = $derived(CY + INNER_OR * Math.sin(innerSegs[1].mid));
	const outerFemPx  = $derived(CX + OUTER_OR * Math.cos(outerSegs[1].mid));
	const outerFemPy  = $derived(CY + OUTER_OR * Math.sin(outerSegs[1].mid));

	const innerMascPercStr = $derived(percFmt(innerSegs[0].perc));
	const outerMascPercStr = $derived(percFmt(outerSegs[0].perc));
	const innerFemPercStr  = $derived(percFmt(innerSegs[1].perc));
	const outerFemPercStr  = $derived(percFmt(outerSegs[1].perc));

	// Annotation box: connection point on the nearest vertical edge
	function connTarget(px: number, bx: number, by: number, bh: number) {
		return px < bx
			? { tx: bx,         ty: by + bh / 2 }
			: { tx: bx + BOX_W, ty: by + bh / 2 };
	}

	const mi_c = $derived(connTarget(innerMascPx, RIGHT_BOX_X, BOX_Y_UPPER, BOX_H));
	const mo_c = $derived(connTarget(outerMascPx, RIGHT_BOX_X, BOX_Y_LOWER, BOX_H));
	const fi_c = $derived(connTarget(innerFemPx,  LEFT_BOX_X,  BOX_Y_UPPER, BOX_H));
	const fo_c = $derived(connTarget(outerFemPx,  LEFT_BOX_X,  BOX_Y_LOWER, BOX_H));

	// ── Legend ────────────────────────────────────────────────────────────────
	const LG_Y = CY + OUTER_OR + 36;
	const lx1 = CX - 95;
	const lx2 = CX + 10;
</script>

<svg
	viewBox="0 0 {W} {H}"
	width="600"
	height={Math.round((600 * H) / W)}
	role="img"
	aria-label="Gráfico donut duplo: distribuição por sexo do valor repassado (anel externo) e agentes contemplados de contemplados (anel interno)"
	font-family={FONT}
>
	<!-- ── Outer ring ──────────────────────────────────────────────────────── -->
	{#each outerSegs as seg}
		<path d={annularPath(OUTER_OR, OUTER_IR, seg.start, seg.end)} fill={seg.color} />
	{/each}

	<!-- ── Inner ring ──────────────────────────────────────────────────────── -->
	{#each innerSegs as seg}
		<path d={annularPath(INNER_OR, INNER_IR, seg.start, seg.end)} fill={seg.color} opacity="0.72" />
	{/each}

	<!-- ── Center hole text ──────────────────────────────────────────────────── -->
	<text x={CX} y={CY - 12} text-anchor="middle" font-size="12" font-weight="700" fill="currentColor">
		{innerTotal.toLocaleString('pt-BR')}
	</text>
	<text x={CX} y={CY + 7}  text-anchor="middle" font-size="12" fill="currentColor" opacity="0.5">agentes (PF)</text>
	<text x={CX} y={CY + 20} text-anchor="middle" font-size="12" fill="currentColor" opacity="0.5">contemplados</text>

	<!-- ── Annotation helper macro ───────────────────────────────────────────
	     Black connector + dot; colored box border + accent bar + text.
	──────────────────────────────────────────────────────────────────────── -->

	<!-- Masculino inner — upper right (blue) -->
	<line x1={innerMascPx} y1={innerMascPy} x2={mi_c.tx} y2={mi_c.ty} stroke="black" stroke-width="1" opacity="0.55" />
	<circle cx={innerMascPx} cy={innerMascPy} r="3.5" fill="black" opacity="0.55" />
	<rect x={RIGHT_BOX_X} y={BOX_Y_UPPER} width={BOX_W} height={BOX_H} rx="0"
		fill="white" stroke={colorMasc} stroke-width="1.5" />
	<rect x={RIGHT_BOX_X} y={BOX_Y_UPPER} width="4" height={BOX_H} rx="0" fill={colorMasc} />
	<text x={RIGHT_BOX_X + 12} y={BOX_Y_UPPER + 21}
		font-size="12" font-weight="700" fill={colorMasc}>{innerMascPercStr}</text>
	<text x={RIGHT_BOX_X + 12} y={BOX_Y_UPPER + 38}
		font-size="12" fill="currentColor" opacity="0.6">agentes contemplados</text>

	<!-- Masculino outer — lower right (blue) -->
	<line x1={outerMascPx} y1={outerMascPy} x2={mo_c.tx} y2={mo_c.ty} stroke="black" stroke-width="1" opacity="0.55" />
	<circle cx={outerMascPx} cy={outerMascPy} r="3.5" fill="black" opacity="0.55" />
	<rect x={RIGHT_BOX_X} y={BOX_Y_LOWER} width={BOX_W} height={BOX_H} rx="0"
		fill="white" stroke={colorMasc} stroke-width="1.5" />
	<rect x={RIGHT_BOX_X} y={BOX_Y_LOWER} width="4" height={BOX_H} rx="0" fill={colorMasc} />
	<text x={RIGHT_BOX_X + 12} y={BOX_Y_LOWER + 21}
		font-size="12" font-weight="700" fill={colorMasc}>{outerMascPercStr}</text>
	<text x={RIGHT_BOX_X + 12} y={BOX_Y_LOWER + 38}
		font-size="12" fill="currentColor" opacity="0.6">valor repassado</text>

	<!-- Feminino inner — upper left (pink) -->
	<line x1={innerFemPx} y1={innerFemPy} x2={fi_c.tx} y2={fi_c.ty} stroke="black" stroke-width="1" opacity="0.55" />
	<circle cx={innerFemPx} cy={innerFemPy} r="3.5" fill="black" opacity="0.55" />
	<rect x={LEFT_BOX_X} y={BOX_Y_UPPER} width={BOX_W} height={BOX_H} rx="0"
		fill="white" stroke={colorFem} stroke-width="1.5" />
	<rect x={LEFT_BOX_X} y={BOX_Y_UPPER} width="4" height={BOX_H} rx="0" fill={colorFem} />
	<text x={LEFT_BOX_X + 12} y={BOX_Y_UPPER + 21}
		font-size="12" font-weight="700" fill={colorFem}>{innerFemPercStr}</text>
	<text x={LEFT_BOX_X + 12} y={BOX_Y_UPPER + 38}
		font-size="12" fill="currentColor" opacity="0.6">agentes contemplados</text>

	<!-- Feminino outer — lower left (pink) -->
	<line x1={outerFemPx} y1={outerFemPy} x2={fo_c.tx} y2={fo_c.ty} stroke="black" stroke-width="1" opacity="0.55" />
	<circle cx={outerFemPx} cy={outerFemPy} r="3.5" fill="black" opacity="0.55" />
	<rect x={LEFT_BOX_X} y={BOX_Y_LOWER} width={BOX_W} height={BOX_H} rx="0"
		fill="white" stroke={colorFem} stroke-width="1.5" />
	<rect x={LEFT_BOX_X} y={BOX_Y_LOWER} width="4" height={BOX_H} rx="0" fill={colorFem} />
	<text x={LEFT_BOX_X + 12} y={BOX_Y_LOWER + 21}
		font-size="12" font-weight="700" fill={colorFem}>{outerFemPercStr}</text>
	<text x={LEFT_BOX_X + 12} y={BOX_Y_LOWER + 38}
		font-size="12" fill="currentColor" opacity="0.6">valor repassado</text>

	<!-- ── Legend ────────────────────────────────────────────────────────────── -->
	<rect x={lx1} y={LG_Y - 6} width={12} height={12} rx="0" fill={colorFem} />
	<text x={lx1 + 16} y={LG_Y + 1} font-size="12" fill="currentColor" dominant-baseline="central">Feminino</text>
	<rect x={lx2} y={LG_Y - 6} width={12} height={12} rx="0" fill={colorMasc} />
	<text x={lx2 + 16} y={LG_Y + 1} font-size="12" fill="currentColor" dominant-baseline="central">Masculino</text>
</svg>
