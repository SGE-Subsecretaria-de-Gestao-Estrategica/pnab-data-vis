// All Section 4 data, parsed from CSVs at build time.
// Narrativa: vínculo com trabalho formal entre os beneficiários do PNAB.

import csvTotalRaw       from '../../../data/section_4/aggregate_vinculo_formal_labor.csv?raw';
import csvAgeRaw         from '../../../data/section_4/aggregate_vinculo_formal_labor_by_age_group.csv?raw';
import csvEscolaridadeRaw from '../../../data/section_4/aggregate_vinculo_trabalho_formal_by_escolaridade_clean.csv?raw';
import csvRegionRaw      from '../../../data/section_4/aggregate_vinculo_formal_labor_by_region.csv?raw';
import csvSexoRaw        from '../../../data/section_4/aggregate_vinculo_formal_labor_by_sexo.csv?raw';
import csvRacaCorRaw     from '../../../data/section_4/aggregate_vinculo_formal_labor_by_raca_cor.csv?raw';
import csvRacaCorSexoRaw from '../../../data/section_4/aggregate_raca_cor_vinculo_formal_labor_by_sexo.csv?raw';
import csvUfRaw          from '../../../data/section_4/aggregate_vinculo_formal_labor_by_uf.csv?raw';
import csvUfIbgeRaw      from '../../../data/section_4/aggregate_vinculo_formal_labor_by_uf_ibge.csv?raw';
import csvCboRaisRaw     from '../../../data/section_4/aggregate_cbo_rais.csv?raw';

// Handles quoted fields with embedded commas (standard CSV)
function parseCSV(text: string): Record<string, string>[] {
	function parseLine(line: string): string[] {
		const result: string[] = [];
		let i = 0;
		while (i <= line.length) {
			if (i === line.length) { result.push(''); break; }
			if (line[i] === '"') {
				i++; // skip opening quote
				let val = '';
				while (i < line.length && line[i] !== '"') val += line[i++];
				i++; // skip closing quote
				result.push(val);
				if (line[i] === ',') i++;
			} else {
				const j = line.indexOf(',', i);
				if (j === -1) { result.push(line.slice(i)); break; }
				result.push(line.slice(i, j));
				i = j + 1;
			}
		}
		return result;
	}

	const lines = text.trim().split('\n');
	const headers = parseLine(lines[0]);
	return lines
		.slice(1)
		.filter((l) => l.trim())
		.map((line) => {
			const values = parseLine(line);
			return Object.fromEntries(headers.map((h, idx) => [h, values[idx] ?? '']));
		});
}

function shortRaceLabel(desc: string): string {
	if (desc.startsWith('Amarela')) return 'Amarela';
	if (desc.startsWith('Branca')) return 'Branca';
	if (desc.startsWith('Indígena')) return 'Indígena';
	if (desc === 'Não informado') return 'Não informado';
	if (desc.startsWith('Parda')) return 'Parda';
	if (desc.startsWith('Preta')) return 'Preta/negra';
	return desc;
}

// ── Totais ─────────────────────────────────────────────────────────────────────
const [totalRow] = parseCSV(csvTotalRaw);

export const totalSemVinculo  = +totalRow.numero_contemplados_sem_vinculo_trabalho_formal;
export const totalComVinculo  = +totalRow.numero_contemplados_com_vinculo_trabalho_formal;
export const totalBenef       = +totalRow.numero_contemplados_total;
export const percSemVinculo   = +totalRow.percentual_contemplados_sem_vinculo_trabalho_formal * 100;
export const percComVinculo   = +totalRow.percentual_contemplados_com_vinculo_trabalho_formal * 100;
export const valorSemVinculo  = +totalRow.valor_pago_sem_vinculo_trabalho_formal;
export const valorComVinculo  = +totalRow.valor_pago_com_vinculo_trabalho_formal;
export const valorTotal       = +totalRow.valor_pago_total;

export const valorAreaData = [
	{ label: 'Sem vínculo formal', value: valorSemVinculo },
	{ label: 'Com vínculo formal', value: valorComVinculo },
];

// ── Por faixa etária ────────────────────────────────────────────────────────────
const ageRows = parseCSV(csvAgeRaw);

export const ageGroupStackedData = ageRows.map((r) => ({
	label:       r.faixa_etaria,
	sem_vinculo: +r.percentual_contemplados_sem_vinculo_trabalho_formal * 100,
	com_vinculo: +r.percentual_contemplados_com_vinculo_trabalho_formal * 100,
}));

