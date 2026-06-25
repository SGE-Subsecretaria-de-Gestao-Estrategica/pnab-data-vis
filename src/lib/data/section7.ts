// Section 7 data — Distribuição de beneficiários e recursos por tipo de documento.
//
// Three "visões" (níveis de execução), cada uma com totais nacionais divididos
// em duas linhas (CNPJ, CPF):
//   • uf         → estado + municípios combinados (aggregate_execution_by_person_type_uf.csv)
//   • estados    → apenas execução estadual        (..._state.csv)
//   • municipios → apenas execução municipal        (..._municipality.csv)
//
// Não há recorte por região nem por UF para tipo de documento, portanto a
// Seção 7 usa apenas estas três visões.

import csvUfRaw    from '../../../data/section_2/aggregate_execution_by_person_type_uf.csv?raw';
import csvStateRaw from '../../../data/section_2/aggregate_execution_by_person_type_state.csv?raw';
import csvMunRaw   from '../../../data/section_2/aggregate_execution_by_person_type_municipality.csv?raw';

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

export type DocVisao = 'uf' | 'estados' | 'municipios';

export interface DocType {
	valor: number; // valor executado (R$)
	percValor: number; // % do valor executado (0–100)
	contemplados: number;
	percContemplados: number; // % dos contemplados (0–100)
}

export interface DocVisaoData {
	cpf: DocType;
	cnpj: DocType;
	totalValor: number;
	totalContemplados: number;
}

function rowFor(raw: Record<string, string>): DocType {
	return {
		valor: +raw.valor_executado_rs || 0,
		percValor: (+raw.perc_valor_executado || 0) * 100,
		contemplados: +raw.qtde_contemplados || 0,
		percContemplados: (+raw.perc_qtde_contemplados || 0) * 100,
	};
}

function build(raw: string): DocVisaoData {
	const rows = parseCSV(raw);
	const byDoc = new Map(rows.map((r) => [r.tipo_documento, r]));
	const cpf = rowFor(byDoc.get('CPF') ?? {});
	const cnpj = rowFor(byDoc.get('CNPJ') ?? {});
	return {
		cpf,
		cnpj,
		totalValor: cpf.valor + cnpj.valor,
		totalContemplados: cpf.contemplados + cnpj.contemplados,
	};
}

export const docByVisao: Record<DocVisao, DocVisaoData> = {
	uf: build(csvUfRaw),
	estados: build(csvStateRaw),
	municipios: build(csvMunRaw),
};

// ── Stacked-bar input (100% empilhado: Recursos vs Contemplados) ──────────────
export const docStackedKeys = ['cpf', 'cnpj'] as const;
export const docStackedLabels: Record<string, string> = {
	cpf: 'CPF (pessoa física)',
	cnpj: 'CNPJ (pessoa jurídica)',
};

export function stackedData(d: DocVisaoData) {
	return [
		{ label: 'Recursos executados', cpf: d.cpf.percValor, cnpj: d.cnpj.percValor },
		{ label: 'Contemplados', cpf: d.cpf.percContemplados, cnpj: d.cnpj.percContemplados },
	];
}
