// Metadata for the anonymised microdata table (/dados-abertos).
// The `name` values are the exact Parquet column names — used verbatim (and
// whitelisted) when building SQL, so never let user input reach a column name.

export type ColType = 'text' | 'number';

export interface ColumnMeta {
	name: string;
	label: string;
	group: string;
	type: ColType;
}

// Source datasets, in display order. Keys match the `group` on each column.
export const GROUPS: { key: string; label: string }[] = [
	{ key: 'bbagil', label: 'Pagamento (Aldir Blanc)' },
	{ key: 'receita_cpf', label: 'Pessoa Física (Receita Federal)' },
	{ key: 'receita_cnpj', label: 'Pessoa Jurídica (Receita Federal)' },
	{ key: 'rais', label: 'Vínculo formal (RAIS)' },
	{ key: 'inss', label: 'Relação de trabalho (INSS)' },
	{ key: 'cnefe', label: 'Endereço (CNEFE)' },
	{ key: 'cadunico', label: 'Perfil socioeconômico (CadÚnico)' },
	{ key: 'ibge', label: 'Município (IBGE)' }
];

export const COLUMNS: ColumnMeta[] = [
	// ── Pagamento (Aldir Blanc / BB Ágil) ──
	{ name: 'uf_bbagil', label: 'UF', group: 'bbagil', type: 'text' },
	{ name: 'cod_ibge_bbagil', label: 'Código IBGE do município', group: 'bbagil', type: 'text' },
	{ name: 'nome_ente_bbagil', label: 'Ente federado', group: 'bbagil', type: 'text' },
	{ name: 'documento_beneficiario_bbagil', label: 'Documento (anonimizado)', group: 'bbagil', type: 'text' },
	{ name: 'tipo_ente_bbagil', label: 'Tipo de ente', group: 'bbagil', type: 'text' },
	{ name: 'tipo_documento_bbagil', label: 'Tipo de documento', group: 'bbagil', type: 'text' },
	{ name: 'valor_transacao_total_bbagil', label: 'Valor total (R$)', group: 'bbagil', type: 'number' },
	{ name: 'faixa_vlr_pago_bbagil', label: 'Faixa de valor pago', group: 'bbagil', type: 'text' },

	// ── Pessoa Física (Receita Federal) ──
	{ name: 'residenteexterior_receita_cpf', label: 'Residente no exterior', group: 'receita_cpf', type: 'text' },
	{ name: 'sexo_receita_cpf', label: 'Sexo', group: 'receita_cpf', type: 'text' },
	{ name: 'estrangeiro_receita_cpf', label: 'Estrangeiro', group: 'receita_cpf', type: 'text' },
	{ name: 'nomenaturezaocupacao_receita_cpf', label: 'Natureza da ocupação', group: 'receita_cpf', type: 'text' },
	{ name: 'nomeocupacaoprincipal_receita_cpf', label: 'Ocupação principal', group: 'receita_cpf', type: 'text' },
	{ name: 'idade_receita_cpf', label: 'Idade', group: 'receita_cpf', type: 'number' },
	{ name: 'faixa_etaria_receita_cpf', label: 'Faixa etária', group: 'receita_cpf', type: 'text' },
	{ name: 'codigomunicipio_receita_cpf', label: 'Código do município (CPF)', group: 'receita_cpf', type: 'text' },
	{ name: 'flag_cpf_mei_receita_cpf', label: 'MEI (CPF)', group: 'receita_cpf', type: 'text' },

	// ── Pessoa Jurídica (Receita Federal) ──
	{ name: 'cnaeprincipal_receita_cnpj', label: 'CNAE principal', group: 'receita_cnpj', type: 'text' },
	{ name: 'cnaesecundarias_receita_cnpj', label: 'CNAEs secundárias', group: 'receita_cnpj', type: 'text' },
	{ name: 'naturezajuridica_receita_cnpj', label: 'Natureza jurídica', group: 'receita_cnpj', type: 'text' },
	{ name: 'porte_receita_cnpj', label: 'Porte da empresa', group: 'receita_cnpj', type: 'text' },
	{ name: 'cnpj_optante_mei_receita_cnpj', label: 'Optante MEI (CNPJ)', group: 'receita_cnpj', type: 'text' },
	{ name: 'flag_cnae_cultural_receita_cnpj', label: 'CNAE cultural', group: 'receita_cnpj', type: 'text' },
	{ name: 'codigo_municipio_receita_cnpj', label: 'Código do município (CNPJ)', group: 'receita_cnpj', type: 'text' },
	{ name: 'cod_cnae_principal_receita_cnpj', label: 'Código CNAE principal', group: 'receita_cnpj', type: 'text' },
	{ name: 'descr_cnae_principal_receita_cnpj', label: 'Descrição CNAE principal', group: 'receita_cnpj', type: 'text' },
	{ name: 'naturezajuridica_agrupada_receita_cnpj', label: 'Natureza jurídica (agrupada)', group: 'receita_cnpj', type: 'text' },
	{ name: 'flag_cnae_educacao_receita_cnpj', label: 'CNAE educação', group: 'receita_cnpj', type: 'text' },
	{ name: 'flag_cnae_audiovisual_receita_cnpj', label: 'CNAE audiovisual', group: 'receita_cnpj', type: 'text' },

	// ── Vínculo formal (RAIS) ──
	{ name: 'raca_cor_desc_description_rais', label: 'Raça/cor', group: 'rais', type: 'text' },
	{ name: 'escolaridade_description_rais', label: 'Escolaridade', group: 'rais', type: 'text' },
	{ name: 'escolaridade_agregado_rais', label: 'Escolaridade (agregada)', group: 'rais', type: 'text' },
	{ name: 'tipo_deficiencia_description_rais', label: 'Tipo de deficiência', group: 'rais', type: 'text' },
	{ name: 'indicador_pcd_rais', label: 'Pessoa com deficiência', group: 'rais', type: 'text' },
	{ name: 'tipo_vinculo_description_rais', label: 'Tipo de vínculo', group: 'rais', type: 'text' },
	{ name: 'tipo_vinculo_agregado_rais', label: 'Tipo de vínculo (agregado)', group: 'rais', type: 'text' },
	{ name: 'cbo_2002_ocupacao_codigo_rais', label: 'Código CBO 2002', group: 'rais', type: 'text' },
	{ name: 'vinculo_ativo_2024_rais', label: 'Vínculo ativo em 2024', group: 'rais', type: 'text' },
	{ name: 'flag_cbo_cultural_rais', label: 'CBO cultural (RAIS)', group: 'rais', type: 'text' },
	{ name: 'faixa_salarial_rais', label: 'Faixa salarial', group: 'rais', type: 'text' },

	// ── Relação de trabalho (INSS) ──
	{ name: 'cbo_codigo_rel_trabalhista_inss', label: 'Código CBO (INSS)', group: 'inss', type: 'text' },
	{ name: 'cbo_descricao_rel_trabalhista_inss', label: 'Descrição CBO (INSS)', group: 'inss', type: 'text' },
	{ name: 'flag_cbo_cultural_rel_trabalhista_inss', label: 'CBO cultural (INSS)', group: 'inss', type: 'text' },

	// ── Endereço (CNEFE) ──
	{ name: 'situacao_cnfe', label: 'Situação (CNEFE)', group: 'cnefe', type: 'text' },
	{ name: 'cod_situacao_nome_cnefe', label: 'Situação do endereço', group: 'cnefe', type: 'text' },
	{ name: 'cod_tipo_nome_cnefe', label: 'Tipo do endereço', group: 'cnefe', type: 'text' },

	// ── Perfil socioeconômico (CadÚnico) ──
	{ name: 'pessoacadastrada_cadunico', label: 'Pessoa cadastrada', group: 'cadunico', type: 'text' },
	{ name: 'familiabeneficiariapbf_cadunico', label: 'Família beneficiária do PBF', group: 'cadunico', type: 'text' },
	{ name: 'faixarendafamiliartotal_descricao_cadunico', label: 'Faixa de renda familiar total', group: 'cadunico', type: 'text' },
	{ name: 'caracteristicaslocaldomicilio_descricao_cadunico', label: 'Características do domicílio', group: 'cadunico', type: 'text' },
	{ name: 'faixarendafamiliarpercapita_descricao_cadunico', label: 'Faixa de renda per capita', group: 'cadunico', type: 'text' },
	{ name: 'situacao_renda_cadunico', label: 'Situação de renda', group: 'cadunico', type: 'text' },
	{ name: 'pertence_bpc', label: 'Pertence ao BPC', group: 'cadunico', type: 'text' },

	// ── Município (IBGE) ──
	{ name: 'populacao_ibge', label: 'População do município', group: 'ibge', type: 'number' },
	{ name: 'flag_capital_ibge', label: 'Capital', group: 'ibge', type: 'text' },
	{ name: 'porte_populacional_ibge', label: 'Porte populacional', group: 'ibge', type: 'text' },
	{ name: 'nome_macrorregiao_ibge', label: 'Macrorregião', group: 'ibge', type: 'text' },
	{ name: 'categoria_municipio_ibge', label: 'Categoria do município', group: 'ibge', type: 'text' },
	{ name: 'local_residencia_contemplados_ibge', label: 'Local de residência', group: 'ibge', type: 'text' }
];

// Columns shown by default (60 columns is too many to open with).
export const DEFAULT_VISIBLE = [
	'uf_bbagil',
	'nome_ente_bbagil',
	'tipo_documento_bbagil',
	'valor_transacao_total_bbagil',
	'faixa_vlr_pago_bbagil',
	'sexo_receita_cpf',
	'faixa_etaria_receita_cpf',
	'naturezajuridica_agrupada_receita_cnpj'
];

export const COLUMN_BY_NAME: Record<string, ColumnMeta> = Object.fromEntries(
	COLUMNS.map((c) => [c.name, c])
);

// Whitelist guard: only column names we know about may appear in SQL.
export function isKnownColumn(name: string): boolean {
	return Object.prototype.hasOwnProperty.call(COLUMN_BY_NAME, name);
}
