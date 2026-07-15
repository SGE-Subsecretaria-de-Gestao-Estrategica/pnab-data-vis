<script lang="ts">
	import SiteHeaderDados from '$lib/components/SiteHeaderDados.svelte';
	import DataTable from '$lib/dadosAbertos/DataTable.svelte';
</script>

<svelte:head>
	<title>PNAB — Dados abertos</title>
</svelte:head>

<main>
	<SiteHeaderDados />

	<div class="doc-bg">
		<div class="aba-dados-abertos">
			<div class="intro-header">

				<div class="context-box">
					<h3>Sobre a pesquisa</h3>
					<p>
						O estudo analisa o primeiro ciclo da PNAB (Lei nº 14.399/2022), implementado entre 2023 e
						2025, a partir de três eixos: distribuição territorial dos recursos, perfil dos agentes
						culturais contemplados e ações fomentadas. A base consolidada reúne
						<strong>167.817 agentes</strong> distribuídos por <strong>5.125 entes federativos</strong>
						(26 estados, o Distrito Federal e 5.098 municípios). Os dados têm origem nas transações
						financeiras registradas no BB Gestão Ágil e foram enriquecidos com informações da Receita
						Federal, CadÚnico, RAIS e IBGE.
					</p>
					<h3>Transparência e Privacidade</h3>
					<p>
						Alinhada às
						<a href="https://www.gov.br/governodigital/pt-br/dados-abertos" target="_blank" rel="noreferrer"
							>diretrizes de dados abertos</a
						>
						e à <strong>Lei de Acesso à Informação (LAI)</strong>, esta página garante o acesso
						público e irrestrito aos dados utilizados na avaliação dos resultados da política. Em
						conformidade com a <strong>Lei Geral de Proteção de Dados Pessoais (LGPD)</strong>, a base
						de microdados passou por um processo de anonimização. Identificadores diretos (como nomes
						e documentos pessoais) foram suprimidos, assegurando que o escrutínio público seja seguro
						e focado na avaliação do impacto territorial e social dos recursos. A disponibilização dos
						dados — tanto nas visualizações interativas quanto para download em formato aberto —
						fomenta a participação cidadã e estimula a produção de pesquisas, reportagens e
						indicadores sobre o alcance da política cultural no Brasil.
					</p>

					<p>
						<strong>Repositório oficial:</strong> Este material também está disponível no repositório
						da Subsecretaria de Gestão Estratégica (SGE) no GitHub:
						<a
							href="https://github.com/SGE-Subsecretaria-de-Gestao-Estrategica/dados-abertos-pnab-ciclo1"
							target="_blank"
							rel="noreferrer">dados-abertos-pnab-ciclo1</a
						>.
					</p>
				</div>

				<div class="sections-container">
					<details id="acc-obtencao" class="custom-accordion">
						<summary>Obtenção e Tratamento dos Dados</summary>
						<div class="accordion-body">
							<p>
								A metodologia foi estruturada em etapas complementares, organizadas a partir dos três
								eixos analíticos da pesquisa: distribuição territorial dos recursos, perfil dos
								agentes culturais contemplados e ações culturais fomentadas. A extração, a validação e
								o tratamento dos dados deram suporte à análise territorial, enquanto o enriquecimento
								da base permitiu caracterizar os perfis. Para a análise das ações, foi necessário
								categorizar as despesas, como detalhado a seguir.
							</p>
							<h3>1. Extração, validação e tratamento dos dados</h3>
							<ul>
								<li>
									<strong>Fonte principal:</strong> BB Gestão Ágil, acessado via API no âmbito de Acordo
									de Cooperação Técnica entre o Banco do Brasil e o Ministério da Cultura.
								</li>
								<li>
									<strong>Período:</strong> movimentações até 31 de dezembro de 2025 – data limite para
									movimentação dos recursos do primeiro ciclo da Aldir Blanc –, incluindo tanto dados dos
									extratos quanto das ‘subtransações’ associadas. A extração completa foi finalizada em 24
									de abril de 2026.
								</li>
								<li>
									<strong>Critérios de inclusão:</strong> apenas registros com destinatário identificável
									(CPF ou CNPJ) e natureza de crédito. Estornos, duplicidades e transações residuais foram
									removidos.
								</li>
								<li>
									<strong>Filtros aplicados:</strong> valor igual ou superior a R$ 375,00; idade do beneficiário
									igual ou superior a 16 anos; documentos com situação válida na Receita Federal.
								</li>
								<li>
									<strong>Validação:</strong> comparação dos valores movimentados com os saldos das contas
									dos entes, obtendo diferenças residuais (mediana inferior a 1%).
								</li>
								<li>
									<strong>Definição de contemplado:</strong> documento (CPF ou CNPJ) que recebeu recurso de
									um ente federativo. Um mesmo agente pode constar mais de uma vez na base caso tenha recebido
									de entes diferentes.
								</li>
							</ul>

							<h3>2. Enriquecimento dos dados</h3>
							<p>
								O enriquecimento foi feito por meio de cruzamentos com bases administrativas acessadas
								via Conecta Gov e acordos de cooperação:
							</p>
							<ul>
								<li><strong>Receita Federal:</strong> qualificação cadastral de pessoas físicas e jurídicas.</li>
								<li><strong>CadÚnico (MDS):</strong> indicadores socioeconômicos e faixas de renda.</li>
								<li><strong>RAIS (MTE/INSS):</strong> vínculos formais de trabalho, ocupação e escolaridade.</li>
								<li><strong>IBGE (SIDRA e CNEFE):</strong> dados territoriais, tipologia urbana e localização.</li>
							</ul>
							<p>
								<em
									>*Nota: As bases têm temporalidades distintas. Dados da Receita Federal e do CadÚnico
									refletem a informação mais recente disponível no momento da extração (maio/2026). A
									RAIS é anual, abrangendo 2022 a 2024. Essas diferenças devem ser consideradas na
									interpretação das variáveis.</em
								>
							</p>

							<p>
								O resultado do processo é uma <strong>única tabela enriquecida</strong>, que consolida
								todas as variáveis disponíveis para os agentes contemplados. O detalhamento completo de
								cada variável (nome, descrição, tipo e fonte) está no <strong>Dicionário de Dados</strong
								>, disponível na seção seguinte.
							</p>

							<h3>3. Categorização das despesas (análise das ações culturais)</h3>
							<p>
								Para a análise das ações culturais fomentadas, foi necessário categorizar as despesas
								registradas no BB Gestão Ágil. Diante do preenchimento parcial dos campos, adotou-se
								uma combinação de harmonização dos registros (alinhamento a domínios culturais) e
								inferência estatística. A estimação foi aplicada apenas aos municípios, utilizando
								pós-estratificação e calibração de pesos, com porte populacional, região geográfica e
								natureza jurídica (PF/PJ) como variáveis estruturantes. A variabilidade das estimativas
								foi obtida por meio do método Bootstrap, permitindo a construção de intervalos de
								confiança de 95%.
							</p>
							<p>
								<strong>Importante:</strong> essa etapa foi utilizada exclusivamente no estudo das ações
								culturais e <strong>não interfere nos dados de agentes disponibilizados nesta página</strong
								>. Os microdados para download referem-se à tabela enriquecida de contemplados, sem
								qualquer modificação decorrente da categorização de despesas.
							</p>
						</div>
					</details>

					<details id="acc-dicionario" class="custom-accordion">
						<summary>Dicionário de Dados</summary>
						<div class="accordion-body">
							<p>
								Confira abaixo o significado e a origem de todas as variáveis da base consolidada dos
								agentes culturais contemplados no Ciclo I da PNAB.
							</p>

							<h3>Banco do Brasil (BB Gestão Ágil)</h3>
							<p><em>Dados originais das transações financeiras e identificação dos beneficiários e entes pagadores.</em></p>
							<div class="table-x">
								<table>
									<thead>
										<tr><th>Variável</th><th>Descrição</th></tr>
									</thead>
									<tbody>
										<tr><td><code>uf_bbagil</code></td><td>Unidade da Federação do ente pagador.</td></tr>
										<tr><td><code>cod_ibge_bbagil</code></td><td>Código IBGE do ente pagador.</td></tr>
										<tr><td><code>nome_ente_bbagil</code></td><td>Nome do ente pagador.</td></tr>
										<tr><td><code>documento_beneficiario_bbagil</code></td><td>CPF anonimizado ou CNPJ do beneficiário do pagamento.</td></tr>
										<tr><td><code>tipo_ente_bbagil</code></td><td>Tipo do ente pagador (Estado ou Município).</td></tr>
										<tr><td><code>tipo_documento_bbagil</code></td><td>Tipo do documento do beneficiário (CPF ou CNPJ).</td></tr>
										<tr><td><code>valor_transacao_total_bbagil</code></td><td>Valor total recebido pelo beneficiário (em reais).</td></tr>
										<tr><td><code>faixa_vlr_pago_bbagil</code></td><td>Faixa de valor total recebido.</td></tr>
									</tbody>
								</table>
							</div>

							<h3>Receita Federal do Brasil</h3>
							<p><em>Dados cadastrais de Pessoas Físicas (CPF) e Pessoas Jurídicas (CNPJ).</em></p>

							<h4>Pessoa Física (CPF)</h4>
							<div class="table-x">
								<table>
									<thead>
										<tr><th>Variável</th><th>Descrição</th></tr>
									</thead>
									<tbody>
										<tr><td><code>residenteexterior_receita_cpf</code></td><td>Indica se a pessoa física é residente no exterior.</td></tr>
										<tr><td><code>sexo_receita_cpf</code></td><td>Sexo cadastrado da pessoa física.</td></tr>
										<tr><td><code>estrangeiro_receita_cpf</code></td><td>Indica se a pessoa física é estrangeira.</td></tr>
										<tr><td><code>nomenaturezaocupacao_receita_cpf</code></td><td>Natureza da ocupação cadastrada da pessoa física.</td></tr>
										<tr><td><code>nomeocupacaoprincipal_receita_cpf</code></td><td>Ocupação principal cadastrada da pessoa física.</td></tr>
										<tr><td><code>idade_receita_cpf</code></td><td>Idade da pessoa física.</td></tr>
										<tr><td><code>faixa_etaria_receita_cpf</code></td><td>Faixa etária da pessoa física.</td></tr>
										<tr><td><code>codigomunicipio_receita_cpf</code></td><td>Código IBGE do município de residência da pessoa física.</td></tr>
										<tr><td><code>flag_cpf_mei_receita_cpf</code></td><td>Indica se o CPF está associado a um Microempreendedor Individual (MEI).</td></tr>
									</tbody>
								</table>
							</div>

							<h4>Pessoa Jurídica (CNPJ)</h4>
							<div class="table-x">
								<table>
									<thead>
										<tr><th>Variável</th><th>Descrição</th></tr>
									</thead>
									<tbody>
										<tr><td><code>cnaeprincipal_receita_cnpj</code></td><td>Descrição do CNAE principal da empresa.</td></tr>
										<tr><td><code>cnaesecundarias_receita_cnpj</code></td><td>Lista dos CNAEs secundários da empresa.</td></tr>
										<tr><td><code>naturezajuridica_receita_cnpj</code></td><td>Natureza jurídica da empresa.</td></tr>
										<tr><td><code>porte_receita_cnpj</code></td><td>Porte da empresa.</td></tr>
										<tr><td><code>cnpj_optante_mei_receita_cnpj</code></td><td>Indica se o CNPJ é optante pelo MEI.</td></tr>
										<tr><td><code>flag_cnae_cultural_receita_cnpj</code></td><td>Indica se o CNAE principal pertence ao setor cultural.</td></tr>
										<tr><td><code>codigo_municipio_receita_cnpj</code></td><td>Código IBGE do município da empresa.</td></tr>
										<tr><td><code>cod_cnae_principal_receita_cnpj</code></td><td>Código do CNAE principal.</td></tr>
										<tr><td><code>descr_cnae_principal_receita_cnpj</code></td><td>Descrição do CNAE principal.</td></tr>
										<tr><td><code>naturezajuridica_agrupada_receita_cnpj</code></td><td>Agrupamento simplificado da natureza jurídica.</td></tr>
										<tr><td><code>flag_cnae_educacao_receita_cnpj</code></td><td>Indica se o CNAE principal pertence ao setor de educação.</td></tr>
										<tr><td><code>flag_cnae_audiovisual_receita_cnpj</code></td><td>Indica se o CNAE principal pertence ao setor audiovisual.</td></tr>
									</tbody>
								</table>
							</div>

							<h3>RAIS e Relações Trabalhistas (MTE / INSS)</h3>
							<p><em>Dados de vínculos formais de emprego, ocupações e perfil do trabalhador.</em></p>
							<div class="table-x">
								<table>
									<thead>
										<tr><th>Variável</th><th>Descrição</th></tr>
									</thead>
									<tbody>
										<tr><td><code>raca_cor_desc_description_rais</code></td><td>Raça/cor do trabalhador.</td></tr>
										<tr><td><code>escolaridade_description_rais</code></td><td>Escolaridade detalhada.</td></tr>
										<tr><td><code>escolaridade_agregado_rais</code></td><td>Escolaridade agrupada.</td></tr>
										<tr><td><code>tipo_deficiencia_description_rais</code></td><td>Tipo de deficiência do trabalhador.</td></tr>
										<tr><td><code>indicador_pcd_rais</code></td><td>Indica se o trabalhador possui deficiência (0 = não; 1 = sim).</td></tr>
										<tr><td><code>tipo_vinculo_description_rais</code></td><td>Tipo de vínculo empregatício.</td></tr>
										<tr><td><code>tipo_vinculo_agregado_rais</code></td><td>Agrupamento do tipo de vínculo empregatício.</td></tr>
										<tr><td><code>cbo_2002_ocupacao_codigo_rais</code></td><td>Código CBO da ocupação.</td></tr>
										<tr><td><code>vinculo_ativo_2024_rais</code></td><td>Indica se havia vínculo ativo em 2024 na RAIS.</td></tr>
										<tr><td><code>flag_cbo_cultural_rais</code></td><td>Indica se a ocupação pertence ao setor cultural.</td></tr>
										<tr><td><code>faixa_salarial_rais</code></td><td>Faixa salarial do trabalhador.</td></tr>
										<tr><td><code>cbo_codigo_rel_trabalhista_inss</code></td><td>Código CBO do vínculo registrado no INSS.</td></tr>
										<tr><td><code>cbo_descricao_rel_trabalhista_inss</code></td><td>Descrição da ocupação do vínculo registrado no INSS.</td></tr>
										<tr><td><code>flag_cbo_cultural_rel_trabalhista_inss</code></td><td>Indica se a ocupação registrada no INSS pertence ao setor cultural.</td></tr>
									</tbody>
								</table>
							</div>

							<h3>Cadastro Único (CadÚnico / MDS)</h3>
							<p><em>Dados socioeconômicos e de participação em programas sociais.</em></p>
							<div class="table-x">
								<table>
									<thead>
										<tr><th>Variável</th><th>Descrição</th></tr>
									</thead>
									<tbody>
										<tr><td><code>pessoacadastrada_cadunico</code></td><td>Indica se a pessoa está cadastrada no CadÚnico.</td></tr>
										<tr><td><code>familiabeneficiariapbf_cadunico</code></td><td>Indica se pertence a família beneficiária do Programa Bolsa Família.</td></tr>
										<tr><td><code>faixarendafamiliartotal_descricao_cadunico</code></td><td>Faixa da renda familiar total.</td></tr>
										<tr><td><code>caracteristicaslocaldomicilio_descricao_cadunico</code></td><td>Característica do local do domicílio.</td></tr>
										<tr><td><code>faixarendafamiliarpercapita_descricao_cadunico</code></td><td>Faixa da renda familiar per capita.</td></tr>
										<tr><td><code>situacao_renda_cadunico</code></td><td>Classificação da situação de renda familiar.</td></tr>
										<tr><td><code>pertence_bpc</code></td><td>Indica se a pessoa pertence ao público do Benefício de Prestação Continuada (BPC).</td></tr>
									</tbody>
								</table>
							</div>

							<h3>IBGE (CNEFE e Bases Territoriais)</h3>
							<p><em>Características geográficas, tipologia urbana e porte populacional.</em></p>
							<div class="table-x">
								<table>
									<thead>
										<tr><th>Variável</th><th>Descrição</th></tr>
									</thead>
									<tbody>
										<tr><td><code>situacao_cnfe</code></td><td>Classificação da localização do domicílio no CNEFE (urbana/rural).</td></tr>
										<tr><td><code>cod_situacao_nome_cnefe</code></td><td>Descrição da situação do domicílio.</td></tr>
										<tr><td><code>cod_tipo_nome_cnefe</code></td><td>Tipo de aglomerado/subnormalidade do domicílio.</td></tr>
										<tr><td><code>populacao_ibge</code></td><td>População do ente federativo.</td></tr>
										<tr><td><code>flag_capital_ibge</code></td><td>Indica se o município é capital estadual (True/False).</td></tr>
										<tr><td><code>porte_populacional_ibge</code></td><td>Classificação do porte populacional do município ("-99" para entes estaduais).</td></tr>
										<tr><td><code>nome_macrorregiao_ibge</code></td><td>Macrorregião do Brasil à qual pertence o ente.</td></tr>
										<tr><td><code>categoria_municipio_ibge</code></td><td>Categoria do município (capital, metropolitano, interior etc.).</td></tr>
										<tr><td><code>local_residencia_contemplados_ibge</code></td><td>Classificação do local de residência do contemplado segundo a tipologia do município.</td></tr>
									</tbody>
								</table>
							</div>

							<p style="margin-top: 15px;">
								<em
									>Nota: Todas as variáveis que poderiam permitir a identificação direta de pessoas
									físicas foram anonimizadas ou agrupadas, em conformidade com a LGPD.</em
								>
							</p>
						</div>
					</details>

					<details id="acc-citar" class="custom-accordion">
						<summary>Como citar a utilização dos dados disponibilizados</summary>
						<div class="accordion-body">
							<p>
								Estes dados são <strong>públicos e abertos</strong>. Você é livre para compartilhar,
								analisar, cruzar e utilizar os dados para qualquer finalidade acadêmica, jornalística
								ou cidadã, desde que a fonte seja obrigatoriamente citada.
							</p>

							<div class="citation-box">
								<strong>Formato sugerido para citação:</strong><br /><br />
								<em
									>Ministério da Cultura / Subsecretaria de Gestão Estratégica (SGE/MinC). Dados
									Abertos do Ciclo I da Política Nacional Aldir Blanc (PNAB) - Base Consolidada de
									Agentes Contemplados. Disponível no Sistema Nacional de Informações e Indicadores
									Culturais (SNIIC). Acesso em: [Sua Data de Acesso].</em
								>
							</div>
						</div>
					</details>

					<!-- <details id="acc-ciclo2" class="custom-accordion">
						<summary>Perspectivas para o Ciclo II da PNAB</summary>
						<div class="accordion-body">
							<p>
								Um dos desafios enfrentados na análise do Ciclo I foi a ausência de preenchimento
								padronizado e a incompletude das categorias de despesas no sistema BB Ágil, o que
								exigiu o uso de técnicas de inferência estatística — como pós-estratificação e o
								Bootstrap descritos na metodologia da pesquisa.
							</p>

							<p>
								Para mitigar esse problema e aprimorar a governança da política, o
								<strong>Ministério da Cultura (MinC)</strong> orienta, no âmbito do
								<strong>Sistema Nacional de Informações e Indicadores Culturais (SNIIC)</strong>, que
								os entes federativos utilizem um
								<strong
									><a
										href="https://github.com/SGE-Subsecretaria-de-Gestao-Estrategica/aldir-blanc-ciclo2"
										target="_blank"
										rel="noreferrer">padrão de dados para o Ciclo II da PNAB</a
									></strong
								>. A adoção de uma taxonomia e de campos obrigatórios harmonizados permitirá o
								monitoramento em tempo real, dispensará estimativas estatísticas secundárias e
								garantirá maior precisão na avaliação do impacto do fomento cultural no Brasil.
							</p>

							<p>
								Saiba mais sobre o padrão de dados e a iniciativa
								<a
									href="https://github.com/SGE-Subsecretaria-de-Gestao-Estrategica/aldir-blanc-ciclo2"
									target="_blank"
									rel="noreferrer">neste link</a
								>.
							</p>
						</div>
					</details> -->
				</div>
			</div>

			<section class="table-section">
				<h3>Explore a base de dados</h3>
				<p class="table-intro">
					Consulte a tabela enriquecida completa dos agentes contemplados. Use a busca, os filtros
					por coluna e a ordenação; escolha quais variáveis exibir em <strong>Colunas</strong>.
					Consulte o significado de cada campo no <strong>Dicionário de Dados</strong> acima.
				</p>
				<DataTable />
			</section>
		</div>
	</div>
