<script lang="ts">
	interface Entry {
		posicao: number;
		descricao: string;
		percValor: number;
		percFormatted: string;
	}

	interface Props {
		data: Entry[];
		width?: number;
	}

	let { data, width = 700 }: Props = $props();

	// ── Layout constants ──────────────────────────────────────────────────────
	const HEADER_H  = 40;
	const RANK_CX   = 28;   // rank column center x
	const DESC_X    = 58;   // description text start x
	const DESC_W    = 272;  // description available width
	const BAR_X     = 346;  // bar track start x
	const BAR_TW    = 224;  // bar track width
	const PCT_X     = width - 10; // percentage label right edge
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

	// ── Medal palette ─────────────────────────────────────────────────────────
	type Medal = { body: string; ring: string; textFill: string; accent: string; bgTint: string; barFill: string };
	const MEDALS: Record<number, Medal> = {
		1: { body: '#F4C430', ring: '#B8920C', textFill: '#2C1800', accent: '#C9A000', bgTint: 'rgba(244,196,48,0.08)',  barFill: '#C9A000' },
		2: { body: '#C8CDD6', ring: '#8A9099', textFill: '#1a1a1a', accent: '#8A9099', bgTint: 'rgba(200,205,214,0.10)', barFill: '#8A9099' },
		3: { body: '#CE8B47', ring: '#9B5E1A', textFill: '#fff4e0', accent: '#A06830', bgTint: 'rgba(206,139,71,0.08)',  barFill: '#A06830' },
	};
	const DEF_BAR   = '#317a68';
	const TRACK_CLR = 'rgba(0,0,0,0.07)';
	const HDR_CLR   = '#265c4f';
	const SEP_CLR   = 'rgba(0,0,0,0.09)';
	const TXT_CLR   = 'var(--chart-fg-strong, #1a1a1a)';
	const FONT      = "'Inter', system-ui, sans-serif";

	// ── Text wrapping ─────────────────────────────────────────────────────────
	function wrap(text: string): string[] {
		const max = Math.max(1, Math.floor(DESC_W / CW));
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
	const rows = $derived.by(() => {
		return data.map((e) => {
			const lines  = wrap(e.descricao);
			const isPod  = e.posicao <= 3;
			const minH   = isPod ? MIN_H_POD : MIN_H;
			const rowH   = Math.max(minH, lines.length * LH + PAD_Y * 2);
			const medal  = MEDALS[e.posicao] ?? null;
			return { ...e, lines, rowH, isPod, medal };
		});
	});

	const rowYs = $derived.by(() => {
		const ys: number[] = [];
		let cy = HEADER_H;
		for (const r of rows) { ys.push(cy); cy += r.rowH; }
		return ys;
	});

	const maxVal = $derived(Math.max(...data.map(d => d.percValor)));
</script>

<g font-family={FONT}>

	<!-- ── Header ──────────────────────────────────────────────────────────── -->
	<text x={RANK_CX} y={HEADER_H - 12} text-anchor="middle"
		font-size={FS_HDR} fill={HDR_CLR} font-weight="700" letter-spacing="0.8">#</text>
	<text x={DESC_X} y={HEADER_H - 12}
		font-size={FS_HDR} fill={HDR_CLR} font-weight="700" letter-spacing="0.8">OCUPAÇÃO</text>
	<text x={BAR_X} y={HEADER_H - 12}
		font-size={FS_HDR} fill={HDR_CLR} font-weight="700" letter-spacing="0.8">% DO VALOR TRANSFERIDO</text>
	<line x1={0} y1={HEADER_H} x2={width} y2={HEADER_H}
		stroke={HDR_CLR} stroke-width={1.5} opacity={0.35} />

	<!-- ── Rows ────────────────────────────────────────────────────────────── -->
	{#each rows as row, i}
		{@const ry  = rowYs[i]}
		{@const rh  = row.rowH}
		{@const cy  = ry + rh / 2}
		{@const bh  = row.isPod ? BAR_H_POD : BAR_H_DEF}
		{@const bw  = (row.percValor / maxVal) * BAR_TW}
		{@const bFill = row.medal ? row.medal.barFill : DEF_BAR}

		<!-- Row background -->
		{#if row.medal}
			<rect x={0} y={ry} width={width} height={rh} fill={row.medal.bgTint} />
			<!-- Left accent border -->
			<rect x={0} y={ry} width={3} height={rh} fill={row.medal.accent} />
		{:else if i % 2 === 1}
			<rect x={0} y={ry} width={width} height={rh} fill="rgba(0,0,0,0.02)" />
		{/if}

		<!-- ── Medal / rank badge ── -->
		<g transform="translate({RANK_CX},{cy})">
			{#if row.medal}
				<!-- Outer glow ring for podium -->
				<circle r={MEDAL_R + 3} fill={row.medal.body} opacity={0.18} />
				<!-- Medal body -->
				<circle r={MEDAL_R} fill={row.medal.body} />
				<!-- Shine highlight (top-left arc) -->
				<ellipse cx={-4} cy={-4.5} rx={MEDAL_R * 0.48} ry={MEDAL_R * 0.4}
					fill="rgba(255,255,255,0.32)" />
				<!-- Inner decorative ring -->
				<circle r={MEDAL_R - 3.5} fill="none" stroke={row.medal.ring}
					stroke-width={1.2} opacity={0.55} />
				<!-- Rank number -->
				<text text-anchor="middle" dominant-baseline="central"
					font-size={13} font-weight="800" fill={row.medal.textFill}>{row.posicao}</text>
			{:else}
				<!-- Plain rank badge (subtle circle) -->
				<circle r={BADGE_R} fill="rgba(0,0,0,0.05)" stroke="rgba(0,0,0,0.12)" stroke-width={0.8} />
				<text text-anchor="middle" dominant-baseline="central"
					font-size={11} font-weight="600"
					fill={TXT_CLR} opacity={0.6}>{row.posicao}</text>
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

		<!-- ── Bar track + fill ── -->
		<rect x={BAR_X} y={cy - bh / 2} width={BAR_TW} height={bh}
			rx={bh / 2} fill={TRACK_CLR} />
		<rect x={BAR_X} y={cy - bh / 2} width={bw} height={bh}
			rx={bh / 2} fill={bFill} />

		<!-- ── Percentage label ── -->
		<text
			x={PCT_X}
			y={cy + FS * 0.38}
			text-anchor="end"
			font-size={FS}
			font-weight={row.isPod ? '700' : '500'}
			fill={row.medal ? row.medal.accent : TXT_CLR}
			opacity={row.medal ? 1 : 0.75}
		>{row.percFormatted}</text>

		<!-- Row separator -->
		<line x1={0} y1={ry + rh} x2={width} y2={ry + rh}
			stroke={SEP_CLR} stroke-width={0.5} />
	{/each}

</g>
