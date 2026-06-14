// All Section 1 data, parsed from CSVs at build time.

import csvStateRaw      from '../../../data/section_1/executed_value_by_state.csv?raw';
import csvMunRaw        from '../../../data/section_1/executed_value_by_municipality.csv?raw';
import csvUfRaw         from '../../../data/section_1/executed_value_by_uf.csv?raw';
import csvRegionRaw     from '../../../data/section_1/executed_value_by_region_state.csv?raw';
// import csvZoneRaw       from '../../../data/section_1/executed_value_zone_by_state.csv?raw'; // CSV faltante
// import csvZoneUfRaw     from '../../../data/section_1/executed_value_zone_by_uf.csv?raw';   // CSV faltante
import csvPorteRaw      from '../../../data/section_1/values_by_population_size.csv?raw';
import csvSpecialRaw    from '../../../data/section_1/special_territory_w_ibge_by_brazil.csv?raw';
import csvSpecialStRaw  from '../../../data/section_1/values_by_special_territory_state.csv?raw';
import csvSpecialMunRaw from '../../../data/section_1/values_by_special_territory_municipality.csv?raw';
// import csvBnRaw         from '../../../data/section_1/bignumber1.csv?raw';         // CSV faltante
import csvRegionUfRaw   from '../../../data/section_1/executed_value_by_region_uf.csv?raw';
import csvCapitalRaw    from '../../../data/section_1/aggregate_values_by_capital.csv?raw';
import csvSpecialUfRaw  from '../../../data/section_1/values_by_special_territory_uf.csv?raw';
// import csvPorteMeanRaw  from '../../../data/section_1/population_size_mean.csv?raw'; // CSV faltante
import csvLocalResidRaw       from '../../../data/section_1/aggregate_by_local_residencia_uf.csv?raw';
// import csvPortePopRaw         from '../../../data/section_1/resumo_por_porte_populacional.csv?raw'; // CSV faltante (existe em section_2/)
import csvEstadoLocalResidRaw from '../../../data/section_1/aggregate_estado_by_uf_local_residencia.csv?raw';

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

// // ── Totais (bignumber1.csv faltante) ──────────────────────────────────────────
// const [bnRow] = parseCSV(csvBnRaw);
// export const percExecEstados    = +bnRow.perc_executado_estados    * 100;
// export const percExecMunicipios = +bnRow.perc_executado_municipios * 100;
// export const valorExecEstados    = +bnRow.Estados_DF;
// export const valorExecMunicipios = +bnRow.Municipios_DF;
// export const valorExecTotal      = +bnRow.Estados_DF + +bnRow.Municipios_DF;

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
	'>R$200k':     number;
}

