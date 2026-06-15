<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import BodySilhouette from '$lib/components/BodySilhouette.svelte';
	import HorizontalGroupedBarChart from '$lib/components/HorizontalGroupedBarChart.svelte';
	import CboRaisTable from '$lib/components/CboRaisTable.svelte';
	import VerticalGroupedBarChart from '$lib/components/VerticalGroupedBarChart.svelte';
	import HorizontalBarChartCustom from '$lib/components/HorizontalBarChartCustom.svelte';
	import HorizontalStackedBarChartCustom from '$lib/components/HorizontalStackedBarChartCustom.svelte';
	import {
		BigNumber,
		HorizontalBarChart,
		HorizontalStackedBarChart,
		DivergingBarChart,
		HeatMap,
		TreemapChart,
		RegionSilhouetteChart,
		colorPairs,
		colorScales,
		categorical8,
	} from 'sniic-design-system';
	import {
		percSemVinculo,
		percComVinculo,
		totalBenef,
		totalSemVinculo,
		totalComVinculo,
		valorTotal,
		ageGroupStackedData,
		ageGroupKeys,
		ageGroupLabels,
		escolaridadeProporcionalData,
		escolaridadeValorMedioData,
		regionStackedData,
		regionSilhouetteData,
		regionComparisonGroupedData,
		ufComparisonGroupedData,
		sexoDivergingData,
		sexoVinculoFormalGroupedData,
		sexoComparisonStackedData,
		sexoComparisonStackedKeys,
		sexoComparisonStackedLabels,
		racaCorBarData,
		racaCorGroupedData,
		racaCorComparisonGroupedData,
		racaCorTreemapData,
		racaCorSexoHeatmapData,
		racaCorSexoGroupedData,
		racaCorSexoComparisonData,
		ufRankingData,
		ufByRegionGroups,
		cboRaisTop20,
		cboRaisTableHeight,
		escolaridadeComparisonGroupedData,
		escolaridadeValorMedioNewData,
	} from '$lib/data/section4';
	import { top20CboData } from '$lib/data/section3';

	const formatBRL = (v: number) =>
		`R$${new Intl.NumberFormat('pt-BR', { notation: 'compact', maximumFractionDigits: 1 }).format(v)}`;
	const formatN    = (v: number) => v.toLocaleString('pt-BR');
	const formatPct  = (v: number) => `${v.toFixed(1)}%`;
	const formatPctN = (v: number) =>
		v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';

	const bodyAnnotations = [
		{ side: 'right' as const, pointX: 230, pointY: 68,  boxX: 445, boxY: 20,  title: 'Identidade',     subtitle: 'Homem negro.',                color: '#265c4f', circleRadius: 16 },
		{ side: 'right' as const, pointX: 154, pointY: 155, boxX: 445, boxY: 105, title: 'Território',      subtitle: 'Nordeste.',                   color: '#4271b5', circleRadius: 12 },
		{ side: 'right' as const, pointX: 226, pointY: 220, boxX: 445, boxY: 190, title: 'Idade',           subtitle: '45 anos.',                    color: '#ea662f', circleRadius: 12 },
		{ side: 'right' as const, pointX: 334, pointY: 255, boxX: 445, boxY: 275, title: 'Trabalho',        subtitle: 'Professor.',                  color: '#a44c7f', circleRadius: 12 },
		{ side: 'right' as const, pointX: 260, pointY: 380, boxX: 445, boxY: 360, title: 'Escolaridade',    subtitle: 'Ensino superior completo.',   color: '#81a72f', circleRadius: 12 },
		{ side: 'right' as const, pointX: 250, pointY: 520, boxX: 445, boxY: 445, title: 'Valor repassado', subtitle: 'Aporte de R$ 12 mil.',        color: '#cb4034', circleRadius: 12 },
	];
</script>