export const ageGroupKeys   = ['sem_vinculo', 'com_vinculo'] as const;
export const ageGroupLabels: Record<string, string> = {
	sem_vinculo: 'Sem vínculo formal',
	com_vinculo: 'Com vínculo formal',
};

// ── Por escolaridade ────────────────────────────────────────────────────────────
const escRows = parseCSV(csvEscolaridadeRaw);

const escShort: Record<string, string> = {
	'Médio completo e superior incompleto':    'Médio completo / superior incompleto',
	'Superior completo':                       'Superior completo',
	'Fundamental completo e médio incompleto': 'Fundamental completo / médio incompleto',
	'Sem instrução e fundamental incompleto':  'Sem instrução / fund. incompleto',
	'Mestrado ou doutorado completo':          'Mestrado ou doutorado',
};

export const escolaridadeBarData = [...escRows]
	.sort((a, b) => +b.numero_contemplados_com_vinculo_trabalho_formal - +a.numero_contemplados_com_vinculo_trabalho_formal)
	.map((r) => ({
		label: escShort[r.escolaridade_agregado_rais] ?? r.escolaridade_agregado_rais,
		value: +r.numero_contemplados_com_vinculo_trabalho_formal,
	}));

// Average value paid per formal worker, sorted ascending
export const escolaridadeValorMedioData = [...escRows]
	.map((r) => ({
		label: escShort[r.escolaridade_agregado_rais] ?? r.escolaridade_agregado_rais,
		value: +r.valor_pago_com_vinculo_trabalho_formal / +r.numero_contemplados_com_vinculo_trabalho_formal,
	}))
	.sort((a, b) => a.value - b.value);

// Proportional share of formal workers by education level, sorted ascending
export const escolaridadeProporcionalData = [...escRows]
	.map((r) => ({
		label: escShort[r.escolaridade_agregado_rais] ?? r.escolaridade_agregado_rais,
		value: +r.percentual_numero_contemplados_com_vinculo_no_total_geral * 100,
	}))
	.sort((a, b) => a.value - b.value);

// Grouped comparison: PNAB vs. Brasil (RAIS 2024) by education level
const _raisEscRef: Record<string, number> = {
	'Sem instrução e fundamental incompleto':  7.0626,
	'Fundamental completo e médio incompleto': 11.3631,
	'Médio completo e superior incompleto':    53.3906,
	'Superior completo':                       27.0379,
	'Mestrado ou doutorado completo':           1.1457,
};

const _escOrder = [
	'Mestrado ou doutorado completo',
	'Sem instrução e fundamental incompleto',
	'Fundamental completo e médio incompleto',
	'Superior completo',
	'Médio completo e superior incompleto',
];

const _escLabelAbrev: Record<string, string> = {
	'Sem instrução e fundamental incompleto':  'Sem instrução',
	'Fundamental completo e médio incompleto': 'Fund./méd. incompl.',
	'Médio completo e superior incompleto':    'Médio/sup. incompl.',
	'Superior completo':                       'Superior compl.',
	'Mestrado ou doutorado completo':          'Mestrado/dout.',
};

export const escolaridadeGroupedData = _escOrder.map((esc) => {
	const row = escRows.find((r) => r.escolaridade_agregado_rais === esc)!;
	return {
		label: _escLabelAbrev[esc] ?? esc,
		values: [
			+row.percentual_numero_contemplados_com_vinculo_no_total_geral * 100,
			_raisEscRef[esc],
		],
	};
});

// ── Por região ──────────────────────────────────────────────────────────────────
const regionRows4 = parseCSV(csvRegionRaw);

const regionOrderSec4 = ['Nordeste', 'Sudeste', 'Norte', 'Sul', 'Centro-Oeste'];

export const regionStackedData = regionOrderSec4.map((regiao) => {
	const r = regionRows4.find((d) => d.regiao === regiao)!;
	return {
		label:       regiao,
		sem_vinculo: +r.percentual_contemplados_sem_vinculo_trabalho_formal * 100,
		com_vinculo: +r.percentual_contemplados_com_vinculo_trabalho_formal * 100,
	};
});

export const regionSilhouetteData = regionRows4.map((r) => ({
	region: r.regiao === 'Centro-Oeste' ? 'CentroOeste' : r.regiao,
	value:  +r.numero_contemplados_com_vinculo_trabalho_formal,
}));

// ── Por sexo ────────────────────────────────────────────────────────────────────
const sexoRows = parseCSV(csvSexoRaw);

export const sexoDivergingData = sexoRows.map((r) => ({
	label:    r.Sexo,
	leftPct:  +r.percentual_contemplados_sem_vinculo_trabalho_formal * 100,
	rightPct: +r.percentual_contemplados_com_vinculo_trabalho_formal * 100,
}));

