<script lang="ts">
	interface Entry {
		posicao: number;
		descricao: string;
		percQuantidade: number;
		percQuantidadeFormatted: string;
		percValor: number;
		percValorFormatted: string;
	}

	interface Props {
		data: Entry[];
		metric: 'quantidade' | 'valor';
		width?: number;
	}

	let { data, metric, width = 700 }: Props = $props();

	// ── Layout constants ──────────────────────────────────────────────────────
	const HEADER_H  = 44;
	const RANK_CX   = 28;
	const DESC_X    = 58;
	const DESC_W    = 360;
	const BAR_X     = 430;
	const BAR_TW    = 210;
	const PCT_X     = 646;  // text-anchor="start", 6px after bar end (640)
	const PAD_Y     = 10;
	const FS        = 13;
	const FS_HDR    = 10;
	const LH        = FS * 1.4;
	const CW        = FS * 0.55;
	const MIN_H_POD = 54;
	const MIN_H     = 42;
	const BAR_H_POD = 10;
	const BAR_H_DEF = 7;
	const MEDAL_R   = 15;
	const BADGE_R   = 12;

	// ── sniic design-system palette ───────────────────────────────────────────
	// teal:   #cce8e3 / #95c0b7 / #317a68 / #255c4f / #102a24
	// blue:   #d5e4f7 / #9fbbe0 / #4271b5 / #2e4e8a / #0b1540
	// yellow: #fef6cc / #f9e6a1 / #f6c341 / #bf8e2b / #5c3908
	// orange: #fde9d4 / #f7bf95 / #ea662f / #ab4723 / #431609
	// lavend: #f4eff3 / #e5dbe3 / #c9b6c5 / #958191 / #3d2a3a

	// ── Medal palette (uses sniic yellow / lavender / orange) ─────────────────
	type Medal = { body: string; ring: string; textFill: string; accent: string; bgTint: string; qtdFill: string; valFill: string };
	const MEDALS: Record<number, Medal> = {
		1: { body: '#f6c341', ring: '#bf8e2b', textFill: '#5c3908', accent: '#bf8e2b', bgTint: 'rgba(246,195,65,0.10)',  qtdFill: '#bf8e2b', valFill: '#5c3908' },
		2: { body: '#c9b6c5', ring: '#958191', textFill: '#1a1a1a', accent: '#958191', bgTint: 'rgba(201,182,197,0.12)', qtdFill: '#958191', valFill: '#3d2a3a' },
		3: { body: '#ea662f', ring: '#ab4723', textFill: '#fff',    accent: '#ab4723', bgTint: 'rgba(234,102,47,0.08)',  qtdFill: '#ab4723', valFill: '#431609' },
	};
	const DEF_QTD   = '#317a68'; // teal[2]
	const DEF_VAL   = '#4271b5'; // blue[2]
	const TRACK_CLR = 'rgba(0,0,0,0.07)';
	const HDR_CLR   = '#255c4f'; // teal[3]
	const SEP_CLR   = 'rgba(0,0,0,0.09)';
	const TXT_CLR   = 'var(--chart-fg-strong, #1a1a1a)';
	const FONT      = "'Inter', system-ui, sans-serif";

	// ── Derived from metric ───────────────────────────────────────────────────
	const isQtd      = $derived(metric === 'quantidade');
	const hdrLabel   = $derived(isQtd ? '% BENEFICIÁRIOS' : '% VALOR REPASSADO');
	const hdrSub     = $derived(isQtd ? 'quantidade' : 'valor');
	const hdrSubClr  = $derived(isQtd ? DEF_QTD : DEF_VAL);
	const defBarClr  = $derived(isQtd ? DEF_QTD : DEF_VAL);
	const maxVal     = $derived(isQtd
		? Math.max(...data.map((d) => d.percQuantidade))
		: Math.max(...data.map((d) => d.percValor)));

	// ── Text wrapping ─────────────────────────────────────────────────────────
	function wrap(text: string): string[] {
		const max   = Math.max(1, Math.floor(DESC_W / CW));
		const words = text.split(' ');
		const lines: string[] = [];
		let cur = '';
		for (const w of words) {
			const cand = cur ? `${cur} ${w}` : w;
			if (cand.length > max && cur) { lines.push(cur); cur = w; }
			else cur = cand;
		}
		if (cur) lines.push(cur);
		return lines;
	}

	// ── Row layout ────────────────────────────────────────────────────────────
	const rows = $derived.by(() =>
		data.map((e) => {
			const lines   = wrap(e.descricao);
			const isPod   = e.posicao <= 3;
			const minH    = isPod ? MIN_H_POD : MIN_H;
			const rowH    = Math.max(minH, lines.length * LH + PAD_Y * 2);
			const medal   = MEDALS[e.posicao] ?? null;
			const percVal = isQtd ? e.percQuantidade : e.percValor;
			const percFmt = isQtd ? e.percQuantidadeFormatted : e.percValorFormatted;
			return { ...e, lines, rowH, isPod, medal, percVal, percFmt };
		})
	);

	const rowYs = $derived.by(() => {
		const ys: number[] = [];
		let cy = HEADER_H;
		for (const r of rows) { ys.push(cy); cy += r.rowH; }
		return ys;
	});
