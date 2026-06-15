// All Section 3 data, parsed from CSVs at build time.

import csvAgeGroupSexoRaw from '../../../data/section_3/aggregate_valor_quantity_by_age_group_sexo_wide.csv?raw';
import csvAgeGroupRegionRaw from '../../../data/section_3/aggregate_value_quantity_by_age_group_region_wide.csv?raw';
import csvSexoPropRaw from '../../../data/section_3/aggregate_contemplados_by_sexo_proportion.csv?raw';
// import csvPfPjRaw from '../../../data/section_3/aggregate_contemplados_pf_pj_proportion.csv?raw'; // CSV faltante
import csvCboRaw  from '../../../data/section_4/aggregate_cbo_rais.csv?raw';
import csvCnaesRaw from '../../../data/section_3/top_cnaes_cnpj.csv?raw';
import csvCnaesCulturaRaw from '../../../data/section_3/top_cnaes_cnpj_cultura.csv?raw';
import csvNaturezaJuridicaRegiaoRaw from '../../../data/section_3/aggregate_cnpj_natureza_juridica_por_regiao.csv?raw';
import csvNaturezaJuridicaRaw from '../../../data/section_3/aggregate_cnpj_natureza_juridica.csv?raw';
import csvSexoUfIbgeRaw from '../../../data/section_3/aggregate_sexo_uf_ibge_pnab.csv?raw';
import csvValuesByPorteRaw from '../../../data/section_3/values_by_population_size_v2.csv?raw';

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

// // ── PF vs PJ (aggregate_contemplados_pf_pj_proportion.csv faltante) ──────────
// const [pfPjRow] = parseCSV(csvPfPjRaw);
// export const totalBeneficiarios = +pfPjRow.quantidade_contemplados;
// export const pfPjDonutData = [
// 	{ label: 'Pessoa Física (PF)', value: +pfPjRow.quantidade_contemplados_pf },
// 	{ label: 'Pessoa Jurídica (PJ)', value: +pfPjRow.quantidade_contemplados_pj },
// ];
export const valorTotalPJ = 1_591_311_693;
export const valorTotalMEI = 238_855_896;

// ── Sexo ─────────────────────────────────────────────────────────────────────
const [sexoRow] = parseCSV(csvSexoPropRaw);
export const totalPF = +sexoRow.quantidade_contemplados;
export const valorTotalPF = +sexoRow.valor_contemplados;
export const sexoQuantityDonutData = [
	{ label: 'Feminino', value: +sexoRow.quantidade_contemplados_feminino },
	{ label: 'Masculino', value: +sexoRow.quantidade_contemplados_masculino },
];
export const sexoValueDonutData = [
	{ label: 'Feminino', value: +sexoRow.valor_contemplados_feminino },
	{ label: 'Masculino', value: +sexoRow.valor_contemplados_masculino },
];
export const sexoPropMasculino = +sexoRow.quantidade_contemplados_masculino / +sexoRow.quantidade_contemplados;
export const sexoPropFeminino = +sexoRow.quantidade_contemplados_feminino / +sexoRow.quantidade_contemplados;

// ── Pirâmide etária por sexo ──────────────────────────────────────────────────
const ageGroupSexoRows = parseCSV(csvAgeGroupSexoRaw);

// Grouped bar: % of total value vs % of total quantity, by age group
export const ageGroupValueQtyData = ageGroupSexoRows.map((r) => ({
	faixa_etaria: r.faixa_etaria,
	perc_valor: +r.perc_valor_total_geral,
	perc_quantidade: +r.perc_quantidade_total_geral,
}));
export const ageGroupValueQtyKeys = ['perc_valor', 'perc_quantidade'];
export const ageGroupValueQtyLabels: Record<string, string> = {
	perc_valor: 'Valor recebido',
	perc_quantidade: 'Quantidade contemplados',
};

export const pyramidData = ageGroupSexoRows.map((r) => ({
	label: r.faixa_etaria,
	left: +r.quantidade_contemplados_masculino,
	right: +r.quantidade_contemplados_feminino,
}));

// ── Top 20 CNAEs culturais (CNPJ) ────────────────────────────────────────────
function parseCSVLine(line: string): string[] {
	const result: string[] = [];
	let current = '';
	let inQuotes = false;
	for (const ch of line) {
		if (ch === '"') { inQuotes = !inQuotes; }
		else if (ch === ',' && !inQuotes) { result.push(current); current = ''; }
		else { current += ch; }
	}
	result.push(current);
	return result;
}