// Share of each sex among those with formal work (for grouped bar comparison)
const _totalComVinculoSexo = sexoRows.reduce((s, r) => s + +r.numero_contemplados_com_vinculo_trabalho_formal, 0);

export const sexoVinculoFormalGroupedData = [
	{
		label: 'PNAB',
		fullLabel: 'Pessoas com vínculo formal de trabalho contempladas no PNAB',
		values: sexoRows.map((r) => (+r.numero_contemplados_com_vinculo_trabalho_formal / _totalComVinculoSexo) * 100),
	},
	{
		label: 'Brasil',
		fullLabel: 'Pessoas com vínculo formal de trabalho no Brasil',
		values: [45.0, 55.0], // Reference: RAIS 2024
	},
];

// ── Por raça/cor ────────────────────────────────────────────────────────────────
const racaCorRows = parseCSV(csvRacaCorRaw).filter(
	(r) => r.raca_cor_desc_description !== 'Não informado'
);

export const racaCorBarData = [...racaCorRows]
	.sort((a, b) => +b.percentual_numero_contemplados_com_vinculo_no_total_geral - +a.percentual_numero_contemplados_com_vinculo_no_total_geral)
	.map((r) => ({
		label: shortRaceLabel(r.raca_cor_desc_description),
		value: +r.percentual_numero_contemplados_com_vinculo_no_total_geral * 100,
	}));

// RAIS 2024 reference: racial composition of Brazil's formal workers
const _raisRacaRef: Record<string, number> = {
	'Amarela':     1.0,
	'Branca':      45.0,
	'Indígena':    0.3,
	'Parda':       41.8,
	'Preta/negra': 7.2,
};

export const racaCorGroupedData = [...racaCorRows]
	.sort((a, b) => +b.percentual_numero_contemplados_com_vinculo_no_total_geral - +a.percentual_numero_contemplados_com_vinculo_no_total_geral)
	.map((r) => {
		const label = shortRaceLabel(r.raca_cor_desc_description);
		return {
			label,
			values: [
				+r.percentual_numero_contemplados_com_vinculo_no_total_geral * 100,
				_raisRacaRef[label] ?? 0,
			],
		};
	});

export const racaCorTreemapData = {
	name:     'root',
	children: racaCorRows.map((r) => ({
		name:  shortRaceLabel(r.raca_cor_desc_description),
		value: +r.percentual_numero_contemplados_com_vinculo_no_total_geral * 100,
	})),
};

export const racaCorTreemapValorData = {
	name:     'root',
	children: racaCorRows.map((r) => ({
		name:  shortRaceLabel(r.raca_cor_desc_description),
		value: +r.percentual_valor_pago_no_total_geral * 100,
	})),
};

// ── Por raça/cor × sexo (HeatMap) ───────────────────────────────────────────────
const racaCorSexoRows = parseCSV(csvRacaCorSexoRaw).filter(
	(r) => r.raca_cor_desc_description !== 'Não informado'
);

const racaDisplayOrder = ['Parda', 'Branca', 'Preta/negra', 'Indígena', 'Amarela'];

export const racaCorSexoHeatmapData = racaDisplayOrder.flatMap((race) => {
	const r = racaCorSexoRows.find((d) => shortRaceLabel(d.raca_cor_desc_description) === race);
	if (!r) return [];
	return [
		{ x: 'Masculino', y: race, value: +r.numero_contemplados_masculino },
		{ x: 'Feminino',  y: race, value: +r.numero_contemplados_feminino  },
	];
});

// ── Por raça/cor × sexo (Vertical Grouped Bar) ──────────────────────────────────
const _racaSexoOrder = ['Amarela', 'Branca', 'Indígena', 'Parda', 'Preta/negra'];
const _racaSexoTotalQty   = racaCorSexoRows.reduce((s, r) => s + +r.numero_contemplados_total, 0);
const _racaSexoTotalValor = racaCorSexoRows.reduce((s, r) => s + +r.valor_pago_total, 0);

export const racaCorSexoGroupedData = _racaSexoOrder.map((race) => {
	const r = racaCorSexoRows.find((d) => shortRaceLabel(d.raca_cor_desc_description) === race)!;
	return {
		label:     race,
		fullLabel: r.raca_cor_desc_description,
		values: [
			(+r.numero_contemplados_feminino / _racaSexoTotalQty)   * 100,
			(+r.valor_pago_feminino          / _racaSexoTotalValor) * 100,
			(+r.numero_contemplados_masculino / _racaSexoTotalQty)  * 100,
			(+r.valor_pago_masculino          / _racaSexoTotalValor) * 100,
		],
	};
});