<!-- ══════════════════════════════════════════════════════════════════════════
     INTRODUÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-intro">
	<h2>4. Quem são e no que se ocupam os trabalhadores formais contemplados pela Aldir Blanc?</h2>
	<p>
		Esta seção analisa a inserção dos trabalhadores culturais contemplados pela Aldir Blanc no
		mercado de trabalho formal, considerando suas ocupações, tipos de vínculo e condições de
		atuação profissional.
	</p>
	<div class="annotation-box">
		As análises desta seção foram elaboradas a partir do cruzamento dos dados dos agentes culturais
		contemplados com os dados da RAIS (Relação Anual de Informações Sociais) entre os anos de 2022
		e 2024. A RAIS é um registro administrativo do governo federal que reúne informações sobre
		vínculos formais de trabalho no Brasil. Os dados são declarados anualmente pelos empregadores e
		incluem informações sobre trabalhadores e estabelecimentos. É importante destacar que a ausência
		de registro dos agentes culturais na RAIS não necessariamente significa que esses estão na
		informalidade, haja vista a possibilidade de atuarem por meio da constituição de pessoas
		jurídicas.
	</div>
	<div class="bignumbers-row" style="margin-top: 2rem;">
		<div class="bignumber-cell">
			<BigNumber value={percComVinculo.toFixed(1)} suffix="%" fontSize={80} label="com vínculo formal de trabalho" />
		</div>
	</div>
	<p>
		Parcela significativa dos agentes culturais contemplados possuem vínculo formal de trabalho,
		enquanto <strong>{formatPct(percSemVinculo)}</strong> não tiveram vínculo formal identificado na
		fonte de informação referente à situação trabalhista consultada.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PERSONA — PERFIL DO BENEFICIÁRIO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-persona">
	<h3>Perfil Representativo das Pessoas Físicas que Acessaram Recursos da PNAB e estão no Mercado Formal de Trabalho</h3>
	<div class="silhouette-wrap">
		<BodySilhouette annotations={bodyAnnotations} />
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.1 — ONDE ESTÃO OS TRABALHADORES FORMAIS?
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-41">
	<h2>4.1. Onde estão os trabalhadores formais contemplados pela Aldir Blanc?</h2>
	<p class="frase-destaque">
		Nordeste é a Região que mais se destaca, com <strong>48,6%</strong> do total de contemplados
		pela Aldir Blanc com vínculo formal de trabalho. Esse percentual é expressivo quando comparado
		à participação da região no mercado formal brasileiro, uma vez que o Nordeste respondia por
		<strong>18,58%</strong> dos trabalhadores formais do país em 2024.
	</p>
	<p>
		O peso expressivo da região Nordeste é puxado principalmente pelas UFs Bahia
		(<strong>11,2%</strong>), Pernambuco (<strong>8,1%</strong>) e Paraíba (<strong>6,3%</strong>).
	</p>
	<p>
		Em comparação, o Sudeste aparece em segundo lugar, com <strong>26,5%</strong>, com destaque
		para a participação de Minas Gerais (<strong>13,4%</strong>) e São Paulo (<strong>9,3%</strong
		>). Apesar disso, a região está proporcionalmente abaixo de seu peso no mercado formal, uma vez
		que concentrava <strong>48,34%</strong> dos vínculos formais da RAIS 2024.
	</p>
	<p>
		Já as demais regiões apresentam participação significativamente menor: Norte
		(<strong>10,6%</strong>), Sul (<strong>8,2%</strong>) e Centro-Oeste (<strong>6,2%</strong>).
		Em comparação com a base completa da RAIS 2024, o Norte aparece proporcionalmente acima de seu
		peso no mercado formal (<strong>6,15%</strong> dos vínculos formais do país). Já o Sul e o
		Centro-Oeste aparecem abaixo de sua participação na RAIS, onde respondem por
		<strong>17,08%</strong> e <strong>9,86%</strong> dos vínculos, respectivamente.
	</p>
	<RegionSilhouetteChart
		data={regionSilhouetteData}
		maxSize={100}
		colors={categorical8}
		format={formatN}
		showLabels={true}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     GRÁFICO 23 — Distribuição por Região: PNAB vs RAIS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-grafico-23">
	<h3>Gráfico 23 — Distribuição dos Agentes Culturais Pessoas Físicas contemplados pela Aldir Blanc com Vínculo de Trabalho Formal por Região</h3>
	<HorizontalGroupedBarChart
		data={regionComparisonGroupedData}
		seriesLabels={['Contemplados PNAB', 'Vínculos RAIS 2024']}
		colors={[categorical8[0], '#cb4034']}
		format={formatPctN}
		xLabel="% do total"
		margin={{ top: 20, right: 80, bottom: 40, left: 120 }}
		barHeight={20}
		groupPad={24}
		rx={0}
		crispEdges
		labelsInside
		legendBottom={true}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.1 — DISTRIBUIÇÃO REGIONAL (STACKED) E POR UF
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-41-regions">
	<HorizontalStackedBarChart
		data={regionStackedData}
		keys={[...ageGroupKeys]}
		labels={ageGroupLabels}
		colors={[colorScales.red[2], colorScales.blue[2]]}
		format={formatPct}
		showTotalLabel={false}
	/>
	<p style="margin-top: 2rem;">
		Os estados com maior proporção de trabalhadores sem vínculo formal estão quase todos no
		Nordeste. Piauí, Pernambuco e Paraíba lideram dentro da região. No outro extremo, Amapá, Acre
		e Rondônia, no Norte, são os estados com maior formalização relativa.
	</p>
	{#each ufByRegionGroups as { regiao, colors, avgInformal, data }}
		<div class="region-block">
			<div class="region-header">
				<span class="region-swatch" style="background: {colors[1]}"></span>
				<strong>{regiao}</strong>
				<span class="region-avg">média: {formatPctN(avgInformal)} sem vínculo</span>
			</div>
			<HorizontalStackedBarChart
				{data}
				keys={[...ageGroupKeys]}
				labels={ageGroupLabels}
				{colors}
				format={formatPct}
				showTotalLabel={false}
			/>
		</div>
	{/each}
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     GRÁFICO 24 — Distribuição por UF: PNAB vs RAIS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-grafico-24">
	<h3>Gráfico 24 — Distribuição dos Agentes Culturais Pessoas Físicas contemplados pela Aldir Blanc com vínculo de trabalho formal por UF</h3>
	<HorizontalGroupedBarChart
		data={ufComparisonGroupedData}
		seriesLabels={['Contemplados PNAB', 'Vínculos RAIS 2024']}
		colors={[categorical8[0], '#cb4034']}
		format={formatPctN}
		xLabel="% do total"
		margin={{ top: 20, right: 80, bottom: 40, left: 50 }}
		barHeight={14}
		barPad={3}
		rx={0}
		crispEdges
		labelsInside
		legendBottom={true}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.2 — PERFIL: SEXO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-42-sexo">
	<h2>4.2. Qual o perfil dos trabalhadores formais contemplados pela Aldir Blanc?</h2>
	<h3>4.2.1. Sexo</h3>
	<p class="frase-destaque">
		Desigualdade entre homens e mulheres é mais acentuada no mercado de trabalho formal
	</p>
	<p>
		Entre os trabalhadores contemplados que estão inseridos no mercado formal,
		<strong>58,3%</strong> são homens e <strong>41,7%</strong> são mulheres. Essa diferença,
		superior ao patamar geral observado na análise do total de pessoas físicas contempladas
		(<strong>53,2%</strong> de homens e <strong>46,8%</strong> de mulheres), indica que as
		desigualdades de acesso são ainda mais acentuadas entre agentes culturais contemplados
		inseridos nos postos formais de trabalho.
	</p>
	<div style="overflow: hidden;">
		<DivergingBarChart
			data={sexoDivergingData}
			leftLabel="Sem vínculo formal"
			rightLabel="Com vínculo formal"
			referenceValue={50}
			referenceLabel="50%"
			colors={colorPairs.blueOrange}
		/>
	</div>
	<VerticalGroupedBarChart
		data={sexoVinculoFormalGroupedData}
		seriesLabels={['Feminino', 'Masculino']}
		colors={['#cb4034', '#a44c7f']}
		format={(v) => `${v.toFixed(1)}%`}
		barWidth={40}
		barPad={8}
		innerH={280}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     GRÁFICO 25 — Sexo: PNAB vs RAIS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-grafico-25">
	<h3>Gráfico 25 — Comparativo entre Distribuição de Agentes Culturais com Vínculo Formal de Trabalho Contemplados na Aldir Blanc por Sexo e Distribuição de Pessoas com Vínculo Formal no Brasil por Sexo</h3>
	<HorizontalStackedBarChartCustom
		data={sexoComparisonStackedData}
		keys={[...sexoComparisonStackedKeys]}
		labels={sexoComparisonStackedLabels}
		colors={[categorical8[0], '#cb4034']}
		format={formatPctN}
		labelsAbove
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.2.2 — PERFIL: IDADE
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-42-idade">
	<h3>4.2.2. Idade</h3>
	<p class="frase-destaque">
		Vínculos formais se concentram entre profissionais de 25 a 54 anos
	</p>
	<HorizontalStackedBarChart
		data={ageGroupStackedData}
		keys={[...ageGroupKeys]}
		labels={ageGroupLabels}
		colors={[colorScales.red[2], colorScales.blue[2]]}
		format={formatPct}
		showTotalLabel={false}
	/>
	<p>
		Os profissionais entre 25 e 54 anos concentram a maior parte dos vínculos formais no programa,
		somando <strong>81,6%</strong> do total, retratando a população economicamente ativa.
	</p>
	<p>
		Essa participação diminui nas extremidades da pirâmide etária: os jovens de 15 a 24 anos
		representam <strong>6,7%</strong> e as pessoas acima de 65 anos respondem por
		<strong>2,3%</strong>. A participação desses dois grupos é menor do que a observada no conjunto
		geral da política (<strong>8%</strong> de jovens e <strong>8,6%</strong> de idosos). Acredita-se
		que essa dinâmica decorre da própria estrutura do mercado de trabalho formal.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.2.3 — PERFIL: RAÇA/COR
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-42-raca">
	<h3>4.2.3. Raça/cor</h3>
	<p class="frase-destaque">
		A maioria dos trabalhadores formais que receberam recursos da Aldir Blanc é negra: pessoas
		pretas e pardas somam <strong>62,4%</strong> do total de contemplados
	</p>
	<h4>Gráfico 26 — Distribuição dos Agentes Culturais Pessoas Físicas Contemplados pela Aldir Blanc com Vínculo Formal de Trabalho por Raça/Cor</h4>
	<HorizontalGroupedBarChart
		data={racaCorComparisonGroupedData}
		seriesLabels={['Contemplados PNAB', 'Vínculos RAIS 2024']}
		colors={[categorical8[0], '#cb4034']}
		format={formatPctN}
		xLabel="% do total"
		margin={{ top: 20, right: 80, bottom: 40, left: 120 }}
		barHeight={20}
		rx={0}
		crispEdges
		labelsInside
		legendBottom={true}
	/>
	<p>
		Pessoas pardas formam o grupo mais expressivo, representando <strong>51,4%</strong> dos agentes
		e <strong>46,8%</strong> dos recursos repassados. Somadas à população preta
		(<strong>10,9%</strong> dos contemplados e <strong>15,6%</strong> dos recursos), as pessoas
		negras concentram <strong>62,4%</strong> dos trabalhadores formais e <strong>62,5%</strong> do
		volume total de recursos.
	</p>
	<p>
		Esse resultado é particularmente importante em perspectiva ao perfil racial de trabalhadores
		gerais da economia criativa. Entre os terceiros trimestres de 2023 e 2024, a proporção de
		trabalhadores negros em relação ao total de ocupados na economia criativa foi, em média, de
		<strong>42%</strong> (33% pardos e 9% pretos), em contraste com os 55% observados para o
		agregado do mercado de trabalho da economia brasileira no mesmo período. Nesse sentido, o
		resultado de uma participação de trabalhadores negros 20 pontos percentuais maior no universo
		de contemplados da Aldir Blanc ganha expressividade, sendo possivelmente resultado das ações
		afirmativas voltadas aos agentes culturais com esse perfil.
	</p>
	<p>
		O segundo grupo com maior participação é o de pessoas brancas, que representam
		<strong>34,7%</strong> dos contemplados e <strong>33,8%</strong> dos recursos. Já as pessoas
		indígenas e amarelas aparecem com menor presença, ambas com representação de
		<strong>1,5%</strong>. Destaca-se, sobretudo, o baixo percentual de pessoas indígenas frente à
		previsão de reserva mínima de 10% das vagas — dado também afetado pela baixa presença de
		pessoas indígenas com vínculo de trabalho formal no universo da RAIS (<strong>0,33%</strong> em
		2024).
	</p>
	<p>
		A distribuição racial observada acompanha de perto o perfil demográfico identificado no último
		Censo (IBGE, 2022). Na população brasileira, pessoas pardas correspondem a <strong>45,3%</strong
		>, brancas a <strong>43,5%</strong>, pretas a <strong>10,2%</strong>, indígenas a
		<strong>0,6%</strong> e amarelas a <strong>0,3%</strong>.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.2.3 — RAÇA/COR × SEXO (INTERSECCIONALIDADE)
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-42-raca-intersec">
	<p class="frase-destaque">
		Dentre os trabalhadores formais, os homens negros foram os mais contemplados pela Aldir Blanc
		com <strong>37,8%</strong>
	</p>
	<h4>Gráfico 27 — Distribuição Pessoas Físicas Contempladas na Aldir Blanc com Vínculo Formal de Trabalho por Raça/Cor e Sexo</h4>
	<HorizontalGroupedBarChart
		data={racaCorSexoComparisonData}
		seriesLabels={['Masculino', 'Feminino']}
		colors={[categorical8[0], '#cb4034']}
		format={formatPctN}
		xLabel="% do total de beneficiários com vínculo formal"
		margin={{ top: 20, right: 80, bottom: 40, left: 120 }}
		barHeight={20}
		rx={0}
		crispEdges
		labelsInside
		legendBottom={true}
	/>
	<p>
		Ao analisar a interseccionalidade entre raça e gênero, os dados revelam desigualdades
		importantes. As pessoas negras (pretas e pardas) constituem o grupo mais expressivo, porém com
		forte assimetria interna: os homens negros concentram maior participação (<strong>37,8%</strong>
		dos contemplados e <strong>36,1%</strong> dos recursos), enquanto as mulheres negras aparecem
		com presença significativamente menor (<strong>24,5%</strong> e <strong>26,4%</strong> dos
		recursos).
	</p>
	<p>
		Entre as pessoas brancas, também se observa predominância masculina (<strong>19,1%</strong> dos
		contemplados e <strong>17,9%</strong> dos recursos, frente a <strong>15,6%</strong> e
		<strong>15,9%</strong> entre mulheres), ainda que com maior equilíbrio proporcional. Já
		indígenas e amarelos apresentam baixa participação em ambos os gêneros.
	</p>
	<p>
		Em conjunto, a análise interseccional evidencia que raça e gênero se combinam para produzir
		diferentes níveis de acesso, com maior concentração entre homens — especialmente homens negros
		— e menor inserção relativa das mulheres, sobretudo nas interseções mais vulnerabilizadas.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.2.4 — PERFIL: ESCOLARIDADE
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-42-escolaridade">
	<h3>4.2.4. Escolaridade</h3>
	<p class="frase-destaque">
		Ensino médio e superior completos predominam entre os trabalhadores formais contemplados pela
		Aldir Blanc
	</p>
	<h4>Gráfico 28 — Distribuição de Agentes Culturais Pessoas Físicas Contemplados na Aldir Blanc com Vínculo Formal de Trabalho por Escolaridade</h4>
	<HorizontalGroupedBarChart
		data={escolaridadeComparisonGroupedData}
		seriesLabels={['PNAB', 'Total trabalhadores formais']}
		colors={[categorical8[0], '#cb4034']}
		format={formatPctN}
		xLabel="% do total"
		margin={{ top: 20, right: 80, bottom: 40, left: 260 }}
		barHeight={20}
		rx={0}
		crispEdges
		labelsInside
		legendBottom={true}
	/>
	<p>
		Quase metade dos agentes fomentados no primeiro ciclo possui ensino médio completo ou curso
		superior incompleto (<strong>44,1%</strong>). O segundo grupo mais representativo foi o dos
		contemplados com ensino superior completo, que corresponderam a <strong>42,8%</strong> do total.
	</p>
	<p>
		Essa predominância reflete uma característica particular do campo cultural, cuja força de
		trabalho apresenta nível de escolaridade mais elevado do que a média nacional. Enquanto
		<strong>23,4%</strong> do total de trabalhadores formais possuem ensino superior, no setor
		cultural esse percentual chega a <strong>30,1%</strong> (IBGE, 2024).
	</p>
	<p>
		Em contraste, os contemplados com escolaridade até o ensino médio incompleto representam apenas
		<strong>9,9%</strong> dos contemplados. Os números sugerem que, embora o fomento valorize a
		qualificação técnica, a estrutura dos editais ainda impõe barreiras para quem possui menos
		tempo de instrução formal.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.2.4 — ESCOLARIDADE: VALOR MÉDIO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-42-escolaridade-valor">
	<p class="frase-destaque">
		Escolaridade mais alta está associada a valores médios maiores
	</p>
	<h4>Gráfico 29 — Valor Médio Recebido pelas Pessoas Físicas Contemplados na Aldir Blanc com Vínculo Formal de Trabalho por Escolaridade</h4>
	<HorizontalBarChartCustom
		data={escolaridadeValorMedioNewData}
		color={categorical8[0]}
		format={formatBRL}
		xLabel="Valor médio recebido (R$)"
		margin={{ top: 20, right: 100, bottom: 40, left: 260 }}
	/>
	<p>
		Os dados mostram que o valor médio dos projetos fomentados aumenta a cada etapa de estudo
		concluída. <strong>Entre os agentes culturais que receberam recursos e possuem vínculo de
		trabalho formal — os com ensino superior receberam, em média, o dobro do valor destinado
		àqueles que estudaram até o ensino fundamental.</strong>
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.2.5 — PESSOAS COM DEFICIÊNCIA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-42-pcd">
	<h3>4.2.5. Pessoas com deficiência</h3>
	<p class="frase-destaque">
		Embora tenham recebido, em média, valores R$8,7 mil superiores aos dos demais contemplados, as
		pessoas com deficiência representam apenas <strong>0,9%</strong> dos trabalhadores formais
		contemplados com recursos da Aldir Blanc
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value="R$10,8mi" fontSize={64} label="para PcD" subtitle="1,7% do total" />
		</div>
		<div class="bignumber-cell">
			<BigNumber value="R$18.805" fontSize={64} label="repasse médio — PcD" />
		</div>
	</div>
	<p>
		Apesar da participação numérica ainda incipiente, o repasse médio recebido por esse grupo
		destacou-se frente à média geral de <strong>R$10.021</strong> entre os contemplados inseridos
		no mercado formal.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.3 — OCUPAÇÕES DOS TRABALHADORES FORMAIS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-43">
	<h2>4.3. Quais as ocupações dos trabalhadores formais contemplados pela Aldir Blanc?</h2>
	<h3>4.3.1. Ocupações gerais</h3>
	<div class="annotation-box">
		Foram identificadas as ocupações dos agentes culturais contemplados pela Aldir Blanc que
		possuíam vínculo formal de trabalho entre 2022 e 2024. A classificação das ocupações segue o
		Código Brasileiro de Ocupações (CBO).
	</div>
	<p>
		O conjunto dos dados demonstra que a política alcançou pessoas que atuam em funções não
		estritamente culturais, possivelmente conciliando a atuação no campo cultural com outras
		atividades profissionais.
	</p>
	<p>
		O grupo de maior destaque é o das ocupações ligadas à educação, especialmente professores em
		diferentes níveis e áreas de ensino e formação. No ranking das 20 ocupações mais proeminentes,
		oito correspondem a professores e instrutores, que juntos somam <strong>13,9%</strong> dos
		contemplados.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     4.3.1 — TOP 20 OCUPAÇÕES (CBO)
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-43-cbo">
	<HorizontalBarChart
		data={top20CboData}
		color={categorical8[0]}
		format={formatN}
		xLabel="Quantidade de vínculos formais"
		margin={{ top: 20, right: 60, bottom: 40, left: 320 }}
	/>
	<div style="overflow-x: auto; margin-top: 2rem;">
		<svg width={700} height={cboRaisTableHeight}>
			<CboRaisTable data={cboRaisTop20} width={700} />
		</svg>
	</div>
	<p>
		A análise revela ainda a forte presença de funções administrativas variadas. A ocupação de
		assistente administrativo lidera com <strong>8,2%</strong> dos vínculos, seguida por auxiliar
		de escritório (<strong>4,3%</strong>), supervisor administrativo (<strong>1,6%</strong>),
		recepcionista (<strong>1,1%</strong>) e secretário executivo (<strong>0,8%</strong>). Juntas,
		essas ocupações somam <strong>16%</strong> dos contemplados.
	</p>
	<p>
		Atividades de serviços gerais, como faxineiro (<strong>2,5%</strong>) e trabalhadores de
		limpeza (<strong>1,5%</strong>), também aparecem com participação relevante.
	</p>
	<div class="cnae-box" style="margin-top: 2rem;">
		<strong>Ocupações Relacionadas a Eventos Culturais — o pessoal "da graxa"</strong>
		<p>
			Analisamos as 20 ocupações diretamente ligadas à realização de eventos culturais mais
			proeminentes a partir das classificações utilizadas para o projeto "Mapeamento das ocupações
			técnicas da cultura: o mapa da graxa" (IPEA, 2025). Os resultados indicam que essas
			atividades possuem baixa participação no total dos agentes culturais contemplados com vínculos
			formais — todas abaixo de 1%.
		</p>
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
		justify-content: center;
		margin-top: 1.5rem;
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

	.silhouette-wrap {
		margin-top: 1.5rem;
		max-width: 680px;
		margin-inline: auto;
	}

	.silhouette-wrap :global(svg) {
		width: 100%;
		height: auto;
		display: block;
	}

	.region-block {
		margin-bottom: 2rem;
	}

	.region-header {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 0.25rem;
	}

	.region-swatch {
		display: inline-block;
		width: 12px;
		height: 12px;
		border-radius: 3px;
		flex-shrink: 0;
	}

	.region-avg {
		font-size: 0.8rem;
		opacity: 0.6;
		margin-left: auto;
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
