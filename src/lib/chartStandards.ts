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

/**
 * Hairline outline drawn around state-flag chips so flags with white areas
 * stay separated from the (usually white) background. Enabled by default via
 * each chart's `flagBorder` prop.
 */
export const FLAG_BORDER_COLOR = '#94a3b8';
export const FLAG_BORDER_WIDTH = 0.5;

/** True when a row label is a Brazilian state abbreviation (has a flag). */
export function isState(label: string): boolean {
	return Object.prototype.hasOwnProperty.call(siglaToName, String(label).toUpperCase());
}

/** True when a row label is the national "Brasil" aggregate (has a flag). */
export function isBrasil(label: string): boolean {
	return String(label).trim().toLowerCase() === 'brasil';
}

/** True when a row label has a flag chip available (a state or the Brasil total). */
export function hasFlag(label: string): boolean {
	return isState(label) || isBrasil(label);
}

/** Flag file id for a row label: `BR` for the Brasil total, the sigla otherwise. */
export function flagId(label: string): string {
	return isBrasil(label) ? 'BR' : String(label).toUpperCase();
}

/** Human-readable title for a flag chip (tooltip). */
export function flagTitle(label: string): string {
	if (isBrasil(label)) return 'Brasil';
	return siglaToName[String(label).toUpperCase()] ?? label;
}

/**
 * Axis label shown next to a flag chip. When flags are visible the Brasil total
 * is abbreviated to "BR" so it lines up with the state siglas (SP, RJ, …); with
 * no flags the full "Brasil" label is kept.
 */
export function flagAwareLabel(label: string, showFlags: boolean): string {
	return showFlags && isBrasil(label) ? 'BR' : label;
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
