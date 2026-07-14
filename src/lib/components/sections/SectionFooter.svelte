<script lang="ts">
	import { base } from '$app/paths';
</script>

<section class="footer-band">
	<div class="footer">
		<!-- <img class="logo" src="{base}/logos/logo-sniic.png" alt="SNIIC — Sistema Nacional de Informações e Indicadores Culturais" /> -->
		<p class="credit">
			Pesquisa realizada no <strong>SNIIC — Sistema Nacional de Informações e Indicadores
			Culturais</strong>.
		</p>
		<p class="open-data">
			Para acessar os dados desta pesquisa na íntegra, visite o
			<a
				href="https://github.com/SGE-Subsecretaria-de-Gestao-Estrategica/dados-abertos-pnab-ciclo1"
				target="_blank"
				rel="noopener noreferrer">repositório de dados abertos da SGE/MinC</a>.
		</p>
	</div>
</section>

<style>
	.footer-band {
		width: 100%;
		color: #000;
	}

	.footer {
		max-width: 1200px;
		margin: 0 auto;
		padding: 4rem 2rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
		text-align: center;
	}

	.logo {
		max-width: 280px;
		width: 100%;
		height: auto;
		display: block;
	}

	.credit {
		font-size: 1.05rem;
		line-height: 1.6;
		margin: 0;
		max-width: 60ch;
	}

	.open-data {
		font-size: 1.05rem;
		line-height: 1.6;
		margin: 0;
		max-width: 60ch;
	}

	.open-data a {
		color: #1351b4;
		font-weight: 700;
		text-decoration: underline;
	}

	@media (max-width: 520px) {
		.footer {
			padding: 3rem 1rem;
		}

		.logo {
			max-width: 220px;
		}

		.credit {
			font-size: 0.95rem;
		}
	}
</style>
