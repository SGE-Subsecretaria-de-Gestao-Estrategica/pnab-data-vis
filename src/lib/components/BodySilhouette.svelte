<script lang="ts">
	import { AnnotationBox } from 'sniic-design-system';

	const teal = '#265c4f';
	const orange = '#ea662f';
	const chartValueFontFamily = "'Space Grotesk', system-ui, sans-serif";

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

	const headPath = `
    M 230,40
    C 246,40 258,52 258,68
    C 258,84 246,96 230,96
    C 214,96 202,84 202,68
    C 202,52 214,40 230,40
    Z
  `;

	const bodyPath = `
    M 220,96
    L 220,116
    L 154,140
    C 142,144 134,156 132,168
    L 110,248
    C 108,254 112,260 118,260
    L 134,260
    C 140,260 145,254 147,248
    L 166,188
    L 178,168
    L 178,304
    L 170,400
    L 166,432
    L 158,528
    C 156,536 162,542 170,542
    L 202,542
    C 208,542 212,538 212,532
    L 218,432
    L 226,344
    L 234,432
    L 240,532
    C 240,538 244,542 250,542
    L 282,542
    C 290,542 296,536 294,528
    L 286,432
    L 282,400
    L 274,304
    L 274,168
    L 286,188
    L 305,248
    C 307,254 312,260 318,260
    L 334,260
    C 340,260 344,254 342,248
    L 320,168
    C 318,156 310,144 298,140
    L 240,116
    L 240,96
  `;
</script>

<svg {width} {height} viewBox="0 0 {width} {height}" style="font-family: {chartValueFontFamily};">
	<path
		d={bodyPath}
		fill="var(--silhouette-fill, #dce8e5)"
		stroke={strokeColor}
		stroke-width={strokeWidth}
		stroke-linejoin="round"
		stroke-linecap="round"
	/>
	<path
		d={headPath}
		fill="var(--silhouette-fill, #dce8e5)"
		stroke={strokeColor}
		stroke-width={strokeWidth}
		stroke-linejoin="round"
		stroke-linecap="round"
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
