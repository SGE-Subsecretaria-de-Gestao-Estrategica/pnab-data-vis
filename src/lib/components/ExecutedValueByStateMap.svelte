<script lang="ts">
  import { geoMercator, geoPath } from 'd3-geo';
  import { scaleSequential } from 'd3-scale';
  import { interpolateRgbBasis } from 'd3-interpolate';
  import {
    loadBrazilGeoJSON,
    colorScales,
    measureTextWidth,
    getContrastColor,
    typography,
  } from 'sniic-design-system';

  const FONT_FAMILY = typography.chartValueFontFamily;
  const FONT_SIZE = 11;
  const LINE_SPACING = 13;    // px between label lines
  const FORCE_LEFT     = new Set(['AP', 'DF']);                // labels go left regardless of centroid
  const FORCE_RIGHT    = new Set(['SC', 'TO']);               // labels go right regardless of centroid
  const FORCE_EXTERNAL = new Set(['SC', 'PE', 'PI', 'DF', 'SP', 'AC', 'RR', 'AP', 'TO']);   // always use external leader line
  // Extra rightward offset for specific states (on top of bboxMaxX + ELBOW_GAP)
  const EXTRA_X: Record<string, number> = { RN: 22 };
  // Extra leftward offset for specific left-side labels (subtracted from bboxMinX)
  const EXTRA_LEFT_X: Record<string, number> = { DF: 140 };
  const EXTRA_Y: Record<string, number> = { PI: -100, CE: -30, RN: -25, PB: -15, SE: 10, SP: 20, RR: 0, AP: -40, RJ: 20, ES: 5, SC: 10, TO: -140 };

  interface Props {
    states: Record<string, any>;
    metric: string;
    label?: string;
    format?: (v: number) => string;
    /** Optional second line — receives the full state data row. */
    formatLine2?: (row: any) => string;
  }

  let {
    states,
    metric,
    label = '',
    format = (v: number) => v.toLocaleString('pt-BR'),
    formatLine2 = undefined,
  }: Props = $props();

  let geojson = $state<any>(null);
  let containerEl: HTMLDivElement | undefined = $state();
  let width = $state(600);

  const LABEL_W = 135;
  const ELBOW_GAP = 6;
  // Estimated label block width for overlap checks (sigla + value text)

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

  const TOP_PAD = 45;
  const mapW = $derived(Math.max(0, width - LABEL_W * 2));
  const mapH = $derived(Math.round(mapW * 0.72));
  const svgH = $derived(mapH + 20 + TOP_PAD);

  const valueMap = $derived(
    new Map(Object.entries(states).map(([name, d]) => [name, (d[metric] ?? 0) as number]))
  );

  const maxVal = $derived(Math.max(...valueMap.values(), 1));

  const colorScale = $derived(
    scaleSequential<string>()
      .domain([0, maxVal])
      .interpolator(interpolateRgbBasis(colorScales.blue))
  );

  const projection = $derived.by(() => {
    if (!geojson || mapW <= 0) return null;
    return geoMercator().fitSize([mapW, mapH], geojson);
  });

  const pathFn = $derived(projection ? geoPath(projection) : null);

  // How many label lines are there (sigla + format + optional formatLine2)
  const lineCount = $derived(formatLine2 ? 3 : 2);
  const labelBlockH = $derived((lineCount - 1) * LINE_SPACING);
  const LINE_H = $derived(labelBlockH + 20); // min gap between external label centers

  type StateEntry = {
    name: string;
    sigla: string;
    val: number;
    row: any;
    fill: string;
    cx: number;
    cy: number;
    bboxMinX: number; // leftmost screen x of the state boundary
    bboxMaxX: number; // rightmost screen x of the state boundary
    internal: boolean;
  };

  const stateEntries = $derived.by((): StateEntry[] => {
    if (!pathFn || !geojson) return [];
    return (geojson.features as any[])
      .map((f): StateEntry | null => {
        const name = f.properties.name as string;
        const sigla = f.properties.sigla as string;
        const row = states[name];
        const val = row?.[metric] ?? 0;
        if (val <= 0) return null;

        const c = pathFn.centroid(f) as [number, number];
        if (!isFinite(c[0]) || !isFinite(c[1])) return null;

        const [[x1, y1], [x2, y2]] = pathFn.bounds(f) as [[number, number], [number, number]];
        const bboxW = x2 - x1;
        const bboxH = y2 - y1;
        const fill = colorScale(val);

        const formattedVal = format(val);
        const line2 = formatLine2 ? formatLine2(row) : '';

        const siglaW  = measureTextWidth(sigla,        12,        FONT_FAMILY, 700);
        const valW    = measureTextWidth(formattedVal, FONT_SIZE, FONT_FAMILY, 400);
        const line2W  = line2 ? measureTextWidth(line2, FONT_SIZE, FONT_FAMILY, 400) : 0;
        const neededW = Math.max(siglaW, valW, line2W) + 12;
        const neededH = labelBlockH + 16;

        const internal = !FORCE_EXTERNAL.has(sigla) && bboxW >= neededW && bboxH >= neededH;
        return { name, sigla, val, row, fill, cx: c[0], cy: c[1], bboxMinX: x1, bboxMaxX: x2, internal };
      })
      .filter((d): d is StateEntry => d !== null);
  });

  const internalLabels = $derived(stateEntries.filter((d) => d.internal));
  const externalCentroids = $derived(stateEntries.filter((d) => !d.internal));

  function spaceLabels(items: StateEntry[]) {
    if (!items.length) return items.map((d) => ({ ...d, labelY: d.cy }));
    const result = items.map((d) => ({ ...d, labelY: d.cy }));

    for (let i = 1; i < result.length; i++) {
      const minY = result[i - 1].labelY + LINE_H;
      if (result[i].labelY < minY) result[i].labelY = minY;
    }

    const last = result[result.length - 1];
    const maxY = mapH - labelBlockH / 2 - 4;
    if (last.labelY > maxY) {
      const shift = last.labelY - maxY;
      result.forEach((d) => (d.labelY -= shift));
      const minTop = labelBlockH / 2 + 4;
      if (result[0].labelY < minTop) {
        result[0].labelY = minTop;
        for (let i = 1; i < result.length; i++) {
          const minY = result[i - 1].labelY + LINE_H;
          if (result[i].labelY < minY) result[i].labelY = minY;
        }
      }
    }
    return result;
  }

  const leftExternal = $derived.by(() => {
    const items = externalCentroids
      .filter((d) => !FORCE_RIGHT.has(d.sigla) && (d.cx < mapW / 2 || FORCE_LEFT.has(d.sigla)))
      .sort((a, b) => a.cy - b.cy);
    if (!items.length) return [];

    const MIN_Y_GAP = labelBlockH + 4;
    const X_PROXIMITY = 58;
    const placed: { name: string; labelX: number; labelY: number; [k: string]: any }[] = [];

    for (const d of items) {
      const lx = d.bboxMinX - ELBOW_GAP - (EXTRA_LEFT_X[d.sigla] ?? 0);
      let ly = d.cy;

      const nearX = placed
        .filter((p) => Math.abs(p.labelX - lx) < X_PROXIMITY)
        .sort((a, b) => a.labelY - b.labelY);

      for (const p of nearX) {
        if (ly < p.labelY + MIN_Y_GAP) ly = p.labelY + MIN_Y_GAP;
      }

      placed.push({ ...d, labelX: lx, labelY: ly });
    }

    return placed.map((d) => ({ ...d, labelY: d.labelY + (EXTRA_Y[d.sigla] ?? 0) }));
  });

  const rightExternal = $derived.by(() => {
    // Sort north→south so the northernmost labels are placed first and stay closest to their natural y.
    const items = externalCentroids
      .filter((d) => FORCE_RIGHT.has(d.sigla) || (d.cx >= mapW / 2 && !FORCE_LEFT.has(d.sigla)))
      .sort((a, b) => a.cy - b.cy);
    if (!items.length) return [];

    // labelX = state's own rightmost boundary + small gap.
    // This makes coastal states (bboxMaxX ≈ mapW) sit right next to the coast,
    // and more inland states sit further left — naturally following the coast curve.
    const MIN_Y_GAP = labelBlockH + 4;
    // Labels compete for y-space only when they are close in x (would visually overlap).
    const X_PROXIMITY = 58;

    const placed: { name: string; labelX: number; labelY: number; [k: string]: any }[] = [];

    for (const d of items) {
      const lx = d.bboxMaxX + ELBOW_GAP + (EXTRA_X[d.sigla] ?? 0);
      let ly = d.cy;

      // Among already-placed labels at similar x, push y down to avoid overlap.
      const nearX = placed
        .filter((p) => Math.abs(p.labelX - lx) < X_PROXIMITY)
        .sort((a, b) => a.labelY - b.labelY);

      for (const p of nearX) {
        if (ly < p.labelY + MIN_Y_GAP) ly = p.labelY + MIN_Y_GAP;
      }

      placed.push({ ...d, labelX: lx, labelY: ly });
    }

    return placed.map((d) => ({ ...d, labelY: d.labelY + (EXTRA_Y[d.sigla] ?? 0) }));
  });
