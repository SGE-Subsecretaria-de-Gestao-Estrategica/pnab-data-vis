// Section 9 data — Distribuição de contemplados PJ por tipo de organização.
//
// Fonte: cruzamento PNAB × Receita Federal (pessoas jurídicas / CNPJ).
// Há quebra por UF para cada visão (nível de execução):
//   • uf         → estado + municípios combinados (…_por_uf.csv)
//   • estados    → apenas execução estadual         (…_por_state.csv)
//   • municipios → apenas execução municipal         (…_por_municipio.csv)
//   • regioes    → mesmo recorte de `uf` (combinado), agregado por região
// O escopo (Brasil / região / UF) é resolvido somando-se as UFs em foco.

import csvUfRaw    from '../../../data/section_3/aggregate_cnpj_natureza_juridica_por_uf.csv?raw';
import csvStateRaw from '../../../data/section_3/aggregate_cnpj_natureza_juridica_por_state.csv?raw';
import csvMunRaw   from '../../../data/section_3/aggregate_cnpj_natureza_juridica_por_municipio.csv?raw';

import type { Visao } from '$lib/data/dashboard';

function parseCSV(text: string): Record<string, string>[] {
	const [headerLine, ...dataLines] = text.trim().split('\n');
	const headers = headerLine.split(',').map((h) => h.trim());
	return dataLines
		.filter((l) => l.trim())
		.map((line) => {
			const values = line.split(',').map((v) => v.trim());
			return Object.fromEntries(headers.map((h, i) => [h, values[i] ?? '']));
		});
}

export interface OrgBar {
	label: string; // natureza jurídica
	value: number; // quantidade de contemplados
	perc: number; // % dos contemplados PJ no escopo (0–100)
}

export interface OrgScope {
	bars: OrgBar[]; // ordenado por quantidade desc
	total: number; // total de contemplados PJ no escopo
}

const _NJ_ORDER = [
	'Microempresa-ME',
	'MEI',
	'Empresa de Pequeno Porte (EPP)',
	'Administração Pública',
	'Entidades sem fins lucrativos',
	'Entidades Empresariais',
];

// ── Per-UF, per-natureza quantities, indexed by [uf][natureza] ────────────────
type UfNatureza = Record<string, Record<string, number>>;

function indexByUf(raw: string): UfNatureza {
	const out: UfNatureza = {};
	for (const r of parseCSV(raw)) {
		if (!r.uf || !_NJ_ORDER.includes(r.natureza_juridica)) continue;
		(out[r.uf] ??= {})[r.natureza_juridica] = +r.quantidade_contemplados || 0;
	}
	return out;
}

const ufTable: Record<Visao, UfNatureza> = {
	uf: indexByUf(csvUfRaw),
	estados: indexByUf(csvStateRaw),
	municipios: indexByUf(csvMunRaw),
	regioes: indexByUf(csvUfRaw), // região = soma das UFs no nível combinado
};

/**
 * Agrega a distribuição por natureza jurídica para a `visao` somando as `ufs`
 * em foco (Brasil = todas as 27 UFs; região/UF conforme o filtro).
 */
export function orgScope(visao: Visao, ufs: string[]): OrgScope {
	const table = ufTable[visao];
	const sums: Record<string, number> = {};
	for (const nj of _NJ_ORDER) sums[nj] = 0;
	for (const uf of ufs) {
		const row = table[uf];
		if (!row) continue;
		for (const nj of _NJ_ORDER) sums[nj] += row[nj] ?? 0;
	}
	const total = _NJ_ORDER.reduce((s, nj) => s + sums[nj], 0);
	const bars = _NJ_ORDER
		.map((nj) => ({
			label: nj,
			value: sums[nj],
			perc: total > 0 ? (sums[nj] / total) * 100 : 0,
		}))
		.sort((a, b) => b.value - a.value);
	return { bars, total };
}
