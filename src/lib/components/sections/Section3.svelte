<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import {
		BigNumber,
		DonutChart,
		GroupedColumnChart,
		PictogramChart,
		colorPairs,
		colorScales,
		categorical8,
		AnnotationBox
	} from 'sniic-design-system';
	import PyramidChartCustom from '$lib/components/PyramidChartCustom.svelte';
	import {
		totalBeneficiarios,
		totalPF,
		valorTotalPF,
		pfPjDonutData,
		sexoQuantityDonutData,
		sexoValueDonutData,
		sexoPropMasculino,
		sexoPropFeminino,
		pyramidData,
		ageGroupRegionData,
		ageGroupRegionKeys,
		ageGroupRegionLabels,
	} from '$lib/data/section3';

	const formatNum = (v: number) => v.toLocaleString('pt-BR');
	const formatBRL = (v: number) =>
		new Intl.NumberFormat('pt-BR', {
			style: 'currency',
			currency: 'BRL',
			notation: 'compact',
			maximumFractionDigits: 1,
		}).format(v);

	// feminino=purple, masculino=blue (consistent with pyramid default)
	const sexColors = [colorPairs.bluePurple[1], colorPairs.bluePurple[0]];
	// feminino=orange, masculino=lime (pictogram)
	const sexPictogramColors = [colorScales.orange[2], colorScales.lime[2]];
	const formatPct = (v: number) =>
		(v * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';
	const pictogramData = [
		{ label: 'Masculino', value: 8, color: colorScales.lime[2] },
		{ label: 'Feminino', value: 7, color: colorScales.orange[2] },
	];
	// PF=teal, PJ=orange
	const pfPjColors = [colorScales.teal[2], colorScales.orange[2]];
</script>

<!-- ══════════════════════════════════════════════════════════════════════════
     INTRODUÇÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-intro">
	<h2>3. Quem acessou os recursos da Política Nacional Aldir Blanc?</h2>
	<p>
		Neste capítulo, mergulhamos nos dados para traçar o perfil dos agentes culturais e das
		organizações contempladas no primeiro ciclo da Aldir Blanc, destacando alguns indicadores que
		ajudam a compreender quem acessou os recursos da política.
	</p>
	<svg width={600} height={130} style="overflow: hidden; margin-top: 1rem;">
		<AnnotationBox
			title=""
			subtitle={"As análises apresentadas neste capítulo resultam do cruzamento dos dados de agentes culturais contemplados pela Política Nacional Aldir Blanc com bases da Receita Federal. Para as pessoas físicas, foram utilizadas as variáveis idade e sexo (masculino/feminino), sendo, esta última adotada conforme disponibilidade da base, referindo-se ao sexo biológico registrado — o que não contempla a diversidade de identidades de gênero (como pessoas trans, travestis, não binárias, entre outras). Para as pessoas jurídicas, foram utilizadas as variáveis natureza jurídica e CNAE (principal e secundários)."}
			boxX={0}
			boxY={0}
			boxWidth={1000}
			pointX={-30}
			pointY={63}
			showTitle={false}
			circleRadius={0}
		/>
	</svg>
	<p>
		Ao todo, <strong>{totalBeneficiarios.toLocaleString('pt-BR')} agentes culturais</strong> foram
		contemplados pelo programa, entre pessoas físicas e jurídicas.
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={totalBeneficiarios.toLocaleString('pt-BR')} fontSize={72} />
			<p class="bignumber-caption">agentes culturais contemplados</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorTotalPF)} fontSize={72} />
			<p class="bignumber-caption">distribuídos a pessoas físicas</p>
		</div>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PF vs PJ
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-pfpj">
	<h3>A grande maioria é pessoa física</h3>
	<p>
		Dos {totalBeneficiarios.toLocaleString('pt-BR')} contemplados, <strong>80,7% são pessoas
		físicas</strong> — artistas, músicos, cineastas e demais trabalhadores individuais da cultura.
		Apenas 19,3% correspondem a organizações formais como associações, coletivos e empresas
		culturais.
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
     SEXO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-sexo">
	<h3>Leve maioria masculina, perto da paridade</h3>
	<p>
		Entre as <strong>{totalPF.toLocaleString('pt-BR')} pessoas físicas</strong> contempladas, os
		homens representam 53,2% e as mulheres, 46,8% — uma diferença de cerca de 7 pontos percentuais.
		Quando olhamos o valor recebido, a proporção é muito semelhante: 53,9% para homens e 46,1% para
		mulheres.
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(sexoPropMasculino)} fontSize={72} />
			<p class="bignumber-caption">dos agentes culturais contemplados do sexo masculino</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatPct(sexoPropFeminino)} fontSize={72} />
			<p class="bignumber-caption">dos agentes culturais contemplados do sexo feminino</p>
		</div>
	</div>
	<p class="pictogram-caption">Cada ícone representa 1 em cada 15 agentes culturais contemplados</p>
	<PictogramChart
		data={pictogramData}
		unitValue={1}
		columns={15}
		iconSize={32}
		gap={6}
		showLabels={true}
		format={formatNum}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PIRÂMIDE ETÁRIA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-pyramid">
	<h3>Adultos em idade ativa dominam o programa</h3>
	<p>
		A faixa de <strong>25 a 54 anos</strong> concentra a esmagadora maioria dos beneficiários —
		cerca de <strong>70,5% do total</strong>. Jovens de 15 a 24 anos representam apenas 8%, e
		idosos acima de 65 anos, 8,6%. O perfil etário reflete o mercado de trabalho cultural: uma
		população economicamente ativa e em plena carreira.
	</p>
	<p>
		Nas faixas de <strong>55 a 64 anos</strong> e <strong>65 anos ou mais</strong>, as mulheres
		superam os homens em quantidade, invertendo a tendência das faixas mais jovens.
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
     FAIXA ETÁRIA POR REGIÃO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-3-age-region">
	<h3>Nordeste lidera em todas as faixas etárias</h3>
	<p>
		Em todas as faixas etárias, o <strong>Nordeste</strong> concentra o maior número de agentes
		culturais contemplados — reflexo tanto de sua população como dos critérios redistributivos do
		programa. O <strong>Sudeste</strong> aparece em segundo lugar, enquanto o
		<strong>Centro-Oeste</strong> registra os menores volumes em todas as faixas.
	</p>
	<p>
		A faixa de <strong>25 a 54 anos</strong> é dominante em todas as regiões, confirmando o padrão
		nacional visto na pirâmide etária.
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

	.pictogram-caption {
		font-size: 0.8rem;
		opacity: 0.55;
		margin: 0.75rem 0 0.25rem;
		font-style: italic;
	}

	.pyramid-wrap {
		max-width: 680px;
	}

	.donut-single {
		margin-top: 1.5rem;
		max-width: 420px;
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
</style>
