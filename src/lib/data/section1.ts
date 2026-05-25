// All Section 1 data, parsed from CSVs at build time.

import csvStateRaw      from '../../../data/section_1/executed_value_by_state.csv?raw';
import csvMunRaw        from '../../../data/section_1/executed_value_by_municipality.csv?raw';
import csvUfRaw         from '../../../data/section_1/executed_value_by_uf.csv?raw';
import csvRegionRaw     from '../../../data/section_1/executed_value_by_region_state.csv?raw';
import csvZoneRaw       from '../../../data/section_1/executed_value_zone_by_state.csv?raw';
import csvZoneUfRaw     from '../../../data/section_1/executed_value_zone_by_uf.csv?raw';
import csvPorteRaw      from '../../../data/section_1/values_by_population_size.csv?raw';
import csvSpecialRaw    from '../../../data/section_1/special_territory_w_ibge_by_brazil.csv?raw';
import csvSpecialStRaw  from '../../../data/section_1/values_by_special_territory_state.csv?raw';
import csvSpecialMunRaw from '../../../data/section_1/values_by_special_territory_municipality.csv?raw';
import csvBnRaw         from '../../../data/section_1/bignumber1.csv?raw';

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

// ── Totais ────────────────────────────────────────────────────────────────────
const [bnRow] = parseCSV(csvBnRaw);
export const percExecEstados    = +bnRow.perc_executado_estados    * 100;
export const percExecMunicipios = +bnRow.perc_executado_municipios * 100;
export const valorExecEstados    = +bnRow.Estados_DF;
export const valorExecMunicipios = +bnRow.Municipios_DF;
export const valorExecTotal      = +bnRow.Estados_DF + +bnRow.Municipios_DF;

// ── Lookup tables ─────────────────────────────────────────────────────────────
export const siglaToName: Record<string, string> = {
	AC: 'Acre',              AL: 'Alagoas',             AM: 'Amazonas',
	AP: 'Amapá',             BA: 'Bahia',               CE: 'Ceará',
	DF: 'Distrito Federal',  ES: 'Espírito Santo',      GO: 'Goiás',
	MA: 'Maranhão',          MG: 'Minas Gerais',        MS: 'Mato Grosso do Sul',
	MT: 'Mato Grosso',       PA: 'Pará',                PB: 'Paraíba',
	PE: 'Pernambuco',        PI: 'Piauí',               PR: 'Paraná',
	RJ: 'Rio de Janeiro',    RN: 'Rio Grande do Norte', RO: 'Rondônia',
	RR: 'Roraima',           RS: 'Rio Grande do Sul',   SC: 'Santa Catarina',
	SE: 'Sergipe',           SP: 'São Paulo',            TO: 'Tocantins',
};

export const regionMap: Record<string, string> = {
	AC: 'Norte',       AM: 'Norte',       AP: 'Norte',       PA: 'Norte',
	RO: 'Norte',       RR: 'Norte',       TO: 'Norte',
	AL: 'Nordeste',    BA: 'Nordeste',    CE: 'Nordeste',    MA: 'Nordeste',
	PB: 'Nordeste',    PE: 'Nordeste',    PI: 'Nordeste',    RN: 'Nordeste',
	SE: 'Nordeste',
	DF: 'Centro-Oeste', GO: 'Centro-Oeste', MS: 'Centro-Oeste', MT: 'Centro-Oeste',
	ES: 'Sudeste',     MG: 'Sudeste',     RJ: 'Sudeste',     SP: 'Sudeste',
	PR: 'Sul',         RS: 'Sul',         SC: 'Sul',
};

// ── Região ────────────────────────────────────────────────────────────────────
const regionRows = parseCSV(csvRegionRaw);

export const regions = Object.fromEntries(
	regionRows.map((d) => [
		d.regiao,
		{
			valor_executado_rs:   +d.valor_executado_rs,
			perc_valor_executado: +d.perc_valor_executado,
			perc_populacao:       +d.perc_populacao,
		},
	])
);

export const regionAreaData = [...regionRows]
	.sort((a, b) => +b.valor_executado_rs - +a.valor_executado_rs)
	.map((d) => ({ label: d.regiao, value: +d.valor_executado_rs }));

