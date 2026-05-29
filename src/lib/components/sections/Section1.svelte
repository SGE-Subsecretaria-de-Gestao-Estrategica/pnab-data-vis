<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import ExecutedValueByStateMap from '$lib/components/ExecutedValueByStateMap.svelte';
	import {
		BigNumber,
		HorizontalStackedBarChart,
		VerticalStackedBarChart,
		DivergingBarChart,
		TreemapChart,
		DataTable,
		AnnotationBox,
		colorPairs,
		colorScales,
		categorical8,
	} from 'sniic-design-system';
	import {
		percExecEstados, percExecMunicipios,
		valorExecEstados, valorExecMunicipios, valorExecTotal,
		percInteriorContemplados,
		valorInteriorTotal,
		capitalInteriorStackedData,
		percapitaData,
		ufSplitData,
		zoneData, zoneQtdData,
		porteTreemapData,
		porteStackedKeys, porteStackedLabels, porteStackedData,
		percPopulacaoEspecial,
		specialStackedData,
		specialTerritoriesMetrics,
		ufData,
		states,
		valorRuralTotal,
		qtdeRuralTotal,
		percRuralQtde,
		percRuralValor,
		specialTerritoryCount,
		specialTerritoryValue,
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
	const formatPercFix = (v: number) => `${v.toFixed(1)}%`;

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
		Neste capítulo, vamos entender como foram distribuídos territorialmente os <strong>R$ 3 bilhões</strong> da Política Nacional Aldir Blanc. Vamos descrever e analisar a distribuição entre os municípios, estados e Distrito Federal; entre os diversos portes de municípios; entre zona urbana ou rural e também a distribuição em territórios específicos como as favelas, comunidades urbanas e as comunidades indígenas e quilombolas.
	</p>
	<svg width={600} height={200} style="overflow: hidden; margin-top: 1rem;">
		<AnnotationBox
			title=""
			subtitle={"As análises apresentadas neste capítulo resultam do banco de dados do BB ágil\na partir de recortes para unidades federativas, estados, municípios e territórios\nespeciais. Nesta pesquisa, os dados de uma unidade federativa devem ser\nentendidos como a soma da execução do estado e dos municípios. Os dados dos\nmunicípios foram organizados a partir da organização dos municípios por porte\npopulacional utilizada pelo IBGE, considerando pequeno porte I – até 20 mil\nhabitantes, pequeno porte II – de 20 a 50 mil habitantes, médio porte – de 50 a\n100 mil habitantes e grande porte – acima de 100 mil habitantes. Os territórios\nespeciais também foram trabalhados a partir da classificação proposta pelo IBGE."}
			boxX={0}
			boxY={0}
			boxWidth={560}
			pointX={-30}
			pointY={100}
			showTitle={false}
			circleRadius={0}
		/>
	</svg>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     SEÇÃO 1.1 — DISTRIBUIÇÃO DOS RECURSOS — BIGNUMBERS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-totals">
	<h2>1.1. Como ocorreu a distribuição dos recursos?</h2>
	<p>
		A Lei 14.399/2022 que institui a Política Nacional Aldir Blanc de Fomento à Cultura estabelece a divisão de destinação de <strong>50% dos recursos para os Estados e Distrito Federal</strong> e de <strong>50% dos recursos para os Municípios e ao Distrito Federal</strong>.
	</p>
	<p>
		No Ciclo I da Política Nacional Aldir Blanc, o Governo Federal, por meio do Ministério da Cultura, repassou R$ 3 bilhões para estados, municípios e Distrito Federal. O montante executado, em 2025, pelos Estados e pelo Distrito Federal representa <strong>96%</strong> do recurso repassado. Já os municípios e Distrito Federal executaram, em 2025, <strong>93,6%</strong> do recurso recebido. Confira os valores:
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorExecTotal)} fontSize={80} />
			<p class="bignumber-caption">Total</p>
		</div>
	</div>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorExecEstados)} fontSize={80} />
			<p class="bignumber-caption">Estados e Distrito Federal</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorExecMunicipios)} fontSize={80} />
			<p class="bignumber-caption">Municípios e Distrito Federal</p>
		</div>
	</div>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={percExecEstados.toFixed(1)} suffix="%" fontSize={80} />
			<p class="bignumber-caption">dos repasses a estados e DF foram executados</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={percExecMunicipios.toFixed(1)} suffix="%" fontSize={80} />
			<p class="bignumber-caption">dos repasses a municípios foram executados</p>
		</div>
	</div>
	<p style="margin-top: 1.5rem;">
		Os percentuais de execução dos recursos observados, ainda em 2025, são expressivos — o resultado sugere uma elevada capacidade institucional por parte dos entes federativos, mesmo em um contexto ainda recente de implementação da política.
	</p>
	<p>
		A distribuição dos recursos da Política Nacional Aldir Blanc é orientada por um índice que contabiliza dois critérios: o rateio do Fundos de Participação dos Estados e do Distrito Federal (FPE) e do Fundo de Participação dos Municípios (FPM), que correspondem a <strong>20%</strong> desse índice; e a proporcionalidade da população, que corresponde a <strong>80%</strong>. Isso quer dizer que o cálculo de repasse estabelece que mais recursos cheguem em municípios mais populosos.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     SEÇÃO 1.1 — MAPA POR UF
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-map">
	<p>
		Você pode conferir no gráfico a seguir os valores executados por Unidade Federativa (UF). Os valores apresentados são a soma da execução dos estados e dos municípios de cada UF até 31/12/2025. Os percentuais representam a participação da UF no valor total executado no país.
	</p>
	<div style="margin-top: 2.5rem;">
		<ExecutedValueByStateMap
			{states}
			metric="valor_executado_rs"
			format={formatBRL}
			formatLine2={(row) => formatPercFix(row.valor_executado_perc * 100)}
		/>
	</div>
	<p style="margin-top: 2rem;">
		De maneira geral, a execução dos recursos apresentou uma distribuição equilibrada entre entes estaduais e municipais. Chamam atenção, entretanto, as UFs do Acre, Amapá, Roraima e Tocantins, todos da região Norte, que tiveram uma atuação mais concentrada no nível estadual. Em Rondônia, por outro lado, os municípios foram responsáveis pela maior parte do recurso executado.
	</p>
	<p>
		A seguir, é possível verificar os valores executados e o percentual de participação dos governos estaduais e dos governos municipais na execução de cada UF:
	</p>
	<div style="overflow: hidden; margin-top: 1.5rem;">
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
     SEÇÃO 1.1 — TABELA POR UF
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-uf-table">
	<div style="overflow-x: auto;">
		<svg width={1020} height={920}>
			<DataTable columns={ufTableColumns} rows={ufTableRows} />
		</svg>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     1.1.2 — VALORES PER CAPITA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-percapita">
	<h3>1.1.2. Valores per Capita</h3>
	<p class="frase-destaque">
		A maioria das Unidades Federativas com o maior valor per capita são aquelas que têm as menores populações
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
	<p style="margin-top: 1.5rem;">
		Analisamos o valor per capita da Política Nacional Aldir Blanc para entender a proporcionalidade do montante da Política que foi executado em relação ao tamanho da população em cada UF. O cálculo foi feito a partir da divisão entre o total executado pela UF (valor executado por estados e municípios) e sua população.
	</p>
	<p>
		O valor per capita nos dá uma visão sobre a distribuição do dinheiro e reafirma a lógica de distribuição do recurso presente no texto da Lei. Enquanto a maioria das UFs com populações menores possuem maiores valores per capita, o contrário também é verdade, com exceção de Rondônia e Mato Grosso, que não figuram entre as maiores populações do país.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     1.1.3 — VALORES POR PORTE DOS MUNICÍPIOS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-porte">
	<h3>1.1.3. Valores por porte dos municípios</h3>
	<p class="frase-destaque">
		A análise por porte de município indica que a Aldir Blanc não se restringe aos grandes centros urbanos.
	</p>
	<p>
		Foram analisados <strong>5.097 municípios</strong> que executaram recursos no Ciclo I da Política Nacional Aldir Blanc. Os municípios foram analisados segundo o porte populacional, definido por faixas que classificam as localidades de acordo com o número de habitantes.
	</p>
	<TreemapChart
		data={porteTreemapData}
		height={420}
		format={formatBRL}
		colors={categorical8}
	/>
	<p style="margin-top: 1.5rem;">
		Mais da metade dos recursos foi executada pelos municípios de Grande Porte, que representam <strong>6,5%</strong> dos municípios analisados pela pesquisa. Já as médias dos municípios de Médio e Grande Porte estão acima da média de execução do total dos municípios, que é de <strong>R$ 273.784,83</strong>.
	</p>
	<p>
		Quando analisamos a participação dos municípios na execução do valor total executado na Política Nacional Aldir Blanc, incluindo os entes estaduais, percebemos que a participação dos municípios de Grande Porte representa <strong>25%</strong> do valor total executado. O gráfico a seguir apresenta essa distribuição.
	</p>
	<div style="padding-left: 100px; margin-top: 1.5rem;">
		<HorizontalStackedBarChart
			data={porteStackedData}
			keys={porteStackedKeys}
			labels={porteStackedLabels}
			colors={categorical8}
			format={formatPercFix}
			showTotalLabel={true}
		/>
	</div>
	<p style="margin-top: 1.5rem;">
		Os <strong>3.401 municípios de Pequeno Porte I</strong> juntos executaram mais de <strong>R$ 266 milhões</strong>, o que equivale ao valor total executado pelas seguintes UFs: Mato Grosso, Mato Grosso do Sul, Sergipe, Tocantins, Acre, Amapá e Distrito Federal.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     SEÇÃO 1.2 — DESCONCENTRAÇÃO TERRITORIAL
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-desconcentration">
	<h2>1.2. Como ocorreu a desconcentração territorial?</h2>
	<p>
		A Política Nacional Aldir Blanc tem como objetivo democratizar o acesso à fruição e à produção artística e cultural e estabelece um percentual de pelo menos <strong>20%</strong> para projetos e ações de democratização do acesso à fruição e à produção artística e cultural em áreas periféricas, urbanas e rurais, e em territórios e regiões de maior vulnerabilidade econômica ou social, bem como em áreas de povos e comunidades tradicionais.
	</p>
	<p>
		Embora não tenha sido possível aferir todas as ações listadas pela IN nº10/2023 para desconcentração territorial, é possível identificar que os valores executados em Zonas Rurais, Favelas e Comunidades Urbanas, bem como Agrupamentos Indígenas e Quilombolas refletem esse compromisso.
	</p>
	<p class="frase-destaque">
		Ou seja, a desconcentração é ainda maior do que pudemos verificar nesta pesquisa.
	</p>
	<p>
		A presença desses grupos no conjunto de beneficiários evidencia o potencial das políticas culturais para promover inclusão e diversidade, ao mesmo tempo em que aponta para a importância de estratégias mais direcionadas para ampliar o acesso nesses territórios.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     1.2.1 — INTERIOR VERSUS CAPITAL
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-capital-interior">
	<h3>1.2.1. Interior <em>versus</em> capital</h3>
	<p class="metodologico">
		Para fins desta análise, os municípios foram classificados em três grupos: capitais, regiões metropolitanas e interior. Considerou-se como interior todo município que não é capital e que não pertence à região metropolitana.
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={percInteriorContemplados.toFixed(0)} suffix="%" fontSize={72} />
			<p class="bignumber-caption">dos contemplados na PNAB residem em cidades do interior</p>
		</div>
	</div>
	<p style="margin-top: 1.5rem;">
		Os dados analisados mostram que a Política Nacional Aldir Blanc teve forte capilaridade territorial, alcançando majoritariamente contemplados residentes no interior do país.
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorInteriorTotal)} fontSize={72} />
			<p class="bignumber-caption">foi o montante total destinado para os agentes culturais do interior</p>
		</div>
	</div>
	<p style="margin-top: 1.5rem;">
		Embora o desenho de repasse da PNAB favoreça, em alguma medida, territórios mais populosos — como capitais e regiões metropolitanas —, os dados revelam uma distribuição financeira relativamente equilibrada entre os diferentes espaços do país. Interior, regiões metropolitanas e capitais concentraram, respectivamente, <strong>34%</strong>, <strong>30%</strong> e <strong>36%</strong> do valor executado. Esse resultado sugere que a PNAB não se restringiu aos grandes centros urbanos, alcançando também de forma expressiva os municípios do interior.
	</p>
	<p>
		Pode-se dizer que a mobilização dos recursos para o interior é também um movimento que ajuda a lidar com a demanda dos agentes culturais dos pequenos e médios municípios que, em sua maioria, não receberam grandes valores.
	</p>
	<div style="padding-left: 60px; margin-top: 1.5rem;">
		<HorizontalStackedBarChart
			data={capitalInteriorStackedData}
			keys={['capital', 'metropolitana', 'interior']}
			labels={{ capital: 'Capital', metropolitana: 'Região Metropolitana', interior: 'Interior' }}
			colors={[categorical8[1], categorical8[3], categorical8[0]]}
			format={formatPercFix}
			showTotalLabel={false}
		/>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     1.2.2 — ZONA RURAL
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-zone">
	<h3>1.2.2. Zona rural</h3>
	<div class="bignumbers-row" style="margin-bottom: 1.5rem;">
		<div class="bignumber-cell">
			<BigNumber
				value={qtdeRuralTotal.toLocaleString('pt-BR')}
				fontSize={72}
			/>
			<p class="bignumber-perc">({percRuralQtde.toFixed(1).replace('.', ',')}%)</p>
			<p class="bignumber-caption">foram os contemplados em zona rural</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber
				value={`R$${(valorRuralTotal / 1e6).toFixed(0)}M`}
				fontSize={72}
			/>
			<p class="bignumber-perc">({percRuralValor.toFixed(1).replace('.', ',')}%)</p>
			<p class="bignumber-caption">foi o recurso destinado</p>
		</div>
	</div>
	<p>
		Quando visualizamos as regiões do país, percebemos que essa tendência se mantém. O Nordeste, região com maior população rural (22,3%), foi a que mais destinou recursos para agentes culturais em área rural, o que constitui 19,5% do total dos agentes contemplados nesta região. Já o Sudeste, região com maior população urbana (94,4%), foi a que mais destinou para área urbana: 92,6% dos agentes sudestinos encontram-se em territórios mais urbanizados.
	</p>
	<p>
		Ao analisar como ocorreu essa distribuição nas unidades federativas, verificamos que Ceará (23,8%), Bahia (23,4%), Sergipe (21,5%), Pará (20%) e Piauí (19,3%) foram os estados que mais contemplaram agentes culturais da zona rural, quase todos do Nordeste, com exceção do Pará.
	</p>
	<p>
		Por outro lado, as unidades federativas que mais contemplaram agentes na zona urbana são São Paulo (95,3%), Rio de Janeiro (94,5%), Paraná (92,3%) e Goiás (90,5%).
	</p>
	<p>
		Os estados que proporcionalmente mais destinaram recursos para a zona rural foram Tocantins (14,7%), Acre (12,9%), Rondônia (12,9%), Paraíba (11,9%), Bahia (10,2%) e Sergipe (10,0%). Já os estados que mais destinaram recursos para a zona rural em termos absolutos foram Bahia (R$ 7.781.357,73), São Paulo (R$ 7.607.110,89), Pernambuco (R$ 6.683.248,13), Minas Gerais (R$ 5.708.916,42) e Ceará (R$ 5.660.591,63).
	</p>
	<VerticalStackedBarChart
		data={zoneQtdData}
		keys={['qtde_rural', 'qtde_urbano']}
		labels={{ qtde_urbano: 'Urbano', qtde_rural: 'Rural' }}
		colors={[colorScales.red[2], colorScales.blue[2]]}
		normalize={true}
		height={320}
		sortDirection="desc"
	/>
	<p style="margin-top: 1.5rem;">
		Ao analisar a proporção de contemplados da Política Nacional Aldir Blanc entre áreas rurais e urbanas, observa-se que Acre (21,0%), Tocantins (20,8%), Sergipe (12,6%), Pará (12,2%) e Bahia (12,0%) foram os estados com maior participação relativa de agentes culturais residentes em territórios rurais.
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
	<p style="margin-top: 1.5rem;">
		Na análise da distribuição proporcional dos valores destinados aos contemplados residentes em áreas rurais, destacam-se Tocantins (14,7%) e Acre (12,9%) como os estados com maior participação relativa de recursos direcionados a esses territórios. Contudo, Acre e Tocantins também apresentam parcelas expressivas de sua população residente em áreas rurais, correspondendo a 19,8% e 14,2%, respectivamente.
	</p>
	<p>
		Já no âmbito municipal, verifica-se que os municípios de pequeno porte I são os que mais contemplaram agentes culturais na zona rural (22,3%), seguido dos de pequeno porte II (17,2%), médio porte (9,5%) e grande porte (3%).
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     1.2.3 — TERRITÓRIOS ESPECIAIS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-1-special">
	<h3>1.2.3. Territórios especiais</h3>
	<p class="metodologico">
		O IBGE (Instituto Brasileiro de Geografia e Estatística) define os setores censitários como as menores divisões territoriais utilizadas para organizar e realizar pesquisas, como o Censo Demográfico. Essa classificação permite identificar a população residente em diferentes tipos de áreas, como urbanas e rurais, entre outras categorias territoriais.
	</p>
	<p>
		Ao analisar os recursos executados sob o ponto de vista dos setores censitários do IBGE, os dados mostram que, embora a maior parte dos recursos da Política Nacional Aldir Blanc esteja concentrada em setores classificados como "não especiais", há a presença de investimentos em territórios denominados "especiais", como favelas, comunidades urbanas, agrupamentos indígenas e quilombolas.
	</p>

	<h4>Favelas e Comunidades Urbanas</h4>
	<p>
		Cerca de <strong>16 milhões de pessoas</strong>, 8% da população brasileira, habitam favelas e comunidades urbanas. Entre os agentes contemplados com a PNAB, <strong>2,7%</strong> estão nestes territórios e receberam <strong>4,9%</strong> dos recursos totais da PNAB, o que representa mais de <strong>R$ 138 milhões</strong>, demonstrando que há espaço para o avanço da indução da política para esse território.
	</p>
	<p>
		Esse desempenho é impulsionado pela Região Norte, onde o aporte nesses territórios atinge <strong>19,9%</strong> do valor executado na região, com destaque para as execuções no Amapá (27,6%), Pará (27,3%) e Amazonas (22,7%). Cabe assinalar que a presença de repasses em todas as 27 unidades da federação atesta a capilaridade nacional da medida.
	</p>

	<h4>Agrupamentos Quilombolas</h4>
	<p>
		No Brasil, um total de <strong>1,3 milhões de pessoas</strong> residem em comunidades quilombolas, o que equivale a <strong>0,66%</strong> da população. Os agrupamentos quilombolas receberam um aporte de recursos superior a <strong>R$ 7 milhões</strong> da Política Nacional Aldir Blanc, o que equivale a <strong>0,26%</strong> dos recursos totais. Essa presença se distribui de forma ampla pelo território nacional, com ações identificadas em <strong>20 estados</strong>, abrangendo todas as regiões do país.
	</p>
	<p>
		O Nordeste concentra a maior parte desses recursos, tendo repassado <strong>R$ 4.032.436,80</strong>, valor que representa <strong>54,7%</strong> do total destinado aos contemplados residentes em agrupamentos quilombolas. Essa distribuição é coerente com a concentração territorial da população quilombola no país, tendo em vista que a região Nordeste reúne <strong>68,14%</strong> da população quilombola brasileira.
	</p>
	<p>
		As unidades federativas da Bahia e Minas Gerais lideram individualmente os maiores repasses nessa categoria, respondendo juntas por <strong>46,2%</strong> do total nacional. Na Bahia, agentes culturais que residem em agrupamentos quilombolas representam <strong>0,93%</strong> do recurso e em Sergipe esse percentual chega a <strong>1,04%</strong>, o maior peso relativo no país.
	</p>

	<h4>Agrupamentos Indígenas</h4>
	<p>
		A população indígena representa <strong>0,83%</strong> da população brasileira. O valor total de projetos apoiados pela PNAB destinado especificamente aos agentes culturais residentes em agrupamentos indígenas é superior a <strong>R$ 5 milhões</strong>.
	</p>
	<p>
		O impacto dessa política estende-se por <strong>18 estados</strong> brasileiros, abrangendo todas as regiões do país. Destacam-se a Paraíba, onde os agrupamentos indígenas concentram <strong>1,52%</strong> de todo o recurso executado, e o Mato Grosso do Sul, com <strong>1,35%</strong>.
	</p>
	<p>
		Um achado relevante diz respeito à distribuição regional: o Nordeste concentra <strong>58,2%</strong> do montante total destinado a agrupamentos indígenas, liderado por Paraíba, Pernambuco e Ceará.
	</p>

	<div class="bignumbers-row" style="margin-top: 2rem;">
		<div class="bignumber-cell">
			<BigNumber
				value={specialTerritoryCount.toLocaleString('pt-BR')}
				fontSize={72}
			/>
			<p class="bignumber-caption">agentes culturais contemplados em Favelas, Quilombos e Territórios Indígenas</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber
				value={formatBRL(specialTerritoryValue)}
				fontSize={72}
			/>
			<p class="bignumber-caption">destinados a agentes em territórios especiais</p>
		</div>
	</div>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber
				value={percPopulacaoEspecial}
				suffix="%"
				fontSize={72}
			/>
			<p class="bignumber-caption">da população brasileira vive em Favelas, Quilombos e Territórios Indígenas</p>
		</div>
	</div>

	<svg
		viewBox="0 0 560 310"
		style="width: 100%; overflow: visible; display: block; margin-top: 1.5rem;"
		role="img"
		aria-label="Comparação de quatro métricas por território especial"
	>
		<!-- Legend -->
		<rect x={0}   y={2}  width={12} height={12} fill={categorical8[0]} rx={2} />
		<text x={16}  y={12} class="st-legend">% da população no território</text>
		<rect x={190} y={2}  width={12} height={12} fill={categorical8[2]} rx={2} />
		<text x={206} y={12} class="st-legend">% dos recursos executados</text>
		<rect x={370} y={2}  width={12} height={12} fill={categorical8[4]} rx={2} />
		<text x={386} y={12} class="st-legend">% dos agentes contemplados</text>

		{#each specialTerritoriesMetrics as d, ti}
			{@const blockY = 30 + ti * 92}
			{@const w0 = d.perc_populacao / 10 * 290}
			{@const w1 = d.perc_recurso   / 10 * 290}
			{@const w2 = d.perc_agentes   / 10 * 290}

			<text x={0}   y={blockY + 10} class="st-territory">{d.shortLabel}</text>
			<text x={560} y={blockY + 10} text-anchor="end" class="st-valor">{formatBRL(d.valor)}</text>
			<line x1={0} y1={blockY + 16} x2={560} y2={blockY + 16} class="st-separator" />

			<text x={154} y={blockY + 34} text-anchor="end" class="st-label">% da população</text>
			<rect x={160} y={blockY + 22} width={290} height={14} fill="#f1f5f9" rx={2} />
			<rect x={160} y={blockY + 22} width={w0}  height={14} fill={categorical8[0]} rx={2} />
			<text x={160 + w0 + 5} y={blockY + 33} class="st-value">{d.perc_populacao.toFixed(2)}%</text>

			<text x={154} y={blockY + 56} text-anchor="end" class="st-label">% dos recursos</text>
			<rect x={160} y={blockY + 44} width={290} height={14} fill="#f1f5f9" rx={2} />
			<rect x={160} y={blockY + 44} width={w1}  height={14} fill={categorical8[2]} rx={2} />
			<text x={160 + w1 + 5} y={blockY + 55} class="st-value">{d.perc_recurso.toFixed(2)}%</text>

			<text x={154} y={blockY + 78} text-anchor="end" class="st-label">% dos agentes</text>
			<rect x={160} y={blockY + 66} width={290} height={14} fill="#f1f5f9" rx={2} />
			<rect x={160} y={blockY + 66} width={w2}  height={14} fill={categorical8[4]} rx={2} />
			<text x={160 + w2 + 5} y={blockY + 77} class="st-value">{d.perc_agentes.toFixed(2)}%</text>
		{/each}
	</svg>

	<div style="padding-left: 100px; margin-top: 2rem;">
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
		max-width: 20ch;
	}

	.frase-destaque {
		font-size: 1.15rem;
		font-weight: 600;
		font-style: italic;
		border-left: 3px solid var(--color-accent, currentColor);
		padding-left: 1rem;
		opacity: 0.85;
		margin: 1.5rem 0;
	}

	.metodologico {
		font-size: 0.88rem;
		opacity: 0.7;
		background: var(--color-surface, #f8fafc);
		border: 1px solid var(--color-border, #e2e8f0);
		border-radius: 6px;
		padding: 0.75rem 1rem;
		margin-bottom: 1.5rem;
	}

	:global(.st-legend) {
		font-size: 10px;
		fill: var(--color-text, #334155);
		dominant-baseline: middle;
	}

	:global(.st-territory) {
		font-size: 12px;
		font-weight: 700;
		fill: var(--color-text, #334155);
		dominant-baseline: middle;
	}

	:global(.st-valor) {
		font-size: 11px;
		fill: var(--color-text, #334155);
		opacity: 0.55;
		dominant-baseline: middle;
	}

	:global(.st-separator) {
		stroke: var(--color-border, #e2e8f0);
		stroke-width: 1;
	}

	:global(.st-label) {
		font-size: 11px;
		fill: var(--color-text, #334155);
		opacity: 0.7;
		dominant-baseline: middle;
	}

	:global(.st-value) {
		font-size: 11px;
		font-weight: 600;
		fill: var(--color-text, #334155);
		dominant-baseline: middle;
	}
</style>
