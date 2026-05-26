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

// ── Por raça/cor ────────────────────────────────────────────────────────────────
const racaCorRows = parseCSV(csvRacaCorRaw).filter(
	(r) => r.raca_cor_desc_description !== 'Não informado'
);

export const racaCorBarData = [...racaCorRows]
	.sort((a, b) => +b.numero_contemplados_com_vinculo_trabalho_formal - +a.numero_contemplados_com_vinculo_trabalho_formal)
	.map((r) => ({
		label: shortRaceLabel(r.raca_cor_desc_description),
		value: +r.numero_contemplados_com_vinculo_trabalho_formal,
	}));

export const racaCorTreemapData = {
	name:     'root',
	children: racaCorRows.map((r) => ({
		name:  shortRaceLabel(r.raca_cor_desc_description),
		value: +r.numero_contemplados_com_vinculo_trabalho_formal,
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