export const silhouetteRegionData = [...regionRows]
	.sort((a, b) => +b.valor_executado_rs - +a.valor_executado_rs)
	.map((d) => ({ region: d.regiao === 'Centro-Oeste' ? 'CentroOeste' : d.regiao, value: +d.valor_executado_rs }));

export const silhouetteRegionPopData = [...regionRows]
	.sort((a, b) => +b.populacao - +a.populacao)
	.map((d) => ({ region: d.regiao === 'Centro-Oeste' ? 'CentroOeste' : d.regiao, value: +d.populacao }));

// ── Por estado (executed_value_by_state.csv) ──────────────────────────────────
interface StateRow {
	uf: string;
	valor_executado_rs:   number;
	valor_executado_perc: number;
	sum_populacao:        number;
	qtde_contemplados:    number;
	mediana_valor:        number;
	'Até R$2k':    number;
	'R$2–10k':     number;
	'R$10–50k':    number;
	'R$50–200k':   number;
	'R$200–500k':  number;
	'R$500k–1M':   number;
	'R$1–10M':     number;
	'>R$10M':      number;
}

export const stateRows: StateRow[] = parseCSV(csvStateRaw).map((d) => ({
	uf:                   d.uf,
	valor_executado_rs:   +d.valor_executado_rs,
	valor_executado_perc: +d.valor_executado_perc,
	sum_populacao:        +d.sum_populacao,
	qtde_contemplados:    +d.qtde_contemplados,
	mediana_valor:        +d.mediana_valor,
	'Até R$2k':   +d['Até 2 mil'],
	'R$2–10k':    +d['2 a 10 mil'],
	'R$10–50k':   +d['10 a 50 mil'],
	'R$50–200k':  +d['50 a 200 mil'],
	'R$200–500k': +d['200 a 500 mil'],
	'R$500k–1M':  +d['500 mil a 1 milhão'],
	'R$1–10M':    +d['1 milhão a 10 milhões'],
	'>R$10M':     +d['Acima de 10 milhões'],
}));

export const states = Object.fromEntries(
	stateRows.map((d) => [siglaToName[d.uf], d])
);

export const rankingData = [...stateRows]
	.sort((a, b) => b.valor_executado_rs - a.valor_executado_rs)
	.map((d) => ({ label: d.uf, value: d.valor_executado_rs }));

export const silhouetteStateData = stateRows.map((d) => ({ state: d.uf, value: d.valor_executado_rs }));

export const bubbleStateData = stateRows.map((d) => ({
	label: d.uf,
	x:     d.sum_populacao,
	y:     d.valor_executado_rs,
	size:  d.qtde_contemplados,
	group: regionMap[d.uf],
}));

// ── Slope: ranking valor vs ranking população (todos os 27 estados) ───────────
export const n = stateRows.length;

const byValue = [...stateRows].sort((a, b) => b.valor_executado_rs - a.valor_executado_rs);
const byPop   = [...stateRows].sort((a, b) => b.sum_populacao - a.sum_populacao);

const valueRankMap = Object.fromEntries(byValue.map((d, i) => [d.uf, i + 1]));
const popRankMap   = Object.fromEntries(byPop.map((d, i)   => [d.uf, i + 1]));

export const slopeItems = stateRows.map((d) => ({
	name:   d.uf,
	values: [n + 1 - valueRankMap[d.uf], n + 1 - popRankMap[d.uf]],
}));
export const slopeLabels = ['Ranking por valor', 'Ranking por população'];
export const formatSlope = (v: number) => `${n + 1 - v}º`;

// ── BoxPlot: mediana de repasse por região ────────────────────────────────────
const regionOrder = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'];

export const boxPlotData = regionOrder.map((regiao) => ({
	label:  regiao,
	values: stateRows
		.filter((d) => regionMap[d.uf] === regiao)
		.sort((a, b) => a.uf.localeCompare(b.uf))
		.map((d) => d.mediana_valor),
}));

