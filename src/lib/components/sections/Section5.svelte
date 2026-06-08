<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import {
		BigNumber,
		DonutChart,
		HorizontalStackedBarChart,
		TreemapChart,
		colorPairs,
		colorScales,
		categorical8,
	} from 'sniic-design-system';
	import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
	import {
		percContempladosCadunico,
		qtdContempladosCadunico,
		qtdDocumentosUnicos,
		valorRecebidoCadunico,
		percValorCadunico,
		percFemCadunico,
		perc2554Cadunico,
		faixaEtariaSexoData,
		FAIXA_SEXO_KEYS,
		FAIXA_SEXO_LABELS,
		rendaDonutData,
		situacaoRendaDonutData,
		percUrbanoCadunico,
		domicilioTreemapData,
		percPequenoPorteCadunico,
		porteTreemapData5,
		cadunicoUfGroupedData,
		representacaoUfGroupedData,
		valorGroupedData,
		percBolsaFamilia,
		valorBolsaFamilia,
		percBpc,
		valorBpc,
	} from '$lib/data/section5';

	const formatBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency',
			currency: 'BRL',
			notation: 'compact',
			maximumFractionDigits: 1,
		}).format(v);
	const formatNum = (v: number) => v.toLocaleString('pt-BR');
	const formatPct = (v: number) =>
		v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';
	const formatPctFixed = (v: number) => `${v.toFixed(1)}%`;
</script>

