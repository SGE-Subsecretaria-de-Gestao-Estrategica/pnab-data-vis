<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import BodySilhouette from '$lib/components/BodySilhouette.svelte';
	import EnterpriseSilhouette from '$lib/components/EnterpriseSilhouette.svelte';
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

	const bodyAnnotations = [
		{ side: 'right' as const, pointX: 230, pointY: 68,  boxX: 445, boxY: 20,  title: 'Identidade',       subtitle: 'Homem negro.',                color: '#265c4f', circleRadius: 16 },
		{ side: 'right' as const, pointX: 154, pointY: 155, boxX: 445, boxY: 105, title: 'Território',        subtitle: 'Nordeste.',                    color: '#4271b5', circleRadius: 12 },
		{ side: 'right' as const, pointX: 226, pointY: 220, boxX: 445, boxY: 190, title: 'Idade',             subtitle: '45 anos.',                     color: '#ea662f', circleRadius: 12 },
		{ side: 'right' as const, pointX: 334, pointY: 255, boxX: 445, boxY: 275, title: 'Trabalho',          subtitle: 'Professor.',                   color: '#a44c7f', circleRadius: 12 },
		{ side: 'right' as const, pointX: 260, pointY: 380, boxX: 445, boxY: 360, title: 'Escolaridade',      subtitle: 'Ensino superior completo.',    color: '#81a72f', circleRadius: 12 },
		{ side: 'right' as const, pointX: 250, pointY: 520, boxX: 445, boxY: 445, title: 'Valor repassado',   subtitle: 'Aporte de R$ 12 mil.',         color: '#cb4034', circleRadius: 12 },
	];
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
		ufByRegionGroups,
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
     PERSONA — PERFIL DO BENEFICIÁRIO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-persona">
	<h3>Um retrato do beneficiário</h3>
	<p>
		Para dar rosto aos números, vejamos um perfil concreto: um homem negro, professor do
		Nordeste, com ensino superior completo, que recebeu um aporte de <strong>R$ 12 mil</strong>
		pela política. À direita, o mercado formal organizado — o mesmo ao qual a maioria dos
		contemplados <em>não</em> possui vínculo.
	</p>
	<div class="silhouette-row">
		<div class="silhouette-col">
			<BodySilhouette annotations={bodyAnnotations} />
		</div>
		<div class="silhouette-col">
			<EnterpriseSilhouette />
		</div>
	</div>
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

<!-- ══════════════════════════════════════════════════════════════════════════
     POR REGIÃO — CORES POR REGIÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-region-color">
	<h3>Comparativo regional: informalidade e vínculo formal</h3>
	<p>
		Cada região tem um perfil distinto. O <strong>Nordeste</strong> lidera a informalidade
		com quase 60% de beneficiários sem vínculo formal. <strong>Centro-Oeste</strong> e
		<strong>Norte</strong> ficam próximos de 50%, enquanto <strong>Sudeste</strong> e
		<strong>Sul</strong> têm a maior proporção de trabalhadores formais.
	</p>
	<p class="chart-legend">
		Tons mais claros = sem vínculo formal &nbsp;·&nbsp; Tons mais escuros = com vínculo formal
	</p>
	<div class="region-compare">
		{#each ufByRegionGroups as { regiao, colors, avgInformal }}
			<div class="rc-row">
				<span class="rc-label">{regiao}</span>
				<div class="rc-bar">
					<div class="rc-seg" style="width: {avgInformal}%; background: {colors[0]}" title="Sem vínculo: {formatPctN(avgInformal)}"></div>
					<div class="rc-seg" style="width: {100 - avgInformal}%; background: {colors[1]}" title="Com vínculo: {formatPctN(100 - avgInformal)}"></div>
				</div>
				<span class="rc-pct">{formatPctN(avgInformal)} sem vínculo</span>
			</div>
		{/each}
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     POR UF × REGIÃO — CORRELAÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-4-uf-region-corr">
	<h3>Estados do Nordeste concentram a maior informalidade do país</h3>
	<p>
		Cruzando os dados estaduais com o recorte regional, vemos que os estados com
		maior proporção de trabalhadores sem vínculo formal estão quase todos no
		<strong>Nordeste</strong>. Piauí (66,9%), Pernambuco e Paraíba lideram dentro
		da região. No outro extremo, <strong>Amapá, Acre e Rondônia</strong>, no Norte,
		são os estados com maior formalização relativa.
	</p>
	<p class="chart-legend">
		<span>Tons mais claros</span> = sem vínculo formal &nbsp;·&nbsp;
		<span>Tons mais escuros</span> = com vínculo formal
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

<style>
	.silhouette-row {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
		margin-top: 1.5rem;
	}

	.silhouette-col {
		flex: 1 1 300px;
		min-width: 0;
	}

	.silhouette-col :global(svg) {
		width: 100%;
		height: auto;
		display: block;
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

	.bignumber-caption {
		font-size: 0.95rem;
		color: var(--color-text);
		text-align: center;
		opacity: 0.75;
		max-width: 20ch;
	}

	.chart-legend {
		font-size: 0.82rem;
		opacity: 0.65;
		margin-bottom: 1rem;
	}

	.region-compare {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		margin-top: 1rem;
	}

	.rc-row {
		display: grid;
		grid-template-columns: 9rem 1fr 10rem;
		align-items: center;
		gap: 0.75rem;
	}

	.rc-label {
		font-size: 0.9rem;
		font-weight: 600;
		text-align: right;
	}

	.rc-bar {
		display: flex;
		height: 28px;
		border-radius: 4px;
		overflow: hidden;
	}

	.rc-seg {
		height: 100%;
		transition: width 0.4s ease;
	}

	.rc-pct {
		font-size: 0.78rem;
		opacity: 0.65;
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

</style>
