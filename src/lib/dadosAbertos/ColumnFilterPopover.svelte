<script lang="ts">
	import { onMount } from 'svelte';
	import type { ColumnMeta } from './columns';
	import type { ColumnFilter } from './db';
	import { distinctCount, distinctValues, numericRange } from './db';

	let {
		column,
		current,
		onApply,
		onClose
	}: {
		column: ColumnMeta;
		current: ColumnFilter | undefined;
		onApply: (f: ColumnFilter | null) => void;
		onClose: () => void;
	} = $props();

	const CHECKBOX_MAX = 200;

	let loading = $state(true);
	let error = $state<string | null>(null);
	let mode = $state<'range' | 'checkbox' | 'contains'>('contains');

	// checkbox mode
	let options = $state<string[]>([]);
	let hasNull = $state(false);
	let truncated = $state(false);
	let selected = $state<Set<string>>(new Set());
	let includeNull = $state(false);
	let optFilter = $state('');

	// contains mode
	let containsText = $state('');

	// range mode
	let rangeLo = $state('');
	let rangeHi = $state('');
	let dataMin = $state<number | null>(null);
	let dataMax = $state<number | null>(null);

	let panelEl: HTMLDivElement | null = $state(null);

	onMount(() => {
		load();
	});

	async function load() {
		loading = true;
		error = null;
		try {
			if (column.type === 'number') {
				mode = 'range';
				const r = await numericRange(column.name);
				dataMin = r.min;
				dataMax = r.max;
				if (current?.kind === 'range') {
					rangeLo = current.min != null ? String(current.min) : '';
					rangeHi = current.max != null ? String(current.max) : '';
				}
			} else {
				const n = await distinctCount(column.name);
				if (n <= CHECKBOX_MAX) {
					mode = 'checkbox';
					const d = await distinctValues(column.name, CHECKBOX_MAX);
					options = d.values;
					hasNull = d.hasNull;
					truncated = d.truncated;
					if (current?.kind === 'in') {
						selected = new Set(current.values);
						includeNull = !!current.includeNull;
					}
				} else {
					mode = 'contains';
					if (current?.kind === 'contains') containsText = current.text;
				}
			}
		} catch (e) {
			error = (e as Error).message;
		} finally {
			loading = false;
		}
	}

	const shownOptions = $derived(
		optFilter.trim()
			? options.filter((o) => o.toLowerCase().includes(optFilter.trim().toLowerCase()))
			: options
	);

	function toggleOpt(v: string) {
		const next = new Set(selected);
		if (next.has(v)) next.delete(v);
		else next.add(v);
		selected = next;
	}

	function apply() {
		if (mode === 'range') {
			const min = rangeLo.trim() === '' ? null : Number(rangeLo);
			const max = rangeHi.trim() === '' ? null : Number(rangeHi);
			if ((min != null && !Number.isFinite(min)) || (max != null && !Number.isFinite(max))) {
				error = 'Informe números válidos.';
				return;
			}
			if (min == null && max == null) onApply(null);
			else onApply({ kind: 'range', min, max });
		} else if (mode === 'checkbox') {
			if (selected.size === 0 && !includeNull) onApply(null);
			else onApply({ kind: 'in', values: [...selected], includeNull });
		} else {
			const t = containsText.trim();
			onApply(t ? { kind: 'contains', text: t } : null);
		}
	}

	function clear() {
		selected = new Set();
		includeNull = false;
		containsText = '';
		rangeLo = '';
		rangeHi = '';
		onApply(null);
	}

	function onKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') onClose();
		else if (e.key === 'Enter' && mode !== 'checkbox') apply();
	}

	function onWindowClick(e: MouseEvent) {
		if (panelEl && !panelEl.contains(e.target as Node)) onClose();
	}
</script>

<svelte:window onclick={onWindowClick} />

<div
	class="popover"
	bind:this={panelEl}
	role="dialog"
	aria-label={`Filtrar ${column.label}`}
	onkeydown={onKeydown}
