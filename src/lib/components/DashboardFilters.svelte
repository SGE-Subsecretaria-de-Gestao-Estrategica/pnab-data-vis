<script lang="ts">
	import type { Visao, Regiao } from '$lib/stores/filters.svelte';
	import { REGIOES, UF_LIST } from '$lib/stores/filters.svelte';
	import { regionMap } from '$lib/data/section1';

	interface Props {
		visao: Visao;
		regiao: Regiao;
		uf: string;
		ufsForRegiao: string[];
		showVisao?: boolean;
		onchange: (key: 'visao' | 'regiao' | 'uf', value: string) => void;
	}

	let { visao, regiao, uf, ufsForRegiao, showVisao = true, onchange }: Props = $props();

	const VISAO_LABELS: Record<Visao, string> = {
		uf: 'UF (Estado + Municípios)',
		estados: 'Apenas Estados',
		municipios: 'Apenas Municípios',
	};
</script>

<div class="filters">
	{#if showVisao}
		<div class="filter-group">
			<label for="visao-select">Visão</label>
			<select
				id="visao-select"
				value={visao}
				onchange={(e) => onchange('visao', e.currentTarget.value)}
			>
				{#each Object.entries(VISAO_LABELS) as [key, label]}
					<option value={key}>{label}</option>
				{/each}
			</select>
		</div>
	{/if}

	<div class="filter-group">
		<label for="regiao-select">Região</label>
		<select
			id="regiao-select"
			value={regiao}
			onchange={(e) => onchange('regiao', e.currentTarget.value)}
		>
			{#each REGIOES as r}
				<option value={r}>{r}</option>
			{/each}
		</select>
	</div>

	<div class="filter-group">
		<label for="uf-select">UF</label>
		<select
			id="uf-select"
			value={uf}
			onchange={(e) => onchange('uf', e.currentTarget.value)}
		>
			<option value="Todas">Todas</option>
			{#each ufsForRegiao as u}
				<option value={u}>{u}</option>
			{/each}
		</select>
	</div>
</div>

<style>
	.filters {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		padding: 0.75rem 0;
		background: transparent;
		margin-bottom: 1.5rem;
		align-items: flex-end;
	}

	.filter-group {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	label {
		font-size: 0.7rem;
		font-weight: 600;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: #666;
	}

	select {
		font-family: 'Rawline', system-ui, sans-serif;
		font-size: 0.85rem;
		padding: 0.4rem 2rem 0.4rem 0.6rem;
		border: 1px solid #ccc;
		border-radius: 0.4rem;
		background: white;
		color: #333;
		cursor: pointer;
		appearance: none;
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M3 5l3 3 3-3z'/%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right 0.5rem center;
	}

	select:hover {
		border-color: #999;
	}

	select:focus {
		outline: 2px solid #1351B4;
		outline-offset: 1px;
	}
</style>
