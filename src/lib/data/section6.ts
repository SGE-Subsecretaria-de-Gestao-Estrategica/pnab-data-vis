// Section 6 data — Distribuição de recursos por tipo de despesa

import csvGrafico1Raw from '../../../data/section_6/capitulo_6_grafico_1.csv?raw';
import csvGrafico2Raw from '../../../data/section_6/capitulo_6_grafico_2.csv?raw';
import csvGrafico3Raw from '../../../data/section_6/capitulo_6_grafico_3.csv?raw';
import csvGrafico4Raw from '../../../data/section_6/capitulo_6_grafico_4.csv?raw';
import csvPncvOuOutrosRaw from '../../../data/section_6/capitulo_6_grafico_pncv_ou_outros__2026-06-03_17-52.csv?raw';
import csvTipoExecRegiaoRaw from '../../../data/section_6/capitulo_6_grafico_tipo_exec_regiao__2026-06-03_18-36.csv?raw';

import type { MekkoDatum, TreemapNode } from 'sniic-design-system';

// ── Parser ──────────────────────────────────────────────────────────────────────
function parseCSV(text: string): Record<string, string>[] {
	// Strip BOM if present
	const clean = text.replace(/^\uFEFF/, '');
	const lines = clean.trim().split('\n');
	const headers = lines[0].split(';').map((h) => h.trim());
	return lines
		.slice(1)
		.filter((l) => l.trim())
		.map((line) => {
			const values = line.split(';').map((v) => v.trim());
			return Object.fromEntries(headers.map((h, i) => [h, values[i] ?? '']));
		});
}

const formatBRL = (v: number) =>
	new Intl.NumberFormat('pt-BR', {
		style: 'currency',
		currency: 'BRL',
		notation: 'compact',
		maximumFractionDigits: 1,
	}).format(v);

// ── Grafico 1 — Categorias de despesa ──────────────────────────────────────────
const g1Rows = parseCSV(csvGrafico1Raw);

// Keys used in MekkoDatum per category name
const CATEGORY_KEY: Record<string, string> = {
	'Fomento Cultural':                                          'fomento',
	'Política Nacional de Cultura Viva':                         'cultura_viva',
	'Subsídio e manutenção de espaços e organizações culturais': 'subsidio',
	'Obras, Reformas e Aquisição de Bens Culturais':             'obras',
	'Operacionalização da Política':                             'operacionalizacao',
	'Vazio':                                                     'vazio',
	'Outros':                                                    'outros_cat',
};

const MAIN_CATEGORIES = new Set(['fomento', 'cultura_viva', 'obras']);

const formatMi = (v: number) =>
	new Intl.NumberFormat('pt-BR', { notation: 'compact', maximumFractionDigits: 1 }).format(v);

const g1Data = g1Rows.map((r) => ({
	key:   CATEGORY_KEY[r.expenses_agrupado] ?? r.expenses_agrupado,
	label: r.expenses_agrupado,
	valor: +r.valor_estimado,
	p025:  +r.p025,
	p975:  +r.p975,
	pct:   +r.valor_estimado_pct,
}));

const mainRows  = g1Data.filter((r) => MAIN_CATEGORIES.has(r.key));
const otherRows = g1Data.filter((r) => !MAIN_CATEGORIES.has(r.key));

const mainTotal  = mainRows.reduce((s, r) => s + r.valor, 0);
const otherTotal = otherRows.reduce((s, r) => s + r.valor, 0);
const mainPct    = mainRows.reduce((s, r) => s + r.pct, 0);

// Boost right column visual width to ~7% of chart width.
const RIGHT_VISUAL_FRACTION = 0.07;
const otherVisualTotal = Math.max(otherTotal, mainTotal * (RIGHT_VISUAL_FRACTION / (1 - RIGHT_VISUAL_FRACTION)));

