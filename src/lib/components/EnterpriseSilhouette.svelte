<script lang="ts">
	import { AnnotationBox } from 'sniic-design-system';

	const teal = '#265c4f';
	const orange = '#ea662f';
	const chartValueFontFamily = "'Rawline', system-ui, sans-serif";

	interface Annotation {
		side: 'left' | 'right';
		pointX: number;
		pointY: number;
		boxX: number;
		boxY: number;
		title: string;
		subtitle?: string;
		color?: string;
		boxWidth?: number;
		boxHeight?: number;
		circleRadius?: number;
	}

	interface Props {
		width?: number;
		height?: number;
		strokeColor?: string;
		strokeWidth?: number;
		annotations?: Annotation[];
	}

	let {
		width = 900,
		height = 600,
		strokeColor = teal,
		strokeWidth = 2,
		annotations = [],
	}: Props = $props();

	const buildingPath = `
    M 638,88
    L 638,135
    L 518,135
    L 518,548
    L 660,548
    L 660,475
    L 726,475
    L 726,548
    L 865,548
    L 865,135
    L 748,135
    L 748,88
    Z
  `;

	const winW = 20;
	const winH = 30;

	function grid(cols: number[], rows: number[]): { x: number; y: number }[] {
		return cols.flatMap((cx) => rows.map((ry) => ({ x: cx, y: ry })));
	}

	const centerWindows = grid([652, 680, 708], [108, 150, 192, 234, 276, 318, 360, 402]);
	const leftWindows = grid([536, 572], [158, 210, 262, 314, 366, 418]);
	const rightWindows = grid([764, 800], [158, 210, 262, 314, 366, 418]);
	const allWindows = [...centerWindows, ...leftWindows, ...rightWindows];
</script>

<svg {width} {height} viewBox="0 0 {width} {height}" style="font-family: {chartValueFontFamily};">
	<path
		d={buildingPath}
		fill="var(--silhouette-fill, #dce8e5)"
		stroke={strokeColor}
		stroke-width={strokeWidth}
		stroke-linejoin="round"
		stroke-linecap="round"
	/>
	{#each allWindows as w (w.x + '-' + w.y)}
		<rect
			x={w.x}
			y={w.y}
			width={winW}
			height={winH}
			fill="var(--window-fill, #b0cfc9)"
			stroke={strokeColor}
			stroke-width="0.8"
			rx="2"
		/>
	{/each}
	<line
		x1={518}
		y1={548}
		x2={865}
		y2={548}
		stroke={strokeColor}
		stroke-width={strokeWidth}
	/>
	{#each annotations as ann (ann.title + ann.side)}
		<AnnotationBox
			pointX={ann.pointX}
			pointY={ann.pointY}
			boxX={ann.boxX}
			boxY={ann.boxY}
			title={ann.title}
			subtitle={ann.subtitle ?? ''}
			color={ann.color ?? orange}
			boxWidth={ann.boxWidth ?? 190}
			boxHeight={ann.boxHeight}
			circleRadius={ann.circleRadius ?? 12}
		/>
	{/each}
</svg>
