// All Section 2 data, parsed from CSVs at build time.
// Narrativa: CPF (pessoas físicas) vs CNPJ (entidades) — quem recebe o quê.

import { stateRows, siglaToName } from '$lib/data/section1';

import csvStateRaw         from '../../../data/section_2/aggregate_execution_by_person_type_state.csv?raw';
import csvUfRaw            from '../../../data/section_2/aggregate_execution_by_person_type_uf.csv?raw';
import csvMunRaw           from '../../../data/section_2/aggregate_execution_by_person_type_municipality.csv?raw';
import csvRangeRaw         from '../../../data/section_2/values_range_by_brazil.csv?raw';
import csvPorteRaw         from '../../../data/section_1/values_by_population_size.csv?raw';
import csvSpecialTerritRaw from '../../../data/section_1/values_by_special_territory_uf.csv?raw';
import csvFaixaUfRaw       from '../../../data/section_2/aggregate_faixa_valor_ju_wide_by_uf.csv?raw';
import csvFaixaStateRaw    from '../../../data/section_2/aggregate_faixa_valor_ju_wide_by_state.csv?raw';
import csvAuxQuartisBrasilRaw from '../../../data/section_2/aux_quartis_estados_brasil.csv?raw';
import csvQuartisEstadosRaw from '../../../data/section_2/quartis_estados.csv?raw';
import csvResumoValoresUfEstadoRaw from '../../../data/section_2/resumo_valores_uf_estado.csv?raw';
import csvTerrUfRaw      from '../../../data/section_2/territorios_especiais_por_uf.csv?raw';
import csvTerrEstadoRaw  from '../../../data/section_2/territorios_especiais_por_estado.csv?raw';
import csvTerrMunRaw     from '../../../data/section_2/territorios_especiais_por_municipio.csv?raw';
import csvFaixaValorPorteRaw from '../../../data/section_2/faixa_valor_porte_populacional.csv?raw';

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

// ── 3b. HorizontalGroupedBarChart — contemplados e recursos por faixa (5 tiers)
const recursoPercByBand: Record<string, number> = {
	'Até 2 mil':         2.2,
	'2 a 10 mil':       13.1,
	'10 a 50 mil':      31.5,
	'50 a 200 mil':     28.1,
	'Acima de 200 mil': 25.2,
};

export const faixaGroupedData = (() => {
	const pagMap: Record<string, number> = {};
	for (const r of rangeRows) {
		const faixa = r.faixa_vlr_pago;
		if (!faixa) continue;
		const v = +r['% de contemplados'] * 100;
		const key =
			faixa === '200 a 500 mil' ||
			faixa === '500 mil a 1 milhão' ||
			faixa === '1 milhão a 10 milhões' ||
			faixa === 'Acima de 10 milhões'
				? 'Acima de 200 mil'
				: faixa;
		pagMap[key] = (pagMap[key] ?? 0) + v;
	}
	return ['Até 2 mil', '2 a 10 mil', '10 a 50 mil', '50 a 200 mil', 'Acima de 200 mil'].map(
		(label) => ({
			label,
			values: [pagMap[label] ?? 0, recursoPercByBand[label]],
		})
	);
})();

// ── 3c. HorizontalBarChart — agentes culturais por região ─────────────────────
export const regiaoDistData = [
	{ label: 'Nordeste',     value: 47.7, count: 79446 },
	{ label: 'Sudeste',      value: 27.4, count: 45655 },
	{ label: 'Sul',          value: 10.8, count: 17946 },
	{ label: 'Norte',        value: 8.7,  count: 14504 },
	{ label: 'Centro-Oeste', value: 5.4,  count: 9018  },
];

