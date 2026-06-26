<script lang="ts">
</script>

<section class="intro-band">
	<div class="intro">
		<p class="lead">
			A pesquisa analisou <b>167.817</b> agentes culturais contemplados em <b>5.125</b> entes federados,
			sendo 26 estados, o Distrito Federal e <b>5.098</b> municípios. O painel baseou-se em dados de
			transações financeiras de municípios, estados e Distrito Federal, extraídos do BB Gestão
			Ágil.
		</p>
		<p class="lead">
			A extração abrangeu movimentações realizadas até 31 de dezembro de 2025, data limite para
			a movimentação dos recursos do primeiro ciclo da Aldir Blanc. A extração completa foi
			finalizada em 24 de abril de 2026.
		</p>
		<p class="lead note">
			*O filtro Visão permite selecionar até três formas de agregação dos dados: UF, que
			apresenta os valores consolidados de estados e seus respectivos municípios; Estado, que
			considera apenas os valores executados pelos governos estaduais; e Município, que
			considera apenas os valores executados pelos municípios.
		</p>
	</div>
</section>

<style>
	.intro-band {
		width: 100%;
		background: var(--green);
		color: black;
	}

	.intro {
		max-width: 1200px;
		margin: 0 auto;
		padding: 3rem 2rem;
	}

	.lead {
		font-size: 1.125rem;
		line-height: 1.6;
		margin: 0;
	}

	.lead + .lead {
		margin-top: 1rem;
	}

	.lead.note {
		font-size: 0.9375rem;
		font-style: italic;
		margin-top: 1.5rem;
		opacity: 0.92;
	}

	@media (max-width: 520px) {
		.intro {
			padding: 2rem 1rem;
		}

		.lead {
			font-size: 1rem;
		}
	}
</style>
