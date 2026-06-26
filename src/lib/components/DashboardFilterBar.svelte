<script lang="ts">
	import { REGIAO_OPTIONS, VISAO_LABELS } from '$lib/stores/dashboardFilters.svelte';
	import type { DashboardFilters } from '$lib/stores/dashboardFilters.svelte';
	import type { Visao } from '$lib/data/dashboard';
	import { siglaToName } from '$lib/data/dashboard';

	interface Props {
		filters: DashboardFilters;
		/** Limit which visão options are offered (default: all). */
		visoes?: Visao[];
		/** Show the región scoping dropdown (default true). */
		showRegiao?: boolean;
		/** Show the UF scoping dropdown (default true). */
		showUf?: boolean;
	}

	let { filters, visoes, showRegiao = true, showUf = true }: Props = $props();

	const visaoOptions = $derived(
		(visoes ?? (Object.keys(VISAO_LABELS) as Visao[])).map((v) => [v, VISAO_LABELS[v]] as const)
	);

	const hasSelection = $derived(filters.uf !== 'Todas' || filters.regiao !== 'Todas');
</script>

<div class="filter-bar">
	<div class="filter-group">
		<span class="filter-label">Visão</span>
		<select aria-label="Visão" value={filters.visao} onchange={(e) => (filters.visao = e.currentTarget.value as Visao)}>
			{#each visaoOptions as [key, label]}
				<option value={key}>{label}</option>
			{/each}
		</select>
	</div>

	{#if showRegiao}
		<div class="filter-group">
			<span class="filter-label">Região</span>
			<select aria-label="Região" value={filters.regiao} onchange={(e) => (filters.regiao = e.currentTarget.value as any)}>
				{#each REGIAO_OPTIONS as r}
					<option value={r}>{r}</option>
				{/each}
			</select>
		</div>
	{/if}

	{#if showUf}
		<div class="filter-group" class:disabled={filters.visao === 'regioes'}>
			<span class="filter-label">UF</span>
			<select
				aria-label="UF"
				value={filters.uf}
				disabled={filters.visao === 'regioes'}
				onchange={(e) => (filters.uf = e.currentTarget.value)}
			>
				<option value="Todas">Todas</option>
				{#each filters.ufsForRegiao as u}
					<option value={u}>{u} — {siglaToName[u]}</option>
				{/each}
			</select>
		</div>
	{/if}

	{#if hasSelection}
		<button class="clear-btn" onclick={() => filters.reset()}>Limpar filtros ✕</button>
	{/if}
</div>

<style>
	.filter-bar {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		align-items: flex-end;
		padding: 1rem 1.25rem;
		background: rgba(19, 81, 180, 0.04);
		border: 1px solid rgba(19, 81, 180, 0.12);
		border-radius: 0;
		margin-bottom: 1.75rem;
	}

	.filter-group {
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
	}

	.filter-group.disabled {
		opacity: 0.5;
	}

	.filter-label {
		font-size: 0.68rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: #666;
	}

	select {
		font-family: inherit;
		font-size: 0.88rem;
		padding: 0.45rem 2rem 0.45rem 0.7rem;
		border: 1px solid #ccc;
		border-radius: 0;
		background: white;
		color: #1B1B1B;
		cursor: pointer;
		appearance: none;
		background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M3 5l3 3 3-3z'/%3E%3C/svg%3E");
		background-repeat: no-repeat;
		background-position: right 0.55rem center;
		min-width: 9rem;
	}

	select:hover:not(:disabled) { border-color: #1351B4; }
	select:focus { outline: 2px solid #1351B4; outline-offset: 1px; }
	select:disabled { cursor: not-allowed; }

	.clear-btn {
		margin-left: auto;
		font-family: inherit;
		font-size: 0.8rem;
		font-weight: 600;
		padding: 0.5rem 0.9rem;
		border: 1px solid rgba(19, 81, 180, 0.3);
		border-radius: 0;
		background: white;
		color: #1351B4;
		cursor: pointer;
	}
	.clear-btn:hover { background: rgba(19, 81, 180, 0.08); }
</style>
