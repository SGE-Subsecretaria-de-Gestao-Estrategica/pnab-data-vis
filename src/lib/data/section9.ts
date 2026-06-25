// Section 9 data — Distribuição de contemplados PJ por tipo de organização.
//
// Fonte: cruzamento PNAB × Receita Federal (pessoas jurídicas / CNPJ).
// Os dados existem apenas em nível nacional e por região — não há quebra por
// UF, estado nem município. O escopo da Seção 9 é, portanto, "Brasil" + as 5
// regiões; as visões uf/estados/municípios não têm dados de natureza jurídica.

import csvNacionalRaw from '../../../data/section_3/aggregate_cnpj_natureza_juridica.csv?raw';
import csvRegiaoRaw   from '../../../data/section_3/aggregate_cnpj_natureza_juridica_por_regiao.csv?raw';

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

export const REGIOES_PJ = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'] as const;

function toScope(rows: { natureza_juridica: string; quantidade: number }[]): OrgScope {
	const total = rows.reduce((s, r) => s + r.quantidade, 0);
	const bars = rows
		.map((r) => ({
			label: r.natureza_juridica,
			value: r.quantidade,
			perc: total > 0 ? (r.quantidade / total) * 100 : 0,
		}))
		.sort((a, b) => b.value - a.value);
	return { bars, total };
}

// ── Nacional (escopo "Todas" / Brasil) ────────────────────────────────────────
const nacionalRows = parseCSV(csvNacionalRaw)
	.filter((r) => _NJ_ORDER.includes(r.natureza_juridica))
	.map((r) => ({ natureza_juridica: r.natureza_juridica, quantidade: +r.quantidade_contemplados || 0 }));

const nacionalScope = toScope(nacionalRows);

// ── Por região ────────────────────────────────────────────────────────────────
const regiaoRows = parseCSV(csvRegiaoRaw);

const regiaoScopes: Record<string, OrgScope> = {};
for (const regiao of REGIOES_PJ) {
	const rows = regiaoRows
		.filter((r) => r.regiao === regiao && _NJ_ORDER.includes(r.natureza_juridica))
		.map((r) => ({ natureza_juridica: r.natureza_juridica, quantidade: +r.quantidade_contemplados || 0 }));
	regiaoScopes[regiao] = toScope(rows);
}

// Map keyed by the dashboard's `regiao` filter value ('Todas' = Brasil).
export const orgByRegiao: Record<string, OrgScope> = {
	Todas: nacionalScope,
	...regiaoScopes,
};