// ── Heatmap: estados × faixas de valor pago ───────────────────────────────────
export const heatmapBuckets = [
	'Até R$2k', 'R$2–10k', 'R$10–50k', 'R$50–200k', 'R$200–500k', 'R$500k–1M', 'R$1–10M', '>R$10M',
] as const;

export const heatmapStates = [...stateRows]
	.sort((a, b) => b.valor_executado_rs - a.valor_executado_rs)
	.map((d) => d.uf);

export const heatmapData = heatmapStates.flatMap((uf) => {
	const row = stateRows.find((d) => d.uf === uf)!;
	return heatmapBuckets.map((bucket) => ({ x: bucket, y: uf, value: row[bucket] }));
});

// ── Per capita e split estado/município ────────────────────────────────────────
const ufRows  = parseCSV(csvUfRaw);
const munRows = parseCSV(csvMunRaw);

const stateValByUf = Object.fromEntries(stateRows.map((d) => [d.uf, d.valor_executado_rs]));
const munValByUf   = Object.fromEntries(munRows.map((d)   => [d.uf, +d.valor_executado_rs]));

export const percapitaData = [...ufRows]
	.map((d) => ({
		uf:               d.uf,
		valor_percapita_uf: +d.sum_populacao > 0 ? +d.valor_executado_rs / +d.sum_populacao : 0,
	}))
	.sort((a, b) => b.valor_percapita_uf - a.valor_percapita_uf);

export const ufSplitData = ufRows.map((d) => {
	const stVal = stateValByUf[d.uf] ?? 0;
	const muVal = munValByUf[d.uf]   ?? 0;
	const total = stVal + muVal || 1;
	return {
		label:    d.uf,
		leftPct:  (stVal / total) * 100,
		rightPct: (muVal / total) * 100,
	};
});

// ── Urbano vs Rural por UF (executed_value_zone_by_state.csv) ─────────────────
export const zoneData = parseCSV(csvZoneRaw)
	.map((d) => ({ label: d.uf, valor_urbano: +d.valor_urbano, valor_rural: +d.valor_rural }))
	.sort(
		(a, b) =>
			b.valor_rural / (b.valor_urbano + b.valor_rural) -
			a.valor_rural / (a.valor_urbano + a.valor_rural)
	);

// ── Porte municipal (values_by_population_size.csv) ───────────────────────────
const porteNameMap: Record<string, string> = {
	'4_grande':    'Grande',
	'1_pequeno_i': 'Pequeno I',
	'2_pequeno_ii': 'Pequeno II',
	'3_medio':     'Médio',
};
const porteKeyMap: Record<string, string> = {
	'Grande':     'grande',
	'Pequeno I':  'pequeno_i',
	'Pequeno II': 'pequeno_ii',
	'Médio':      'medio',
};

export const porteRaw = parseCSV(csvPorteRaw)
	.filter((d) => d.porte_populacional in porteNameMap)
	.map((d) => ({
	porte:           porteNameMap[d.porte_populacional],
	municipios:      +d.numero_municipios,
	valor_total:     +d.valor_total_por_porte,
	valor_urbano:    +d.valor_urbano_por_porte,
	valor_rural:     +d.valor_rural_por_porte,
	beneficiarios:   +d.quantidade_contemplados_por_porte,
	perc_valor:      +d.percentual_valor_por_porte    * 100,
	perc_quantidade: +d.percentual_quantidade_por_porte * 100,
}));

export const porteTreemapData = {
	name:     'root',
	children: porteRaw.map((d) => ({ name: d.porte, value: d.valor_total })),
};

export const porteDivergingData = porteRaw.map((d) => {
	const total = d.valor_urbano + d.valor_rural;
	return {
		label:    d.porte,
		leftPct:  (d.valor_urbano / total) * 100,
		rightPct: (d.valor_rural  / total) * 100,
	};
});

export const porteBubbleData = porteRaw.map((d) => ({
	label: d.porte,
	x:     d.municipios,
	y:     d.valor_total,
	size:  d.beneficiarios,
	group: d.porte,
}));

