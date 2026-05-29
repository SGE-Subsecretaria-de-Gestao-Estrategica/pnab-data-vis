<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import {
		BigNumber,
		HorizontalBarChart,
		VerticalStackedBarChart,
		BoxPlotChart,
		AnnotationBox,
		colorScales,
		categorical8,
	} from 'sniic-design-system';
	import {
		faixaDistData,
		faixaValorPercData,
		regiaoDistData,
		ufBandPercData,
		UF_BAND_KEYS,
		UF_BAND_LABELS,
		stateBandPercData,
		portePagamentosData,
		PORTE_BAND_KEYS,
		PORTE_BAND_LABELS,
		specialTerritoryBarData,
		terrEspeciaisData,
		TERR_KEYS,
		TERR_LABELS,
		estadosBoxPlotData,
	} from '$lib/data/section2';
	import { HorizontalStackedBarChart, categorical3 } from 'sniic-design-system';

	const formatBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency',
			currency: 'BRL',
			notation: 'compact',
			maximumFractionDigits: 1,
		}).format(v);

	const formatPct  = (v: number) =>
		v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';
	const formatPctFixed = (v: number) => `${v.toFixed(1)}%`;
</script>

<!-- ══════════════════════════════════════════════════════════════════════════
     INTRODUÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-intro">
	<h2>2. Como os recursos foram distribuídos aos agentes culturais?</h2>
	<p>
		Depois de entendermos a distribuição dos recursos nos territórios, vamos identificar e analisar as tendências da distribuição dos recursos para os contemplados da Aldir Blanc.
	</p>
	<svg width={600} height={220} style="overflow: hidden; margin-top: 1rem;">
		<AnnotationBox
			title=""
			subtitle={'As análises apresentadas neste capítulo resultam do banco de dados do BB\nágil e cruzamentos entre a quantidade de pagamentos e o recurso executado\ncom variáveis territoriais (unidade federativa, região, estado, municípios e\nterritórios especiais) e faixas de valores. O BB ágil registra o repasse de\nrecursos dos entes federados para os agentes contemplados pela Política\nNacional Aldir Blanc, podendo uma mesma pessoa ou organização ter recebido\nmais de uma vez, por mais de um ente. Assim, ao longo do texto utilizamos os\ntermos "contemplados", "agentes culturais contemplados" para fazer referência\na esta característica da base de dados.'}
			boxX={0}
			boxY={0}
			boxWidth={560}
			pointX={-30}
			pointY={82}
			showTitle={false}
			circleRadius={0}
		/>
	</svg>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.1 / 2.1.1 — DISTRIBUIÇÃO POR FAIXAS DE VALORES (NACIONAL)
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-21">
	<h2>2.1. Como os pagamentos e recursos foram distribuídos?</h2>
	<h3>2.1.1. Distribuição de pagamentos e recursos nas unidades federativas, por faixas de valores</h3>
	<p>
		Para analisar se houve concentração dos recursos em poucos contemplados, analisamos os pagamentos realizados pelas unidades federativas, por faixas de valores.
	</p>
	<p>
		Do ponto de vista da distribuição dos pagamentos, observa-se forte predominância de repasses de menor valor: <strong>71,6%</strong> dos contemplados receberam valores até 10 mil reais. Do outro lado, contemplados que receberam valores acima de 200 mil reais representam somente <strong>0,8%</strong> dos contemplados pela Aldir Blanc.
	</p>
	<p>
		Embora a maioria dos contemplados estejam concentrados nas faixas de valores até 10 mil reais, os recursos repassados para este grupo representam somente <strong>15,2%</strong> dos recursos totais executados pela Aldir Blanc. A maior parte do recurso (<strong>31,5%</strong>) foi destinado para contemplados que receberam entre R$ 10 mil e R$ 50 mil.
	</p>
	<HorizontalBarChart
		data={faixaDistData}
		color={colorScales.blue[2]}
		format={formatPct}
		xLabel="% dos contemplados"
		margin={{ top: 20, right: 80, bottom: 40, left: 200 }}
	/>
	<HorizontalBarChart
		data={faixaValorPercData}
		color={colorScales.blue[2]}
		format={formatPct}
		xLabel="% do valor total executado"
		margin={{ top: 20, right: 80, bottom: 40, left: 200 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.1.1 — DISTRIBUIÇÃO POR UF E FAIXA (STACKED)
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-uf-faixas">
	<div class="chart-wide">
		<VerticalStackedBarChart
			data={ufBandPercData}
			keys={[...UF_BAND_KEYS]}
			labels={UF_BAND_LABELS}
			colors={categorical8}
			format={formatPctFixed}
			yLabel="% dos contemplados"
			normalize={true}
			showLegend={true}
			height={480}
		/>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.2 — DISTRIBUIÇÃO NOS ESTADOS (REGIÕES)
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-22">
	<h2>2.2. Como os pagamentos e recursos foram distribuídos nos Estados?</h2>
	<p>
		Veremos a seguir como foi a distribuição da quantidade de pagamentos da Política pelas regiões do país.
	</p>
	<div class="regioes-list">
		<p><strong>14.504 (8,7%)</strong> contemplados no Norte</p>
		<p><strong>79.446 (47,6%)</strong> contemplados no Nordeste</p>
		<p><strong>9.335 (5,6%)</strong> contemplados no Centro-Oeste</p>
		<p><strong>45.655 (27,4%)</strong> contemplados no Sudeste</p>
		<p><strong>17.946 (10,8%)</strong> contemplados no Sul</p>
	</div>
	<HorizontalBarChart
		data={regiaoDistData}
		color={colorScales.blue[2]}
		format={formatPct}
		xLabel="% dos agentes culturais"
		margin={{ top: 20, right: 80, bottom: 40, left: 140 }}
	/>
	<p>
		As regiões Norte, Centro-Oeste e Sul apresentaram uma proporção de agentes culturais contemplados com recursos da Aldir Blanc muito semelhante à participação de sua população em relação à população nacional.
	</p>
	<p>
		A região Nordeste liderou em quantidade de contemplados, com <strong>47,7%</strong> do total de contemplados da Aldir Blanc, quase metade do total. Já o Sudeste apresentou uma proporção de agentes culturais contemplados inferior à proporção da população nacional. Isso indica que a região concentrou mais os recursos em um número menor de agentes.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.2.1 — DISTRIBUIÇÃO POR FAIXAS NOS ESTADOS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-221">
	<h3>2.2.1. Distribuição de pagamentos e recursos nos Estados, por faixas de valores</h3>
	<p>
		Ao analisar as faixas de valores conseguimos visualizar como cada Estado escolheu distribuir os recursos.
	</p>
	<p>
		Este gráfico apresenta como os contemplados pelos Estados foram distribuídos nas faixas de valores analisadas, a partir dos valores que receberam. Pode-se ver que a maioria dos contemplados na Aldir Blanc receberam valores entre 10 e 50 mil reais, o que equivale a <strong>51,9%</strong>.
	</p>
	<p>
		Os contemplados com valores entre 50 e 200 mil reais se destacam como o segundo grupo mais representativo, responsáveis por <strong>22,3%</strong> do total. Os estados do Rio Grande do Sul (71,5%), Mato Grosso (70,3%), Distrito Federal (63,2%), Goiás (45,9%) e Rio de Janeiro (43,6%) apresentaram as maiores proporções de recursos destinados aos contemplados nessa faixa de valor.
	</p>
	<p>
		Por outro lado, os contemplados que receberam entre 2 e 10 mil reais aparecem logo em seguida, representando <strong>20,3%</strong> do total dos contemplados pelos Estados. Paraíba (49,7%), Rondônia (48,4%), Piauí (46,6%), Mato Grosso do Sul (46%) e Roraima (44,2%) foram os Estados que mais fizeram pagamentos para contemplados nesta faixa de valor.
	</p>
	<div class="chart-wide">
		<VerticalStackedBarChart
			data={stateBandPercData}
			keys={[...UF_BAND_KEYS]}
			labels={UF_BAND_LABELS}
			colors={categorical8}
			format={formatPctFixed}
			yLabel="% dos contemplados"
			normalize={true}
			showLegend={true}
			height={480}
		/>
	</div>
	<p style="margin-top: 1.5rem;">
		Enquanto a maioria dos pagamentos ficaram na faixa de valor de 10 a 50 mil reais, a maior parte dos recursos executados pelos Estados se encontram na faixa de valor de 50 a 200 mil reais (<strong>35,1%</strong>). É um padrão observado na maioria dos estados, sobretudo no Rio Grande do Sul (69,4%), Mato Grosso (59,4%) e Piauí (58%).
	</p>
	<p>
		Amapá, Distrito Federal, Pará e São Paulo se destacam dessa tendência, ao destinar mais de <strong>60%</strong> do total de recursos executados a pagamentos acima de 200 mil reais.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.2.2 — TENDÊNCIAS, DISTRIBUIÇÕES E CONCENTRAÇÕES NOS ESTADOS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-222">
	<h3>2.2.2. Tendências, distribuições e concentrações nos Estados</h3>
	<p>
		A organização dos recursos por quartis possibilita analisar a distribuição dos pagamentos de menores e maiores valores. Nesse sentido, observou-se que os valores do primeiro quartil situaram-se, em geral, entre 10 e 30 mil reais, enquanto os valores do terceiro quartil concentraram-se predominantemente entre 30 e 80 mil reais na maior parte dos estados.
	</p>
	<div class="chart-wide">
		<BoxPlotChart
			data={estadosBoxPlotData}
			xLabel="Estado"
			yLabel="Valor recebido (R$)"
			format={formatBRL}
			showOutliers={false}
			height={440}
		/>
	</div>
	<p style="margin-top: 1.5rem;">
		O Estado de Rondônia se destaca por apresentar o menor valor no primeiro quartil, indicando que os menores pagamentos realizados pelo estado foram inferiores aos observados pelos demais estados (R$ 2.893). São Paulo aparece no outro extremo, com o maior valor no terceiro quartil, evidenciando a presença de pagamentos mais elevados dentre todos os estados (R$ 30.000).
	</p>
	<p>
		O cálculo da mediana permite identificar os valores centrais dos pagamentos no universo analisado. A partir desta análise, percebemos que os Estados tiveram uma tendência de realizar pagamentos em torno de <strong>R$ 30.000</strong> para seus contemplados.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.3 — MUNICÍPIOS — GRANDES NÚMEROS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-23">
	<h2>2.3. Como os pagamentos e recursos foram distribuídos nos municípios?</h2>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="144.836" fontSize={72} />
			<p class="bignumber-perc">(86,8%)</p>
			<p class="bignumber-caption">dos contemplados totais da Aldir Blanc receberam recursos através dos municípios</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="R$1,4bi" fontSize={72} />
			<p class="bignumber-perc">(49%)</p>
			<p class="bignumber-caption">foi o valor executado pelos municípios</p>
		</div>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.3.1 — DISTRIBUIÇÃO NOS MUNICÍPIOS POR PORTE
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-231">
	<h3>2.3.1. Distribuição dos pagamentos e recursos nos municípios</h3>
	<p>
		Municípios de diferentes portes populacionais distribuíram de forma distinta os pagamentos aos seus contemplados. Enquanto os municípios de pequeno e médio porte concentraram os pagamentos em valores até 10 mil reais, os municípios de grande porte concentraram os pagamentos na faixa de valor de 10 a 50 mil reais.
	</p>
	<p>
		Nos municípios de pequeno porte I, <strong>91,3%</strong> dos contemplados receberam até R$ 10 mil. Dentro desse grupo, <strong>50,1%</strong> receberam pagamentos de até R$ 2 mil. Essa concentração nas faixas de menor valor também se mantém elevada nos municípios de pequeno porte II, onde <strong>87,7%</strong> dos contemplados receberam até R$ 10 mil, e nos municípios de médio porte, com <strong>75,9%</strong>. Já nos municípios de grande porte, a participação dos pagamentos de até R$ 10 mil cai para <strong>49%</strong>. Nesse grupo, a faixa de R$ 10 mil a R$ 50 mil representa, sozinha, <strong>42,7%</strong> dos pagamentos.
	</p>
	<div class="chart-wide">
		<VerticalStackedBarChart
			data={portePagamentosData}
			keys={[...PORTE_BAND_KEYS]}
			labels={PORTE_BAND_LABELS}
			colors={categorical8}
			format={formatPctFixed}
			yLabel="% dos contemplados"
			normalize={true}
			showLegend={true}
			height={420}
		/>
	</div>
	<p style="margin-top: 1.5rem;">
		Nos municípios de pequeno porte I e II, observa-se uma concentração do recurso executado na faixa de R$ 2 mil a R$ 10 mil. Já nos municípios de médio e grande porte, percebe-se a destinação do recurso para faixas de maiores valores, com a concentração presente na faixa de R$ 10 mil a R$ 50 mil.
	</p>
	<p>
		Quando observados todos os municípios da base em conjunto, <strong>70,3%</strong> dos recursos executados se concentraram em pagamentos de até R$ 50 mil.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.3.2 — TENDÊNCIAS, DISTRIBUIÇÕES E CONCENTRAÇÕES NOS MUNICÍPIOS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-232">
	<h3>2.3.2. Tendências, distribuições e concentrações nos municípios</h3>
	<p>
		A análise dos quartis mostra uma tendência já esperada por parte dos municípios, em que municípios de pequeno porte repassaram menores valores, enquanto municípios de grande porte destinaram maiores valores para seus contemplados. Enquanto a tendência dos valores do primeiro quartil nos municípios de pequeno porte I foi de <strong>R$ 1.013</strong>, nos municípios de grande porte o primeiro quartil ficou em <strong>R$ 5.000</strong>, indicando valores mais elevados mesmo entre os contemplados que receberam menos recursos.
	</p>
	<p>
		Por outro lado, os valores do terceiro quartil nos municípios de grande porte chegaram a <strong>R$ 25.000</strong>, valor cerca de 5 vezes maior que o terceiro quartil observado nos municípios de pequeno porte (<strong>R$ 4.600</strong>). Esse resultado sugere uma tendência de maior concentração de pagamentos em faixas mais elevadas nos municípios de grande porte.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.4 — TERRITÓRIOS ESPECIAIS — GRANDES NÚMEROS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-special">
	<h2>2.4. Como os pagamentos e recursos foram distribuídos nos territórios especiais?</h2>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="5.290" fontSize={72} />
			<p class="bignumber-perc">(3,2% do total)</p>
			<p class="bignumber-caption">pagamentos direcionados para contemplados em agrupamentos indígenas, quilombolas e favelas e comunidades urbanas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="R$150,6mi" fontSize={72} />
			<p class="bignumber-perc">(5,3% do total)</p>
			<p class="bignumber-caption">foi o valor total repassado para estes contemplados</p>
		</div>
	</div>
	<p style="margin-top: 2rem;">
		Mais da metade do recurso destinado para territórios especiais foi feito por quatro unidades federativas: Pará, Amazonas, Bahia e Pernambuco. Só o governo do estado e os municípios do Pará foram responsáveis por destinar o equivalente a <strong>22,6%</strong> dos recursos para estes territórios.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.4 — TERRITÓRIOS ESPECIAIS — GRÁFICO POR UF
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-special-uf">
	<div class="chart-wide">
		<HorizontalStackedBarChart
			data={terrEspeciaisData}
			keys={[...TERR_KEYS]}
			labels={TERR_LABELS}
			colors={categorical3}
			format={formatBRL}
			showTotalLabel={true}
			rowHeight={36}
		/>
	</div>
	<p style="margin-top: 1.5rem;">
		Do montante total destinado aos territórios especiais, <strong>R$ 91.459.463 (60,7%)</strong> foram destinados pelos governos estaduais. Esse valor representa 6,3% de todo o recurso executado pelos Estados.
	</p>
	<p>
		Destacam-se os governos estaduais do Pará, Amapá e Amazonas que, proporcionalmente, mais destinaram recursos para os territórios especiais. O Pará destinou <strong>37,8%</strong> dos recursos executados, o Amapá direcionou <strong>27,6%</strong> e o Amazonas direcionou <strong>23,3%</strong>.
	</p>
	<p>
		Somente 10 Estados destinaram recursos para os três territórios especiais trabalhados pela pesquisa: Minas Gerais, Pernambuco, Bahia, Rio Grande do Norte, Ceará, Paraná, Santa Catarina, Alagoas, Paraíba e Mato Grosso do Sul.
	</p>
	<p>
		Já entre os municípios, <strong>49,8%</strong> dos contemplados em territórios especiais receberam pagamentos através dos municípios de grande porte. Foram estes municípios que também direcionaram a maior quantidade de recursos para os territórios especiais: <strong>R$ 47.049.600</strong>, o equivalente a 79,6% do valor total destinado pelos municípios.
	</p>
	<p>
		A partir da análise da mediana, percebe-se que a tendência dos pagamentos destinados aos territórios especiais se concentraram na faixa de R$ 10 mil a R$ 50 mil.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.4 — AGRUPAMENTOS INDÍGENAS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-indigenas">
	<h3>Tendências dos pagamentos e recursos destinados aos agrupamentos indígenas</h3>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="R$5,1mi" fontSize={64} />
			<p class="bignumber-caption">foi o valor total destinado aos agrupamentos indígenas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="254" fontSize={64} />
			<p class="bignumber-caption">foi o total de contemplados destes territórios que receberam recursos</p>
		</div>
	</div>
	<p style="margin-top: 1.5rem;">
		A maioria dos pagamentos das Unidades Federativas direcionados para os agrupamentos indígenas foram na faixa de valor de 2 até 10 mil reais.
	</p>
	<p>
		Ao todo, os Estados destinaram <strong>R$ 3.969.151</strong> para os agrupamentos indígenas, o que representa <strong>0,3%</strong> dos recursos executados pelos Estados.
	</p>
	<p>
		Os governos estaduais da Paraíba, Pernambuco e Mato Grosso do Sul foram os Estados que mais fizeram pagamentos para agrupamentos indígenas. O recurso destinado pelo Governo da Paraíba corresponde a <strong>25%</strong> do valor total destinado por entes estaduais aos agrupamentos indígenas.
	</p>
	<p>
		Os municípios fizeram <strong>143 pagamentos</strong> para agrupamentos indígenas, com 44% desses pagamentos feitos por municípios de Pequeno Porte I. Os contemplados pelos municípios em agrupamentos indígenas, no geral, receberam recursos na faixa de valor de 2 a 10 mil reais.
	</p>
	<p>
		Já a maior parte dos recursos destinados por municípios aos territórios indígenas foram provenientes dos municípios de Grande Porte, responsáveis por um aporte de <strong>R$ 666.694 (60%)</strong>.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.4 — AGRUPAMENTOS QUILOMBOLAS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-quilombolas">
	<h3>Tendências dos pagamentos e recursos destinados aos agrupamentos quilombolas</h3>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="R$7,4mi" fontSize={64} />
			<p class="bignumber-caption">foi o recurso total destinado aos agrupamentos quilombolas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="481" fontSize={64} />
			<p class="bignumber-caption">foi o total de pagamentos feitos para contemplados destes territórios</p>
		</div>
	</div>
	<p style="margin-top: 1.5rem;">
		Bahia, Maranhão e Minas Gerais foram as Unidades Federativas que fizeram mais pagamentos para contemplados em agrupamentos quilombolas. A Bahia, sozinha, é responsável por <strong>39,5%</strong> destes pagamentos e os três estados juntos foram responsáveis por <strong>52,8%</strong> dos recursos destinados a este território: um total de R$ 3.891.114.
	</p>
	<p>
		Esse destaque da Bahia se deve, no entanto, aos municípios do Estado, que foram responsáveis por <strong>177 dos 190 pagamentos</strong> destinados a contemplados em agrupamentos quilombolas.
	</p>
	<p>
		O Governo de Minas Gerais foi o que destinou, proporcionalmente, o maior valor em relação ao total destinado pelos Estados para os contemplados em territórios quilombolas: cerca de <strong>23,5%</strong> dos mais de 1 milhão de reais. Em sua maioria, os pagamentos de Minas Gerais foram na faixa de valor de 10 a 50 mil reais.
	</p>
	<p>
		Já entre os municípios, os de Pequeno Porte I concentraram <strong>43,2%</strong> dos 391 pagamentos realizados. Em termos de valor, a maior participação ficou com os municípios de Grande Porte, responsáveis por <strong>34%</strong> dos quase R$ 3 milhões executados.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     2.4 — FAVELAS E COMUNIDADES URBANAS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-favelas">
	<h3>Tendências dos pagamentos e recursos destinados às favelas e comunidades urbanas</h3>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="R$138mi" fontSize={64} />
			<p class="bignumber-caption">foi o valor total destinado às favelas e comunidades urbanas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value="4.555" fontSize={64} />
			<p class="bignumber-caption">foi o total de pagamentos feitos para contemplados destes territórios</p>
		</div>
	</div>
	<p style="margin-top: 1.5rem;">
		Os contemplados de favelas e comunidades urbanas receberam <strong>86,1%</strong> dos pagamentos direcionados aos territórios especiais e foram destinatários de <strong>91,7%</strong> de todo o recurso destinado a esses territórios.
	</p>
	<p>
		Pará, Pernambuco e Bahia foram as Unidades Federativas responsáveis pela maior parte dos pagamentos. No Pará, o Governo do Estado e os municípios, somados, também foram responsáveis por quase <strong>24,5%</strong> de todo o recurso destinado às favelas e comunidades urbanas, um montante equivalente a R$ 33.878.759.
	</p>
	<p>
		Este destaque do Pará se deve à atuação do Governo do Estado, que foi responsável por <strong>81,2%</strong> de todo recurso repassado pela Unidade Federativa para as favelas e comunidades urbanas, um montante de R$ 27.501.773.
	</p>
	<p>
		Os estados foram responsáveis por <strong>60%</strong> de todo o valor repassado para contemplados em favelas e comunidades urbanas e, juntos, o Pará, Amazonas, Pernambuco e Bahia foram os que mais destinaram recursos para estes territórios. Mato Grosso foi o único estado que não direcionou recursos para contemplados em favelas e comunidades urbanas.
	</p>
	<p>
		A maioria dos pagamentos realizados pelos estados ficaram na faixa entre 10 e 50 mil reais.
	</p>
	<p>
		Os <strong>40%</strong> de recursos destinados pelos municípios aos contemplados em favelas e comunidades urbanas ficaram, em sua maioria, sob responsabilidade dos municípios de Grande Porte: estes foram responsáveis por <strong>R$ 45.395.705</strong>, um equivalente a 55,6% de todo o recurso repassado por municípios do país.
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
		max-width: 22ch;
	}

	.regioes-list {
		margin: 1.5rem 0;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.regioes-list p {
		margin: 0;
		font-size: 1.1rem;
	}

	.chart-wide {
		overflow-x: auto;
		margin-left: -1rem;
		margin-right: -1rem;
	}

	p {
		margin-top: 1.5rem;
	}
</style>