// ── 3d. HorizontalGroupedBarChart — agentes culturais vs população por região ──
export const regiaoGroupedData = [
	{ label: 'Nordeste',     values: [47.6, 26.9] },
	{ label: 'Sudeste',      values: [27.4, 41.7] },
	{ label: 'Sul',          values: [10.8, 14.6] },
	{ label: 'Norte',        values: [8.7,  8.8]  },
	{ label: 'Centro-Oeste', values: [5.6,  8.0]  },
];

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
// Fonte: aggregate_faixa_valor_ju_wide_by_uf.csv (todos os executores por UF).
// Ordenado pela % de beneficiários nas faixas mais altas (≥ R$50k) — decrescente.
export const UF_BAND_KEYS  = ['ate2k', 'de2a10k', 'de10a50k', 'de50a200k', 'acima200k'] as const;
export const UF_BAND_LABELS: Record<string, string> = {
	ate2k:     'Até R$2k',
	de2a10k:   'R$2–10k',
	de10a50k:  'R$10–50k',
	de50a200k: 'R$50–200k',
	acima200k: 'Acima R$200k',
};

// ── BigNumbers por esfera (estado vs município) ────────────────────────────────
export const percCPFEstados     = +stCPF.perc_qtde_contemplados  * 100;
export const percCNPJEstados    = +stCNPJ.perc_qtde_contemplados * 100;
export const percCPFMunicipios  = +munCPF.perc_qtde_contemplados  * 100;
export const percCNPJMunicipios = +munCNPJ.perc_qtde_contemplados * 100;

// ── Porte municipal — distribuição de pagamentos por faixa de valor (row 38) ──
const PORTE_NAME_MAP: Record<string, string> = {
	'4_grande':     'Grande',
	'1_pequeno_i':  'Pequeno I',
	'2_pequeno_ii': 'Pequeno II',
	'3_medio':      'Médio',
};
const PORTE_SORT: Record<string, number> = {
	'1_pequeno_i': 0, '2_pequeno_ii': 1, '3_medio': 2, '4_grande': 3,
};
const PORTE_CSV_BANDS = [
	'Até 2 mil', '2 a 10 mil', '10 a 50 mil', '50 a 200 mil',
	'200 a 500 mil', '500 mil a 1 milhão', '1 milhão a 10 milhões', 'Acima de 10 milhões',
] as const;

const porteRowsS2 = parseCSV(csvPorteRaw)
	.filter((d) => d.porte_populacional in PORTE_NAME_MAP)
	.sort((a, b) => PORTE_SORT[a.porte_populacional] - PORTE_SORT[b.porte_populacional]);

export const portePagamentosData = porteRowsS2.map((d) => {
	const bands = PORTE_CSV_BANDS.map((k) => +(d[k] ?? 0));
	const total = bands.reduce((s, v) => s + v, 0) || 1;
	return {
		label:     PORTE_NAME_MAP[d.porte_populacional],
		ate2k:     (bands[0] / total) * 100,
		de2a10k:   (bands[1] / total) * 100,
		de10a50k:  (bands[2] / total) * 100,
		de50a200k: (bands[3] / total) * 100,
		acima200k: ((bands[4] + bands[5] + bands[6] + bands[7]) / total) * 100,
	};
});

export const porteValorPercData = parseCSV(csvFaixaValorPorteRaw)
	.filter((d) => {
		const p = d.porte_populacional?.trim();
		return p && p !== '-99' && p in PORTE_NAME_MAP;
	})
	.sort((a, b) => PORTE_SORT[a.porte_populacional.trim()] - PORTE_SORT[b.porte_populacional.trim()])
	.map((d) => {
		const p = d.porte_populacional.trim();
		return {
			label:     PORTE_NAME_MAP[p],
			ate2k:     +d.perc_valor_transacao_ate_2_mil        * 100,
			de2a10k:   +d.perc_valor_transacao_de_2_a_10_mil    * 100,
			de10a50k:  +d.perc_valor_transacao_de_10_a_50_mil   * 100,
			de50a200k: +d.perc_valor_transacao_de_50_a_200_mil  * 100,
			acima200k: +d.perc_valor_transacao_acima_de_200_mil * 100,
		};
	});

// ── Row 40: Valor total por território especial (HorizontalBarChart) ──────────
const SPECIAL_EXCLUDE = new Set(['Não especial', 'Não informado']);
export const specialTerritoryBarData = parseCSV(csvSpecialTerritRaw)
	.filter((r) => !SPECIAL_EXCLUDE.has(r.cod_tipo_nome))
	.map((r) => ({ label: r.cod_tipo_nome, value: +r.valor_transacao }))
	.sort((a, b) => b.value - a.value);