// Boost Cultura Viva visual height to at least 20% of the left column.
const CULTURA_MIN_LEFT_FRACTION = 0.20;
const culturaRow    = mainRows.find((r) => r.key === 'cultura_viva')!;
const fomentoRow    = mainRows.find((r) => r.key === 'fomento')!;
const obrasRow      = mainRows.find((r) => r.key === 'obras')!;

// Boost Obras visual height to at least 13% of the left column.
const OBRAS_MIN_LEFT_FRACTION = 0.13;
const nonObrasSum   = culturaRow.valor + fomentoRow.valor;
const obrasVisual   = Math.max(
	obrasRow.valor,
	nonObrasSum * (OBRAS_MIN_LEFT_FRACTION / (1 - OBRAS_MIN_LEFT_FRACTION)),
);

const nonCulturaSum = fomentoRow.valor + obrasVisual;
const culturaVivaVisual = Math.max(
	culturaRow.valor,
	nonCulturaSum * (CULTURA_MIN_LEFT_FRACTION / (1 - CULTURA_MIN_LEFT_FRACTION)),
);

const mainPctFormatted = mainPct.toLocaleString('pt-BR', {
	minimumFractionDigits: 1,
	maximumFractionDigits: 1,
}) + '%';

export const expensesGrandTotal = g1Data.reduce((s, r) => s + r.valor, 0);

export const expensesChartData: MekkoDatum[] = [
	{
		label: `Fomento Cultural, Política Nacional de Cultura Viva e Obras, Reformas e Aquisição de Bens Culturais — 88,4%`,
		total: mainTotal,
		...Object.fromEntries(mainRows.map((r) =>
			r.key === 'cultura_viva' ? [r.key, culturaVivaVisual] :
			r.key === 'obras'        ? [r.key, obrasVisual]        : [r.key, r.valor]
		)),
	},
	{
		label: 'Outros Investimentos',
		total: otherVisualTotal,
		...Object.fromEntries(otherRows.map((r) => [r.key, r.valor])),
	},
];

export const expensesKeys = [
	'fomento',
	'cultura_viva',
	'obras',
	'subsidio',
	'operacionalizacao',
	'vazio',
	'outros_cat',
];

// Short labels for the SVG legend bar
export const expensesLabels: Record<string, string> = {
	fomento:           'Fomento',
	cultura_viva:      'Cultura Viva',
	subsidio:          'Subsídio',
	obras:             'Obras',
	operacionalizacao: 'Operac.',
	vazio:             'Vazio',
	outros_cat:        'Outros',
};

// Full legend items for the HTML reference table
export const expensesLegendItems = g1Data.map((r) => ({
	key:   r.key,
	label: r.label,
	valor: r.valor,
	value: formatMi(r.valor),
	ci:    `IC95%: ${formatMi(r.p025)} – ${formatMi(r.p975)}`,
}));

// ── Grafico 2 — Subcategorias de Fomento Cultural ──────────────────────────────
const fomentoSubRaw = parseCSV(csvGrafico2Raw).map((r) => ({
	label: r['Categorização Nivel 0'],
	valor: +r.valor_estimado,
	p025:  +r.p025,
	p975:  +r.p975,
	valorFormatted: formatBRL(+r.valor_estimado),
}));
const fomentoSubTotal = fomentoSubRaw.reduce((s, r) => s + r.valor, 0);
export const fomentoSubData = fomentoSubRaw.map((r) => ({
	...r,
	pct: (r.valor / fomentoSubTotal) * 100,
}));

// ── Grafico 3 — Domínios de Fomento Cultural (Treemap) ────────────────────────
const g3Rows = parseCSV(csvGrafico3Raw).map((r) => ({
	name:  r['Categorização Domínios'],
	value: +r.valor_estimado,
	p025:  +r.p025,
	p975:  +r.p975,
	pct:   +r.valor_estimado_pct,
}));

export const fomentoDomainsTreemap: TreemapNode = {
	name: 'Fomento Cultural',
	children: g3Rows.map((r) => ({ name: r.name, value: r.value })),
};

export const fomentoDomainsRows = g3Rows;

