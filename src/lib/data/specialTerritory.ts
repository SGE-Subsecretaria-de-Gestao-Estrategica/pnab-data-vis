// Special-territory participation in resource distribution (Section 6).
//
// Source: values_by_special_territory_uf.csv — national (uf-combined) aggregate,
// one row per special-territory type. We compare each territory's share of the
// resources (% do recurso) against its share of the population (% da população),
// which shows whether it is over- or under-represented in the distribution.

import csvRaw from '../../../data/section_1/values_by_special_territory_uf.csv?raw';

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

const SHORT_LABELS: Record<string, string> = {
	'Favela e Comunidade Urbana': 'Favela / Com. Urbana',
	'Agrupamento quilombola': 'Quilombola',
	'Agrupamento indígena': 'Indígena',
};

export interface SpecialTerritory {
	label: string;
	valor: number;       // R$ executado
	percRecurso: number; // % do recurso total
	percPopulacao: number; // % da população
	percAgentes: number; // % dos agentes contemplados
	values: number[];    // [percRecurso, percPopulacao] for the grouped chart
}

export const specialTerritories: SpecialTerritory[] = parseCSV(csvRaw)
	.filter((d) => d.cod_tipo_nome)
	.map((d) => {
		const percRecurso = (+d.perc_valor_transacao || 0) * 100;
		const percPopulacao = (+d.perc_populacao_brasil || 0) * 100;
		const percAgentes = (+d.perc_quantidade_contemplados || 0) * 100;
		return {
			label: SHORT_LABELS[d.cod_tipo_nome] ?? d.cod_tipo_nome,
			valor: +d.valor_transacao || 0,
			percRecurso,
			percPopulacao,
			percAgentes,
			values: [percRecurso, percPopulacao],
		};
	})
	.sort((a, b) => b.percRecurso - a.percRecurso);

export const SPECIAL_SERIES_LABELS = ['% do recurso', '% da população'];

// Total share of resources going to special territories.
export const percRecursoEspecialTotal = specialTerritories.reduce((s, d) => s + d.percRecurso, 0);
