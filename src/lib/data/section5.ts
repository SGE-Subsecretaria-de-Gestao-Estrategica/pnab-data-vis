// Section 5 data — CadÚnico cross-reference

import csvCadunicoRaw      from '../../../data/section_5/aggregate_cadunico_summary.csv?raw';
import csvSexoRaw          from '../../../data/section_5/aggregate_cadunico_profile_summary_by_sexo.csv?raw';
import csvFaixaEtariaRaw   from '../../../data/section_5/aggregate_cadunico_profile_summary_by_faixa_etaria.csv?raw';
import csvFaixaSexoRaw     from '../../../data/section_5/aggregate_cadunico_faixa_etaria_by_sexo.csv?raw';
import csvRendaRaw         from '../../../data/section_5/aggregate_cadunico_by_fx_renda_per_capita.csv?raw';
import csvSituacaoRendaRaw from '../../../data/section_5/aggregate_cadunico_by_situacao_renda.csv?raw';
import csvDomicilioRaw     from '../../../data/section_5/aggregate_cadunico_by_situacao_domicilio.csv?raw';
import csvPorteRaw         from '../../../data/section_5/aggregate_cadunico_by_population_size.csv?raw';
import csvUfRaw            from '../../../data/section_5/aggregate_cadunico_by_uf.csv?raw';
import csvValorGrupoRaw    from '../../../data/section_5/aggregate_cadunico_by_value_group.csv?raw';
import csvBolsaFamiliaRaw  from '../../../data/section_5/aggregate_bolsa_familia_summary.csv?raw';
import csvBpcRaw           from '../../../data/section_5/aggregate_bpc_summary.csv?raw';

// Quoted-CSV aware parser (handles fields like "De R$ 109,01 até R$ 218")
function parseCSVLine(line: string): string[] {
	const result: string[] = [];
	let current = '';
	let inQuotes = false;
	for (let i = 0; i < line.length; i++) {
		const ch = line[i];
		if (ch === '"') { inQuotes = !inQuotes; }
		else if (ch === ',' && !inQuotes) { result.push(current.trim()); current = ''; }
		else { current += ch; }
	}
	result.push(current.trim());
	return result;
}

function parseCSV(text: string): Record<string, string>[] {
	const lines = text.trim().split('\n');
	const headers = parseCSVLine(lines[0]);
	return lines.slice(1)
		.filter((l) => l.trim())
		.map((line) => {
			const values = parseCSVLine(line);
			return Object.fromEntries(headers.map((h, i) => [h, values[i] ?? '']));
		});
}

// ── Summary ────────────────────────────────────────────────────────────────────
const [cadRow] = parseCSV(csvCadunicoRaw);
export const percContempladosCadunico = +cadRow.perc_contemplados_cadunico * 100;
export const qtdContempladosCadunico  = +cadRow.qtd_contemplados_cadunico;
export const qtdDocumentosUnicos      = +cadRow.qtd_documentos_unicos_cadunico;
export const valorRecebidoCadunico    = +cadRow.valor_recebido_cadunico;
export const percValorCadunico        = +cadRow.perc_valor_cadunico * 100;

// ── Sexo ───────────────────────────────────────────────────────────────────────
const sexoRows = parseCSV(csvSexoRaw);
const femRow   = sexoRows.find((r) => r.categoria === 'Feminino')!;
export const percFemCadunico = +femRow.percentual_contemplados_cadunico * 100;

// ── Faixa etária summary ───────────────────────────────────────────────────────
const faixaEtariaRows = parseCSV(csvFaixaEtariaRaw);
const row2554 = faixaEtariaRows.find((r) => r.categoria === '25-54 anos')!;
export const perc2554Cadunico = +row2554.percentual_contemplados_cadunico * 100;

// ── Faixa etária × sexo (HorizontalStackedBarChart) ───────────────────────────
const faixaSexoRows = parseCSV(csvFaixaSexoRaw);
export const faixaEtariaSexoData = faixaSexoRows.map((r) => ({
	label:     r.faixa_etaria,
	feminino:  +r.perc_quantidade_feminino  * 100,
	masculino: +r.perc_quantidade_masculino * 100,
}));
export const FAIXA_SEXO_KEYS   = ['feminino', 'masculino'] as const;
export const FAIXA_SEXO_LABELS: Record<string, string> = {
	feminino:  'Feminino',
	masculino: 'Masculino',
};