export const stateRows: StateRow[] = parseCSV(csvUfRaw).map((d) => ({
	uf:                   d.uf,
	valor_executado_rs:   +d.valor_executado_rs,
	valor_executado_perc: +d.valor_executado_perc,
	sum_populacao:        +d.sum_populacao,
	qtde_contemplados:    +d.qtde_contemplados,
	mediana_valor:        +d.mediana_valor,
	'Até R$2k':   +d['Até 2 mil'],
	'R$2–10k':    +d['De 2 a 10 mil'],
	'R$10–50k':   +d['De 10 a 50 mil'],
	'R$50–200k':  +d['De 50 a 200 mil'],
	'>R$200k':    +d['Acima de 200 mil'],
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

// ── BoxPlot: distribuição de repasses por região ─────────────────────────────
const regionOrder = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'];
const regionUfRows = parseCSV(csvRegionUfRaw);

// Opção 3: mediana por estado dentro de cada região (4–9 pontos por caixa)
// Para grupos com menos de 5 pontos, desativa detecção de outliers — quartis interpolados
// podem ultrapassar os valores reais quando n é muito pequeno, tornando os whiskers invisíveis.
function boxStats(values: number[], minForOutliers = 5) {
	const s = [...values].sort((a, b) => a - b);
	const q = (p: number) => {
		const i = (s.length - 1) * p;
		const lo = Math.floor(i), hi = Math.ceil(i);
		return s[lo] + (s[hi] - s[lo]) * (i - lo);
	};
	const q1 = q(0.25), median = q(0.5), q3 = q(0.75);
	if (s.length < minForOutliers) {
		return { min: s[0], q1, median, q3, max: s[s.length - 1] };
	}
	const iqr = q3 - q1;
	const lo = q1 - 1.5 * iqr, hi = q3 + 1.5 * iqr;
	const inner = s.filter(v => v >= lo && v <= hi);
	const outer = s.filter(v => v < lo || v > hi);
	return {
		min: inner.length > 0 ? inner[0] : s[0],
		q1, median, q3,
		max: inner.length > 0 ? inner[inner.length - 1] : s[s.length - 1],
		...(outer.length > 0 ? { outliers: outer } : {}),
	};
}

export const boxPlotData = regionOrder.map((regiao) => {
	const values = stateRows
		.filter((d) => regionMap[d.uf] === regiao)
		.map((d) => d.mediana_valor);
	return { label: regiao, stats: boxStats(values) };
});

// Opção 1: mediana agregada da região (individual-level) para barra simples
export const regionMedianData = regionOrder.map((regiao) => {
	const row = regionUfRows.find((d) => d.regiao === regiao)!;
	return { label: regiao, value: +row.mediana_valor };
});

// ── Heatmap: estados × faixas de valor pago ───────────────────────────────────
export const heatmapBuckets = [
	'Até R$2k', 'R$2–10k', 'R$10–50k', 'R$50–200k', '>R$200k',
] as const;

export const heatmapStates = [...stateRows]
	.sort((a, b) => b.valor_executado_rs - a.valor_executado_rs)
	.map((d) => d.uf);

export const heatmapData = heatmapStates.flatMap((uf) => {
	const row = stateRows.find((d) => d.uf === uf)!;
	return heatmapBuckets.map((bucket) => ({ x: bucket, y: uf, value: row[bucket] }));
});

// ── Per capita e split estado/município ────────────────────────────────────────
const ufRows  = stateRows;
const munRows = parseCSV(csvMunRaw);

const stateValByUf = Object.fromEntries(parseCSV(csvStateRaw).map((d) => [d.uf, +d.valor_executado_rs]));
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

// ── Urbano vs Rural por UF — contagem de contemplados (executed_value_by_state.csv) ──
export const zoneQtdData = parseCSV(csvStateRaw)
	.map((d) => ({
		label:       d.uf,
		qtde_urbano: +d.qtde_urbano,
		qtde_rural:  +d.qtde_rural,
	}))
	.sort(
		(a, b) =>
			b.qtde_rural / (b.qtde_urbano + b.qtde_rural) -
			a.qtde_rural / (a.qtde_urbano + a.qtde_rural)
	);

// // ── Urbano vs Rural por UF (executed_value_zone_by_uf.csv faltante) ──────────
// export const zoneData = parseCSV(csvZoneUfRaw)
// 	.map((d) => ({ label: d.uf, valor_urbano: +d.valor_uf_urbano, valor_rural: +d.valor_uf_rural }))
// 	.sort(
// 		(a, b) =>
// 			b.valor_rural / (b.valor_urbano + b.valor_rural) -
// 			a.valor_rural / (a.valor_urbano + a.valor_rural)
// 	);

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

export const porteStackedKeys   = ['grande', 'medio', 'pequeno_i', 'pequeno_ii'];
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

// ── CPF vs CNPJ por porte populacional ────────────────────────────────────────
const _porteOrder = ['1_pequeno_i', '2_pequeno_ii', '3_medio', '4_grande'];
const _porteCpfCnpjRaw = parseCSV(csvPorteRaw)
	.filter((d) => d.porte_populacional in porteNameMap)
	.sort((a, b) => _porteOrder.indexOf(a.porte_populacional) - _porteOrder.indexOf(b.porte_populacional));
export const porteCpfCnpjStackedData = _porteCpfCnpjRaw.map((d) => ({
	label: porteNameMap[d.porte_populacional],
	cpf:   +d.perc_valor_CPF  * 100,
	cnpj:  +d.perc_valor_CNPJ * 100,
}));
export const porteCpfCnpjKeys   = ['cpf', 'cnpj'] as const;
export const porteCpfCnpjLabels: Record<string, string> = {
	cpf:  'CPF (Pessoa Física)',
	cnpj: 'CNPJ (Pessoa Jurídica)',
};

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

// // ── Zona municipal (CSVs faltantes: executed_value_zone_by_state/uf) ──────────
// const zoneStateRaw = parseCSV(csvZoneRaw)
// 	.map((d) => ({ label: d.uf, valor_urbano: +d.valor_urbano, valor_rural: +d.valor_rural }));
// const zoneStateMap = Object.fromEntries(zoneStateRaw.map((d) => [d.label, d]));
//
// export const zoneMunicipalityData = parseCSV(csvZoneUfRaw)
// 	.map((d) => {
// 		const st = zoneStateMap[d.uf] ?? { valor_urbano: 0, valor_rural: 0 };
// 		return {
// 			label:        d.uf,
// 			valor_urbano: +d.valor_uf_urbano - st.valor_urbano,
// 			valor_rural:  +d.valor_uf_rural  - st.valor_rural,
// 		};
// 	})
// 	.sort(
// 		(a, b) =>
// 			b.valor_rural / (b.valor_urbano + b.valor_rural) -
// 			a.valor_rural / (a.valor_urbano + a.valor_rural)
// 	);

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

// ── Territory totals ───────────────────────────────────────────────────────────
const rawSpecial = parseCSV(csvSpecialRaw);
export const specialTerritoryCount = rawSpecial.reduce((s, d) => s + +d['Quantidade de contemplados'], 0);
export const specialTerritoryValue = rawSpecial.reduce((s, d) => s + +d['Valor (R$)'], 0);

// ── Métricas completas: 4 variáveis por território especial ───────────────────
const specialUfRows = parseCSV(csvSpecialUfRaw);
const shortLabelMap: Record<string, string> = {
	'Favela e Comunidade Urbana': 'Favela / Com. Urbana',
	'Agrupamento quilombola':     'Quilombola',
	'Agrupamento indígena':       'Indígena',
};
export const specialTerritoriesMetrics = specialUfRows.map((d) => {
	const ibge = rawSpecial.find((r) => r.territorio === d.cod_tipo_nome);
	return {
		territorio:     d.cod_tipo_nome,
		shortLabel:     shortLabelMap[d.cod_tipo_nome] ?? d.cod_tipo_nome,
		valor:          +d.valor_transacao,
		perc_recurso:   +d.perc_valor_transacao * 100,
		perc_agentes:   +d.perc_quantidade_contemplados * 100,
		perc_populacao: ibge ? +ibge['% população no território'] : 0,
	};
});

// // ── Rural total (executed_value_zone_by_uf.csv faltante) ──────────────────────
// export const valorRuralTotal = parseCSV(csvZoneUfRaw)
// 	.reduce((s, d) => s + +d.valor_uf_rural, 0);

// ── Contemplados em zona rural (estado + município) ────────────────────────────
const _qtdeRuralState = parseCSV(csvStateRaw).reduce((s, d) => s + +d.qtde_rural, 0);
const _qtdeRuralMun   = parseCSV(csvMunRaw).reduce((s, d) => s + +d.qtde_rural, 0);
const _qtdeTotalState = parseCSV(csvStateRaw).reduce((s, d) => s + +d.qtde_contemplados, 0);
const _qtdeTotalMun   = parseCSV(csvMunRaw).reduce((s, d) => s + (+d.qtde_rural + +d.qtde_urbano), 0);
export const qtdeRuralTotal  = _qtdeRuralState + _qtdeRuralMun;
export const percRuralQtde   = (qtdeRuralTotal / (_qtdeTotalState + _qtdeTotalMun)) * 100;
// export const percRuralValor  = (valorRuralTotal / parseCSV(csvZoneUfRaw).reduce((s, d) => s + +d.valor_uf, 0)) * 100; // CSV faltante

// ── Capital vs Região Metropolitana vs Interior (aggregate_by_local_residencia_uf.csv) ──
const localResidRows = parseCSV(csvLocalResidRaw);
const _interiorRow   = localResidRows.find((d) => d.local_residencia_contemplados === 'Interior')!;
const _metroRow      = localResidRows.find((d) => d.local_residencia_contemplados === 'Regiao Metropolitana')!;
const _capitalRow2   = localResidRows.find((d) => d.local_residencia_contemplados === 'Capital')!;

export const percInteriorContemplados = +_interiorRow.percentual_quantidade * 100;  // ~58.14
export const percInteriorPagamentos   = +_interiorRow.percentual_valor       * 100;
export const valorInteriorTotal       = +_interiorRow.valor_total;                  // ~966,747,807

export const capitalInteriorStackedData = [
	{
		label:         '% do recurso executado',
		capital:       +_capitalRow2.percentual_valor    * 100,
		metropolitana: +_metroRow.percentual_valor       * 100,
		interior:      +_interiorRow.percentual_valor    * 100,
	},
	{
		label:         '% dos agentes contemplados',
		capital:       +_capitalRow2.percentual_quantidade * 100,
		metropolitana: +_metroRow.percentual_quantidade    * 100,
		interior:      +_interiorRow.percentual_quantidade * 100,
	},
];

// ── Capital / Metropolitana / Interior por UF — execução estadual ─────────────
export const capitalInteriorByUfData = parseCSV(csvEstadoLocalResidRaw)
	.filter((d) => d.uf)
	.map((d) => ({
		label:         d.uf,
		capital:       +d.percentual_quantidade_capital       * 100,
		metropolitana: +d.percentual_quantidade_regiao_metropolitana * 100,
		interior:      +d.percentual_quantidade_interior      * 100,
	}))
	.sort((a, b) => b.interior - a.interior);

// // ── Métricas por porte populacional (resumo_por_porte_populacional.csv faltante em section_1/) ──
// export const porteMeanData = parseCSV(csvPortePopRaw)
// 	.filter((d) => d.porte_populacional)
// 	.map((d) => ({
// 		label:           porteNameMap[d.porte_populacional] ?? d.porte_populacional,
// 		municipios:      +d.numero_municipios,
// 		valor_total:     +d.valor_total_por_porte,
// 		valor_medio:     +d.valor_medio_por_porte,
// 		valor_mediano:   +d.valor_mediano_por_porte,
// 		quantidade:      +d.quantidade_contemplados_por_porte,
// 		perc_valor:      +d.percentual_valor_por_porte * 100,
// 		perc_quantidade: +d.percentual_quantidade_contemplados_por_porte * 100,
// 	}))
// 	.sort((a, b) => b.valor_mediano - a.valor_mediano);
