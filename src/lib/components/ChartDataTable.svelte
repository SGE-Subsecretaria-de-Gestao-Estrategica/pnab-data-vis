<script lang="ts">
	// Equivalente textual (tabela de dados) para um gráfico/mapa. Por padrão fica
	// visualmente oculto (.sr-only) e serve apenas a leitores de tela; ao passar
	// `visible`, a tabela é exibida normalmente.
	interface Props {
		/** Título da tabela (vira <caption>). */
		caption: string;
		/** Rótulos das colunas. A 1ª coluna é tratada como cabeçalho de linha. */
		columns: string[];
		/** Linhas já formatadas; cada linha alinha-se a `columns`. */
		rows: (string | number)[][];
		/** Exibe a tabela em vez de escondê-la (default: oculta). */
		visible?: boolean;
	}

	let { caption, columns, rows, visible = false }: Props = $props();
</script>

<table class="data-table" class:sr-only={!visible}>
	<caption>{caption}</caption>
	<thead>
		<tr>
			{#each columns as col, i}
				<th scope="col" class:num={i > 0}>{col}</th>
			{/each}
		</tr>
	</thead>
	<tbody>
		{#each rows as row}
			<tr>
				{#each row as cell, i}
					{#if i === 0}
						<th scope="row">{cell}</th>
					{:else}
						<td class="num">{cell}</td>
					{/if}
				{/each}
			</tr>
		{/each}
	</tbody>
</table>

<style>
	/* Estilos aplicados apenas quando a tabela está visível (prop `visible`). */
	.data-table:not(.sr-only) {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.85rem;
		margin-top: 1rem;
	}

	.data-table:not(.sr-only) caption {
		text-align: left;
		font-weight: 700;
		color: #1b1b1b;
		margin-bottom: 0.5rem;
	}

	.data-table:not(.sr-only) th,
	.data-table:not(.sr-only) td {
		padding: 0.4rem 0.6rem;
		border-bottom: 1px solid #e0e0e0;
		text-align: left;
	}

	.data-table:not(.sr-only) .num {
		text-align: right;
		font-variant-numeric: tabular-nums;
	}

	.data-table:not(.sr-only) thead th {
		border-bottom: 2px solid #ccc;
		font-weight: 700;
	}
</style>