<!-- ══════════════════════════════════════════════════════════════════════════
     INTRODUÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-intro">
	<h2>5. Quantos agentes culturais contemplados estão em situação de vulnerabilidade social?</h2>
	<p>
		Muito se especula que os recursos das políticas culturais estejam concentrados nas mãos de
		grandes artistas e produtoras culturais. A implementação da Aldir Blanc, no entanto, introduziu
		mudanças estruturais no fomento à cultura, como a execução federativa dos recursos e a adoção
		de ações afirmativas, ampliando as possibilidades de acesso. Este levantamento busca
		compreender como os agentes culturais contemplados por esta política se distribuem a partir de
		marcadores e programas sociais.
	</p>
	<div class="annotation-box">
		As análises desta seção foram elaboradas a partir do cruzamento dos dados dos agentes culturais
		pessoas físicas contemplados com a base do Cadastro Único, um registro utilizado pelo Governo
		Federal para identificar e conhecer as famílias de baixa renda.
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     GRANDES NÚMEROS — CADUNICO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-bignumbers">
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percContempladosCadunico)} fontSize={72} />
			<p class="bignumber-caption">das pessoas contempladas no Ciclo 1 da Aldir Blanc estão cadastradas no Cadastro Único</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatNum(qtdContempladosCadunico)} fontSize={72} />
			<p class="bignumber-caption">contemplados representam esse grupo</p>
		</div>
	</div>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatNum(qtdDocumentosUnicos)} fontSize={72} />
			<p class="bignumber-caption">pessoas (documentos únicos) no cruzamento</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorRecebidoCadunico)} fontSize={72} />
			<p class="bignumber-caption">foram transferidos diretamente a esses agentes culturais contemplados</p>
		</div>
	</div>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percValorCadunico)} fontSize={72} />
			<p class="bignumber-caption">dos recursos totais da Aldir Blanc foram destinados a essas pessoas físicas</p>
		</div>
	</div>
	<p>
		Na prática, esse percentual sinaliza que parte significativa dos contemplados pela Aldir Blanc
		também está registrada no cadastro oficial de famílias de baixa renda do governo federal.
	</p>
	<p>
		Estar no Cadastro Único não significa automaticamente que a pessoa recebe um benefício
		específico, mas indica que ela se enquadra nos critérios de renda para estar cadastrada. Em
		geral, o cadastro é voltado para:
	</p>
	<ul class="bullet-list">
		<li>Famílias com renda mensal de até meio salário mínimo por pessoa; ou</li>
		<li>
			Famílias com renda acima desse valor também podem ser cadastradas, desde que o Cadastro Único
			seja exigido para acesso a algum programa ou serviço social específico.
		</li>
		<li>
			O Cadastro Único também considera características específicas de grupos em maior
			vulnerabilidade, como povos indígenas, comunidades quilombolas e outros.
		</li>
	</ul>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     5.1 — QUEM SÃO OS AGENTES CULTURAIS CADASTRADOS NO CADUNICO?
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-51">
	<h2>5.1. Quem são os agentes culturais contemplados na Aldir Blanc e cadastrados no Cadastro Único?</h2>
	<p class="frase-destaque">
		As mulheres adultas residentes em cidades pequenas e em situação de pobreza ou baixa renda são
		o perfil mais recorrente entre os contemplados na Aldir Blanc e cadastrados no Cadastro Único.
	</p>
	<div class="profile-card">
		<div class="profile-header">Perfil 3 — Pessoa Física Contemplada no Ciclo 1 da Aldir Blanc e Cadastrada no CadÚnico</div>
		<ul class="profile-list">
			<li><strong>Identidade:</strong> Mulher</li>
			<li><strong>Território:</strong> Centro-Oeste, município com menos de 20 mil habitantes</li>
			<li><strong>Idade:</strong> 37 anos</li>
			<li><strong>Renda:</strong> Beneficiária do Bolsa Família. Atua na cultura de maneira eventual.</li>
			<li><strong>Fomento:</strong> Aporte de R$ 6 mil</li>
		</ul>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     5.1.1 — SEXO E FAIXA ETÁRIA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-511-sexo">
	<h3>5.1.1. Sexo e faixa etária</h3>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percFemCadunico)} fontSize={72} />
			<p class="bignumber-caption">dos contemplados CadÚnico são mulheres</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatPct(perc2554Cadunico)} fontSize={72} />
			<p class="bignumber-caption">estão entre 25 e 54 anos</p>
		</div>
	</div>
	<HorizontalStackedBarChart
		data={faixaEtariaSexoData}
		keys={[...FAIXA_SEXO_KEYS]}
		labels={FAIXA_SEXO_LABELS}
		colors={[colorPairs.bluePurple[1], colorPairs.bluePurple[0]]}
		format={formatPctFixed}
		showTotalLabel={false}
	/>
	<p>
		As mulheres representam a maioria dos contemplados da Aldir Blanc cadastrados no Cadastro Único
		(<strong>{formatPct(percFemCadunico)}</strong>), em consonância com sua forte presença no
		próprio CadÚnico, onde correspondem a <strong>57%</strong> das pessoas cadastradas. Elas
		predominam em quase todas as faixas etárias, com exceção da mais jovem, de 15 a 24 anos. Entre
		os contemplados de 25 a 54 anos, as mulheres somam <strong>37,9%</strong> do total, frente a
		<strong>30,8%</strong> dos homens. A predominância feminina também se mantém nas faixas acima
		de 55 e 65 anos, embora de forma mais sutil.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     5.1.2 — RENDA FAMILIAR E VULNERABILIDADE SOCIOECONÔMICA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-512-renda">
	<h3>5.1.2. Renda familiar e vulnerabilidade socioeconômica</h3>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="63,2%" fontSize={72} />
			<p class="bignumber-caption">tem renda familiar de até 1 salário mínimo</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="43,6%" fontSize={72} />
			<p class="bignumber-caption">estão em situação de pobreza, com renda familiar per capita de até R$218</p>
		</div>
	</div>
	<div class="donut-row">
		<div class="donut-col">
			<p class="donut-label">Por faixa de renda per capita</p>
			<DonutChart
				data={rendaDonutData}
				colors={categorical8}
				centerLabel="pessoas"
				centerValue={formatNum(rendaDonutData.reduce((s, d) => s + d.value, 0))}
				format={formatNum}
				height={400}
			/>
		</div>
		<div class="donut-col">
			<p class="donut-label">Por situação de renda</p>
			<DonutChart
				data={situacaoRendaDonutData}
				colors={[colorScales.red[2], colorScales.orange[2], colorScales.blue[2]]}
				centerLabel="pessoas"
				centerValue={formatNum(situacaoRendaDonutData.reduce((s, d) => s + d.value, 0))}
				format={formatNum}
				height={320}
			/>
		</div>
	</div>
	<div class="annotation-box" style="margin-top: 1.5rem;">
		São consideradas em situação de pobreza as famílias que têm renda por pessoa de até R$218,00
		e, em baixa renda, aquelas com renda por pessoa entre R$218,00 e meio salário mínimo
		(Ministério do Desenvolvimento e Assistência Social, Família e Combate à Fome).
	</div>
	<p>
		Os dados evidenciam um cenário de intensa vulnerabilidade socioeconômica entre uma parcela
		significativa dos agentes culturais contemplados pela Aldir Blanc e cadastrados no Cadastro
		Único. Uma parte expressiva desses agentes culturais vive em situação de pobreza
		(<strong>43,6%</strong>), com rendimentos mensais abaixo de R$218. Esse quadro indica que a
		política conseguiu alcançar grupos historicamente marginalizados ou submetidos a condições
		socioeconômicas precárias.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     5.2 — ONDE ESTÃO LOCALIZADOS?
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-52">
	<h2>5.2. Onde estão localizados os agentes culturais cadastrados no Cadastro Único e contemplados na Aldir Blanc?</h2>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percUrbanoCadunico)} fontSize={72} />
			<p class="bignumber-caption">vivem em áreas urbanas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percPequenoPorteCadunico)} fontSize={72} />
			<p class="bignumber-caption">residem em municípios de pequeno porte — percentual maior do que os demais agentes culturais contemplados</p>
		</div>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     5.2.1 — ÁREA E PORTE POPULACIONAL
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-521-area">
	<h3>5.2.1. Área e porte populacional</h3>
	<div class="treemap-row">
		<div class="treemap-col">
			<p class="donut-label">Por situação de domicílio</p>
			<TreemapChart
				data={domicilioTreemapData}
				height={260}
				format={formatNum}
				colors={[colorScales.blue[2], colorScales.teal[2]]}
			/>
		</div>
		<div class="treemap-col">
			<p class="donut-label">Por porte do município</p>
			<TreemapChart
				data={porteTreemapData5}
				height={260}
				format={formatNum}
				colors={categorical8}
			/>
		</div>
	</div>
	<p>
		Embora a maioria das pessoas contempladas resida em áreas urbanas, aquelas no Cadastro Único
		têm presença proporcionalmente maior em áreas rurais do que o conjunto geral de pessoas físicas
		contempladas no Ciclo 1. Entre as presentes no Cadastro, <strong>23,5%</strong> vivem em zonas
		rurais, número cerca de <strong>7 pontos percentuais</strong> superior ao observado no total de
		contemplados (<strong>14,3%</strong>).
	</p>
	<p>
		Enquanto <strong>78,5%</strong> dos agentes culturais com cadastro no Cadastro Único residem em
		municípios de pequeno porte, com até 50 mil habitantes (Porte I e II), no conjunto geral de
		contemplados esse percentual é de <strong>68,6%</strong>, diferença de quase
		<strong>10 pontos percentuais</strong>.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     5.2.2 — UNIDADES DA FEDERAÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-522-uf">
	<h3>5.2.2. Unidades da federação (UF)</h3>
	<p>
		Distribuímos por UF a quantidade de pessoas cadastradas no Cadastro Único e os contemplados na
		Aldir Blanc que também estão presentes nesse cadastro.
		<strong>Observam-se diferenças territoriais importantes na capacidade de alcance da política
		cultural junto a públicos vulnerabilizados.</strong> Os números a seguir destacam,
		sequencialmente, o percentual de contemplados na Aldir Blanc cadastrados no CadÚnico e o
		percentual total de pessoas inscritas no Cadastro Único em cada UF.
	</p>
	<p>
		As UF <strong>Mato Grosso (9,9% e 1,8%)</strong>, <strong>Paraná (10,7% e 4,6%)</strong>,
		<strong>Paraíba (9,1% e 2,7%)</strong> e <strong>Bahia (14,8% e 9,7%)</strong> apresentam
		forte <strong>sobrerrepresentação</strong> de pessoas cadastrados no Cadastro Único entre os
		contemplados da PNAB. Esse alcance reflete maior orientação distributiva da política nessas
		UFs, possivelmente como resultado de medidas de democratização de acesso.
	</p>
	<p>
		Em contrapartida, estados como <strong>São Paulo (2,4% e 14,7%)</strong>,
		<strong>Minas Gerais (1,0% e 9,1%)</strong>, <strong>Rio de Janeiro (2,0% e 7,2%)</strong> e
		<strong>Rio Grande do Sul (0,2% e 3,9%)</strong> apresentam forte
		<strong>sub-representação</strong> de beneficiários do CadÚnico entre os contemplados da PNAB.
		O caso mais expressivo é o de São Paulo, onde as famílias do CadÚnico representam
		<strong>14,7%</strong> do total, mas apenas <strong>2,4%</strong> dos contemplados da política
		cultural pertencem ao cadastro. Esse cenário pode indicar barreiras de acesso aos editais,
		concentração dos recursos em agentes culturais mais estruturados, burocratização dos
		mecanismos e dificuldades de territorialização das políticas de fomento cultural.
	</p>
	<HorizontalGroupedBarChart
		data={cadunicoUfGroupedData}
		seriesLabels={['% contemplados da UF no CadÚnico', '% agentes culturais PNAB (Brasil)']}
		colors={[colorScales.teal[2], colorScales.orange[2]]}
		format={formatPctFixed}
		margin={{ top: 28, right: 90, bottom: 40, left: 50 }}
	/>
	<p>
		O gráfico a seguir compara diretamente o peso de cada UF no total de contemplados na Aldir
		Blanc com cadastro no CadÚnico com o peso de cada UF na população total inscrita no CadÚnico.
		Quando a barra teal supera a laranja, há <strong>sobrerrepresentação</strong> dos vulneráveis
		locais na política; quando fica abaixo, há <strong>sub-representação</strong>.
	</p>
	<HorizontalGroupedBarChart
		data={representacaoUfGroupedData}
		seriesLabels={[
			'% contemplados PNAB/CadÚnico (UF)',
			'% pessoas CadÚnico (UF)',
		]}
		colors={[colorScales.teal[2], colorScales.orange[2]]}
		format={formatPctFixed}
		margin={{ top: 28, right: 90, bottom: 40, left: 50 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     5.3 — COMO OS RECURSOS FORAM DISTRIBUÍDOS?
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-53">
	<h2>5.3. Como os recursos foram distribuídos entre os agentes culturais cadastrados no Cadastro Único?</h2>
	<h3>5.3.1. Valores dos repasses</h3>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="86,8%" fontSize={72} />
			<p class="bignumber-caption">dos contemplados receberam até R$10 mil</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="R$6.262" fontSize={72} />
			<p class="bignumber-caption">foi o valor médio dos repasses para esse público</p>
		</div>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     5.3.1 — FAIXA DE VALOR (GRÁFICO COMPARATIVO)
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-531-valor">
	<HorizontalGroupedBarChart
		data={valorGroupedData}
		seriesLabels={['% agentes culturais PNAB/CadÚnico', '% agentes culturais PNAB']}
		colors={[colorScales.blue[2], colorScales.red[2]]}
		format={formatPctFixed}
		margin={{ top: 28, right: 90, bottom: 40, left: 160 }}
	/>
	<p>
		No que diz respeito aos valores recebidos, observa-se uma forte concentração dos agentes
		culturais com cadastro no CadÚnico nas faixas de valores menores:
		<strong>86,8%</strong> dos contemplados receberam até <strong>R$10 mil</strong>. Ao calcular o
		valor médio dos repasses, identifica-se uma <strong>média de R$6.262</strong> entre esses
		agentes culturais.
	</p>
	<p>
		Quando comparado com o conjunto total de agentes contemplados pela Política Nacional Aldir
		Blanc, nota-se uma diferença relevante na distribuição. Embora também exista concentração nas
		faixas mais baixas, ela é menos acentuada: <strong>71,6%</strong> receberam até R$10 mil,
		enquanto as faixas superiores têm maior presença relativa. O valor médio dos repasses é de
		<strong>R$17.053</strong>, superior ao observado entre aqueles cadastrados no Cadastro Único.
	</p>
	<p>
		<strong>Essa comparação evidencia que os agentes culturais inscritos no CadÚnico estão ainda
		mais concentrados nos menores valores de repasse do que o universo geral de contemplados, além
		de receberem, em média, valores inferiores.</strong> Esse resultado sugere um padrão
		distributivo de maior pulverização de recursos entre os mais vulnerabilizados, mas com menor
		acesso relativo às faixas de repasse mais elevadas.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     5.3.2 — BENEFÍCIOS E PROGRAMAS ASSISTENCIAIS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-532-beneficios">
	<h3>5.3.2. Benefícios e programas assistenciais associados</h3>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percBolsaFamilia)} fontSize={72} />
			<p class="bignumber-caption">dos agentes culturais são beneficiários do Bolsa Família</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorBolsaFamilia)} fontSize={72} />
			<p class="bignumber-caption">foram repassados para esse público</p>
		</div>
	</div>
	<p>
		Parcela relevante dos recursos foi destinada a pessoas em situação de pobreza ou extrema
		pobreza beneficiárias do Programa Bolsa Família. Para estas pessoas a cultura é um meio de
		expressão simbólica, mas representa também uma estratégia concreta de sobrevivência. Esses
		resultados tensionam a ideia de que o fomento cultural viabilizado pela Aldir Blanc se
		restringiu a agentes já consolidados e inseridos em grandes circuitos comerciais e
		profissionais.
	</p>
	<div class="bignumbers-row" style="margin-top: 2rem;">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percBpc)} fontSize={64} />
			<p class="bignumber-caption">dos agentes culturais são beneficiários do BPC</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorBpc)} fontSize={64} />
			<p class="bignumber-caption">foram repassados para beneficiários do BPC</p>
		</div>
	</div>
	<p>
		Uma pequena mas significativa parcela dos contemplados são beneficiários do Benefício de
		Prestação Continuada (BPC), destinado a idosos e pessoas com deficiência em situação de
		vulnerabilidade.
	</p>