export const porteStackedKeys   = porteRaw.map((d) => porteKeyMap[d.porte]);
export const porteStackedLabels = Object.fromEntries(
	porteRaw.map((d) => [porteKeyMap[d.porte], d.porte])
);
export const porteStackedData = [
	{
		label: 'Valor investido (%)',
		...Object.fromEntries(porteRaw.map((d) => [porteKeyMap[d.porte], d.perc_valor])),
	},
	{
		label: 'Beneficiários (%)',
		...Object.fromEntries(porteRaw.map((d) => [porteKeyMap[d.porte], d.perc_quantidade])),
	},
];

// ── Territórios especiais (special_territory_w_ibge_by_brazil.csv) ────────────
export const specialData = parseCSV(csvSpecialRaw).map((d) => ({
	territorio:     d.territorio,
	perc_recurso:   +d['% recurso total'],
	perc_populacao: +d['% população no território'],
}));

export const percRecursoEspecial   = specialData.reduce((s, d) => s + d.perc_recurso,   0).toFixed(2);
export const percPopulacaoEspecial = specialData.reduce((s, d) => s + d.perc_populacao, 0).toFixed(1);

export const specialDivergingData = specialData.map((d) => {
	const total = d.perc_populacao + d.perc_recurso;
	return {
		label:    d.territorio,
		leftPct:  (d.perc_populacao / total) * 100,
		rightPct: (d.perc_recurso   / total) * 100,
	};
});

// ── UF completo para DataTable ────────────────────────────────────────────
export const ufData = ufRows.map((d) => {
	const stVal = stateValByUf[d.uf] ?? 0;
	const muVal = munValByUf[d.uf]   ?? 0;
	const total = stVal + muVal || 1;
	return {
		uf:                             d.uf,
		valor_executado_estado:         stVal,
		valor_executado_municipio:      muVal,
		valor_executado_total_uf:       total,
		perc_valor_executado_estado:    (stVal / total) * 100,
		perc_valor_executado_municipio: (muVal / total) * 100,
		valor_executado_perc:           +d.valor_executado_perc * 100,
	};
});

// ── Zona municipal (UF total − estado) ────────────────────────────────────
const zoneStateMap = Object.fromEntries(zoneData.map((d) => [d.label, d]));

export const zoneMunicipalityData = parseCSV(csvZoneUfRaw)
	.map((d) => {
		const st = zoneStateMap[d.uf] ?? { valor_urbano: 0, valor_rural: 0 };
		return {
			label:        d.uf,
			valor_urbano: +d.valor_uf_urbano - st.valor_urbano,
			valor_rural:  +d.valor_uf_rural  - st.valor_rural,
		};
	})
	.sort(
		(a, b) =>
			b.valor_rural / (b.valor_urbano + b.valor_rural) -
			a.valor_rural / (a.valor_urbano + a.valor_rural)
	);

// ── Territórios especiais stacked (estado vs município) ───────────────────
const specialShortLabels: Record<string, string> = {
	'Favela e Comunidade Urbana':         'Favela / Com. Urbana',
	'Setor com baixo patamar domiciliar': 'Setor baixo patamar',
	'Não informado':                       'Não informado',
	'Agrupamento quilombola':              'Quilombola',
	'Agrupamento indígena':                'Indígena',
	'Quartel e base militar':              'Quartel / Militar',
	'Agrovila do PA':                      'Agrovila do PA',
	'Convento / hospital / ILPI / IACA':  'Convento / ILPI / IACA',
	'Unidade prisional':                   'Unidade prisional',
	'Alojamento / acampamento':            'Alojamento / Acampamento',
};

const specialStMap  = Object.fromEntries(parseCSV(csvSpecialStRaw).map((d)  => [d.cod_tipo_nome, +d.valor_transacao]));
const specialMunMap = Object.fromEntries(parseCSV(csvSpecialMunRaw).map((d) => [d.cod_tipo_nome, +d.valor_transacao]));

export const specialStackedData = Object.keys(specialShortLabels)
	.map((nome) => ({
		shortLabel:      specialShortLabels[nome],
		valor_estado:    specialStMap[nome]  ?? 0,
		valor_municipio: specialMunMap[nome] ?? 0,
	}))
	.sort((a, b) => (b.valor_estado + b.valor_municipio) - (a.valor_estado + a.valor_municipio));