// ── Grafico 4 — Subcategorias de PNCV ─────────────────────────────────────────
const pncvSubRaw = parseCSV(csvGrafico4Raw).map((r) => ({
	label: r['Categorização Nivel 0'],
	valor: +r.valor_estimado,
	p025:  +r.p025,
	p975:  +r.p975,
	valorFormatted: formatBRL(+r.valor_estimado),
}));
const pncvSubTotal = pncvSubRaw.reduce((s, r) => s + r.valor, 0);
export const pncvSubData = pncvSubRaw.map((r) => ({
	...r,
	pct: (r.valor / pncvSubTotal) * 100,
}));

// ── Grafico PNCV ou Outros — % do valor por faixa de repasse ──────────────────
const pncvOuOutrosRaw = parseCSV(csvPncvOuOutrosRaw);

// Group by regra_pncv, pivot pncv_ou_outros into keys
const REGRA_ORDER = [
	'Brasil',
	'Cidade recebeu mais de 360 mil reais',
	'Cidade recebeu até 360 mil reais',
];

const _pncvOuOutrosMap = new Map<string, { outros_pct: number; pncv_pct: number; outros_val: number; pncv_val: number }>();
for (const r of pncvOuOutrosRaw) {
	const regra = r.regra_pncv;
	if (!_pncvOuOutrosMap.has(regra)) {
		_pncvOuOutrosMap.set(regra, { outros_pct: 0, pncv_pct: 0, outros_val: 0, pncv_val: 0 });
	}
	const entry = _pncvOuOutrosMap.get(regra)!;
	if (r.pncv_ou_outros === 'PNCV') {
		entry.pncv_pct = +r.valor_estimado_pct;
		entry.pncv_val = +r.valor_estimado;
	} else {
		entry.outros_pct = +r.valor_estimado_pct;
		entry.outros_val = +r.valor_estimado;
	}
}

export const pncvOuOutrosData = REGRA_ORDER.filter((r) => _pncvOuOutrosMap.has(r)).map((regra) => ({
	label: regra,
	..._pncvOuOutrosMap.get(regra)!,
}));

export const pncvOuOutrosKeys = ['pncv_pct', 'outros_pct'] as const;
export const pncvOuOutrosLabels: Record<string, string> = {
	pncv_pct:   'PNCV',
	outros_pct: 'Outros',
};

// ── Grafico tipo_exec_regiao — % por tipo de execução × região ────────────────
const tipoExecRegiaoRaw = parseCSV(csvTipoExecRegiaoRaw);

const TIPO_KEY: Record<string, string> = {
	'Ação Cultural - Fomento Cultural': 'acao_pct',
	'Bolsa - Fomento Cultural':         'bolsa_pct',
	'Premiação - Fomento Cultural':     'premiacao_pct',
};

const REGIAO_ORDER_EXEC = [
	'Todo o Brasil',
	'Sul',
	'Sudeste',
	'Nordeste',
	'Norte',
	'Centro-Oeste',
];

const _tipoExecMap = new Map<string, Record<string, number>>();
for (const r of tipoExecRegiaoRaw) {
	const regiao = r.regiao;
	if (!_tipoExecMap.has(regiao)) _tipoExecMap.set(regiao, {});
	const key = TIPO_KEY[r['Categorização Nivel 0']];
	if (key) _tipoExecMap.get(regiao)![key] = +r.valor_estimado_pct;
}

export const tipoExecRegiaoData = REGIAO_ORDER_EXEC
	.filter((r) => _tipoExecMap.has(r))
	.map((regiao) => ({ label: regiao, ..._tipoExecMap.get(regiao)! }));

export const tipoExecRegiaoKeys = ['acao_pct', 'bolsa_pct', 'premiacao_pct'] as const;
export const tipoExecRegiaoLabels: Record<string, string> = {
	acao_pct:      'Ação Cultural',
	bolsa_pct:     'Bolsa',
	premiacao_pct: 'Premiação',
};
