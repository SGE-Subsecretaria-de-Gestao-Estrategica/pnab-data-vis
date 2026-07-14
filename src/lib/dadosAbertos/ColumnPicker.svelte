<script lang="ts">
	import { COLUMNS, GROUPS, DEFAULT_VISIBLE } from './columns';

	let {
		visible,
		onChange
	}: {
		visible: Set<string>;
		onChange: (next: Set<string>) => void;
	} = $props();

	let open = $state(false);
	let panelEl: HTMLDivElement | null = $state(null);

	const count = $derived(visible.size);

	function toggle(name: string) {
		const next = new Set(visible);
		if (next.has(name)) next.delete(name);
		else next.add(name);
		onChange(next);
	}

	function toggleGroup(key: string) {
		const cols = COLUMNS.filter((c) => c.group === key).map((c) => c.name);
		const allOn = cols.every((n) => visible.has(n));
		const next = new Set(visible);
		for (const n of cols) {
			if (allOn) next.delete(n);
			else next.add(n);
		}
		onChange(next);
	}

	function selectAll() {
		onChange(new Set(COLUMNS.map((c) => c.name)));
	}
	function reset() {
		onChange(new Set(DEFAULT_VISIBLE));
	}

	function onWindowClick(e: MouseEvent) {
		if (open && panelEl && !panelEl.contains(e.target as Node)) open = false;
	}
</script>

<svelte:window onclick={onWindowClick} />

<div class="picker" bind:this={panelEl}>
	<button class="trigger" onclick={() => (open = !open)} aria-expanded={open}>
		<span class="cols-icon" aria-hidden="true"></span>
		Colunas <span class="badge">{count}</span>
	</button>

	{#if open}
		<div class="panel" role="dialog" aria-label="Selecionar colunas">
			<div class="panel-head">
				<strong>Colunas visíveis</strong>
				<div class="panel-actions">
					<button onclick={selectAll}>Todas</button>
					<button onclick={reset}>Padrão</button>
				</div>
			</div>
			<div class="groups">
				{#each GROUPS as g}
					{@const cols = COLUMNS.filter((c) => c.group === g.key)}
					{@const on = cols.filter((c) => visible.has(c.name)).length}
					<div class="group">
						<button class="group-head" onclick={() => toggleGroup(g.key)}>
							<span class="group-label">{g.label}</span>
							<span class="group-count">{on}/{cols.length}</span>
						</button>
						<div class="items">
							{#each cols as c}
								<label class="item">
									<input
										type="checkbox"
										checked={visible.has(c.name)}
										onchange={() => toggle(c.name)}
									/>
									<span>{c.label}</span>
								</label>
							{/each}
						</div>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	.picker {
		position: relative;
	}

	.trigger {
		display: inline-flex;
		align-items: center;
		gap: 0.45rem;
		padding: 0.5rem 0.8rem;
		background: #fff;
		border: 1px solid #d5dceb;
		border-radius: 6px;
		font-size: 0.85rem;
		font-weight: 600;
		color: #1b1b1b;
		cursor: pointer;
	}
	.trigger:hover {
		border-color: #4271b5;
		color: #4271b5;
	}
	.cols-icon {
		width: 13px;
		height: 13px;
		border: 1.5px solid currentColor;
		border-radius: 2px;
		position: relative;
	}
	.cols-icon::after {
		content: '';
		position: absolute;
		top: -1.5px;
		bottom: -1.5px;
		left: 50%;
		width: 1.5px;
		background: currentColor;
	}
	.badge {
		background: #eef2fb;
		color: #2e4e8a;
		border-radius: 999px;
		padding: 0.05rem 0.45rem;
		font-size: 0.72rem;
	}

	.panel {
		position: absolute;
		top: calc(100% + 6px);
		right: 0;
		z-index: 40;
		width: 320px;
		max-height: 460px;
		overflow-y: auto;
		background: #fff;
		border: 1px solid #d5dceb;
		border-radius: 8px;
		box-shadow: 0 12px 28px rgba(15, 21, 64, 0.14);
		padding: 0.6rem;
	}
	.panel-head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.2rem 0.3rem 0.6rem;
		font-size: 0.9rem;
	}
	.panel-actions {
		display: flex;
		gap: 0.35rem;
	}
	.panel-actions button {
		background: #f4f6fb;
		border: 1px solid #e2e8f5;
		border-radius: 5px;
		padding: 0.25rem 0.55rem;
		font-size: 0.75rem;
		font-weight: 600;
		color: #2e4e8a;
		cursor: pointer;
	}
	.panel-actions button:hover {
		background: #e8eefb;
	}

	.group {
		border-top: 1px solid #eef1f6;
		padding: 0.4rem 0;
	}
	.group-head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		width: 100%;
		background: none;
		border: none;
		padding: 0.25rem 0.3rem;
		cursor: pointer;
		text-align: left;
	}
	.group-label {
		font-size: 0.78rem;
		font-weight: 700;
		color: #333;
		text-transform: uppercase;
		letter-spacing: 0.02em;
	}
	.group-count {
		font-size: 0.72rem;
		color: #8a93a6;
	}
	.items {
		display: flex;
		flex-direction: column;
	}
	.item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.28rem 0.3rem;
		font-size: 0.85rem;
		color: #1b1b1b;
		cursor: pointer;
		border-radius: 4px;
	}
	.item:hover {
		background: #f6f8fc;
	}
	.item input {
		accent-color: #4271b5;
	}
</style>
