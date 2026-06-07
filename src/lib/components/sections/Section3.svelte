<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import {
		BigNumber,
		DonutChart,
		GroupedColumnChart,
		HorizontalBarChart,
		PictogramChart,
		colorPairs,
		colorScales,
		categorical8,
	} from 'sniic-design-system';
	import PyramidChartCustom from '$lib/components/PyramidChartCustom.svelte';
	import CnaeTable from '$lib/components/CnaeTable.svelte';
	import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import VerticalGroupedBarChart from '$lib/components/VerticalGroupedBarChart.svelte';
	import SexoUfStackedComparison from '$lib/components/SexoUfStackedComparison.svelte';
	import {
		totalBeneficiarios,
		totalPF,
		valorTotalPF,
		valorTotalPJ,
		valorTotalMEI,
		pfPjDonutData,
		sexoQuantityDonutData,
		sexoValueDonutData,
		sexoPropMasculino,
		sexoPropFeminino,
		pyramidData,
		ageGroupRegionData,
		ageGroupRegionKeys,
		ageGroupRegionLabels,
		top20CboData,
		top20CnaesQtdTableData,
		top20CnaesValTableData,
		cnaesQtdTableHeight,
		cnaesValTableHeight,
		naturezaJuridicaRegiaoData,
		naturezaJuridicaSeriesLabels,
		naturezaJuridicaData,
		sexoUfData,
		sexoUfSeriesLabels,
		sexoUfComparisonData,
		valorMedioSexoPorteData,
		valorMedioSexoSeriesLabels,
	} from '$lib/data/section3';

	const formatNum = (v: number) => v.toLocaleString('pt-BR');
	const formatBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency',
			currency: 'BRL',
			notation: 'compact',
			maximumFractionDigits: 1,
		}).format(v);
	const formatPct = (v: number) =>
		(v * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

	const pfPjColors = [colorScales.teal[2], colorScales.orange[2]];
	const sexColors = [colorPairs.bluePurple[1], colorPairs.bluePurple[0]];
	const sexoUfColors = [colorScales.blue[1], colorScales.blue[2], colorScales.purple[1], colorScales.purple[2]];
	const pictogramData = [
		{ label: 'Masculino', value: 8, color: colorScales.lime[2] },
		{ label: 'Feminino', value: 7, color: colorScales.orange[2] },
	];
</script>

<!-- ══════════════════════════════════════════════════════════════════════════
     INTRODUÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-intro">
	<h2>3. Quem acessou os recursos da Política Nacional Aldir Blanc?</h2>
	<p>
		Neste capítulo, mergulhamos nos dados dos agentes culturais e das organizações contempladas no
		primeiro ciclo da Aldir Blanc, destacando alguns indicadores que ajudam a compreender quem
		acessou os recursos da política.
	</p>
	<div class="annotation-box">
		As análises apresentadas neste capítulo resultam do cruzamento dos dados de agentes culturais
		contemplados pela Política Nacional de Fomento à Cultura Aldir Blanc no Ciclo 1 com bases da
		Receita Federal. Para as pessoas físicas, foram utilizadas as variáveis idade e sexo
		(masculino/feminino), sendo esta última adotada conforme disponibilidade da base, referindo-se
		ao sexo biológico registrado — o que não contempla a diversidade de identidades de gênero (como
		pessoas trans, travestis, não binárias, entre outras). Para as pessoas jurídicas, foram
		utilizadas as variáveis natureza jurídica e CNAE (principal e secundários).
	</div>
	<p class="frase-destaque">
		A Política Nacional Aldir Blanc contemplou <strong>166.886</strong> agentes culturais em todo o
		país
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     GRANDES NÚMEROS GERAIS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-totals">
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="134.606" fontSize={64} />
			<p class="bignumber-perc">(80,7%)</p>
			<p class="bignumber-caption">são pessoas físicas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="32.280" fontSize={64} />
			<p class="bignumber-perc">(19,3%)</p>
			<p class="bignumber-caption">são pessoas jurídicas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="9.076" fontSize={64} />
			<p class="bignumber-perc">(5,4% do total)</p>
			<p class="bignumber-caption">são MEIs dentre as pessoas jurídicas</p>
		</div>
	</div>
	<p style="margin-top: 2rem;">
		Do total de <strong>R$2.845.995.593</strong> executado:
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorTotalPF)} fontSize={56} />
			<p class="bignumber-perc">(44,1%)</p>
			<p class="bignumber-caption">recebidos por pessoas físicas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorTotalPJ)} fontSize={56} />
			<p class="bignumber-perc">(55,9%)</p>
			<p class="bignumber-caption">recebidos por pessoas jurídicas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorTotalMEI)} fontSize={56} />
			<p class="bignumber-caption">recebidos pelos MEIs</p>
		</div>
	</div>
	<p>
		A análise dos agentes culturais contemplados pela Política Nacional Aldir Blanc revela que o
		acesso aos recursos combina ampla capilaridade social com padrões diferenciados de distribuição.
		Para iniciar esse capítulo, traçamos perfis médios de agentes contemplados, pessoas físicas e
		jurídicas.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PERFIS REPRESENTATIVOS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-profiles">
	<h3>Perfis representativos dos contemplados</h3>
	<div class="profiles-row">
		<div class="profile-card">
			<div class="profile-header">Perfil da pessoa física mais contemplada</div>
			<ul class="profile-list">
				<li><strong>Sexo:</strong> Homem</li>
				<li><strong>Idade:</strong> 31 anos</li>
				<li><strong>Território:</strong> Nordeste, município com menos de 20 mil habitantes</li>
				<li>
					<strong>Trabalho:</strong> Trabalhador da cultura autônomo sem vínculo formal de trabalho
				</li>
				<li><strong>Valor pago:</strong> Aporte de R$ 9,4 mil</li>
			</ul>
		</div>
		<div class="profile-card">
			<div class="profile-header">Perfil representativo da pessoa jurídica contemplada</div>
			<ul class="profile-list">
				<li><strong>Natureza Jurídica:</strong> Associação Cultural</li>
				<li>
					<strong>Porte:</strong> Organização da sociedade civil sem fins lucrativos, de pequeno
					porte, com atuação comunitária voltada à valorização da cultura
				</li>
				<li>
					<strong>Missão:</strong> Preservar, promover e difundir a cultura, fortalecendo vínculos
					comunitários e a transmissão de saberes
				</li>
				<li><strong>Território:</strong> Região Norte, município com 20 mil habitantes</li>
				<li><strong>Valor pago:</strong> Aporte de R$ 49,3 mil</li>
			</ul>
		</div>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.1 — DIFERENÇAS PF vs PJ
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-31">
	<h2>3.1. Quais as diferenças no acesso aos recursos entre pessoas físicas e jurídicas?</h2>
	<p>
		Em média, os repasses para pessoas físicas são cinco vezes menores que os destinados a pessoas
		jurídicas. Enquanto o valor médio recebido por pessoas físicas ficou em torno de
		<strong>R$9.321</strong>, pessoas jurídicas receberam em média <strong>R$49.297</strong>.
	</p>
	<p>
		A análise por faixas de valor reforça esse padrão. Entre as pessoas físicas, predominam
		pagamentos de menor valor, com <strong>44,1%</strong> concentrados na faixa de R$2 a R$10 mil.
		Já <strong>38,8%</strong> dos pagamentos para pessoas jurídicas foram na faixa de R$10 a R$50
		mil reais.
	</p>
	<p>
		Nesse contexto, os Microempreendedores Individuais (MEIs) apresentam um perfil híbrido de acesso
		aos recursos. A maioria dos MEIs (<strong>42%</strong>) recebeu valores na faixa de R$2 mil a
		R$10 mil, padrão semelhante ao observado entre pessoas físicas. Já o valor médio dos MEIs foi
		<strong>R$26.317</strong>, diferenciando-os tanto das pessoas físicas como jurídicas.
	</p>
	<div class="donut-single">
		<DonutChart
			data={pfPjDonutData}
			colors={pfPjColors}
			centerLabel="total"
			centerValue={totalBeneficiarios.toLocaleString('pt-BR')}
			format={formatNum}
			height={360}
		/>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.1.1 — VARIAÇÃO ENTRE ENTES ESTATAIS E MUNICIPAIS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-311">
	<h3>3.1.1. Variação entre entes estatais e municipais</h3>
	<p>
		De maneira geral, os entes estatais foram responsáveis por contemplar <strong
			>22.050 (13,2%)</strong
		> dos agentes culturais da Aldir Blanc, sendo:
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="14.996" fontSize={64} />
			<p class="bignumber-perc">(68%)</p>
			<p class="bignumber-caption">pessoas físicas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="7.054" fontSize={64} />
			<p class="bignumber-perc">(32%)</p>
			<p class="bignumber-caption">pessoas jurídicas</p>
		</div>
	</div>
	<p>
		Embora o maior número de agentes culturais contemplados sejam de pessoas físicas, predomina um
		repasse majoritário de recursos destinados a pessoas jurídicas (<strong>64,7%</strong>), o que
		corresponde a <strong>R$937.817.660</strong>.
	</p>
	<p>
		Observa-se também uma heterogeneidade entre os estados. Os estados que destinaram mais de 50%
		de seus recursos para pessoas físicas são Acre, Amazonas, Rondônia, Roraima, Tocantins,
		Pernambuco e Minas Gerais, a maioria na região Norte. Dentre os estados que distribuíram um
		percentual maior de recursos para pessoas jurídicas, destacam-se o Rio de Janeiro e o Rio
		Grande do Sul que destinaram <strong>92,4%</strong> e <strong>99,7%</strong> de seus recursos
		para CNPJs, respectivamente.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.1.1 — MUNICÍPIOS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-municipios">
	<p>
		Os municípios concentram a maior parte dos agentes culturais contemplados na Política, ao todo
		<strong>144.836</strong>, sendo ainda mais predominante o repasse para pessoas físicas:
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="119.610" fontSize={64} />
			<p class="bignumber-perc">(82,6%)</p>
			<p class="bignumber-caption">pessoas físicas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="25.226" fontSize={64} />
			<p class="bignumber-perc">(17,4%)</p>
			<p class="bignumber-caption">pessoas jurídicas</p>
		</div>
	</div>
	<p>
		Diferente do observado no nível estadual e nacional, mais da metade dos recursos municipais
		também se destina às pessoas físicas, o que corresponde a <strong>R$741.987.236 (53,2%)</strong
		>.
	</p>
	<p>
		Esse resultado está associado à atuação predominante dos municípios na realização de pagamentos
		de menor valor e com maior dispersão de agentes, especialmente nos municípios de pequeno e
		médio porte. Apenas nos municípios de grande porte observa-se um padrão mais próximo ao
		nacional, com maior concentração relativa de recursos em pessoas jurídicas.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.2 — CARACTERÍSTICAS PF — INTRODUÇÃO E SEXO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-32">
	<h2>3.2. Quais as características das pessoas físicas contempladas?</h2>
	<div class="annotation-box">
		Para a análise das pessoas físicas, foram utilizadas as variáveis idade e sexo, sendo esta
		última analisada conforme é registrada na base da Receita Federal (feminino/masculino), o que
		não contempla, portanto, a diversidade de identidades de gênero. A análise compara a
		participação percentual de agentes culturais do sexo feminino e masculino nas Unidades
		Federativas (UF) com a distribuição desses grupos na população.
	</div>
	<h3>3.2.1. Sexo</h3>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(sexoPropMasculino)} fontSize={72} />
			<p class="bignumber-caption">dos agentes culturais contemplados são do sexo masculino</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatPct(sexoPropFeminino)} fontSize={72} />
			<p class="bignumber-caption">dos agentes culturais contemplados são do sexo feminino</p>
		</div>
	</div>
	<p class="pictogram-caption">Cada ícone representa 1 em cada 15 agentes culturais contemplados</p>
	<div class="pictogram-wrap">
		<PictogramChart
			data={pictogramData}
			unitValue={1}
			columns={15}
			iconSize={48}
			gap={8}
			showLabels={true}
			format={formatNum}
		/>
	</div>
	<p>
		Quando consideramos o percentual de mulheres na população geral brasileira (<strong>51,5%</strong
		>, segundo o último censo), verificamos que elas são sub-representadas. São
		<strong>4,7 pontos percentuais</strong> a menos na sua participação na Aldir Blanc.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.2.1 — SEXO: DONUTS E DESTAQUES POR UF
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-321-donuts">
	<p class="frase-destaque">
		Nas diferentes UFs os homens tendem a acessar a política em proporções superiores à sua
		presença populacional
	</p>
	<p>
		Os dados revelam diferentes padrões de acesso à Aldir Blanc quando comparados à distribuição
		populacional. Evidencia-se um leve desequilíbrio de gênero no alcance da política com
		sub-representação feminina.
	</p>
	<p>
		A maior participação feminina ocorre na Paraíba (PB), onde as mulheres correspondem a
		<strong>48,8%</strong> dos contemplados frente a <strong>43,5%</strong> da população.
	</p>
	<p>
		Já os homens foram mais contemplados no Rio Grande do Sul (RS), representando
		<strong>54,3%</strong> dos agentes culturais, enquanto são <strong>42,3%</strong> da população.
	</p>
	<p>
		A UF que apresenta maior paridade de gênero é o Distrito Federal (DF), onde os percentuais de
		participação são praticamente equivalentes à composição populacional (<strong>42,2% / 42%</strong
		> para mulheres e <strong>57,8% / 58%</strong> para homens).
	</p>
	<div class="donut-row">
		<div class="donut-col">
			<p class="donut-label">Por quantidade de agentes</p>
			<DonutChart
				data={sexoQuantityDonutData}
				colors={sexColors}
				centerLabel="Agentes contemplados"
				centerValue={totalPF.toLocaleString('pt-BR')}
				format={formatNum}
				height={280}
			/>
		</div>
		<div class="donut-col">
			<p class="donut-label">Por valor recebido</p>
			<DonutChart
				data={sexoValueDonutData}
				colors={sexColors}
				centerLabel="valor total"
				centerValue={formatBRL(valorTotalPF)}
				format={formatBRL}
				height={280}
			/>
		</div>
	</div>
	<HorizontalGroupedBarChart
		data={sexoUfData}
		seriesLabels={sexoUfSeriesLabels}
		colors={sexoUfColors}
		format={(v) => v.toFixed(1) + '%'}
		xLabel="% do total de contemplados / população"
		margin={{ top: 20, right: 70, bottom: 44, left: 40 }}
		barHeight={10}
		barPad={3}
		legendBottom={true}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.2.1 — SEXO: BARRAS EMPILHADAS ALDIR BLANC vs IBGE
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-321-stacked">
	<p>
		Para facilitar a comparação entre a distribuição por sexo dos contemplados e a composição
		populacional de cada UF, o gráfico abaixo apresenta duas barras empilhadas por estado: a
		barra superior (cor cheia) representa os agentes culturais da Aldir Blanc; a barra inferior
		(cor clara) representa a população segundo o Censo 2022 do IBGE.
	</p>
	<SexoUfStackedComparison
		data={sexoUfComparisonData}
		colorMasc={colorScales.blue[2]}
		colorFem={colorScales.purple[2]}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.2.1 — SEXO: VALORES MÉDIOS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-321-valores">
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="R$9,2 mil" fontSize={64} />
			<p class="bignumber-caption">valor médio recebido por agentes culturais do sexo feminino</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="2%" fontSize={64} />
			<p class="bignumber-caption">de diferença em relação à média dos homens (R$9,4 mil)</p>
		</div>
	</div>
	<p>
		A diferença de apenas <strong>2%</strong> entre os valores indica que homens e mulheres acessam,
		em média, recursos semelhantes na Aldir Blanc.
	</p>
	<p>
		Os dados mostram que os agentes culturais do sexo masculino receberam, em média, valores
		superiores aos do sexo feminino em todas as faixas de porte municipal. A maior diferença
		proporcional ocorre nos municípios de pequeno porte I, onde as agentes do sexo feminino
		receberam, em média, <strong>R$2,7 mil</strong>, frente a <strong>R$3,4 mil</strong> entre os do
		sexo masculino.
	</p>
	<p>
		Nas capitais, os valores médios são significativamente mais elevados, alcançando
		<strong>R$24,6 mil</strong> entre agentes culturais do sexo masculino e
		<strong>R$23,4 mil</strong> entre agentes culturais do sexo feminino.
	</p>
	<p>
		O cenário reforça a importância de que entes subnacionais, especialmente nos territórios com
		maiores desigualdades sociais, implementem mecanismos de estímulo à participação feminina, como
		os previstos no art. 2º da IN MinC nº 10/2023.
	</p>
	<VerticalGroupedBarChart
		data={valorMedioSexoPorteData}
		seriesLabels={valorMedioSexoSeriesLabels}
		colors={sexColors}
		format={formatBRL}
		barWidth={36}
		barPad={14}
		innerH={300}
		margin={{ top: 20, right: 20, bottom: 10, left: 72 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.2.2 — IDADE: PIRÂMIDE ETÁRIA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-322-idade">
	<h3>3.2.2. Idade</h3>
	<p class="frase-destaque">
		Participação concentra-se na vida adulta, com baixa presença de jovens e idosos
	</p>
	<div class="pyramid-wrap">
		<PyramidChartCustom
			data={pyramidData}
			leftLabel="Masculino"
			rightLabel="Feminino"
			colors={colorPairs.bluePurple}
			format={formatNum}
			height={400}
			centerGap={96}
		/>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.2.2 — IDADE: TEXTOS E GRÁFICO POR REGIÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-322-region">
	<p>
		A distribuição por faixa etária concentra-se principalmente na população adulta. A faixa de
		<strong>25 a 54 anos</strong> reúne <strong>70,6%</strong> dos contemplados e concentra
		<strong>74,6%</strong> do volume total de recursos. Em comparação com os dados do Censo 2022 do
		IBGE, a população brasileira entre 25 e 54 anos corresponde a aproximadamente <strong>39%</strong
		> do total populacional, percentual significativamente inferior ao registrado entre os contemplados,
		indicando elevada concentração do acesso aos recursos nesse grupo etário.
	</p>
	<p>
		A participação de jovens de <strong>15 a 24 anos</strong> entre os contemplados
		(<strong>8%</strong>) é inferior à representatividade dessa faixa na população brasileira, que
		corresponde a cerca de <strong>14,7%</strong> segundo o Censo 2022 do IBGE. Do total de recursos
		destinados a jovens de 15 a 24 anos no Brasil inteiro (<strong>5,9%</strong>), a região Nordeste
		sozinha (<strong>2,6%</strong>) responde por quase a metade dos recursos voltados a esse público.
	</p>
	<p>
		Já a população com <strong>65 anos ou mais</strong> representa aproximadamente
		<strong>10,9%</strong> da população brasileira, percentual ligeiramente superior ao observado
		entre os contemplados (<strong>8,6%</strong>). Em relação a esse grupo, a região Sudeste e
		Nordeste foram as que mais tiveram peso, destinando respectivamente <strong>2,91%</strong> e
		<strong>2,78%</strong> dos recursos para a população idosa.
	</p>
	<GroupedColumnChart
		data={ageGroupRegionData}
		keys={ageGroupRegionKeys}
		categoryKey="faixa_etaria"
		labels={ageGroupRegionLabels}
		colors={categorical8}
		format={formatNum}
		height={420}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.2 — PF COM VÍNCULO FORMAL (CBO/RAIS)
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-pf-formal">
	<h3>Top 20 atividades econômicas dos contemplados com vínculo formal</h3>
	<p>
		Entre os agentes culturais contemplados que possuem vínculo formal de trabalho, as ocupações
		mais frequentes revelam um perfil heterogêneo — com destaque para funções administrativas, de
		ensino e de gestão pública. A lista ilustra que o setor cultural formal no Brasil abrange muito
		além das artes em sentido estrito.
	</p>
	<HorizontalBarChart
		data={top20CboData}
		color={categorical8[0]}
		format={formatNum}
		xLabel="Quantidade de vínculos formais"
		margin={{ top: 20, right: 60, bottom: 40, left: 320 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.3 — CARACTERÍSTICAS PJ
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-33">
	<h2>3.3. Quais as características das pessoas jurídicas contempladas?</h2>
	<div class="annotation-box">
		Para a análise das pessoas jurídicas, utilizaram-se as variáveis natureza jurídica e
		Classificação Nacional de Atividades Econômicas — CNAE (principal e secundários). As categorias
		de natureza jurídica foram agrupadas analiticamente para facilitar a comparação entre diferentes
		perfis institucionais, com base no anexo V da IN Receita Federal do Brasil nº 2.119/2022. Já os
		CNAEs da cultura seguem a metodologia do IBGE, conforme descrito nas Notas Técnicas do Sistema
		de Informações e Indicadores Culturais (SIIC).
	</div>
	<h3>3.3.1. Classificação das empresas e entidades contempladas</h3>
	<p>
		Os dados sobre a natureza jurídica dos agentes culturais contemplados pela Aldir Blanc revelam
		forte presença de estruturas de pequeno porte e organizações da sociedade civil.
		<strong>A expressiva participação das entidades sem fins lucrativos (32,7%) reflete o peso
		dessas organizações na execução de ações culturais</strong>, frequentemente associadas à
		promoção do acesso, à formação cultural e à atuação territorial.
	</p>
	<p>
		Ao mesmo tempo, a soma de <strong>MEIs (28,1%) e microempresas (30,4%) representa quase 58,5%
		dos contemplados</strong>, evidenciando a predominância de agentes econômicos de menor porte.
	</p>
	<p>
		A participação expressiva de agentes identificados como Microempreendedor Individual (MEI)
		também sugere que parte significativa do setor cultural opera por meio de trabalho autônomo
		formalizado e pequenos negócios culturais. O dado pode ainda indicar uma tendência à
		"pejotização" e à precarização das relações de trabalho, fenômeno observado no mercado de
		trabalho de forma mais ampla e que também se manifesta no campo cultural.
	</p>
	<p>
		Dentre os agentes culturais pessoa jurídica contemplados na Aldir Blanc, as microempresas
		configuram uma das naturezas jurídicas mais relevantes em todas as regiões, com destaque para o
		Sudeste (<strong>11,5%</strong>), seguido por Nordeste (<strong>7,9%</strong>) e Sul
		(<strong>7,8%</strong>). Os agentes culturais que são MEIs apresentam maior concentração no
		Sudeste (<strong>12%</strong>), com forte peso nas UFs de São Paulo (<strong>5,4%</strong>) e
		Minas Gerais (<strong>3%</strong>), seguido pelo Nordeste (<strong>7%</strong>) e Sul
		(<strong>6,7%</strong>). A presença das entidades sem fins lucrativos praticamente se equipara
		no Nordeste (<strong>10,8%</strong>) e no Sudeste (<strong>10,6%</strong>).
	</p>
	<HorizontalBarChart
		data={naturezaJuridicaData}
		color={categorical8[4]}
		format={(v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%'}
		xLabel="% de CNPJs contemplados"
		title="% - Distribuição de Agentes Culturais Pessoas Jurídicas Contemplados na Aldir Blanc por Natureza Jurídica"
		margin={{ top: 20, right: 80, bottom: 40, left: 230 }}
	/>
	<HorizontalStackedBarChartCustom
		data={naturezaJuridicaRegiaoData}
		keys={naturezaJuridicaSeriesLabels}
		colors={categorical8.slice(0, 6)}
		format={(v) => v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%'}
		marginLeft={120}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.3.2 — ATIVIDADES ECONÔMICAS (CNAE)
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-332-cnae">
	<h3>3.3.2. Atividades econômicas exercidas pelas pessoas jurídicas contempladas</h3>
	<p>
		Cada empresa, associação, microempreendedor ou outro tipo de pessoa jurídica tem uma atividade
		econômica associada ao seu CNPJ, conforme a Classificação Nacional de Atividades Econômicas
		(CNAE), estabelecida pelo IBGE.
	</p>
	<p class="frase-destaque">
		87,2% das pessoas jurídicas contempladas exercem pelo menos uma atividade econômica diretamente
		ligada à cultura.
	</p>
	<p>
		Considerando o conjunto de atividades econômicas registradas nos CNPJs contemplados pela Aldir
		Blanc, observa-se que a ampla maioria possui ao menos uma atividade diretamente relacionada ao
		setor cultural. As 20 primeiras atividades principais mais recorrentes concentram
		<strong>76,5%</strong> dos recursos repassados para as pessoas jurídicas contempladas.
	</p>
	<p class="frase-destaque">
		CNAEs principais das pessoas jurídicas contempladas evidenciam a diversidade do campo cultural
		contemplado, abrangendo tanto atividades artísticas quanto ações formativas, produção de
		eventos e iniciativas de caráter comunitário.
	</p>
	<p>
		O principal CNAE identificado entre as pessoas jurídicas foi "Atividades de associações de
		defesa de direitos sociais" (<strong>13,7%</strong>), seguido por "Atividades de organizações
		associativas ligadas à cultura e à arte" (<strong>8,5%</strong>).
		<strong>Juntos, esses agentes receberam 30,7% dos recursos repassados, o equivalente a R$266 milhões.</strong>
	</p>
	<div class="cnae-boxes">
		<div class="cnae-box">
			<strong>Educação e cultura</strong>
			<p>
				Entre as pessoas jurídicas contempladas pela PNAB, <strong>14%</strong> têm como CNAE
				principal atividades relacionadas à educação, ensino e formação. Em conjunto, essas
				organizações receberam <strong>10%</strong> dos valores repassados para CNPJs — um total de
				R$158,9 milhões.
			</p>
		</div>
		<div class="cnae-box">
			<strong>Produção de eventos</strong>
			<p>
				A atividade "Serviços de organização de feiras, congressos, exposições e festas" se destaca
				com <strong>7,5%</strong> dos contemplados, concentrando R$100,8 milhões
				(<strong>6,3%</strong> dos recursos).
			</p>
		</div>
		<div class="cnae-box">
			<strong>Produção artístico-cultural</strong>
			<p>
				Produção musical (<strong>7,8%</strong> em quantidade e <strong>5,2%</strong> em valores),
				produção teatral (<strong>3,9%</strong> e <strong>5,1%</strong>) e artes cênicas
				(<strong>2,6%</strong> e <strong>4,7%</strong>) se destacam entre as atividades diretamente
				ligadas à criação cultural.
			</p>
		</div>
		<div class="cnae-box">
			<strong>Empresas do audiovisual</strong>
			<p>
				Representam <strong>4%</strong> das pessoas jurídicas contempladas, com destaque para
				produção e pós-produção de filmes. Receberam <strong>5,9%</strong> dos recursos — R$94,5
				milhões.
			</p>
		</div>
		<div class="cnae-box">
			<strong>Atividades de suporte e execução direta</strong>
			<p>
				A presença de CNAEs como "Construção de edifícios" (<strong>0,6%</strong> e
				<strong>2,4%</strong> em recursos) e atividades de assistência social evidenciam
				organizações cuja atuação não é estritamente cultural, mas que se articulam com o setor.
			</p>
		</div>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     3.3.2 — TOP 20 CNAEs CULTURAIS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-332-cnae-top20">
	<h3>Top 20 CNAEs principais das pessoas jurídicas contempladas</h3>
	<p>Por quantidade de CNPJs contemplados:</p>
	<div style="overflow-x: auto;">
		<svg width={700} height={cnaesQtdTableHeight}>
			<CnaeTable data={top20CnaesQtdTableData} metric="quantidade" width={700} />
		</svg>
	</div>
	<p>Por valor total repassado:</p>
	<div style="overflow-x: auto;">
		<svg width={700} height={cnaesValTableHeight}>
			<CnaeTable data={top20CnaesValTableData} metric="valor" width={700} />
		</svg>
	</div>
</ScrollSection>

<style>
	.bignumbers-row {
		display: flex;
		gap: 2rem;
		flex-wrap: wrap;
		margin-top: 1.5rem;
	}

	.bignumber-cell {
		flex: 1 1 200px;
		min-width: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.5rem;
		margin-top: 1.5rem;
	}

	.bignumber-perc {
		font-size: 1.4rem;
		font-weight: 600;
		text-align: center;
		opacity: 0.65;
		margin: -0.25rem 0 0;
	}

	.bignumber-caption {
		font-size: 0.95rem;
		color: var(--color-text);
		text-align: center;
		opacity: 0.75;
		max-width: 20ch;
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

	.profiles-row {
		display: flex;
		gap: 2rem;
		flex-wrap: wrap;
		margin-top: 1.5rem;
	}

	.profile-card {
		flex: 1 1 280px;
		min-width: 0;
		border: 1px solid currentColor;
		border-radius: 4px;
		overflow: hidden;
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

	.pictogram-caption {
		font-size: 0.8rem;
		opacity: 0.55;
		margin: 0.75rem 0 0.25rem;
		font-style: italic;
	}

	.pictogram-wrap {
		display: flex;
		justify-content: center;
	}

	.pyramid-wrap {
		max-width: 680px;
		margin-inline: auto;
	}

	.donut-single {
		margin-top: 1.5rem;
		max-width: 420px;
		margin-inline: auto;
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
		align-items: center;
	}

	.donut-label {
		font-size: 0.8rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		opacity: 0.55;
		margin: 0 0 0.25rem;
		text-align: center;
	}

	.cnae-boxes {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		margin-top: 1.5rem;
	}

	.cnae-box {
		padding: 1rem 1.25rem;
		border-left: 3px solid currentColor;
		font-size: 0.9rem;
		line-height: 1.6;
		opacity: 0.85;
	}

	.cnae-box strong {
		display: block;
		margin-bottom: 0.35rem;
		font-size: 0.95rem;
	}

	.cnae-box p {
		margin: 0;
	}

	p {
		margin-top: 1.5rem;
	}
</style>