const faixaUfRows    = parseCSV(csvFaixaUfRaw);
export const faixaStateRows = parseCSV(csvFaixaStateRaw);

export const ufBandPercData = faixaUfRows
	.map((row) => {
		const highValuePct = +row.perc_qtd_de_50_a_200_mil + +row.perc_qtd_acima_de_200_mil;
		return {
			label:     row.uf,
			_highValue: highValuePct,
			ate2k:     +row.perc_qtd_ate_2_mil       * 100,
			de2a10k:   +row.perc_qtd_de_2_a_10_mil   * 100,
			de10a50k:  +row.perc_qtd_de_10_a_50_mil  * 100,
			de50a200k: +row.perc_qtd_de_50_a_200_mil * 100,
			acima200k: +row.perc_qtd_acima_de_200_mil * 100,
		};
	})
	.sort((a, b) => b._highValue - a._highValue)
	.map(({ _highValue: _, ...rest }) => rest);

// ── HorizontalStackedBarChart — % recursos executados por faixa de valor × UF ──
export const ufValorBandPercData = faixaUfRows
	.map((row) => {
		const highValPct = +row.perc_valor_de_50_a_200_mil + +row.perc_valor_acima_de_200_mil;
		return {
			label:     row.uf,
			_highValue: highValPct,
			ate2k:     +row.perc_valor_ate_2_mil       * 100,
			de2a10k:   +row.perc_valor_de_2_a_10_mil   * 100,
			de10a50k:  +row.perc_valor_de_10_a_50_mil  * 100,
			de50a200k: +row.perc_valor_de_50_a_200_mil * 100,
			acima200k: +row.perc_valor_acima_de_200_mil * 100,
		};
	})
	.sort((a, b) => b._highValue - a._highValue)
	.map(({ _highValue: _, ...rest }) => rest);

// ── VerticalStackedBarChart — faixa de valor pago × estado (executor estadual) ─
export const stateBandPercData = faixaStateRows
	.map((row) => {
		const highValuePct = +row.perc_qtd_de_50_a_200_mil + +row.perc_qtd_acima_de_200_mil;
		return {
			label:     row.uf,
			_highValue: highValuePct,
			ate2k:     +row.perc_qtd_ate_2_mil       * 100,
			de2a10k:   +row.perc_qtd_de_2_a_10_mil   * 100,
			de10a50k:  +row.perc_qtd_de_10_a_50_mil  * 100,
			de50a200k: +row.perc_qtd_de_50_a_200_mil * 100,
			acima200k: +row.perc_qtd_acima_de_200_mil * 100,
		};
	})
	.sort((a, b) => b._highValue - a._highValue)
	.map(({ _highValue: _, ...rest }) => rest);

// ── BoxPlot — quartis Brasil (aux_quartis_estados_brasil.csv) ─────────────────
const quartisBrasilRow = parseCSV(csvAuxQuartisBrasilRaw)[0];
export const brasilBoxPlotData = [
	{
		label: 'Brasil',
		stats: {
			min:    +quartisBrasilRow.p1,
			q1:     +quartisBrasilRow.p25,
			median: +quartisBrasilRow.mediana,
			q3:     +quartisBrasilRow.p75,
			max:    +quartisBrasilRow.p99,
		},
	},
];

// ── HorizontalStackedBarChart — territórios especiais por UF/estado/município ──
const terrUfRows     = parseCSV(csvTerrUfRaw);
const terrEstadoRows = parseCSV(csvTerrEstadoRaw);
const terrMunRows    = parseCSV(csvTerrMunRaw);

const terrByUf     = Object.fromEntries(terrUfRows.map((r)     => [r.uf, +r.valor_transacao_territorios_especiais]));
const terrByEstado = Object.fromEntries(terrEstadoRows.map((r) => [r.uf, +r.valor_transacao_territorios_especiais]));
const terrByMun    = Object.fromEntries(terrMunRows.map((r)    => [r.uf, +r.valor_transacao_territorios_especiais]));