</script>

<g font-family={FONT}>

	<!-- ── Header ──────────────────────────────────────────────────────────── -->
	<text x={RANK_CX} y={HEADER_H - 14} text-anchor="middle"
		font-size={FS_HDR} fill={HDR_CLR} font-weight="700" letter-spacing="0.8">#</text>
	<text x={DESC_X} y={HEADER_H - 14}
		font-size={FS_HDR} fill={HDR_CLR} font-weight="700" letter-spacing="0.8">ATIVIDADE ECONÔMICA (CNAE)</text>
	<text x={BAR_X} y={HEADER_H - 24}
		font-size={FS_HDR} fill={HDR_CLR} font-weight="700" letter-spacing="0.8">{hdrLabel}</text>
	<text x={BAR_X} y={HEADER_H - 12}
		font-size={FS_HDR - 1} fill={hdrSubClr} font-weight="700">{hdrSub}</text>
	<line x1={0} y1={HEADER_H} x2={width} y2={HEADER_H}
		stroke={HDR_CLR} stroke-width={1.5} opacity={0.35} />

	<!-- ── Rows ────────────────────────────────────────────────────────────── -->
	{#each rows as row, i}
		{@const ry      = rowYs[i]}
		{@const rh      = row.rowH}
		{@const cy      = ry + rh / 2}
		{@const bh      = row.isPod ? BAR_H_POD : BAR_H_DEF}
		{@const barW    = (row.percVal / maxVal) * BAR_TW}
		{@const barFill = row.medal ? row.medal.qtdFill : defBarClr}

		<!-- Row background -->
		{#if row.medal}
			<rect x={0} y={ry} width={width} height={rh} fill={row.medal.bgTint} />
			<rect x={0} y={ry} width={3} height={rh} fill={row.medal.accent} />
		{:else if i % 2 === 1}
			<rect x={0} y={ry} width={width} height={rh} fill="rgba(0,0,0,0.02)" />
		{/if}

		<!-- ── Medal / rank badge ── -->
		<g transform="translate({RANK_CX},{cy})">
			{#if row.medal}
				<circle r={MEDAL_R + 3} fill={row.medal.body} opacity={0.18} />
				<circle r={MEDAL_R} fill={row.medal.body} />
				<ellipse cx={-4} cy={-4.5} rx={MEDAL_R * 0.48} ry={MEDAL_R * 0.4}
					fill="rgba(255,255,255,0.32)" />
				<circle r={MEDAL_R - 3.5} fill="none" stroke={row.medal.ring}
					stroke-width={1.2} opacity={0.55} />
				<text text-anchor="middle" dominant-baseline="central"
					font-size={13} font-weight="800" fill={row.medal.textFill}>{row.posicao}</text>
			{:else}
				<circle r={BADGE_R} fill="rgba(0,0,0,0.05)" stroke="rgba(0,0,0,0.12)" stroke-width={0.8} />
				<text text-anchor="middle" dominant-baseline="central"
					font-size={11} font-weight="600" fill={TXT_CLR} opacity={0.6}>{row.posicao}</text>
			{/if}
		</g>

		<!-- ── Description ── -->
		{#each row.lines as line, li}
			<text
				x={DESC_X}
				y={ry + PAD_Y + li * LH + FS}
				font-size={FS}
				font-weight={row.isPod ? '600' : '400'}
				fill={TXT_CLR}
			>{line}</text>
		{/each}

		<!-- ── Bar ── -->
		<rect x={BAR_X} y={cy - bh / 2} width={BAR_TW} height={bh}
			rx={bh / 2} fill={TRACK_CLR} />
		<rect x={BAR_X} y={cy - bh / 2} width={barW} height={bh}
			rx={bh / 2} fill={barFill} />
		<text
			x={PCT_X}
			y={cy + FS * 0.38}
			text-anchor="start"
			font-size={FS}
			font-weight={row.isPod ? '700' : '500'}
			fill={row.medal ? row.medal.accent : TXT_CLR}
			opacity={row.medal ? 1 : 0.75}
		>{row.percFmt}</text>

		<!-- Row separator -->
		<line x1={0} y1={ry + rh} x2={width} y2={ry + rh}
			stroke={SEP_CLR} stroke-width={0.5} />
	{/each}

</g>
