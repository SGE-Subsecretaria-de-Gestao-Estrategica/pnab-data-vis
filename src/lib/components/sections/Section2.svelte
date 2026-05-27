<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import {
		BigNumber,
		HorizontalBarChart,
		HorizontalStackedBarChart,
		VerticalStackedBarChart,
		DivergingBarChart,
		ProportionalAreaChart,
		BoxPlotChart,
		colorPairs,
		colorScales,
		categorical8,
		AnnotationBox
	} from 'sniic-design-system';
	import {
		percBenefCPF,
		percValorCNPJ,
		totalBenefCPF,
		totalBenefCNPJ,
		valorDivergingData,
		benefVsValorData,
		faixaDistData,
		faixaValorPercData,
		regiaoDistData,
		bandStackedData,
		BAND_STACK_KEYS,
		BAND_LABELS,
		mediaPorTipoData,
		boxPlotData,
		ufBandPercData,
		UF_BAND_KEYS,
		UF_BAND_LABELS,
	} from '$lib/data/section2';

	const formatBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency',
			currency: 'BRL',
			notation: 'compact',
			maximumFractionDigits: 1,
		}).format(v);

	const formatPct = (v: number) =>
		v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

	const formatPctFixed = (v: number) => `${v.toFixed(1)}%`;
</script>

