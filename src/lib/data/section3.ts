// All Section 3 data, parsed from CSVs at build time.

import csvAgeGroupSexoRaw from '../../../data/section_3/aggregate_valor_quantity_by_age_group_sexo_wide.csv?raw';
import csvAgeGroupRegionRaw from '../../../data/section_3/aggregate_value_quantity_by_age_group_region_wide.csv?raw';
import csvSexoPropRaw from '../../../data/section_3/aggregate_contemplados_by_sexo_proportion.csv?raw';
import csvPfPjRaw from '../../../data/section_3/aggregate_contemplados_pf_pj_proportion.csv?raw';
import csvCboRaw  from '../../../data/section_4/aggregate_cbo_rais.csv?raw';

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

// ── PF vs PJ ─────────────────────────────────────────────────────────────────
const [pfPjRow] = parseCSV(csvPfPjRaw);
export const totalBeneficiarios = +pfPjRow.quantidade_contemplados;
export const pfPjDonutData = [
	{ label: 'Pessoa Física (PF)', value: +pfPjRow.quantidade_contemplados_pf },
	{ label: 'Pessoa Jurídica (PJ)', value: +pfPjRow.quantidade_contemplados_pj },
];
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
