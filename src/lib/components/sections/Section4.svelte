<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import {
		BigNumber,
		HorizontalBarChart,
		HorizontalStackedBarChart,
		DivergingBarChart,
		ProportionalAreaChart,
		HeatMap,
		TreemapChart,
		RegionSilhouetteChart,
		StatesSilhouetteChart,
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
		valorAreaData,
		ageGroupStackedData,
		ageGroupKeys,
		ageGroupLabels,
		escolaridadeBarData,
		regionStackedData,
		regionSilhouetteData,
		sexoDivergingData,
		racaCorBarData,
		racaCorTreemapData,
		racaCorSexoHeatmapData,
		ufSilhouetteData,
		ufRankingData,
	} from '$lib/data/section4';

	const formatBRL  = (v: number) =>
		new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact', maximumFractionDigits: 1 }).format(v);
	const formatN    = (v: number) => v.toLocaleString('pt-BR');
	const formatPct  = (v: number) => `${v.toFixed(1)}%`;
	const formatPctN = (v: number) => v.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';
</script>

<!-- ══════════════════════════════════════════════════════════════════════════
     INTRODUÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-intro">
	<h2>4. Qual é o vínculo com o mercado formal de trabalho?</h2>
	<p>
		Os beneficiários da Política Nacional Aldir Blanc são majoritariamente trabalhadores
		<strong>informais</strong>. O cruzamento dos dados do PNAB com a RAIS revela que mais
		da metade não possui nenhum vínculo registrado com o trabalho formal —
		um retrato da precariedade estrutural do setor cultural no Brasil.
	</p>
	<p>
		Nesta seção, analisamos como essa divisão entre trabalhadores com e sem vínculo formal
		se distribui por faixa etária, escolaridade, região, sexo, raça/cor e unidade federativa.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     GRANDES NÚMEROS — TOTAIS
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-totals">
	<h2>4. Quem são e no que se ocupam os trabalhadores formais contemplados pela Aldir Blanc?</h2>
	<p>
		Do total de <strong>{formatN(totalBenef)}</strong> beneficiários analisados,
		<strong>{formatN(totalSemVinculo)}</strong> — ou seja, <strong>{formatPct(percSemVinculo)}</strong> —
		não possuem vínculo com o trabalho formal. Apenas <strong>{formatN(totalComVinculo)}</strong>
		({formatPct(percComVinculo)}) têm registro formal de emprego.
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={percSemVinculo.toFixed(1)} suffix="%" fontSize={80} />
			<p class="bignumber-caption">sem vínculo com o trabalho formal</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={percComVinculo.toFixed(1)} suffix="%" fontSize={80} />
			<p class="bignumber-caption">com vínculo com o trabalho formal</p>
		</div>
	</div>
	<div style="margin-top: 2rem;">
		<p>
			O valor total pago ao conjunto de beneficiários analisados foi de <strong>{formatBRL(valorTotal)}</strong>.
			As áreas abaixo representam proporcionalmente o valor destinado a cada grupo.
		</p>
		<ProportionalAreaChart
			data={valorAreaData}
			maxRadius={120}
			colors={[colorScales.red[2], colorScales.blue[2]]}
			format={formatBRL}
			showLabels={true}
		/>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     POR SEXO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-sexo">
	<h3>Mulheres são mais afetadas pela informalidade</h3>
	<p>
		Entre as mulheres beneficiárias, <strong>60,1%</strong> não possuem vínculo formal —
		proporção maior do que a observada entre os homens (<strong>51,1%</strong>).
		A informalidade atinge ambos os sexos, mas pesa mais sobre as trabalhadoras do setor cultural.
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
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     POR FAIXA ETÁRIA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-age">
	<h3>Trabalhadores mais velhos têm menos vínculo formal</h3>
	<p>
		A faixa de <strong>25 a 54 anos</strong> é a única em que os beneficiários com vínculo formal
		superam os sem vínculo (51,7% vs 48,3%). Entre os <strong>idosos (65+)</strong>,
		a informalidade atinge <strong>88%</strong> — reflexo de carreiras construídas fora do
		mercado formal ao longo de décadas.
	</p>
	<HorizontalStackedBarChart
		data={ageGroupStackedData}
		keys={[...ageGroupKeys]}
		labels={ageGroupLabels}
		colors={[colorScales.red[2], colorScales.blue[2]]}
		format={formatPct}
		showTotalLabel={false}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     POR ESCOLARIDADE
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-escolaridade">
	<h3>Quanto mais estudo, mais vínculo formal</h3>
	<p>
		Entre os beneficiários <em>com</em> vínculo formal, o nível de escolaridade é elevado:
		<strong>médio completo ou superior incompleto</strong> e <strong>superior completo</strong>
		concentram juntos mais de 87% desse grupo. Apenas 3,2% têm pós-graduação, mas esse grupo
		recebe proporcionalmente mais — reflexo de remunerações maiores no mercado formal.
	</p>
	<HorizontalBarChart
		data={escolaridadeBarData}
		color={colorScales.blue[2]}
		format={formatN}
		xLabel="Beneficiários com vínculo formal"
		margin={{ top: 20, right: 60, bottom: 40, left: 260 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     POR REGIÃO — STACKED
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-region-stacked">
	<h3>Nordeste concentra a maior informalidade regional</h3>
	<p>
		O <strong>Nordeste</strong> é a região com maior proporção de beneficiários sem vínculo
		formal (58,5%). <strong>Centro-Oeste</strong> e <strong>Norte</strong> apresentam
		distribuição mais equilibrada, próxima de 50/50.
	</p>
	<HorizontalStackedBarChart
		data={regionStackedData}
		keys={[...ageGroupKeys]}
		labels={ageGroupLabels}
		colors={[colorScales.red[2], colorScales.blue[2]]}
		format={formatPct}
		showTotalLabel={false}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     POR REGIÃO — SILHOUETTE
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-region-silhouette">
	<h3>Nordeste lidera em número absoluto de trabalhadores formais</h3>
	<p>
		Em termos absolutos, o <strong>Nordeste</strong> concentra o maior número de beneficiários
		com vínculo formal — consequência natural do maior volume total de beneficiários na região.
		O <strong>Sudeste</strong> vem em segundo lugar.
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
     POR RAÇA/COR — BARRA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-raca-bar">
	<h3>Pardos e brancos dominam o emprego formal no setor cultural</h3>
	<p>
		Entre os beneficiários com vínculo formal, <strong>pardos</strong> respondem por 44,9%
		e <strong>brancos</strong> por 30,3%. <strong>Pretos/negros</strong> representam
		apenas 9,6% — desproporcionalmente baixo em relação à presença na população geral.
	</p>
	<HorizontalBarChart
		data={racaCorBarData}
		color={categorical8[0]}
		format={formatN}
		xLabel="Beneficiários com vínculo formal"
		margin={{ top: 20, right: 60, bottom: 40, left: 120 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     POR RAÇA/COR — TREEMAP
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-raca-treemap">
	<h3>A concentração racial do emprego formal em área proporcional</h3>
	<p>
		O mapa de áreas torna visível a concentração: <strong>Parda</strong> e
		<strong>Branca</strong> juntas ocupam mais de três quartos do espaço —
		enquanto Preta/negra, Indígena e Amarela permanecem em fatias muito menores.
	</p>
	<TreemapChart
		data={racaCorTreemapData}
		height={380}
		format={formatN}
		colors={categorical8}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     RAÇA/COR × SEXO — HEATMAP
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-raca-sexo">
	<h3>Intersecção raça e sexo: homens pardos lideram</h3>
	<p>
		O cruzamento de raça/cor com sexo revela que <strong>homens pardos</strong> formam o
		maior grupo com vínculo formal, seguidos de <strong>homens brancos</strong>.
		Em todos os grupos raciais, os homens superam as mulheres em termos de vínculo formal —
		reforçando o padrão de desvantagem feminina no mercado formal de trabalho cultural.
	</p>
	<HeatMap
		data={racaCorSexoHeatmapData}
		height={320}
		colorRange={colorScales.blue}
		xLabel="Sexo"
		yLabel="Raça/cor"
		format={(v: number) => formatN(v)}
		showValues={true}
		showLegend={true}
		cellRadius={3}
		cellGap={4}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     POR UF — SILHOUETTE
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-uf-silhouette">
	<h3>Distribuição estadual dos beneficiários com vínculo formal</h3>
	<p>
		A concentração de trabalhadores formais do setor cultural acompanha o peso econômico
		dos estados. <strong>São Paulo, Minas Gerais e Bahia</strong> lideram em volume absoluto.
	</p>
	<StatesSilhouetteChart
		data={ufSilhouetteData}
		maxSize={120}
		colors={categorical8}
		format={formatN}
		showLabels={true}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     POR UF — RANKING % COM VÍNCULO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-uf-ranking">
	<h3>Qual estado tem maior proporção de trabalhadores formais?</h3>
	<p>
		Normalizado pelo total de beneficiários de cada estado, o ranking muda:
		<strong>Amapá</strong> e <strong>Acre</strong> sobem ao topo — estados onde a
		infraestrutura cultural formal, embora pequena em volume, é relativamente mais presente.
		Estados do Nordeste tendem a ocupar as posições inferiores.
	</p>
	<HorizontalBarChart
		data={ufRankingData}
		color={colorScales.blue[2]}
		format={formatPctN}
		xLabel="% beneficiários com vínculo formal"
		margin={{ top: 20, right: 60, bottom: 40, left: 50 }}
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
		margin-top: 1.5rem;
	}

	.bignumber-caption {
		font-size: 0.95rem;
		color: var(--color-text);
		text-align: center;
		opacity: 0.75;
		max-width: 20ch;
	}
</style>