// ── Por UF ─────────────────────────────────────────────────────────────────────
const ufRows4 = parseCSV(csvUfRaw);

export const ufSilhouetteData = ufRows4.map((r) => ({
	state: r.uf,
	value: +r.numero_contemplados_com_vinculo_trabalho_formal,
}));

export const ufRankingData = [...ufRows4]
	.sort((a, b) => +b.percentual_contemplados_com_vinculo_trabalho_formal - +a.percentual_contemplados_com_vinculo_trabalho_formal)
	.map((r) => ({
		label: r.uf,
		value: +r.percentual_contemplados_com_vinculo_trabalho_formal * 100,
	}));

// ── Por UF × IBGE (comparação formalização PNAB vs. população geral) ─────────────
const ufIbgeRows = parseCSV(csvUfIbgeRaw);

// Shared color pairs for IBGE comparison charts (UF and region).
// light = % pop. geral, main = % PNAB. Sul uses yellow scale.
const _ibgeRegionColors: Record<string, [string, string]> = {
	Nordeste:       ['#f7bf95', '#ea662f'], // orange[1] / orange[2]
	Sudeste:        ['#9fbbe0', '#4271b5'], // blue[1]   / blue[2]
	Norte:          ['#95c0b7', '#317a68'], // teal[1]   / teal[2]
	Sul:            ['#f9e6a1', '#f6c341'], // yellow[1] / yellow[2]
	'Centro-Oeste': ['#d5a6c8', '#a44c7f'], // purple[1] / purple[2]
};
const _ibgeRegionForUF: Record<string, string> = {
	AC: 'Norte',  AM: 'Norte',  AP: 'Norte',  PA: 'Norte',  RO: 'Norte',  RR: 'Norte',  TO: 'Norte',
	AL: 'Nordeste', BA: 'Nordeste', CE: 'Nordeste', MA: 'Nordeste', PB: 'Nordeste',
	PE: 'Nordeste', PI: 'Nordeste', RN: 'Nordeste', SE: 'Nordeste',
	DF: 'Centro-Oeste', GO: 'Centro-Oeste', MS: 'Centro-Oeste', MT: 'Centro-Oeste',
	ES: 'Sudeste', MG: 'Sudeste', RJ: 'Sudeste', SP: 'Sudeste',
	PR: 'Sul', RS: 'Sul', SC: 'Sul',
};

// Total formal labor in Brazil (sum across all UFs) — used to compute each UF's share
const _totalBrazilFormalLabor = ufIbgeRows.reduce((s, r) => s + +r.total_vinculos_a_rais_2024, 0);

// Bar 1 (light): % of UF's formal labor out of Brazil's total formal labor (RAIS 2024)
// Bar 2 (dark):  % of UF's PNAB formal participants out of all PNAB formal participants
export const ufIbgeByRegionData = ['Nordeste', 'Sudeste', 'Norte', 'Sul', 'Centro-Oeste'].flatMap(
	(regiao) => {
		const [lightColor, darkColor] = _ibgeRegionColors[regiao];
		const stateRows = [...ufIbgeRows]
			.filter((r) => _ibgeRegionForUF[r.uf] === regiao)
			.sort((a, b) =>
				(+b.percentual_numero_contemplados_com_vinculo_no_total_geral - +b.total_vinculos_a_rais_2024 / _totalBrazilFormalLabor) -
				(+a.percentual_numero_contemplados_com_vinculo_no_total_geral - +a.total_vinculos_a_rais_2024 / _totalBrazilFormalLabor)
			)
			.map((r) => ({
				label: r.uf,
				values: [
					(+r.total_vinculos_a_rais_2024 / _totalBrazilFormalLabor) * 100,
					+r.percentual_numero_contemplados_com_vinculo_no_total_geral * 100,
				],
				colors: [lightColor, darkColor],
			}));
		return [{ label: regiao, values: [], isSeparator: true as const }, ...stateRows];
	}
);

// Region-level comparison: PNAB formal % vs. general population formal %
// General pop % aggregated from UF IBGE rows; PNAB % from region CSV.
export const regionIbgeComparisonData = ['Nordeste', 'Sudeste', 'Norte', 'Sul', 'Centro-Oeste'].map(
	(regiao) => {
		const r = regionRows4.find((d) => d.regiao === regiao)!;
		const ufSet = ufIbgeRows.filter((u) => _ibgeRegionForUF[u.uf] === regiao);
		const totalFormal = ufSet.reduce((s, u) => s + +u.total_vinculos_a_rais_2024, 0);
		const [lightColor, mainColor] = _ibgeRegionColors[regiao];
		return {
			label: regiao,
			values: [
				(totalFormal / _totalBrazilFormalLabor) * 100,
				+r.percentual_numero_contemplados_com_vinculo_no_total_geral * 100,
			],
			colors: [lightColor, mainColor],
		};
	}
);

