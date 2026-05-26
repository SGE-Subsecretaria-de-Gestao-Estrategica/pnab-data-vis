<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import ExecutedValueByStateMap from '$lib/components/ExecutedValueByStateMap.svelte';
	import {
		BigNumber,
		HorizontalBarChart,
		HorizontalStackedBarChart,
		DivergingBarChart,
		BubbleChart,
		ProportionalAreaChart,
		SlopeGraph,
		BoxPlotChart,
		HeatMap,
		TreemapChart,
		DataTable,
		RegionSilhouetteChart,
		StatesSilhouetteChart,
		AnnotationBox,
		colorPairs,
		colorScales,
		categorical8,
	} from 'sniic-design-system';
	import {
		percExecEstados, percExecMunicipios,
		valorExecEstados, valorExecMunicipios, valorExecTotal,
		regionAreaData,
		rankingData, bubbleStateData,
		slopeItems, slopeLabels, formatSlope,
		boxPlotData, regionMedianData,
		heatmapData,
		percapitaData, ufSplitData,
		zoneData,
		porteTreemapData, porteDivergingData, porteBubbleData,
		porteStackedKeys, porteStackedLabels, porteStackedData,
		percRecursoEspecial, percPopulacaoEspecial, specialDivergingData,
		specialStackedData,
		ufData,
		silhouetteStateData,
		silhouetteRegionData,
		silhouetteRegionPopData,
		states,
	} from '$lib/data/section1';

	// ── Flags via import.meta.glob ──────────────────────────────────────────────
	const flagModules = import.meta.glob(
		'/node_modules/sniic-design-system/dist/flags/states/*.svg',
		{ query: '?url', import: 'default', eager: true }
	);
	const stateFlags = Object.fromEntries(
		Object.entries(flagModules).map(([path, url]) => {
			const uf = path.split('/').pop()!.replace('.svg', '');
			return [uf, url as string];
		})
	);

	// ── Formatadores ────────────────────────────────────────────────────────────
	const formatBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);
	const formatBRLM  = (v: number) => `R$ ${(v / 1e6).toFixed(1)}M`;
	const formatBRLpc = (v: number) =>
		`R$ ${v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
	const formatPercPt  = (v: number) =>
		v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';
	const formatPercFix = (v: number) => `${v.toFixed(1)}%`;
	const formatPop     = (v: number) =>
		new Intl.NumberFormat('pt-BR', { notation: 'compact', maximumFractionDigits: 1 }).format(v);

	// ── Tabela UF ────────────────────────────────────────────────────────────────
	const ufTableColumns = [
		{ key: 'uf', label: 'UF', align: 'left', width: 80 },
		{ key: 'valor_executado_estado', label: 'Valor Executado Estado', align: 'right', width: 200 },
		{ key: 'valor_executado_municipio', label: 'Valor Executado Município', align: 'right', width: 200 },
		{ key: 'valor_executado_total_uf', label: 'Valor Executado Total UF', align: 'right', width: 200 },
		{ key: 'perc_valor_executado_estado', label: '% Estado', align: 'right', width: 120 },
		{ key: 'perc_valor_executado_municipio', label: '% Município', align: 'right', width: 120 },
		{ key: 'valor_executado_perc', label: '% Total', align: 'right', width: 100 },
	];
	const brl = (v: number) => `R$ ${v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
	const pct = (v: number) => `${v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%`;
	const ufTableRows = ufData.map((d) => ({
		uf: d.uf,
		valor_executado_estado:         brl(d.valor_executado_estado),
		valor_executado_municipio:      brl(d.valor_executado_municipio),
		valor_executado_total_uf:       brl(d.valor_executado_total_uf),
		perc_valor_executado_estado:    pct(d.perc_valor_executado_estado),
		perc_valor_executado_municipio: pct(d.perc_valor_executado_municipio),
		valor_executado_perc:           pct(d.valor_executado_perc),
	}));

</script>

<!-- ══════════════════════════════════════════════════════════════════════════
     INTRODUÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-intro">
	<h2>1. Em quais territórios os recursos da Política Nacional Aldir Blanc chegaram?</h2>
	<p>
		Neste capítulo, vamos entender como foram distribuídos territorialmente os <strong> R$ 3 bilhões </strong> da Política Nacional Aldir Blanc.
	</p>
	<p>
	Vamos descrever e analisar a distribuição entre os municípios, estados e Distrito Federal; entre os diversos portes de municípios; entre zona urbana ou rural e também a distribuição em territórios específicos como as periferias e as comunidades indígenas e quilombolas.
	</p>
	<svg width={600} height={130} style="overflow: hidden; margin-top: 1rem;">
		<AnnotationBox
			title=""
			subtitle={"As análises apresentadas nesta seção foram elaboradas a partir do\ncruzamento dos dados de agentes culturais contemplados pela Política\nNacional Aldir Blanc com bases da Receita Federal e dados do Censo\n2022 do IBGE."}
			boxX={0}
			boxY={0}
			boxWidth={500}
			pointX={-30}
			pointY={63}
			showTitle={false}
			circleRadius={0}
		/>
	</svg>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     GRANDES NÚMEROS — EXECUÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-totals">
	<h2>Como ocorreu a distribuição dos recursos?</h2>
	<div style="margin-bottom: 1.5rem;">
		<p>
			A Lei 14.399/2022 que institui a Política Nacional Aldir Blanc de Fomento à Cultura prevê uma lógica de repasse igualitária do recurso federal para estados e municípios, sendo com 50% dos recursos destinados aos Estados e Distrito Federal e 50% dos recursos destinados aos Municípios e ao Distrito Federal. 
		</p>
		<p>
			No Ciclo I da Política Nacional Aldir Blanc, o Governo Federal, por meio do Ministério da Cultura, repassou R$ 3 bilhões para estados, municípios e Distrito Federal. O montante executado pelos Estados e pelo Distrito Federal representa 96% do recurso repassado. Já os municípios e Distrito Federal executaram 93,6% do recurso recebido. Confira os valores: 
		</p>
		<div class="bignumbers-row">
			<div class="bignumber-cell">
				<BigNumber
					value={formatBRL(valorExecTotal)}
					fontSize={80}
				/>
				<p class="bignumber-caption">Total</p>
			</div>
		</div>
	</div>
	<h3>Alta execução em ambas as esferas</h3>
	<p>
		Os repasses chegam por dois caminhos: ao <strong>governo estadual</strong> (R$ 1,45 bi) e aos
		<strong>municípios</strong> (R$ 1,40 bi). Em ambos, a execução superou 93% — sinal de que os
		recursos empenhados foram, em grande maioria, de fato aplicados.
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber
				value={formatBRL(valorExecEstados)}
				fontSize={80}
			/>
			<p class="bignumber-caption">Estados e Distrito Federal</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber
				value={formatBRL(valorExecMunicipios)}
				fontSize={80}
			/>
			<p class="bignumber-caption">Municípios e Distrito Federal</p>
		</div>
	</div>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber
				value={percExecEstados.toFixed(1)}
				suffix="%"
				fontSize={80}
			/>
			<p class="bignumber-caption">dos repasses a estados e DF foram executados</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber
				value={percExecMunicipios.toFixed(1)}
				suffix="%"
				fontSize={80}
			/>
			<p class="bignumber-caption">dos repasses a municípios foram executados</p>
		</div>
	</div>
	<div style="margin-top: 1.5rem;">
		<p>
			Os níveis de execução observados são expressivos, indicando um desempenho consistente na implementação da política. Esse resultado sugere, por um lado, uma elevada capacidade de mobilização institucional por parte dos entes federativos, mesmo em um contexto ainda recente de implementação. Por outro, evidencia um baixo nível de represamento de recursos, o que reforça a efetividade operacional da política no curto prazo.
		</p>
	</div>
	<div style="margin-top: 1.5rem;">
		<p>
 			O repasse do recurso da Política Nacional Aldir Blanc é regido também pelos critérios de rateio do Fundos de Participação dos Estados e do Distrito Federal (FPE), do Fundo de Participação dos Municípios (FPM) e pela proporcionalidade da população. Isso quer dizer que o cálculo de repasse prevê que mais recurso chegue em territórios mais populosos.
		</p>
	</div>
	<div style="margin-top: 1.5rem;">
		<p>
			Você pode conferir no gráfico a seguir os valores executados por Unidade Federativa (UF). Os valores apresentados são a soma dos valores executados pelos estados e pelos municípios de cada UF. Os percentuais representam a participação da UF no valor total executado no país.
		</p>
	</div>
	<div style="margin-top: 2.5rem;">
		<ExecutedValueByStateMap
			{states}
			metric="valor_executado_rs"
			format={formatBRL}
			formatLine2={(row) => formatPercFix(row.valor_executado_perc * 100)}
		/>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     MAPA POR REGIÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-region">
	<h3>O mapa dos recursos: o programa segue a população?</h3>
	<p>
		O <strong>Sudeste</strong> recebeu 35,6% do total — mas concentra 41,7% da população. O
		<strong>Nordeste</strong>, com 26,9% da população, absorveu 30,9% dos recursos. O
		<strong>Norte</strong> captou 13% do total com apenas 8,8% da população — proporcionalmente,
		o maior favorecido.
	</p>
	<div class="silhouette-compare">
		<div class="silhouette-col">
			<p class="silhouette-label">Recursos executados</p>
			<RegionSilhouetteChart
				data={silhouetteRegionData}
				maxSize={100}
				colors={categorical8}
				format={formatBRL}
				showLabels={true}
			/>
		</div>
		<div class="silhouette-col">
			<p class="silhouette-label">Peso demográfico</p>
			<RegionSilhouetteChart
				data={silhouetteRegionPopData}
				maxSize={100}
				colors={categorical8}
				format={formatPop}
				showLabels={true}
			/>
		</div>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     MAPA POR ESTADO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-state-map">
	<h3>Estado a estado: a concentração fica evidente</h3>
	<p>
		Dentro das regiões, a desigualdade se aprofunda. <strong>São Paulo sozinho absorveu quase 20%</strong>
		de todo o orçamento executado. Minas Gerais ficou em segundo com 7,6%. No extremo oposto,
		<strong>Rondônia</strong> registrou apenas R$ 467 mil — SP recebeu
		<strong>622 vezes mais</strong>.
	</p>
	<StatesSilhouetteChart
		data={silhouetteStateData}
		maxSize={120}
		colors={categorical8}
		format={formatBRL}
		showLabels={true}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     ÁREA PROPORCIONAL POR REGIÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<!-- <ScrollSection id="section-1-proportional">
	<h3>Sentindo a concentração antes de calculá-la</h3>
	<p>
		Às vezes os números precisam virar forma. Aqui, a <strong>área de cada círculo é proporcional
		ao valor total executado</strong> pela região. O contraste visual entre Sudeste e Centro-Oeste
		comunica em segundos o que qualquer tabela demora a transmitir — e mostra que o Nordeste,
		frequentemente invisível nos debates de investimento, é o segundo maior bloco.
	</p>
	<ProportionalAreaChart
		data={regionAreaData}
		maxRadius={110}
		colors={categorical8}
		format={formatBRL}
		showLabels={true}
	/>
</ScrollSection> -->



<!-- ══════════════════════════════════════════════════════════════════════════
     RANKING POR ESTADO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-ranking">
	<h3>O ranking dos estados: SP muito à frente</h3>
	<p>
		O gráfico deixa explícita a hierarquia. São Paulo aparece isolado no topo, seguido de Minas
		Gerais, Rio de Janeiro, Ceará e Bahia. Rondônia mal aparece na escala — um sinal de barreiras
		estruturais específicas naquele estado.
	</p>
	<p>
		Mas o ranking absoluto esconde que estados grandes naturalmente terão volumes maiores.
		O próximo gráfico abre a comparação por população e por proporcionalidade.
	</p>
	<HorizontalBarChart
		data={rankingData}
		color={categorical8[0]}
		format={formatBRL}
		xLabel="Valor executado (R$)"
		margin={{ top: 20, right: 40, bottom: 40, left: 50 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     BUBBLE: POPULAÇÃO VS INVESTIMENTO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-bubble-state">
	<h3>Tamanho justifica o volume? Quem recebe além do esperado?</h3>
	<p>
		Estados próximos à tendência receberam de forma proporcional ao seu tamanho. <strong>Bolhas
		acima</strong> da diagonal receberam mais per capita; <strong>abaixo</strong>, menos.
	</p>
	<p>
		Vários estados do Norte e Nordeste — CE, MA, PA e AL — aparecem acima da linha, sugerindo
		um viés redistributivo do programa. SC e PR, ao contrário, ficam consistentemente abaixo.
		O tamanho de cada bolha representa o número de entes contemplados.
	</p>
	<BubbleChart
		data={bubbleStateData}
		xLabel="População total"
		yLabel="Valor executado (R$)"
		sizeLabel="Entes contemplados"
		yFormat={formatBRL}
		xFormat={formatPop}
		colors={categorical8}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     SLOPE: RANKING VALOR VS RANKING POPULAÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-slope">
	<h3>Quem subiu ou caiu quando a régua é a população?</h3>
	<p>
		O gráfico de inclinação compara a posição de cada estado no <strong>ranking por valor
		executado</strong> com a posição no <strong>ranking por população</strong>.
		Linhas que sobem (da esquerda para a direita) indicam que o estado recebeu
		<em>mais</em> do que justificaria seu peso demográfico; linhas que descem, <em>menos</em>.
	</p>
	<p>
		<strong>Ganharam proporcionalmente mais:</strong> AL, CE, PI, MA e PA — estados do Nordeste
		e Norte com maior vulnerabilidade social.
		<strong>Receberam proporcionalmente menos:</strong> SC, RO, PR, RS e MT — estados do Sul e
		Centro-Oeste, com indicadores socioeconômicos geralmente mais favoráveis.
	</p>
	<SlopeGraph
		items={slopeItems}
		labels={slopeLabels}
		format={formatSlope}
		height={1000}
		colors={categorical8}
		margin={{ top: 40, right: 80, bottom: 40, left: 80 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     VALOR PER CAPITA POR UF
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-percapita">
	<h3>A régua per capita inverte o ranking</h3>
	<p>
		Normalizado pela população, o ranking muda completamente.
		<strong>Amapá (R$ 29,44/hab)</strong>, <strong>Acre (R$ 27,63/hab)</strong> e
		<strong>Roraima (R$ 22,96/hab)</strong> lideram — estados pequenos que concentraram recursos
		de forma proporcionalmente favorável.
	</p>
	<p>
		São Paulo, que lidera em volume absoluto, cai para posição intermediária: R$ 12,09/hab.
		Rondônia permanece no último lugar com apenas R$ 5,06/hab — confirmando a anomalia já vista
		no ranking absoluto.
	</p>
	<HorizontalStackedBarChart
		data={percapitaData}
		keys={['valor_percapita_uf']}
		categoryKey="uf"
		labels={{ valor_percapita_uf: 'Valor per capita (R$)' }}
		format={formatBRLpc}
		icons={stateFlags}
		iconSize={20}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     BOXPLOT: DISTRIBUIÇÃO DE MEDIANA POR REGIÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-boxplot">
	<h3>Como se distribuem os repasses dentro de cada região?</h3>
	<p>
		Cada caixa representa uma região. Os valores plotados são as
		<strong>medianas de repasse por estado</strong> dentro da região — o valor típico que um
		beneficiário recebe em cada UF.
	</p>
	<p>
		O <strong>Centro-Oeste</strong> tem a maior dispersão interna. O <strong>Nordeste</strong>
		concentra os menores valores típicos. <strong>Sul e Sudeste</strong> têm distribuições mais
		compactas, mas com outliers elevados em RS e SP.
	</p>
	<p class="chart-label-compare">Opção A — Box plot: mediana por estado dentro de cada região</p>
	<BoxPlotChart
		data={boxPlotData}
		xLabel="Região"
		yLabel="Mediana do repasse por estado (R$)"
		format={formatBRL}
		showOutliers={true}
	/>
	<div class="boxplot-legend">
		<p class="boxplot-legend-title">Como ler este gráfico</p>
		<svg class="boxplot-legend-svg" viewBox="0 0 340 90" role="img" aria-label="Legenda do box plot">
			<!-- whisker superior -->
			<line x1="60" y1="12" x2="60" y2="22" stroke="#4271b5" stroke-width="1.5"/>
			<!-- cap superior -->
			<line x1="47" y1="12" x2="73" y2="12" stroke="#4271b5" stroke-width="1.5"/>
			<!-- caixa IQR -->
			<rect x="34" y="22" width="52" height="28" fill="#4271b5" fill-opacity="0.18" stroke="#4271b5" stroke-width="1.5"/>
			<!-- mediana -->
			<line x1="34" y1="36" x2="86" y2="36" stroke="#4271b5" stroke-width="2.5"/>
			<!-- whisker inferior -->
			<line x1="60" y1="50" x2="60" y2="60" stroke="#4271b5" stroke-width="1.5"/>
			<!-- cap inferior -->
			<line x1="47" y1="60" x2="73" y2="60" stroke="#4271b5" stroke-width="1.5"/>
			<!-- outlier -->
			<circle cx="60" cy="76" r="3" fill="none" stroke="#4271b5" stroke-width="1.5"/>

			<!-- rótulo: whisker superior -->
			<line x1="73" y1="12" x2="110" y2="12" stroke="#888" stroke-width="0.8" stroke-dasharray="3,2"/>
			<text x="114" y="15" class="legend-label">Máximo (excl. outliers)</text>

			<!-- rótulo: Q3 -->
			<line x1="86" y1="22" x2="110" y2="22" stroke="#888" stroke-width="0.8" stroke-dasharray="3,2"/>
			<text x="114" y="26" class="legend-label">3º quartil (Q3) — 75%</text>

			<!-- rótulo: mediana -->
			<line x1="86" y1="36" x2="110" y2="36" stroke="#888" stroke-width="0.8" stroke-dasharray="3,2"/>
			<text x="114" y="40" class="legend-label">Mediana (Q2) — valor central</text>

			<!-- rótulo: Q1 -->
			<line x1="86" y1="50" x2="110" y2="50" stroke="#888" stroke-width="0.8" stroke-dasharray="3,2"/>
			<text x="114" y="54" class="legend-label">1º quartil (Q1) — 25%</text>

			<!-- rótulo: whisker inferior -->
			<line x1="73" y1="60" x2="110" y2="60" stroke="#888" stroke-width="0.8" stroke-dasharray="3,2"/>
			<text x="114" y="64" class="legend-label">Mínimo (excl. outliers)</text>

			<!-- rótulo: outlier -->
			<line x1="63" y1="76" x2="110" y2="76" stroke="#888" stroke-width="0.8" stroke-dasharray="3,2"/>
			<text x="114" y="80" class="legend-label">Outlier (valor atípico)</text>
		</svg>
	</div>
	<p class="chart-label-compare">Opção B — Barra simples: mediana agregada de todos os pagamentos da região</p>
	<HorizontalBarChart
		data={regionMedianData}
		color={categorical8[0]}
		format={formatBRLpc}
		xLabel="Mediana do valor pago (R$)"
		margin={{ top: 20, right: 40, bottom: 40, left: 120 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     ESTADO vs MUNICÍPIO POR UF
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-split">
	<h3>Estado ou município? A divisão federativa dos recursos</h3>
	<p>
		Os repasses chegam por dois caminhos — ao governo estadual ou diretamente aos municípios.
		A proporção varia enormemente entre UFs.
	</p>
	<p>
		<strong>Rondônia</strong> é o caso extremo municipal: 94,7% via municípios, com o estado
		respondendo por apenas 5,3%. <strong>Roraima</strong> concentrou 90,6% na esfera estadual.
		A maioria dos estados mantém divisão próxima de 50/50.
	</p>
	<div style="overflow: hidden;">
		<div style="margin-left: -100px; width: calc(100% + 80px);">
			<DivergingBarChart
				data={ufSplitData}
				leftLabel="Estado"
				rightLabel="Município"
				referenceValue={50}
				referenceLabel=" "
				colors={colorPairs.blueOrange}
			/>
		</div>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     TABELA DE REFERÊNCIA POR UF
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-uf-table">
	<h3>Referência completa: o que cada UF executou</h3>
	<p>
		Os gráficos anteriores contam a história visualmente — esta tabela reúne os <strong>números
		exatos</strong> de todas as 27 unidades federativas. Para cada UF: valor executado pelo governo
		estadual, pelos municípios, o total e a participação percentual de cada esfera e no total nacional.
	</p>
	<div style="overflow-x: auto;">
		<svg width={1020} height={920}>
			<DataTable columns={ufTableColumns} rows={ufTableRows} />
		</svg>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     HEATMAP: ESTADO × FAIXA DE VALOR PAGO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-heatmap">
	<h3>Onde estão os municípios beneficiados? Estado × faixa de valor pago</h3>
	<p>
		Este mapa de calor cruza os <strong>estados</strong> (ordenados por valor total executado,
		do maior ao menor) com as <strong>faixas de valor pago por município</strong>. Cada célula mostra
		quantos entes foram contemplados naquela combinação.
	</p>
	<p>
		A grande maioria dos municípios recebeu entre <strong>R$2 mil e R$50 mil</strong> — faixa onde
		se concentra a massa de pequenas cidades. <strong>MG</strong> e <strong>BA</strong> dominam
		as faixas intermediárias. Repasses acima de <strong>R$500 mil</strong> ficam restritos a poucos
		estados com municípios de maior porte. O mapa evidencia que não existe um valor típico do PNAB:
		cada estado tem um perfil de distribuição próprio.
	</p>
	<HeatMap
		data={heatmapData}
		height={820}
		colorRange={colorScales.blue}
		xLabel="Faixa de valor pago"
		yLabel="Estado (UF)"
		format={(v: number) => v > 0 ? String(v) : ''}
		showValues={true}
		showLegend={true}
		cellRadius={2}
		cellGap={3}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     URBANO vs RURAL POR UF
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-zone">
	<h3>O campo ainda fica para trás</h3>
	<p>
		Em todas as unidades federativas, o investimento <strong>urbano é amplamente dominante</strong>.
		Mesmo nos estados com perfil mais rural, a zona urbana concentra a esmagadora maioria dos
		recursos. Os estados estão ordenados pela proporção rural.
	</p>
	<p>
		<strong>Tocantins, Paraíba e Acre</strong> têm as maiores fatias rurais — mas ainda assim
		dificilmente ultrapassam 15% do total. <strong>Rondônia e Distrito Federal</strong> têm as
		menores proporções rurais.
	</p>
	<HorizontalStackedBarChart
		data={zoneData}
		keys={['valor_rural', 'valor_urbano']}
		labels={{ valor_urbano: 'Urbano', valor_rural: 'Rural' }}
		colors={[colorScales.red[2], colorScales.blue[2]]}
		format={formatBRLM}
		showTotalLabel={true}
		icons={stateFlags}
		iconSize={20}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PORTE MUNICIPAL — TREEMAP
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-porte-treemap">
	<h3>Municípios grandes dominam o volume investido</h3>
	<p>
		O PNAB atendeu municípios de todos os portes — mas com profunda assimetria. Os
		<strong>332 municípios de grande porte</strong> (acima de 100 mil habitantes) concentraram
		<strong>52,5% do valor total</strong>. Os <strong>3.401 municípios Pequenos I</strong>
		(até 20 mil habitantes), sendo mais de dez vezes mais cidades, receberam apenas
		<strong>19,1%</strong>.
	</p>
	<TreemapChart
		data={porteTreemapData}
		height={420}
		format={formatBRL}
		colors={categorical8}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PORTE MUNICIPAL — BUBBLE
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-porte-bubble">
	<h3>Municípios pequenos são muitos, mas recebem pouco</h3>
	<p>
		Cada bolha representa um porte populacional. O eixo horizontal mostra quantos municípios o
		compõem; o vertical, o valor total recebido; o tamanho da bolha, o número de beneficiários.
	</p>
	<p>
		A posição de <strong>Pequeno I</strong> é reveladora: é o grupo com mais municípios e mais
		beneficiários, mas o segundo menor em valor total — atrás até de Pequeno II, que reúne
		muito menos cidades.
	</p>
	<BubbleChart
		data={porteBubbleData}
		xLabel="Nº de municípios"
		yLabel="Valor total (R$)"
		sizeLabel="Beneficiários"
		yFormat={(v: number) => `${(v / 1e6).toFixed(0)}M`}
		xFormat={(v: number) => v.toLocaleString('pt-BR')}
		colors={categorical8}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PORTE MUNICIPAL — URBANO vs RURAL
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-porte-zone">
	<h3>O rural é proporcionalmente mais presente nos municípios pequenos</h3>
	<p>
		Em todos os portes, o investimento urbano é dominante. Mas a parcela rural cresce
		à medida que o porte diminui — municípios <strong>Pequenos I</strong> têm a maior
		proporção rural entre todos os grupos, ainda que seja minoria.
		Municípios <strong>Grandes</strong> direcionam quase a totalidade para áreas urbanas.
	</p>
	<div style="overflow: hidden;">
		<div style="margin-left: -60px; width: calc(100% + 80px);">
			<DivergingBarChart
				data={porteDivergingData}
				leftLabel="Urbano"
				rightLabel="Rural"
				referenceValue={50}
				referenceLabel="50%"
				colors={colorPairs.blueOrange}
			/>
		</div> 
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PORTE MUNICIPAL — EQUIDADE VALOR vs BENEFICIÁRIOS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-porte-equity">
	<h3>Municípios grandes recebem mais do que representam</h3>
	<p>
		A comparação entre a fatia do valor investido e a fatia de beneficiários atendidos revela
		o desequilíbrio mais direto desta seção: municípios <strong>Grandes</strong> concentram
		<strong>52,5% dos recursos</strong>, mas apenas <strong>21,6% dos beneficiários</strong>.
	</p>
	<p>
		Municípios <strong>Pequenos I e II</strong> têm o padrão inverso — atendem
		proporcionalmente mais pessoas do que o valor que recebem. A inequidade é estrutural.
	</p>
	<div style="padding-left: 100px;">
		<HorizontalStackedBarChart
			data={porteStackedData}
			keys={porteStackedKeys}
			labels={porteStackedLabels}
			colors={categorical8}
			format={formatPercFix}
			showTotalLabel={true}
		/>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     TERRITÓRIOS ESPECIAIS — GRANDES NÚMEROS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-special-bignumber">
	<h3>O programa chegou a quem mais precisa?</h3>
	<p>
		Favelas, quilombos e territórios indígenas concentram algumas das populações mais vulneráveis
		do Brasil. Os dados revelam uma <strong>lacuna de equidade</strong> significativa:
		<strong>{percPopulacaoEspecial}%</strong> da população vive nesses territórios, mas apenas
		<strong>{percRecursoEspecial}%</strong> dos recursos chegaram até eles.
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber
				value={percPopulacaoEspecial}
				suffix="%"
				fontSize={72}
			/>
			<p class="bignumber-caption">da população brasileira vive em Favelas, Quilombos e Territórios Indígenas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber
				value={percRecursoEspecial}
				suffix="%"
				fontSize={72}
			/>
			<p class="bignumber-caption">dos recursos do PNAB chegaram a Favelas, Quilombos e Territórios Indígenas</p>
		</div>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     TERRITÓRIOS ESPECIAIS — GRÁFICO DIVERGENTE
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-special-chart">
	<h3>Sub-representação sistemática em todos os territórios</h3>
	<p>
		O gráfico divergente torna explícita a assimetria: em todos os territórios especiais,
		a barra de <strong>população</strong> — o que a comunidade representa — é maior do que a
		barra de <strong>recursos</strong> — o que ela recebeu. Todos estão sistematicamente
		sub-representados no programa.
	</p>
	<p>
		O descompasso é maior nas <strong>favelas e comunidades urbanas</strong>: 8% da população,
		4,85% dos recursos. Quilombos e territórios indígenas somam menos de 1,5% da população
		e receberam menos de 0,5% do total.
	</p>
	<DivergingBarChart
		data={specialDivergingData}
		leftLabel="% população no território"
		rightLabel="% do total de recursos"
		referenceValue={50}
		referenceLabel="Equidade"
		colors={colorPairs.blueOrange}
		marginLeft={200}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     TERRITÓRIOS ESPECIAIS — ESTADO vs MUNICÍPIO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-special-split">
	<h3>Dentro dos territórios: quem executa — estado ou município?</h3>
	<p>
		Dos recursos que chegaram aos territórios especiais, há uma divisão entre repasses ao
		<strong>governo estadual</strong> e ao <strong>conjunto de municípios</strong>.
		Favelas e comunidades urbanas concentram a maior fatia — e os municípios respondem por
		parcela significativa da execução em todos os territórios.
	</p>
	<div style="padding-left: 100px;">
		<HorizontalStackedBarChart
			data={specialStackedData}
			keys={['valor_estado', 'valor_municipio']}
			categoryKey="shortLabel"
			labels={{ valor_estado: 'Governo Estadual', valor_municipio: 'Governo Municipal' }}
			colors={[colorScales.blue[2], colorScales.red[2]]}
			format={(v: number) => `R$ ${(v / 1e6).toFixed(1)}M`}
			showTotalLabel={true}
		/>
	</div>
</ScrollSection>

<style>
	.silhouette-compare {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.silhouette-col {
		width: 100%;
	}

	.silhouette-label {
		font-size: 0.85rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		opacity: 0.6;
		margin: 0 0 0.5rem;
		text-align: center;
		width: 100%;
	}

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

	.chart-label-compare {
		font-size: 0.8rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		opacity: 0.55;
		margin: 1.5rem 0 0.25rem;
	}

	.bignumber-caption {
		font-size: 0.95rem;
		color: var(--color-text);
		text-align: center;
		opacity: 0.75;
		max-width: 20ch;
	}

	.boxplot-legend {
		margin-top: 1rem;
		padding: 0.75rem 1rem;
		border: 1px solid var(--color-border, #e2e8f0);
		border-radius: 6px;
		background: var(--color-surface, #f8fafc);
		display: inline-block;
	}

	.boxplot-legend-title {
		font-size: 0.75rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		opacity: 0.55;
		margin: 0 0 0.5rem;
	}

	.boxplot-legend-svg {
		width: 340px;
		height: 90px;
		display: block;
	}

	:global(.legend-label) {
		font-size: 11px;
		fill: var(--color-text, #334155);
		dominant-baseline: middle;
	}
</style>
