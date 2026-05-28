<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import {
		BigNumber,
		DonutChart,
		HorizontalBarChart,
		HorizontalStackedBarChart,
		TreemapChart,
		colorPairs,
		colorScales,
		categorical8,
	} from 'sniic-design-system';
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
		cadunicoUfData,
		cadunicoValorData,
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
	<h2>5. Quem são os contemplados inscritos no Cadastro Único?</h2>
	<p>
		O Cadastro Único (CadÚnico) é o principal instrumento do governo federal para identificar
		e caracterizar famílias de baixa renda. Cruzar os dados da Aldir Blanc com o CadÚnico
		permite compreender em que medida a política alcançou as populações em situação de maior
		vulnerabilidade socioeconômica.
	</p>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     GRANDES NÚMEROS — CADUNICO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-bignumbers">
	<h3>Mais de 43% dos contemplados estão no CadÚnico</h3>
	<p>
		O cruzamento revela que uma parcela expressiva dos agentes culturais beneficiados pela
		Política Nacional Aldir Blanc integra o Cadastro Único — evidência de que a política
		alcançou populações em situação de vulnerabilidade econômica.
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percContempladosCadunico)} fontSize={72} />
			<p class="bignumber-caption">das pessoas físicas contempladas estão inscritas no Cadastro Único</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatNum(qtdContempladosCadunico)} fontSize={72} />
			<p class="bignumber-caption">pessoas contempladas identificadas no CadÚnico</p>
		</div>
	</div>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatNum(qtdDocumentosUnicos)} fontSize={72} />
			<p class="bignumber-caption">pessoas com documentos únicos no cruzamento</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorRecebidoCadunico)} fontSize={72} />
			<p class="bignumber-caption">repassados diretamente a esses agentes culturais</p>
		</div>
	</div>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percValorCadunico)} fontSize={72} />
			<p class="bignumber-caption">dos recursos totais da Aldir Blanc foram destinados a eles</p>
		</div>
	</div>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PERFIL — SEXO E FAIXA ETÁRIA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-perfil-sexo">
	<h3>Maioria feminina e em idade ativa</h3>
	<p>
		Entre os contemplados inscritos no CadÚnico, as mulheres são maioria: <strong>{formatPct(percFemCadunico)}</strong>.
		A faixa etária de <strong>25 a 54 anos</strong> concentra a maior parte do grupo —
		<strong>{formatPct(perc2554Cadunico)}</strong> — perfil semelhante ao dos demais beneficiários.
	</p>
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
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     FAIXA ETÁRIA × SEXO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-faixa-sexo">
	<h3>Distribuição por sexo em cada faixa etária</h3>
	<p>
		Nas faixas de <strong>25 a 64 anos</strong>, as mulheres superam os homens. Apenas na
		faixa mais jovem (15–24 anos) os homens são maioria, reflexo de um padrão visto também
		no perfil geral da Aldir Blanc.
	</p>
	<HorizontalStackedBarChart
		data={faixaEtariaSexoData}
		keys={[...FAIXA_SEXO_KEYS]}
		labels={FAIXA_SEXO_LABELS}
		colors={[colorPairs.bluePurple[1], colorPairs.bluePurple[0]]}
		format={formatPctFixed}
		showTotalLabel={false}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     VULNERABILIDADE SOCIOECONÔMICA — RENDA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-renda">
	<h3>Vulnerabilidade socioeconômica: renda per capita</h3>
	<p>
		A maioria dos contemplados no CadÚnico vive em famílias com renda per capita muito baixa.
		O maior grupo — <strong>34,2%</strong> — está na faixa de pobreza extrema (até R$109/mês).
		Somando as três faixas abaixo de meio salário mínimo, chegamos a mais de <strong>65%</strong>
		do total.
	</p>
	<div class="donut-row">
		<div class="donut-col">
			<p class="donut-label">Por faixa de renda per capita</p>
			<DonutChart
				data={rendaDonutData}
				colors={categorical8}
				centerLabel="pessoas"
				centerValue={formatNum(rendaDonutData.reduce((s, d) => s + d.value, 0))}
				format={formatNum}
				height={320}
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
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     SITUAÇÃO DE DOMICÍLIO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-domicilio">
	<h3>Maioria urbana, mas com presença rural relevante</h3>
	<p>
		<strong>{formatPct(percUrbanoCadunico)}</strong> dos contemplados no CadÚnico vivem em
		áreas urbanas — proporção ligeiramente menor do que a do conjunto geral de beneficiários,
		sugerindo maior penetração rural entre os mais vulneráveis.
	</p>
	<div class="bignumbers-row" style="margin-bottom: 2rem;">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percUrbanoCadunico)} fontSize={72} />
			<p class="bignumber-caption">vivem em áreas urbanas</p>
		</div>
	</div>
	<TreemapChart
		data={domicilioTreemapData}
		height={260}
		format={formatNum}
		colors={[colorScales.blue[2], colorScales.teal[2]]}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     PORTE MUNICIPAL
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-porte">
	<h3>Concentração em municípios de pequeno porte</h3>
	<p>
		<strong>{formatPct(percPequenoPorteCadunico)}</strong> dos beneficiários CadÚnico residem
		em municípios de pequeno porte (Pequeno I e II) — proporção maior do que a observada no
		conjunto geral dos contemplados pela Aldir Blanc, reforçando o perfil de maior
		vulnerabilidade desse grupo.
	</p>
	<div class="bignumbers-row" style="margin-bottom: 2rem;">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percPequenoPorteCadunico)} fontSize={72} />
			<p class="bignumber-caption">residem em municípios de pequeno porte</p>
		</div>
	</div>
	<TreemapChart
		data={porteTreemapData5}
		height={260}
		format={formatNum}
		colors={categorical8}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     POR UF
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-uf">
	<h3>A penetração do CadÚnico varia muito entre os estados</h3>
	<p>
		Estados do Nordeste e Norte lideram na proporção de contemplados inscritos no CadÚnico,
		reflexo da maior vulnerabilidade socioeconômica dessas regiões. O Distrito Federal e
		estados do Sul apresentam as menores taxas de penetração.
	</p>
	<HorizontalBarChart
		data={cadunicoUfData}
		color={colorScales.teal[2]}
		format={formatPctFixed}
		xLabel="% dos contemplados da UF no CadÚnico"
		margin={{ top: 20, right: 80, bottom: 40, left: 50 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     FAIXA DE VALOR RECEBIDO
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-valor">
	<h3>Beneficiários CadÚnico concentrados nas faixas mais baixas</h3>
	<p>
		Quase metade dos beneficiários CadÚnico recebeu até R$2 mil, e mais de <strong>86%</strong>
		ficaram abaixo de R$10 mil — concentração ainda maior do que a observada no conjunto geral
		da Aldir Blanc.
	</p>
	<HorizontalBarChart
		data={cadunicoValorData}
		color={colorScales.blue[2]}
		format={formatPctFixed}
		xLabel="% dos beneficiários CadÚnico"
		margin={{ top: 20, right: 80, bottom: 40, left: 160 }}
	/>
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     BOLSA FAMÍLIA
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-bolsa-familia">
	<h3>1 em cada 5 contemplados é beneficiário do Bolsa Família</h3>
	<p>
		O cruzamento com o programa Bolsa Família revela que <strong>{formatPct(percBolsaFamilia)}</strong>
		dos agentes culturais contemplados pela Aldir Blanc são também beneficiários do Bolsa Família —
		confirmando que a política atingiu famílias em situação de maior vulnerabilidade.
	</p>
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
</ScrollSection>

<!-- ══════════════════════════════════════════════════════════════════════════
     BPC
     ══════════════════════════════════════════════════════════════════════════ -->
<ScrollSection id="section-5-bpc">
	<h3>Beneficiários do BPC também foram contemplados</h3>
	<p>
		Uma pequena mas significativa parcela dos contemplados — <strong>{formatPct(percBpc)}</strong> —
		são beneficiários do Benefício de Prestação Continuada (BPC), destinado a idosos e pessoas
		com deficiência em situação de vulnerabilidade.
	</p>
	<div class="bignumbers-row">
		<div class="bignumber-cell">
			<BigNumber value={formatPct(percBpc)} fontSize={72} />
			<p class="bignumber-caption">dos agentes culturais são beneficiários do BPC</p>
		</div>
		<div class="bignumber-cell">
			<BigNumber value={formatBRL(valorBpc)} fontSize={72} />
			<p class="bignumber-caption">foram repassados para esse público</p>
		</div>
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

	.bignumber-caption {
		font-size: 0.95rem;
		color: var(--color-text);
		text-align: center;
		opacity: 0.75;
		max-width: 20ch;
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
