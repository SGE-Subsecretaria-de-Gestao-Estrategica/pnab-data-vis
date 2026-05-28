<script lang="ts">
	import ScrollSection from '$lib/components/ScrollSection.svelte';
	import { BigNumber } from 'sniic-design-system';
	import {
		percContempladosCadunico,
		qtdContempladosCadunico,
		qtdDocumentosUnicos,
		valorRecebidoCadunico,
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
