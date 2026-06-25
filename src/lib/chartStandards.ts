// Shared visual standard for every horizontal bar chart in the app, so they
// all share the same dimensions (bar thickness, label/flag column) regardless
// of which Custom component renders them. Reference: Gráfico 7.

import { siglaToName } from '$lib/data/dashboard';

/** Row pitch (bar + gap) used by all horizontal bar charts. */
export const CHART_ROW_HEIGHT = 48;

/**
 * Fraction of the row pitch occupied by the bar itself. The single-series chart
 * multiplies `rowHeight` by this; the stacked chart derives the same thickness
 * via `paddingInner = 1 - BAR_FILL`, so both produce visually identical bars.
 */
export const BAR_FILL = 0.84;

/** State-flag aspect ratio (3:2) and the gap between flag and the bars area. */
export const FLAG_RATIO = 3 / 2;
export const FLAG_GAP = 6;

/** True when a row label is a Brazilian state abbreviation (has a flag). */
export function isState(label: string): boolean {
	return Object.prototype.hasOwnProperty.call(siglaToName, String(label).toUpperCase());
}

/**
 * Truncate a label with an ellipsis so it fits `availPx` at the given font size.
 * Keeps charts using the full device width without labels overflowing on mobile.
 */
export function truncateToWidth(label: string, availPx: number, fontSize = 12): string {
	const charPx = fontSize * 0.6;
	const maxChars = Math.floor(availPx / charPx);
	if (maxChars >= label.length) return label;
	if (maxChars <= 1) return '…';
	return label.slice(0, maxChars - 1).trimEnd() + '…';
}