</script>

<div bind:this={containerEl} style="width: 100%">
  {#if geojson && pathFn && mapW > 0}
    <svg width={width} height={svgH}>
      <g transform={`translate(${LABEL_W}, ${TOP_PAD})`}>

        <!-- State fills -->
        {#each geojson.features as f (f.properties.name)}
          {@const d = pathFn(f)}
          {#if d}
            <path
              d={d}
              fill={colorScale(valueMap.get(f.properties.name) ?? 0) ?? '#e5e7eb'}
              stroke="white"
              stroke-width="0.5"
            />
          {/if}
        {/each}

        <!-- Internal labels: sigla / R$ / % stacked at centroid -->
        {#each internalLabels as item (item.name)}
          {@const textFill = getContrastColor(item.fill)}
          <text
            x={item.cx}
            y={item.cy}
            text-anchor="middle"
            font-size={FONT_SIZE}
            font-family={FONT_FAMILY}
            fill={textFill}
            pointer-events="none"
          >
            <tspan x={item.cx} dy={-(labelBlockH / 2)} font-weight="700" font-size="12">{item.sigla}</tspan>
            <tspan x={item.cx} dy={LINE_SPACING}>{format(item.val)}</tspan>
            {#if formatLine2}
              <tspan x={item.cx} dy={LINE_SPACING}>{formatLine2(item.row)}</tspan>
            {/if}
          </text>
        {/each}

        <!-- External labels — left side -->
        {#each leftExternal as item (item.name)}
          <line
            x1={item.cx} y1={item.cy}
            x2={item.labelX} y2={item.labelY}
            stroke="#9ca3af"
            stroke-width="0.7"
          />
          <circle cx={item.cx} cy={item.cy} r={2} fill="#9ca3af" />
          <text
            x={item.labelX - 4}
            y={item.labelY}
            text-anchor="end"
            font-size={FONT_SIZE}
            font-family={FONT_FAMILY}
            fill="#374151"
          >
            <tspan x={item.labelX - 4} dy={-(labelBlockH / 2)} font-weight="700" font-size="12">{item.sigla}</tspan>
            <tspan x={item.labelX - 4} dy={LINE_SPACING}>{format(item.val)}</tspan>
            {#if formatLine2}
              <tspan x={item.labelX - 4} dy={LINE_SPACING}>{formatLine2(item.row)}</tspan>
            {/if}
          </text>
        {/each}

        <!-- External labels — right side -->
        <!-- Straight diagonal line from centroid to label, positioned right next to each state's coast -->
        {#each rightExternal as item (item.name)}
          <line
            x1={item.cx} y1={item.cy}
            x2={item.labelX} y2={item.labelY}
            stroke="#9ca3af"
            stroke-width="0.7"
          />
          <circle cx={item.cx} cy={item.cy} r={2} fill="#9ca3af" />
          <text
            x={item.labelX + 4}
            y={item.labelY}
            text-anchor="start"
            font-size={FONT_SIZE}
            font-family={FONT_FAMILY}
            fill="#374151"
          >
            <tspan x={item.labelX + 4} dy={-(labelBlockH / 2)} font-weight="700" font-size="12">{item.sigla}</tspan>
            <tspan x={item.labelX + 4} dy={LINE_SPACING}>{format(item.val)}</tspan>
            {#if formatLine2}
              <tspan x={item.labelX + 4} dy={LINE_SPACING}>{formatLine2(item.row)}</tspan>
            {/if}
          </text>
        {/each}

      </g>
    </svg>
  {/if}
</div>