>
	<div class="head">
		<strong>{column.label}</strong>
		<button class="x" onclick={onClose} aria-label="Fechar">×</button>
	</div>

	{#if loading}
		<p class="muted">Carregando…</p>
	{:else if error}
		<p class="err">{error}</p>
	{:else if mode === 'range'}
		<p class="muted small">
			Intervalo nos dados: {dataMin?.toLocaleString('pt-BR')} – {dataMax?.toLocaleString('pt-BR')}
		</p>
		<div class="range">
			<input type="number" placeholder="mín." bind:value={rangeLo} />
			<span>até</span>
			<input type="number" placeholder="máx." bind:value={rangeHi} />
		</div>
	{:else if mode === 'contains'}
		<p class="muted small">Muitos valores distintos — filtre por texto contido:</p>
		<input class="text-in" type="text" placeholder="Contém…" bind:value={containsText} />
	{:else}
		<input class="text-in" type="text" placeholder="Buscar valor…" bind:value={optFilter} />
		<div class="opts">
			{#if hasNull}
				<label class="opt">
					<input type="checkbox" bind:checked={includeNull} />
					<span class="null-val">(vazio)</span>
				</label>
			{/if}
			{#each shownOptions as o}
				<label class="opt">
					<input type="checkbox" checked={selected.has(o)} onchange={() => toggleOpt(o)} />
					<span>{o}</span>
				</label>
			{/each}
			{#if shownOptions.length === 0}
				<p class="muted small">Nenhum valor.</p>
			{/if}
		</div>
		{#if truncated}
			<p class="muted small">Exibindo os {CHECKBOX_MAX} valores mais frequentes.</p>
		{/if}
	{/if}

	<div class="foot">
		<button class="ghost" onclick={clear}>Limpar</button>
		<button class="primary" onclick={apply}>Aplicar</button>
	</div>
</div>

<style>
	.popover {
		position: absolute;
		top: calc(100% + 4px);
		left: 0;
		z-index: 50;
		width: 260px;
		background: #fff;
		border: 1px solid #d5dceb;
		border-radius: 8px;
		box-shadow: 0 12px 28px rgba(15, 21, 64, 0.16);
		padding: 0.7rem;
		font-weight: 400;
		text-align: left;
		white-space: normal;
	}
	.head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		margin-bottom: 0.5rem;
	}
	.head strong {
		font-size: 0.85rem;
		color: #1b1b1b;
	}
	.x {
		background: none;
		border: none;
		font-size: 1.2rem;
		line-height: 1;
		color: #8a93a6;
		cursor: pointer;
	}
	.muted {
		color: #8a93a6;
	}
	.small {
		font-size: 0.75rem;
		margin: 0 0 0.4rem;
	}
	.err {
		color: #ab4723;
		font-size: 0.8rem;
	}
	.text-in,
	.range input {
		width: 100%;
		box-sizing: border-box;
		padding: 0.4rem 0.5rem;
		border: 1px solid #d5dceb;
		border-radius: 5px;
		font-size: 0.85rem;
	}
	.range {
		display: flex;
		align-items: center;
		gap: 0.4rem;
	}
	.range span {
		font-size: 0.75rem;
		color: #8a93a6;
	}
	.opts {
		max-height: 220px;
		overflow-y: auto;
		margin-top: 0.4rem;
		display: flex;
		flex-direction: column;
	}
	.opt {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.25rem 0.2rem;
		font-size: 0.82rem;
		color: #1b1b1b;
		cursor: pointer;
		border-radius: 4px;
	}
	.opt:hover {
		background: #f6f8fc;
	}
	.opt input {
		accent-color: #4271b5;
		flex-shrink: 0;
	}
	.null-val {
		font-style: italic;
		color: #8a93a6;
	}
	.foot {
		display: flex;
		justify-content: space-between;
		gap: 0.5rem;
		margin-top: 0.6rem;
	}
	.foot button {
		padding: 0.4rem 0.8rem;
		border-radius: 5px;
		font-size: 0.8rem;
		font-weight: 600;
		cursor: pointer;
	}
	.ghost {
		background: #fff;
		border: 1px solid #d5dceb;
		color: #555;
	}
	.primary {
		background: #4271b5;
		border: 1px solid #4271b5;
		color: #fff;
	}
	.primary:hover {
		background: #2e4e8a;
	}
</style>