export const regionIbgeComparisonLegend = [
	{ label: '% RAIS', color: '#c0c0c0' },
	{ label: '% PNAB', color: '#444444' },
];

export const ufIbgeRegionLegend = [
	{ label: '% RAIS', color: '#c0c0c0' },
	{ label: '% PNAB', color: '#444444' },
];

// ── Por UF × Região (correlação) ────────────────────────────────────────────────
const regionForUF: Record<string, string> = {
	AC: 'Norte',  AM: 'Norte',  AP: 'Norte',  PA: 'Norte',  RO: 'Norte',  RR: 'Norte',  TO: 'Norte',
	AL: 'Nordeste', BA: 'Nordeste', CE: 'Nordeste', MA: 'Nordeste', PB: 'Nordeste',
	PE: 'Nordeste', PI: 'Nordeste', RN: 'Nordeste', SE: 'Nordeste',
	DF: 'Centro-Oeste', GO: 'Centro-Oeste', MS: 'Centro-Oeste', MT: 'Centro-Oeste',
	ES: 'Sudeste', MG: 'Sudeste', RJ: 'Sudeste', SP: 'Sudeste',
	PR: 'Sul', RS: 'Sul', SC: 'Sul',
};

// lighter shade = sem vínculo, darker shade = com vínculo
// shades from colorScales: [0]=lightest … [4]=darkest
const regionColorPairs: Record<string, [string, string]> = {
	Nordeste:       ['#f7bf95', '#ab4723'], // orange [1] / [3]
	Sudeste:        ['#9fbbe0', '#2e4e8a'], // blue   [1] / [3]
	Norte:          ['#95c0b7', '#255c4f'], // teal   [1] / [3]
	Sul:            ['#c3d992', '#5d7920'], // lime   [1] / [3]
	'Centro-Oeste': ['#d5a6c8', '#773561'], // purple [1] / [3]
};

const regionOrderCorr = ['Nordeste', 'Sudeste', 'Norte', 'Sul', 'Centro-Oeste'];

export const ufByRegionGroups = regionOrderCorr.map((regiao) => ({
	regiao,
	colors: regionColorPairs[regiao] as [string, string],
	avgInformal: +regionRows4.find((r) => r.regiao === regiao)!.percentual_contemplados_sem_vinculo_trabalho_formal * 100,
	data: [...ufRows4]
		.filter((r) => regionForUF[r.uf] === regiao)
		.sort((a, b) => +b.percentual_contemplados_sem_vinculo_trabalho_formal - +a.percentual_contemplados_sem_vinculo_trabalho_formal)
		.map((r) => ({
			label:       r.uf,
			sem_vinculo: +r.percentual_contemplados_sem_vinculo_trabalho_formal * 100,
			com_vinculo: +r.percentual_contemplados_com_vinculo_trabalho_formal * 100,
		})),
}));

// ── CBO RAIS — infographic data ───────────────────────────────────────────────
const cboRaisRows = parseCSV(csvCboRaisRaw);

export const cboRaisTop20 = [...cboRaisRows]
	.sort((a, b) => +a[''] - +b[''])
	.slice(0, 20)
	.map((r) => ({
		posicao:       +r[''] + 1,
		descricao:     r.cbo_descricao_rais.toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase()),
		percValor:     +r.percentual_valor * 100,
		percFormatted: `${(+r.percentual_valor * 100).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%`,
	}));

// Pre-computed SVG height (matches CboRaisTable layout constants)
const _FS = 13, _LH = _FS * 1.4, _CW = _FS * 0.55, _DESC_W = 272, _PAD_Y = 10;
function _wrapLines(text: string): number {
	const maxCh = Math.max(1, Math.floor(_DESC_W / _CW));
	const words = text.split(' ');
	let lines = 1, cur = '';
	for (const w of words) {
		const cand = cur ? `${cur} ${w}` : w;
		if (cand.length > maxCh && cur) { lines++; cur = w; } else cur = cand;
	}
	return lines;
}
export const cboRaisTableHeight = cboRaisTop20.reduce((h, e) => {
	const minH = e.posicao <= 3 ? 54 : 42;
	return h + Math.max(minH, _wrapLines(e.descricao) * _LH + _PAD_Y * 2);
}, 40); // 40 = HEADER_H
