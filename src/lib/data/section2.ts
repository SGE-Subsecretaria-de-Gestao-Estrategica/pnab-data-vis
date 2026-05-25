// All Section 2 data, parsed from CSVs at build time.
// Narrativa: CPF (pessoas físicas) vs CNPJ (entidades) — quem recebe o quê.

import { stateRows } from '$lib/data/section1';

import csvStateRaw from '../../../data/section_2/aggregate_execution_by_person_type_state.csv?raw';
import csvUfRaw    from '../../../data/section_2/aggregate_execution_by_person_type_uf.csv?raw';
import csvMunRaw   from '../../../data/section_2/aggregate_execution_by_person_type_municipality.csv?raw';
import csvRangeRaw from '../../../data/section_2/values_range_by_brazil.csv?raw';

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

const s2StateRows = parseCSV(csvStateRaw);
const ufRows      = parseCSV(csvUfRaw);
const munRows     = parseCSV(csvMunRaw);
const rangeRows   = parseCSV(csvRangeRaw);

function byType(rows: Record<string, string>[], tipo: string) {
	return rows.find((r) => r.tipo_documento === tipo)!;
}

const ufCPF   = byType(ufRows,      'CPF');
const ufCNPJ  = byType(ufRows,      'CNPJ');
const stCPF   = byType(s2StateRows, 'CPF');
const stCNPJ  = byType(s2StateRows, 'CNPJ');
const munCPF  = byType(munRows,     'CPF');
const munCNPJ = byType(munRows,     'CNPJ');

const BAND_KEYS = [
	'Até 2 mil', '2 a 10 mil', '10 a 50 mil', '50 a 200 mil',
	'200 a 500 mil', '500 mil a 1 milhão', '1 milhão a 10 milhões', 'Acima de 10 milhões',
] as const;

function getBands(row: Record<string, string>): number[] {
	return BAND_KEYS.map((k) => +(row[k] ?? 0));
}

// ── 1. BigNumbers ─────────────────────────────────────────────────────────────
export const percBenefCPF  = +ufCPF.perc_qtde_contemplados  * 100; // ~80.66
export const percBenefCNPJ = +ufCNPJ.perc_qtde_contemplados * 100; // ~19.34
export const percValorCPF  = +ufCPF.perc_valor_executado     * 100; // ~44.09
export const percValorCNPJ = +ufCNPJ.perc_valor_executado    * 100; // ~55.91

export const totalBenefCPF  = +ufCPF.qtde_contemplados;   // 134606
export const totalBenefCNPJ = +ufCNPJ.qtde_contemplados;  //  32280

// ── 2. DivergingBarChart — CPF vs CNPJ % do valor por esfera ─────────────────
// leftPct = parcela do valor que foi para CPF; rightPct = parcela para CNPJ
// Soma sempre 100 dentro de cada esfera.
export const valorDivergingData = [
	{
		label:    'Executado por estados',
		leftPct:  +stCPF.perc_valor_executado  * 100,  // 35.35
		rightPct: +stCNPJ.perc_valor_executado * 100,  // 64.65
	},
	{
		label:    'Executado por municípios',
		leftPct:  +munCPF.perc_valor_executado  * 100, // 53.17
		rightPct: +munCNPJ.perc_valor_executado * 100, // 46.83
	},
	{
		label:    'Total PNAB',
		leftPct:  +ufCPF.perc_valor_executado  * 100,  // 44.09
		rightPct: +ufCNPJ.perc_valor_executado * 100,  // 55.91
	},
];

// Stacked: beneficiários vs valor — mostra a inversão CPF/CNPJ
export const benefVsValorData = [
	{
		label: 'Beneficiários',
		cpf:   +ufCPF.perc_qtde_contemplados  * 100, // 80.66
		cnpj:  +ufCNPJ.perc_qtde_contemplados * 100, // 19.34
	},
	{
		label: 'Valor recebido',
		cpf:   +ufCPF.perc_valor_executado  * 100,   // 44.09
		cnpj:  +ufCNPJ.perc_valor_executado * 100,   // 55.91
	},
];

// ── 3. HorizontalBarChart — distribuição nacional por faixa de valor ──────────
export const faixaDistData = rangeRows
	.filter((r) => r.faixa_vlr_pago)
	.map((r) => ({
		label: r.faixa_vlr_pago,
		value: +r['% de contemplados'] * 100,
	}));

// ── 4. HorizontalStackedBarChart — faixas por tipo CPF vs CNPJ ───────────────
export const BAND_LABELS: Record<string, string> = {
	ate2k:      'Até R$2k',
	de2a10k:    'R$2–10k',
	de10a50k:   'R$10–50k',
	de50a200k:  'R$50–200k',
	de200a500k: 'R$200–500k',
	de500ka1m:  'R$500k–1M',
	de1ma10m:   'R$1–10M',
	acima10m:   '>R$10M',
};
export const BAND_STACK_KEYS = Object.keys(BAND_LABELS);

