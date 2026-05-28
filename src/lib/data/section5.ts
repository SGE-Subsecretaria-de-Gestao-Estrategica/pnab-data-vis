// Section 5 data — CadÚnico cross-reference

import csvCadunicoRaw from '../../../data/section_5/aggregate_cadunico_summary.csv?raw';

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

// ── aggregate_cadunico_summary.csv ────────────────────────────────────────────
// Columns: perc_contemplados_cadunico, qtd_contemplados_cadunico,
//          qtd_documentos_unicos_cadunico, valor_recebido_cadunico
const [cadRow] = parseCSV(csvCadunicoRaw);

export const percContempladosCadunico = +cadRow.perc_contemplados_cadunico * 100;
export const qtdContempladosCadunico  = +cadRow.qtd_contemplados_cadunico;
export const qtdDocumentosUnicos      = +cadRow.qtd_documentos_unicos_cadunico;
export const valorRecebidoCadunico    = +cadRow.valor_recebido_cadunico;
