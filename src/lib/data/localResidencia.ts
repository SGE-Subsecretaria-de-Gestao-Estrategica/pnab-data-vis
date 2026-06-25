// Capital / Região Metropolitana / Interior distribution for Section 5.
//
// Only one per-UF source exists — aggregate_estado_by_uf_local_residencia.csv —
// and it is at the *estados* (executor estadual) level (its total matches the
// estados visão, ~R$1,47 bi). There is no per-UF file for the uf-combined or
// municipal levels, so this section offers only the Estados and Regiões visões.
// Region rows and the Brasil reference are aggregated from this same source.

import csvRaw from '../../../data/section_1/aggregate_estado_by_uf_local_residencia.csv?raw';
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

export const RESID_KEYS = ['capital', 'metropolitana', 'interior'] as const;
export const RESID_LABELS: Record<string, string> = {
	capital: 'Capital',
	metropolitana: 'Região Metropolitana',
	interior: 'Interior',
};

interface AbsRow {
	uf: string;
	capital: number;
	metropolitana: number;
	interior: number;
}

const absByUf: Record<string, AbsRow> = (() => {
	const out: Record<string, AbsRow> = {};
	for (const d of parseCSV(csvRaw)) {
		if (!d.uf) continue;
		out[d.uf] = {
			uf: d.uf,
			capital: +d.valor_transacao_capital || 0,
			metropolitana: +d.valor_transacao_regiao_metropolitana || 0,
			interior: +d.valor_transacao_interior || 0,
		};
	}
	return out;
})();

// Type alias (not interface) so it satisfies the chart's Record<string, …> prop.
export type ResidRow = {
	label: string;
	capital: number;       // % do valor
	metropolitana: number; // % do valor
	interior: number;      // % do valor
};

function toPct(label: string, rows: AbsRow[]): ResidRow {
	const cap = rows.reduce((s, r) => s + r.capital, 0);
	const met = rows.reduce((s, r) => s + r.metropolitana, 0);
	const int = rows.reduce((s, r) => s + r.interior, 0);
	const total = cap + met + int || 1;
	return {
		label,
		capital: (cap / total) * 100,
		metropolitana: (met / total) * 100,
		interior: (int / total) * 100,
	};
}

type ResidVisao = 'estados' | 'regioes';

/**
 * Build the comparison set: a Brasil reference row first, then one row per
 * scoped UF (visão estados) or per region (visão regioes).
 */
export function residenciaComparison(
	visao: ResidVisao,
	filteredUFs: string[],
	regiaoFilter: 'Todas' | Regiao
): ResidRow[] {
	const brasil = toPct('Brasil', Object.values(absByUf));

	let entities: ResidRow[];
	if (visao === 'regioes') {
		const regs = regiaoFilter === 'Todas' ? REGIOES : [regiaoFilter];
		entities = regs.map((r) =>
			toPct(r, Object.values(absByUf).filter((row) => regionMap[row.uf] === r))
		);
	} else {
		entities = filteredUFs
			.map((uf) => (absByUf[uf] ? toPct(uf, [absByUf[uf]]) : null))
			.filter((e): e is ResidRow => e !== null);
	}
	// Mais interior no topo (depois do Brasil).
	entities.sort((a, b) => b.interior - a.interior);
	return [brasil, ...entities];
}
