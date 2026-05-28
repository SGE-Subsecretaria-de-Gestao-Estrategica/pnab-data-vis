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
