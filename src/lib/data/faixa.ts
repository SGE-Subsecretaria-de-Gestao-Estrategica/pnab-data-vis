// Faixa-de-valor distribution data for Section 3.
//
// For each UF we have, per faixa, the % of payments (qtd) and the % of value
// (valor). Source CSVs cover two visões — `uf` (estado + municípios combinados)
// and `estados` (executor estadual). There is no municipality- or region-level
// faixa file, so region aggregates are reconstructed from the `uf` level by
// turning the percentages back into absolute counts/values (perc × total),
// summing, and re-normalising. The same reconstruction gives the "Brasil" row.

import csvUfRaw    from '../../../data/section_2/aggregate_faixa_valor_ju_wide_by_uf.csv?raw';
import csvStateRaw from '../../../data/section_2/aggregate_faixa_valor_ju_wide_by_state.csv?raw';
import { regionMap, REGIOES } from '$lib/data/dashboard';
import type { Regiao } from '$lib/data/dashboard';

function parseCSV(text: string): Record<string, string>[] {
	const [headerLine, ...dataLines] = text.trim().split('\n');
	const headers = headerLine.split(',');
	return dataLines
		.filter((l) => l.trim())
		.map((line) => {
			const values = line.split(',');
			return Object.fromEntries(headers.map((h, i) => [h, values[i] ?? '']));
		});
}

export const FAIXA_KEYS = ['ate2k', 'de2a10k', 'de10a50k', 'de50a200k', 'acima200k'] as const;
export const FAIXA_LABELS: string[] = ['Até R$2k', 'R$2–10k', 'R$10–50k', 'R$50–200k', '> R$200k'];

const QTD_COLS = [
	'perc_qtd_ate_2_mil', 'perc_qtd_de_2_a_10_mil', 'perc_qtd_de_10_a_50_mil',
	'perc_qtd_de_50_a_200_mil', 'perc_qtd_acima_de_200_mil',
];
const VAL_COLS = [
	'perc_valor_ate_2_mil', 'perc_valor_de_2_a_10_mil', 'perc_valor_de_10_a_50_mil',
	'perc_valor_de_50_a_200_mil', 'perc_valor_acima_de_200_mil',
];

interface AbsRow {
	uf: string;
	qtdAbs: number[];   // absolute payment counts per faixa
	valorAbs: number[]; // absolute value per faixa
}

function absRows(raw: string): Record<string, AbsRow> {
	const out: Record<string, AbsRow> = {};
	for (const d of parseCSV(raw)) {
		if (!d.uf) continue;
		const totQtd = +d.total_contemplados_uf || 0;
		const totVal = +d.valor_total_uf || 0;
		out[d.uf] = {
			uf: d.uf,
			qtdAbs: QTD_COLS.map((c) => (+d[c] || 0) * totQtd),
			valorAbs: VAL_COLS.map((c) => (+d[c] || 0) * totVal),
		};
	}
	return out;
}

// Only `uf` and `estados` have source faixa data.
type FaixaVisao = 'uf' | 'estados' | 'regioes';
const absByVisao: Record<'uf' | 'estados', Record<string, AbsRow>> = {
	uf: absRows(csvUfRaw),
	estados: absRows(csvStateRaw),
};

export interface FaixaEntity {
	label: string;
	isBrasil?: boolean;
	/** % of payments per faixa (aligned to FAIXA_KEYS), sums to ~100. */
	qtd: number[];
	/** % of value per faixa (aligned to FAIXA_KEYS), sums to ~100. */
	valor: number[];
}

function sum(a: number[]): number {
	return a.reduce((s, v) => s + v, 0);
}

function entityFrom(label: string, ufs: AbsRow[], isBrasil = false): FaixaEntity {
	const qtdAbs = FAIXA_KEYS.map((_, i) => sum(ufs.map((r) => r.qtdAbs[i])));
	const valorAbs = FAIXA_KEYS.map((_, i) => sum(ufs.map((r) => r.valorAbs[i])));
	const qs = sum(qtdAbs) || 1;
	const vs = sum(valorAbs) || 1;
	return {
		label,
		isBrasil,
		qtd: qtdAbs.map((v) => (v / qs) * 100),
		valor: valorAbs.map((v) => (v / vs) * 100),
	};
}

/** Share of value in the upper faixas (≥ R$50k) — used for a meaningful sort. */
function highValueShare(e: FaixaEntity): number {
	return e.valor[3] + e.valor[4];
}

/**
 * Build the comparison set for Section 3: a Brasil reference row first, then one
 * entity per scoped UF (visão uf/estados) or per region (visão regioes).
 */
export function faixaComparison(
	visao: FaixaVisao,
	filteredUFs: string[],
	regiaoFilter: 'Todas' | Regiao
): FaixaEntity[] {
	if (visao === 'regioes') {
		const src = absByVisao.uf;
		const brasil = entityFrom('Brasil', Object.values(src), true);
		const regs = regiaoFilter === 'Todas' ? REGIOES : [regiaoFilter];
		const entities = regs
			.map((r) => entityFrom(r, Object.values(src).filter((row) => regionMap[row.uf] === r)))
			.sort((a, b) => highValueShare(b) - highValueShare(a));
		return [brasil, ...entities];
	}

	const src = absByVisao[visao];
	const brasil = entityFrom('Brasil', Object.values(src), true);
	const entities = filteredUFs
		.map((uf) => (src[uf] ? entityFrom(uf, [src[uf]]) : null))
		.filter((e): e is FaixaEntity => e !== null)
		.sort((a, b) => highValueShare(b) - highValueShare(a));
	return [brasil, ...entities];
}