</main>

<style>
	main {
		width: 100%;
		min-height: 100vh;
		background: #ffffff;
	}

	/* ── conteúdo (card sobre fundo claro) ── */
	.doc-bg {
		background-color: #f4f4f9;
		padding: 40px 20px;
	}
	.aba-dados-abertos {
		background-color: #ffffff;
		max-width: 1200px;
		margin: 0 auto;
		padding: 40px;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
		color: #333;
		line-height: 1.6;
	}

	h3 {
		color: #1f2937;
		margin-top: 25px;
		margin-bottom: 15px;
		font-size: 1.2em;
	}
	h4 {
		color: #1f2937;
		margin-top: 18px;
		margin-bottom: 10px;
		font-size: 1.02em;
	}

	.context-box {
		padding: 20px;
		border-radius: 4px 8px 8px 4px;
		margin-bottom: 30px;
	}
	.context-box p {
		margin-top: 0;
		margin-bottom: 10px;
	}
	.context-box p:last-child {
		margin-bottom: 0;
	}
	.context-box h3 {
		margin-top: 20px;
	}

	.sections-container {
		display: flex;
		flex-direction: column;
		gap: 15px;
		margin-bottom: 40px;
	}

	.custom-accordion {
		border: 1px solid #e5e7eb;
		border-radius: 8px;
		background-color: #fff;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
		scroll-margin-top: 1rem;
	}
	.custom-accordion summary {
		font-weight: 600;
		font-size: 1.1em;
		padding: 18px 24px;
		cursor: pointer;
		list-style: none;
		position: relative;
		transition: background-color 0.2s ease;
		border-radius: 8px;
		color: #1f2937;
	}
	.custom-accordion summary::-webkit-details-marker {
		display: none;
	}
	.custom-accordion summary::after {
		content: '+';
		position: absolute;
		right: 24px;
		font-size: 1.4em;
		font-weight: 400;
		color: #6b7280;
		line-height: 1;
		transition: transform 0.2s ease;
	}
	.custom-accordion[open] summary {
		border-bottom-left-radius: 0;
		border-bottom-right-radius: 0;
		border-bottom: 1px solid #e5e7eb;
		background-color: #f9fafb;
	}
	.custom-accordion[open] summary::after {
		content: '−';
	}
	.custom-accordion summary:hover {
		background-color: #f3f4f6;
	}

	.accordion-body {
		padding: 24px;
		color: #4b5563;
	}
	.accordion-body ul {
		margin: 0 0 15px;
		padding-left: 20px;
	}
	.accordion-body li {
		margin-bottom: 8px;
	}

	/* Tabelas do dicionário */
	.table-x {
		overflow-x: auto;
	}
	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.9em;
		margin-bottom: 20px;
	}
	th,
	td {
		padding: 10px 14px;
		text-align: left;
		border-bottom: 1px solid #e5e7eb;
	}
	th {
		background-color: #f9fafb;
		font-weight: 600;
		color: #374151;
	}
	tbody tr:hover {
		background-color: #f3f4f6;
	}
	code {
		background-color: #f3f4f6;
		padding: 2px 6px;
		border-radius: 4px;
		font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
		color: #be185d;
		font-size: 0.9em;
	}

	.citation-box {
		background-color: #f3f4f6;
		padding: 15px;
		border-radius: 6px;
		margin-top: 15px;
	}

	/* Seção da tabela interativa */
	.table-section {
		margin-top: 10px;
		border-top: 1px solid #e5e7eb;
		padding-top: 24px;
	}
	.table-intro {
		max-width: 75ch;
		margin: 0 0 1.25rem;
		color: #4b5563;
	}

	@media (max-width: 860px) {
		.doc-bg {
			padding: 20px 10px;
		}
		.aba-dados-abertos {
			padding: 24px 18px;
		}
	}
</style>