// ── Renda per capita (DonutChart) ──────────────────────────────────────────────
const RENDA_LABEL_MAP: Record<string, string> = {
	'De 0 até R$ 109':                          'Até R$109',
	'De R$ 109,01 até R$ 218':                  'R$109–218',
	'De R$ 218,01 até meio salário mínimo':      'R$218–½SM',
	'De meio salário mínimo a um salário mínimo': '½SM–1SM',
	'Superior a um salário mínimo':              'Acima de 1SM',
};
const rendaRows = parseCSV(csvRendaRaw);
export const rendaDonutData = rendaRows.map((r) => ({
	label: RENDA_LABEL_MAP[r.fxRendaPerCapita_desc_cadunico] ?? r.fxRendaPerCapita_desc_cadunico,
	value: +r.soma_quantidade,
}));

// ── Situação de renda (DonutChart) ─────────────────────────────────────────────
const situacaoRendaRows = parseCSV(csvSituacaoRendaRaw);
export const situacaoRendaDonutData = situacaoRendaRows.map((r) => ({
	label: r.situacao_renda_cadunico,
	value: +r.soma_quantidade,
}));

// ── Situação de domicílio ──────────────────────────────────────────────────────
const domicilioRows = parseCSV(csvDomicilioRaw);
const urbanoRow     = domicilioRows.find((r) => r.SITUACAO === 'Urbana')!;
export const percUrbanoCadunico   = +urbanoRow.percentual_quantidade * 100;
export const domicilioTreemapData = {
	name: 'root',
	children: domicilioRows
		.filter((r) => r.SITUACAO !== 'Não informado')
		.map((r) => ({ name: r.SITUACAO, value: +r.soma_quantidade })),
};

// ── Porte populacional ─────────────────────────────────────────────────────────
const PORTE_MAP: Record<string, string> = {
	'1_pequeno_i':  'Pequeno I',
	'2_pequeno_ii': 'Pequeno II',
	'3_medio':      'Médio',
	'4_grande':     'Grande',
};
const porteRows5  = parseCSV(csvPorteRaw);
const pequenoPct  = porteRows5
	.filter((r) => r.porte_populacional === '1_pequeno_i' || r.porte_populacional === '2_pequeno_ii')
	.reduce((acc, r) => acc + +r.percentual_quantidade, 0);
export const percPequenoPorteCadunico = pequenoPct * 100;
export const porteTreemapData5 = {
	name: 'root',
	children: porteRows5.map((r) => ({
		name:  PORTE_MAP[r.porte_populacional] ?? r.porte_populacional,
		value: +r.soma_quantidade,
	})),
};

// ── Por UF — % dos contemplados da UF que estão no CadÚnico ───────────────────
const ufRows5 = parseCSV(csvUfRaw);
export const cadunicoUfData = ufRows5
	.map((r) => ({
		label: r.uf,
		value: (+r.qtd_contemplados_cadunico / +r.qtd_contemplados_total_uf) * 100,
	}))
	.sort((a, b) => b.value - a.value);

// ── Faixa de valor recebido ────────────────────────────────────────────────────
const valorGrupoRows = parseCSV(csvValorGrupoRaw);
export const cadunicoValorData = valorGrupoRows.map((r) => ({
	label: r.faixa_vlr_pago_ju_bbagil,
	value: +r.percentual_quantidade * 100,
}));

// ── Bolsa Família ──────────────────────────────────────────────────────────────
const [bfRow] = parseCSV(csvBolsaFamiliaRaw);
export const percBolsaFamilia  = +bfRow.perc_contemplados_bolsa_familia * 100;
export const valorBolsaFamilia = +bfRow.valor_recebido_bolsa_familia;

// ── BPC ────────────────────────────────────────────────────────────────────────
const [bpcRow] = parseCSV(csvBpcRaw);
export const percBpc  = +bpcRow.perc_contemplados_bpc * 100;
export const valorBpc = +bpcRow.valor_recebido_bpc;