function bandPercentRow(row: Record<string, string>, label: string) {
	const bands = getBands(row);
	const total = bands.reduce((s, v) => s + v, 0) || 1;
	return {
		label,
		ate2k:      (bands[0] / total) * 100,
		de2a10k:    (bands[1] / total) * 100,
		de10a50k:   (bands[2] / total) * 100,
		de50a200k:  (bands[3] / total) * 100,
		de200a500k: (bands[4] / total) * 100,
		de500ka1m:  (bands[5] / total) * 100,
		de1ma10m:   (bands[6] / total) * 100,
		acima10m:   (bands[7] / total) * 100,
	};
}

export const bandStackedData = [
	bandPercentRow(ufCPF,  'CPF'),
	bandPercentRow(ufCNPJ, 'CNPJ'),
];

// ── 5. ProportionalAreaChart — valor médio por beneficiário ───────────────────
// Área proporcional ao valor médio: CNPJ ~R$62.7k vs CPF ~R$9.6k (6,5× maior)
export const mediaPorTipoData = [
	{ label: 'CPF',  value: +ufCPF.media_valor  }, // 9634
	{ label: 'CNPJ', value: +ufCNPJ.media_valor }, // 62742
];

// ── 6. BoxPlotChart — dispersão de valores CPF vs CNPJ ────────────────────────
// Q1 e Q3 estimados por interpolação linear dentro de cada faixa de valor.
const BAND_LIMITS: [number, number][] = [
	[375,       2_000],
	[2_000,    10_000],
	[10_000,   50_000],
	[50_000,  200_000],
	[200_000, 500_000],
	[500_000,   1_000_000],
	[1_000_000, 10_000_000],
	[10_000_000, 22_109_765],
];

function interpolatePercentile(bands: number[], pct: number): number {
	const total = bands.reduce((s, v) => s + v, 0);
	const target = pct * total;
	let cumul = 0;
	for (let i = 0; i < bands.length; i++) {
		const next = cumul + bands[i];
		if (next >= target && bands[i] > 0) {
			const frac = (target - cumul) / bands[i];
			const [lo, hi] = BAND_LIMITS[i];
			return lo + frac * (hi - lo);
		}
		cumul = next;
	}
	return BAND_LIMITS[BAND_LIMITS.length - 1][1];
}

function buildBoxStats(row: Record<string, string>) {
	const bands  = getBands(row);
	const q1     = interpolatePercentile(bands, 0.25);
	const q3     = interpolatePercentile(bands, 0.75);
	const iqr    = q3 - q1;
	// Tukey whiskers: cap at Q1 ± 1.5×IQR (clamped to actual data range)
	const wMin   = Math.max(+row.min_valor, q1 - 1.5 * iqr);
	const wMax   = Math.min(+row.max_valor, q3 + 1.5 * iqr);
	return {
		min:    wMin,
		q1,
		median: +row.mediana_valor,
		q3,
		max:    wMax,
	};
}

export const boxPlotData = [
	{ label: 'CPF',  stats: buildBoxStats(ufCPF)  },
	{ label: 'CNPJ', stats: buildBoxStats(ufCNPJ) },
];

// ── 7. VerticalStackedBarChart — faixa de valor pago × UF ─────────────────────
// Fonte: stateRows (section 1, execução estadual). % dentro de cada UF.
// Ordenado pela % de beneficiários nas faixas mais altas (≥ R$50k) — decrescente.
export const UF_BAND_KEYS  = ['ate2k', 'de2a10k', 'de10a50k', 'de50a200k', 'de200a500k', 'de500ka1m', 'de1ma10m', 'acima10m'] as const;
export const UF_BAND_LABELS: Record<string, string> = {
	ate2k:      'Até R$2k',
	de2a10k:    'R$2–10k',
	de10a50k:   'R$10–50k',
	de50a200k:  'R$50–200k',
	de200a500k: 'R$200–500k',
	de500ka1m:  'R$500k–1M',
	de1ma10m:   'R$1–10M',
	acima10m:   '>R$10M',
};

export const ufBandPercData = [...stateRows]
	.map((row) => {
		const total =
			row['Até R$2k'] + row['R$2–10k'] + row['R$10–50k'] + row['R$50–200k'] +
			row['R$200–500k'] + row['R$500k–1M'] + row['R$1–10M'] + row['>R$10M'] || 1;
		const highValuePct =
			(row['R$50–200k'] + row['R$200–500k'] + row['R$500k–1M'] + row['R$1–10M'] + row['>R$10M']) / total;
		return {
			label:      row.uf,
			_highValue: highValuePct,
			ate2k:      (row['Até R$2k']    / total) * 100,
			de2a10k:    (row['R$2–10k']     / total) * 100,
			de10a50k:   (row['R$10–50k']    / total) * 100,
			de50a200k:  (row['R$50–200k']   / total) * 100,
			de200a500k: (row['R$200–500k']  / total) * 100,
			de500ka1m:  (row['R$500k–1M']   / total) * 100,
			de1ma10m:   (row['R$1–10M']     / total) * 100,
			acima10m:   (row['>R$10M']      / total) * 100,
		};
	})
	.sort((a, b) => b._highValue - a._highValue)
	.map(({ _highValue: _, ...rest }) => rest);