</ScrollSection>

<style>
	.bignumbers-row {
		display: flex;
		gap: 2rem;
		flex-wrap: wrap;
		margin-top: 1.5rem;
	}

	.bignumber-cell {
		flex: 1 1 240px;
		min-width: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.5rem;
		margin-top: 1.5rem;
	}

	.bignumber-caption {
		font-size: 0.95rem;
		color: var(--color-text);
		text-align: center;
		opacity: 0.75;
		max-width: 22ch;
	}

	.frase-destaque {
		margin-top: 2rem;
		padding-left: 1.25rem;
		border-left: 3px solid currentColor;
		font-size: 1.15rem;
		font-weight: 500;
		line-height: 1.5;
		opacity: 0.9;
	}

	.annotation-box {
		margin-top: 1rem;
		padding: 1rem 1.25rem;
		border: 1px solid currentColor;
		border-radius: 2px;
		font-size: 0.875rem;
		line-height: 1.6;
		opacity: 0.8;
	}

	.bullet-list {
		margin-top: 1rem;
		padding-left: 1.5rem;
		line-height: 1.7;
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}

	.profile-card {
		margin-top: 1.5rem;
		border: 1px solid currentColor;
		border-radius: 4px;
		overflow: hidden;
		max-width: 480px;
		opacity: 0.9;
	}

	.profile-header {
		padding: 0.75rem 1rem;
		font-weight: 600;
		font-size: 0.85rem;
		border-bottom: 1px solid currentColor;
		opacity: 0.7;
	}

	.profile-list {
		list-style: none;
		margin: 0;
		padding: 1rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		font-size: 0.9rem;
		line-height: 1.5;
	}

	.donut-row {
		display: flex;
		gap: 2rem;
		flex-wrap: wrap;
		margin-top: 1.5rem;
	}

	.donut-col {
		flex: 1 1 260px;
		min-width: 0;
		display: flex;
		flex-direction: column;
	}

	.donut-label {
		font-size: 0.8rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		opacity: 0.55;
		margin: 0 0 0.25rem;
		text-align: center;
		align-self: center;
	}

	.treemap-row {
		display: flex;
		gap: 2rem;
		flex-wrap: wrap;
		margin-top: 1.5rem;
	}

	.treemap-col {
		flex: 1 1 280px;
		min-width: 0;
	}

	p {
		margin-top: 1.5rem;
	}
</style>