function parseCSVQuoted(text: string): Record<string, string>[] {
	const [headerLine, ...dataLines] = text.trim().split('\n');
	const headers = parseCSVLine(headerLine);
	return dataLines.filter((l) => l.trim()).map((line) => {
		const values = parseCSVLine(line);
		return Object.fromEntries(headers.map((h, i) => [h, values[i] ?? '']));
	});
}

const cnaesRows = parseCSVQuoted(csvCnaesRaw);

const _fmt1 = (v: number) =>
	(v * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

const _cnaesBase = cnaesRows.map((d) => ({
	descricao:               d.cnae_principal,
	percQuantidade:          +d.perc_quantidade_contemplados * 100,
	percQuantidadeFormatted: _fmt1(+d.perc_quantidade_contemplados),
	percValor:               +d.perc_valor_transacao * 100,
	percValorFormatted:      _fmt1(+d.perc_valor_transacao),
}));

export const top20CnaesQtdTableData = [..._cnaesBase]
	.sort((a, b) => b.percQuantidade - a.percQuantidade)
	.map((d, i) => ({ posicao: i + 1, ...d }));

export const top20CnaesValTableData = [..._cnaesBase]
	.sort((a, b) => b.percValor - a.percValor)
	.map((d, i) => ({ posicao: i + 1, ...d }));

// Pre-computed SVG height (matches CnaeTable layout constants)
const _C_FS = 13, _C_LH = _C_FS * 1.4, _C_CW = _C_FS * 0.55;
const _C_DESC_W = 360, _C_PAD_Y = 10, _C_HEADER_H = 44;
function _cnaeWrap(text: string): number {
	const max = Math.max(1, Math.floor(_C_DESC_W / _C_CW));
	const words = text.split(' ');
	let lines = 1, cur = '';
	for (const w of words) {
		const cand = cur ? `${cur} ${w}` : w;
		if (cand.length > max && cur) { lines++; cur = w; } else cur = cand;
	}
	return lines;
}
function _cnaeHeight(data: { posicao: number; descricao: string }[]): number {
	return data.reduce((h, e) => {
		const minH = e.posicao <= 3 ? 54 : 42;
		return h + Math.max(minH, _cnaeWrap(e.descricao) * _C_LH + _C_PAD_Y * 2);
	}, _C_HEADER_H);
}
export const cnaesQtdTableHeight = _cnaeHeight(top20CnaesQtdTableData);
export const cnaesValTableHeight = _cnaeHeight(top20CnaesValTableData);

// ── Top 20 CNAEs culturais (por valor repassado) ────────────────────────────
const cnaesCulturaRows = parseCSVQuoted(csvCnaesCulturaRaw);
const _cnaesCulturaBase = cnaesCulturaRows.map((d) => ({
	descricao:               d.cnae_principal,
	percQuantidade:          +d.perc_quantidade_contemplados * 100,
	percQuantidadeFormatted: _fmt1(+d.perc_quantidade_contemplados),
	percValor:               +d.perc_valor_transacao * 100,
	percValorFormatted:      _fmt1(+d.perc_valor_transacao),
}));

export const top20CnaesCulturaValTableData = [..._cnaesCulturaBase]
	.sort((a, b) => b.percValor - a.percValor)
	.slice(0, 20)
	.map((d, i) => ({ posicao: i + 1, ...d }));

export const cnaesCulturaValTableHeight = _cnaeHeight(top20CnaesCulturaValTableData);

// ── Top 20 atividades econômicas (CBO/RAIS) ───────────────────────────────────
function toTitleCase(s: string) {
	return s
		.toLowerCase()
		.split(' ')
		.map((w) => w.charAt(0).toUpperCase() + w.slice(1))
		.join(' ');
}
export const top20CboData = parseCSV(csvCboRaw)
	.slice(0, 20)
	.map((d) => ({ label: toTitleCase(d.cbo_descricao_rais), value: +d.soma_quantidade }));

// ── Natureza jurídica (agregado nacional) ─────────────────────────────────────
export const naturezaJuridicaData = parseCSV(csvNaturezaJuridicaRaw)
	.map((r) => ({
		label: r.natureza_juridica,
		value: +r.perc_valor_contemplados * 100,
	}))
	.sort((a, b) => b.value - a.value);

// ── Natureza jurídica por região ──────────────────────────────────────────────
const naturezaJuridicaRegiaoRows = parseCSV(csvNaturezaJuridicaRegiaoRaw);

const _NJ_ORDER = [
	'Microempresa-ME',
	'MEI',
	'Empresa de Pequeno Porte (EPP)',
	'Administração Pública',
	'Entidades sem fins lucrativos',
	'Entidades Empresariais',
];
const _REGIAO_ORDER = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'];

export const naturezaJuridicaRegiaoData = _REGIAO_ORDER.map((regiao) => {
	const rows = naturezaJuridicaRegiaoRows.filter((r) => r.regiao === regiao);
	const entry: Record<string, string | number> = { label: regiao };
	for (const nj of _NJ_ORDER) {
		const row = rows.find((r) => r.natureza_juridica === nj);
		entry[nj] = row ? +row.perc_quantidade_contemplados_na_regiao * 100 : 0;
	}
	return entry;
});
export const naturezaJuridicaSeriesLabels = _NJ_ORDER;

// ── Faixa etária por região ───────────────────────────────────────────────────
const ageGroupRegionRows = parseCSV(csvAgeGroupRegionRaw);
export const ageGroupRegionData = ageGroupRegionRows.map((r) => ({
	faixa_etaria: r.faixa_etaria,
	centro_oeste: +r.quantidade_contemplados_centro_oeste,
	nordeste: +r.quantidade_contemplados_nordeste,
	norte: +r.quantidade_contemplados_norte,
	sudeste: +r.quantidade_contemplados_sudeste,
	sul: +r.quantidade_contemplados_sul,
}));
export const ageGroupRegionKeys = ['centro_oeste', 'nordeste', 'norte', 'sudeste', 'sul'];
export const ageGroupRegionLabels: Record<string, string> = {
	centro_oeste: 'Centro-Oeste',
	nordeste: 'Nordeste',
	norte: 'Norte',
	sudeste: 'Sudeste',
	sul: 'Sul',
};

// ── Sexo por UF vs IBGE ───────────────────────────────────────────────────────
const sexoUfRows = parseCSV(csvSexoUfIbgeRaw);

export const sexoUfComparisonData = sexoUfRows.map((r) => ({
	uf: r.uf,
	aldirMasc: +r.perc_quantidade_contemplados_masculino * 100,
	aldirFem:  +r.perc_quantidade_contemplados_feminino * 100,
	ibgeMasc:  +r.perc_ibge_masculino * 100,
	ibgeFem:   +r.perc_ibge_feminino * 100,
}));

export const sexoUfData = sexoUfRows.map((r) => ({
	label: r.uf,
	values: [
		+r.perc_ibge_masculino * 100,
		+r.perc_quantidade_contemplados_masculino * 100,
		+r.perc_ibge_feminino * 100,
		+r.perc_quantidade_contemplados_feminino * 100,
	],
}));

export const sexoUfSeriesLabels = [
	'% Masculino IBGE',
	'Masculino contemplados',
	'% Feminino IBGE',
	'Feminino contemplados',
];

// ── Valor médio por sexo e porte populacional ─────────────────────────────────
const _PORTE_LABELS: Record<string, string> = {
	'-99': 'Entes Estatais',
	'1_pequeno_i': 'Peq. porte I',
	'2_pequeno_ii': 'Peq. porte II',
	'3_medio': 'Médio porte',
	'4_grande': 'Grande porte',
};
const _PORTE_ORDER = ['1_pequeno_i', '2_pequeno_ii', '3_medio', '4_grande'];
const valuesByPorteRows = parseCSV(csvValuesByPorteRaw);

export const valorMedioSexoPorteData = _PORTE_ORDER.map((porte) => {
	const row = valuesByPorteRows.find((r) => r.porte_populacional === porte)!;
	return {
		label: _PORTE_LABELS[porte],
		values: [+row.valor_medio_sexo_Feminino, +row.valor_medio_sexo_Masculino],
	};
});
export const valorMedioSexoSeriesLabels = ['Feminino', 'Masculino'];

// Pivoted: regions on x-axis, age groups as bar series — percentage of total
const _regions = ['centro_oeste', 'nordeste', 'norte', 'sudeste', 'sul'] as const;
export const regionByAgeGroupPctData = _regions.map((reg) => {
	const entry: Record<string, string | number> = { regiao: ageGroupRegionLabels[reg] };
	ageGroupRegionRows.forEach((r) => {
		entry[r.faixa_etaria] = +r[`perc_quantidade_total_geral_${reg}`];
	});
	return entry;
});
export const ageGroupPctKeys = ageGroupRegionRows.map((r) => r.faixa_etaria);