const allUFs = [...new Set([...Object.keys(terrByUf), ...Object.keys(terrByEstado), ...Object.keys(terrByMun)])].sort();

export const TERR_KEYS   = ['estado', 'municipio'] as const;
export const TERR_LABELS: Record<string, string> = {
	estado:    'Estado',
	municipio: 'Município',
};

export const terrEspeciaisData = allUFs
	.map((uf) => ({
		label:     uf,
		estado:    terrByEstado[uf] ?? 0,
		municipio: terrByMun[uf]    ?? 0,
	}))
	.sort((a, b) => (b.estado + b.municipio) - (a.estado + a.municipio));

// ── BoxPlot — quartis por estado (quartis_estados.csv) ────────────────────────
export const estadosBoxPlotData = parseCSV(csvQuartisEstadosRaw).map((row) => ({
	label: row.uf,
	stats: {
		min:    +row.p1,
		q1:     +row.p25,
		median: +row.mediana,
		q3:     +row.p75,
		max:    +row.p99,
	},
}));

// ── HorizontalStackedBarChart — % contemplados por faixa × região ─────────────
const UF_TO_REGIAO: Record<string, string> = {
	AC: 'Norte', AM: 'Norte', AP: 'Norte', PA: 'Norte', RO: 'Norte', RR: 'Norte', TO: 'Norte',
	AL: 'Nordeste', BA: 'Nordeste', CE: 'Nordeste', MA: 'Nordeste', PB: 'Nordeste',
	PE: 'Nordeste', PI: 'Nordeste', RN: 'Nordeste', SE: 'Nordeste',
	DF: 'Centro-Oeste', GO: 'Centro-Oeste', MS: 'Centro-Oeste', MT: 'Centro-Oeste',
	ES: 'Sudeste', MG: 'Sudeste', RJ: 'Sudeste', SP: 'Sudeste',
	PR: 'Sul', RS: 'Sul', SC: 'Sul',
};
const REGIAO_ORDER = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'];

export const regiaoContempladosFaixaData = (() => {
	const totals: Record<string, Record<string, number>> = {};
	for (const reg of REGIAO_ORDER) {
		totals[reg] = { ate2k: 0, de2a10k: 0, de10a50k: 0, de50a200k: 0, acima200k: 0 };
	}
	for (const row of faixaUfRows) {
		const reg = UF_TO_REGIAO[row.uf];
		if (!reg) continue;
		totals[reg].ate2k     += +row.qtd_ate_2_mil;
		totals[reg].de2a10k   += +row.qtd_de_2_a_10_mil;
		totals[reg].de10a50k  += +row.qtd_de_10_a_50_mil;
		totals[reg].de50a200k += +row.qtd_de_50_a_200_mil;
		totals[reg].acima200k += +row.qtd_acima_de_200_mil;
	}
	return REGIAO_ORDER.map((reg) => {
		const t = totals[reg];
		const total = Object.values(t).reduce((s, v) => s + v, 0) || 1;
		return {
			label:     reg,
			ate2k:     (t.ate2k     / total) * 100,
			de2a10k:   (t.de2a10k   / total) * 100,
			de10a50k:  (t.de10a50k  / total) * 100,
			de50a200k: (t.de50a200k / total) * 100,
			acima200k: (t.acima200k / total) * 100,
		};
	});
})();

// ── ChoroplethMap — ticket médio por estado (resumo_valores_uf_estado.csv) ────
export const mediaValorByState: Record<string, { media_valor: number; mediana_valor: number; media_aparada_1pct_valor: number }> =
	Object.fromEntries(
		parseCSV(csvResumoValoresUfEstadoRaw)
			.filter((r) => r.visao === 'ESTADO')
			.flatMap((r) => {
				const name = siglaToName[r.uf];
				if (!name) return [];
				return [[name, { media_valor: +r.media_valor, mediana_valor: +r.mediana_valor, media_aparada_1pct_valor: +r.media_aparada_1pct_valor }]];
			})
	);