<!-- ══════════════════════════════════════════════════════════════════════════
     GRANDES NÚMEROS — MUITOS CPFs, POUCO DINHEIRO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-bignumber">
	<h2>2. Como os recursos se traduziram em pagamentos aos agentes culturais?</h2>
	<p>
		Depois de entendermos a distribuição dos recursos nos territórios, vamos identificar e analisar a forma como esses recursos foram operacionalizados em pagamentos aos agentes culturais.
	</p>
	<svg width={600} height={130} style="overflow: hidden; margin-top: 1rem;">
		<AnnotationBox
			title=""
			subtitle={"A partir do cruzamento dos dados de agentes culturais contemplados pela Política Nacional Aldir Blanc com bases da Receita Federal."}
			boxX={0}
			boxY={0}
			boxWidth={600}
			pointX={-30}
			pointY={63}
			showTitle={false}
			circleRadius={0}
		/>
	</svg>
	<h2>Como os pagamentos foram estruturados?</h2>
	<p>Como vimos no capítulo anterior, entre os <strong>166.886</strong> agentes culturais contemplados, 81% são pessoas físicas e 19% são pessoas jurídicas.</p>
	
	<ScrollSection id="section-2-faixas-bignumbers">
		<div class="faixas-bignumbers-row">
			<div class="faixa-bignumber-cell">
				<BigNumber value={29} suffix="%" fontSize={64} />
				<p class="faixa-bignumber-count">49.037 agentes</p>
				<p class="faixa-bignumber-caption">receberam até R$2 mil</p>
			</div>
			<div class="faixa-bignumber-cell">
				<BigNumber value={42} suffix="%" fontSize={64} />
				<p class="faixa-bignumber-count">70.493 agentes</p>
				<p class="faixa-bignumber-caption">receberam entre R$2 e R$10 mil</p>
			</div>
			<div class="faixa-bignumber-cell">
				<BigNumber value={23} suffix="%" fontSize={64} />
				<p class="faixa-bignumber-count">37.661 agentes</p>
				<p class="faixa-bignumber-caption">receberam entre R$10 e R$50 mil</p>
			</div>
			<div class="faixa-bignumber-cell">
				<BigNumber value={5} suffix="%" fontSize={64} />
				<p class="faixa-bignumber-count">8.348 agentes</p>
				<p class="faixa-bignumber-caption">receberam entre R$50 e R$200 mil</p>
			</div>
			<div class="faixa-bignumber-cell">
				<BigNumber value={1} suffix="%" fontSize={64} />
				<p class="faixa-bignumber-count">1.347 agentes</p>
				<p class="faixa-bignumber-caption">receberam mais de R$200 mil</p>
			</div>
		</div>
	</ScrollSection>

	<ScrollSection id="section-2-faixas-valor">
		<h3>Onde está o dinheiro? A concentração nas faixas intermediárias</h3>
		<p>
			Enquanto a maioria dos agentes recebe valores pequenos, o grosso dos recursos se concentra
			nas faixas intermediárias e altas. As faixas de <strong>R$10 a R$200 mil</strong> absorvem
			<strong>60%</strong> do total executado.
		</p>
		<HorizontalBarChart
			data={faixaValorPercData}
			color={colorScales.blue[2]}
			format={formatPct}
			xLabel="% do valor total"
			margin={{ top: 20, right: 80, bottom: 40, left: 200 }}
		/>
		<p>Aproximadamente R$ 2,1 bilhões, o equivalente a 75% do orçamento total executado, foram destinados a mais de 165 mil agentes culturais, o que representa 99% do total dos contemplados da política. Esse volume de recursos financiou projetos, bolsas e subsídios com valores individuais de até R$ 200 mil.</p>
		<p>Do ponto de vista da distribuição dos pagamentos, observa-se forte predominância de repasses de menor valor:  71% dos agentes culturais receberam até 10 mil reais. Embora tais pagamentos sejam majoritários em termos de quantidade de agentes, eles representam uma fração reduzida do orçamento (15%).</p>
		<p>As faixas intermediárias, entre R$ 10 mil e R$ 200 mil, desempenham papel central, representando 60% dos recursos. Essas compreendem cerca de 30% dos agentes culturais contemplados.</p>
		<p>Diante desses dados, percebe-se que a execução da Aldir Blanc articula alcance social ampliado e financiamento de projetos de diferentes escalas, sem se restringir a um único perfil de beneficiário ou de valor.</p>
	</ScrollSection>
	
	<ScrollSection id="section-2-distribuicao-pagamentos">
		<h2>Distribuição de pagamentos por região</h2>
		<p>Veremos a seguir como foi a distribuição da quantidade de pagamentos da Política pelas regiões do país.</p>
		<HorizontalBarChart       
     		data={regiaoDistData}   
     		color={colorScales.blue[
          +2]}                           
      		format={formatPct}      
      		xLabel="% dos agentes culturais"                      
      		margin={{ top: 20, right:80, bottom: 40, left: 140 }}
      	/>
		<p>As regiões Norte, Centro-Oeste e Sul apresentaram uma proporção de agentes culturais contemplados com  recursos da Aldir Blanc muito semelhante à participaçãoproporção de sua população em relação à população nacional.</p>
		<p><strong>Maior distribuição:</strong> a região Nordeste liderou a distribuição de recursos da política, beneficiando o maior número de agentes culturais, com 47,7% do total de contemplados da Aldir Blanc, quase metade do total.</p>
		<p><strong>Menor distribuição:</strong> o Sudeste apresentou uma proporção de agentes culturais contemplados inferior à proporção da população nacional. Isso indica que a região concentrou mais os recursos em um número menor de agentes.</p>

		<!-- ══════════════════════════════════════════════════════════════════════════
     	VERTICAL STACKED — FAIXA DE VALOR PAGO × UF
    	 ══════════════════════════════════════════════════════════════════════════ -->
		<h3>Qual o perfil de pagamentos de cada estado?</h3>
		<p>
			Cada barra representa um estado, ordenado pelos que têm <strong>maior proporção de
			beneficiários nas faixas mais altas</strong> (acima de R$50 mil) — à esquerda estão
			os estados com mais pagamentos concentrados em valores elevados; à direita, os que
			atendem quase exclusivamente faixas pequenas.
		</p>
		<p>
			Estados como <strong>DF, RJ e SP</strong> têm fatias relevantes acima de R$50 mil —
			reflexo do peso de CNPJs e entidades de maior porte nesses territórios.
			No extremo oposto, estados do Nordeste como <strong>PI, PB e RN</strong> têm suas barras
			dominadas pelas faixas de até R$10 mil, indicando que o programa atinge principalmente
			pequenos agricultores e extrativistas nesses locais.
		</p>
		<div class="chart-wide">
			<VerticalStackedBarChart
				data={ufBandPercData}
				keys={[...UF_BAND_KEYS]}
				labels={UF_BAND_LABELS}
				colors={categorical8}
				format={(v:any) => `${v.toFixed(1)}%`}
				yLabel="% dos beneficiários"
				normalize={true}
				showLegend={true}
				height={480}
			/>
		</div>
	</ScrollSection>

	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber
				value={percBenefCPF.toFixed(1)}
				suffix="%"
				fontSize={80}
			/>
			<p class="bignumber-caption">dos beneficiários são pessoas físicas (CPF)</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber
				value={percValorCNPJ.toFixed(1)}
				suffix="%"
				fontSize={80}
			/>
			<p class="bignumber-caption">do valor total foi para entidades (CNPJ)</p>
		</div>
	</div>
	<p>
		São <strong>{totalBenefCPF.toLocaleString('pt-BR')}</strong> pessoas físicas contra
		<strong>{totalBenefCNPJ.toLocaleString('pt-BR')}</strong> entidades — uma razão de quase
		<strong>4 para 1</strong> em número, mas o dinheiro segue na direção oposta.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     DIVERGING — A DIVISÃO DO VALOR POR ESFERA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-diverging">
	<h3>O desequilíbrio varia por esfera — e é maior nos estados</h3>
	<p>
		A proporção do valor destinada a CPF ou CNPJ muda conforme a esfera executora.
		Nos repasses <strong>estaduais</strong>, o CNPJ domina com quase dois terços do valor
		(64,7%) — mesmo representando apenas 32% dos beneficiários desse nível.
		Nos <strong>municípios</strong>, a divisão é quase equilibrada (53/47%), mas o CNPJ
		ainda supera sua representação em número de beneficiários (17%).
	</p>
	<DivergingBarChart
		data={valorDivergingData}
		leftLabel="CPF — % do valor"
		rightLabel="CNPJ — % do valor"
		referenceValue={50}
		referenceLabel="Equidade"
		colors={colorPairs.blueOrange}
		marginLeft={220}
	/>
	<h4 class="subsection-label">O "flip": beneficiários vs valor recebido</h4>
	<p>
		A inversão fica explícita quando comparamos as duas dimensões lado a lado.
		No eixo de <strong>beneficiários</strong>, o CPF domina com 80,7%.
		No eixo de <strong>valor recebido</strong>, o CNPJ vira maioria (55,9%).
		A mesma esquerda-direita, lados trocados.
	</p>
	<HorizontalStackedBarChart
		data={benefVsValorData}
		keys={['cpf', 'cnpj']}
		labels={{ cpf: 'CPF', cnpj: 'CNPJ' }}
		colors={colorPairs.blueOrange}
		format={formatPctFixed}
		showTotalLabel={false}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     HORIZONTAL BAR — DISTRIBUIÇÃO NACIONAL POR FAIXA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-faixas">
	<h3>A maioria recebe menos de R$10 mil</h3>
	<p>
		Olhando todos os <strong>166.886 beneficiários</strong> do Brasil, a distribuição é
		fortemente concentrada nos valores mais baixos. Mais de <strong>71%</strong> receberam
		até R$10 mil — enquanto menos de <strong>0,1%</strong> recebeu acima de R$500 mil.
		A cauda direita existe, mas é muito fina.
	</p>
	<HorizontalBarChart
		data={faixaDistData}
		color={colorScales.blue[2]}
		format={formatPct}
		xLabel="% dos beneficiários"
		margin={{ top: 20, right: 80, bottom: 40, left: 160 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     STACKED — FAIXAS POR TIPO CPF vs CNPJ
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-faixas-tipo">
	<h3>Perfis completamente opostos: CPF concentrado em baixo valor, CNPJ distribuído até milhões</h3>
	<p>
		Quando separamos CPF de CNPJ, surgem dois mundos diferentes.
		As <strong>pessoas físicas</strong> se concentram nas faixas de até R$10 mil —
		mais de <strong>79%</strong> dos seus beneficiários estão ali.
		As <strong>entidades</strong> têm distribuição muito mais espalhada: quase
		<strong>57%</strong> receberam acima de R$10 mil, e há beneficiários em todas
		as faixas até dezenas de milhões.
	</p>
	<HorizontalStackedBarChart
		data={bandStackedData}
		keys={BAND_STACK_KEYS}
		labels={BAND_LABELS}
		colors={categorical8}
		format={formatPctFixed}
		showTotalLabel={false}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PROPORCIONAL — VALOR MÉDIO POR BENEFICIÁRIO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-proporcional">
	<h3>Em média, cada CNPJ recebe 6,5× mais que cada CPF</h3>
	<p>
		A área de cada círculo é proporcional ao <strong>valor médio recebido por beneficiário</strong>.
		O CNPJ registra uma média de <strong>R$62.742</strong> por entidade;
		o CPF, apenas <strong>R$9.634</strong> por pessoa.
		A diferença de escala — visível na área — resume em forma o que os números dizem:
		cada entidade recebe, em média, o equivalente ao que <strong>6,5 pessoas físicas</strong>
		receberiam juntas.
	</p>
	<ProportionalAreaChart
		data={mediaPorTipoData}
		maxRadius={130}
		colors={colorPairs.blueOrange}
		format={formatBRL}
		showLabels={true}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     BOXPLOT — DISPERSÃO DE VALORES CPF vs CNPJ
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-2-boxplot">
	<h3>A dispersão revela a concentração extrema do CNPJ</h3>
	<p>
		O box plot compara a distribuição completa de valores entre CPF e CNPJ.
		A <strong>mediana do CPF</strong> é R$3.800 — metade das pessoas físicas recebeu
		menos do que isso. A <strong>mediana do CNPJ</strong> é R$13.500 — mais de três vezes maior.
	</p>
	<p>
		Mas o contraste mais expressivo está na dispersão: a caixa do CNPJ
		(entre Q1 e Q3, estimados por interpolação nas faixas de valor)
		se estende de ~R$6.400 a ~R$45.600, enquanto a do CPF vai de ~R$1.500 a ~R$9.300.
		O Q1 do CNPJ já supera o Q3 do CPF. São distribuições que mal se tocam.
	</p>
	<BoxPlotChart
		data={boxPlotData}
		xLabel="Tipo de beneficiário"
		yLabel="Valor recebido (R$)"
		format={formatBRL}
		showOutliers={false}
	/>
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
	}

	.bignumber-caption {
		font-size: 0.95rem;
		color: var(--color-text);
		text-align: center;
		opacity: 0.75;
		max-width: 20ch;
	}

	.subsection-label {
		margin-top: 2.5rem;
	}

	:global(#section-2-faixas-bignumbers) {
		margin: 0;
		min-height: unset;
		padding: 0;
	}

	.faixas-bignumbers-row {
		display: grid;
		grid-template-columns: auto auto 1fr;
		align-items: center;
		column-gap: 1.5rem;
		row-gap: 0.5rem;
		margin-top: 1.5rem;
	}

	.faixa-bignumber-cell {
		display: contents;
	}

	.faixa-bignumber-count {
		font-size: 1.4rem;
		font-weight: 600;
		color: var(--color-text);
		margin: 0;
	}

	.faixa-bignumber-caption {
		font-size: 1.2rem;
		color: var(--color-text);
		opacity: 0.75;
		margin: 0;
	}

	.chart-wide {
		overflow-x: auto;
		margin-left: -1rem;
		margin-right: -1rem;
	}

	.section-2-faixas-valor {
		padding: 0;
	}

	p {
		margin-top: 1.5rem;
	}

</style>
