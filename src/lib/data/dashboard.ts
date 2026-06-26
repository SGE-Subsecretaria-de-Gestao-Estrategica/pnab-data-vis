// Dashboard data layer for Section 1 — "Valores Gerais da Pesquisa".
//
// Three "visões" (entity levels) are supported, each with one row per UF:
//   • uf         → estado + municípios combinados (executed_value_by_uf.csv)
//   • estados    → apenas execução estadual        (executed_value_by_state.csv)
//   • municipios → apenas execução municipal        (executed_value_by_municipality.csv)
// Region aggregates are derived from the `uf` level grouped by região.
//
// Note: there is no per-UF municipality count in the source data, so the
// "número de entes" headline is exact for the `estados` visão (= nº de UFs) and
// uses the national totals (27 estados / 5.098 municípios) for the other visões.

import csvUfRaw    from '../../../data/section_1/executed_value_by_uf.csv?raw';
import csvStateRaw from '../../../data/section_1/executed_value_by_state.csv?raw';
import csvMunRaw   from '../../../data/section_1/executed_value_by_municipality.csv?raw';

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

// ── Lookup tables ───────────────────────────────────────────────────────────
export const siglaToName: Record<string, string> = {
	AC: 'Acre',              AL: 'Alagoas',             AM: 'Amazonas',
	AP: 'Amapá',             BA: 'Bahia',               CE: 'Ceará',
	DF: 'Distrito Federal',  ES: 'Espírito Santo',      GO: 'Goiás',
	MA: 'Maranhão',          MG: 'Minas Gerais',        MS: 'Mato Grosso do Sul',
	MT: 'Mato Grosso',       PA: 'Pará',                PB: 'Paraíba',
	PE: 'Pernambuco',        PI: 'Piauí',               PR: 'Paraná',
	RJ: 'Rio de Janeiro',    RN: 'Rio Grande do Norte', RO: 'Rondônia',
	RR: 'Roraima',           RS: 'Rio Grande do Sul',   SC: 'Santa Catarina',
	SE: 'Sergipe',           SP: 'São Paulo',           TO: 'Tocantins',
};

export const nameToSigla: Record<string, string> = Object.fromEntries(
	Object.entries(siglaToName).map(([s, n]) => [n, s])
);

export type Regiao = 'Norte' | 'Nordeste' | 'Centro-Oeste' | 'Sudeste' | 'Sul';

export const regionMap: Record<string, Regiao> = {
	AC: 'Norte',        AM: 'Norte',        AP: 'Norte',        PA: 'Norte',
	RO: 'Norte',        RR: 'Norte',        TO: 'Norte',
	AL: 'Nordeste',     BA: 'Nordeste',     CE: 'Nordeste',     MA: 'Nordeste',
	PB: 'Nordeste',     PE: 'Nordeste',     PI: 'Nordeste',     RN: 'Nordeste',
	SE: 'Nordeste',
	DF: 'Centro-Oeste', GO: 'Centro-Oeste', MS: 'Centro-Oeste', MT: 'Centro-Oeste',
	ES: 'Sudeste',      MG: 'Sudeste',      RJ: 'Sudeste',      SP: 'Sudeste',
	PR: 'Sul',          RS: 'Sul',          SC: 'Sul',
};

export const REGIOES: Regiao[] = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'];
export const UF_LIST = Object.keys(siglaToName).sort();

// ── Per-UF rows for each visão ────────────────────────────────────────────────
export interface UfRow {
	uf: string;
	valor: number;        // valor executado (R$)
	repassado: number;    // valor repassado pelo MinC (R$); 0 = indisponível na fonte
	contemplados: number;
	populacao: number;
	percapita: number;
	valorUrbano: number;  // valor executado em zona urbana (R$)
	valorRural: number;   // valor executado em zona rural (R$)
}

function rowsFrom(raw: string): Record<string, UfRow> {
	const out: Record<string, UfRow> = {};
	for (const d of parseCSV(raw)) {
		if (!d.uf) continue;
		out[d.uf] = {
			uf: d.uf,
			valor: +d.valor_executado_rs || 0,
			repassado: +d.valor_repassado_rs || 0,
			contemplados: +d.qtde_contemplados || 0,
			populacao: +d.sum_populacao || 0,
			percapita: +d.valor_executado_percapita || 0,
			valorUrbano: +d.valor_urbano || 0,
			valorRural: +d.valor_rural || 0,
		};
	}
	return out;
}

export type Visao = 'uf' | 'estados' | 'municipios' | 'regioes';

// `regioes` shares the same per-UF rows as `uf` (combined level); the map just
// aggregates/colors them by region.
const ufRows  = rowsFrom(csvUfRaw);
const stRows  = rowsFrom(csvStateRaw);
const munRows = rowsFrom(csvMunRaw);

export const rowsByVisao: Record<Visao, Record<string, UfRow>> = {
	uf: ufRows,
	estados: stRows,
	municipios: munRows,
	regioes: ufRows,
};

// ── Region aggregates (from uf-level rows) ────────────────────────────────────
export interface RegionAgg {
	regiao: Regiao;
	valor: number;
	repassado: number;
	contemplados: number;
	populacao: number;
	valorUrbano: number;
	valorRural: number;
	ufs: string[];
}

export const regionAgg: Record<Regiao, RegionAgg> = (() => {
	const acc = {} as Record<Regiao, RegionAgg>;
	for (const r of REGIOES) acc[r] = { regiao: r, valor: 0, repassado: 0, contemplados: 0, populacao: 0, valorUrbano: 0, valorRural: 0, ufs: [] };
	for (const [uf, row] of Object.entries(ufRows)) {
		const r = regionMap[uf];
		if (!r) continue;
		acc[r].valor += row.valor;
		acc[r].repassado += row.repassado;
		acc[r].contemplados += row.contemplados;
		acc[r].populacao += row.populacao;
		acc[r].valorUrbano += row.valorUrbano;
		acc[r].valorRural += row.valorRural;
		acc[r].ufs.push(uf);
	}
	return acc;
})();

// ── Entity counts ─────────────────────────────────────────────────────────────
export const NUM_ESTADOS = 27;
export const NUM_MUNICIPIOS = 5098;

// ── National totals per visão (sum across all 27 UFs) ─────────────────────────
function totals(rows: Record<string, UfRow>) {
	let valor = 0, repassado = 0, contemplados = 0, populacao = 0;
	for (const r of Object.values(rows)) {
		valor += r.valor;
		repassado += r.repassado;
		contemplados += r.contemplados;
		populacao += r.populacao;
	}
	return { valor, repassado, contemplados, populacao };
}

export const nationalTotals: Record<Visao, { valor: number; repassado: number; contemplados: number; populacao: number }> = {
	uf: totals(ufRows),
	estados: totals(stRows),
	municipios: totals(munRows),
	regioes: totals(ufRows),
};
