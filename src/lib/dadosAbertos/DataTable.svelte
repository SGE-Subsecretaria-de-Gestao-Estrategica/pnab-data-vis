<script lang="ts">
	import { onMount } from 'svelte';
	import { COLUMNS, COLUMN_BY_NAME, DEFAULT_VISIBLE } from './columns';
	import {
		exportCsv,
		queryPage,
		totalRows,
		type ColumnFilter,
		type QueryOptions,
		type Row
	} from './db';
	import ColumnPicker from './ColumnPicker.svelte';
	import ColumnFilterPopover from './ColumnFilterPopover.svelte';

	const PAGE_SIZES = [50, 100, 250];

	let visible = $state<Set<string>>(new Set(DEFAULT_VISIBLE));
	let searchInput = $state('');
	let searchTerm = $state('');
	let filters = $state<Record<string, ColumnFilter>>({});
	let sort = $state<{ col: string; dir: 'asc' | 'desc' } | null>(null);
	let page = $state(0);
	let pageSize = $state(100);

	let rows = $state<Row[]>([]);
	let total = $state(0);
	let grandTotal = $state<number | null>(null);
	let loading = $state(true);
	let firstLoad = $state(true);
	let error = $state<string | null>(null);
	let openFilterCol = $state<string | null>(null);
	let downloadOpen = $state(false);
	let exporting = $state(false);
	let downloadEl: HTMLDivElement | null = $state(null);

	const visibleCols = $derived(COLUMNS.filter((c) => visible.has(c.name)).map((c) => c.name));
	const visibleMetas = $derived(COLUMNS.filter((c) => visible.has(c.name)));
	const totalPages = $derived(Math.max(1, Math.ceil(total / pageSize)));
	const activeFilterCount = $derived(Object.keys(filters).length);

	let searchTimer: ReturnType<typeof setTimeout>;
	function onSearch(v: string) {
		searchInput = v;
		clearTimeout(searchTimer);
		searchTimer = setTimeout(() => {
			searchTerm = v.trim();
			page = 0;
		}, 300);
	}

	onMount(async () => {
		try {
			grandTotal = await totalRows();
		} catch {
			/* surfaced by the query effect */
		}
	});

	let reqId = 0;
	async function runQuery(opts: QueryOptions) {
		const id = ++reqId;
		loading = true;
		error = null;
		try {
			const res = await queryPage(opts);
			if (id !== reqId) return;
			rows = res.rows;
			total = res.total;
		} catch (e) {
			if (id !== reqId) return;
			error = (e as Error).message;
			rows = [];
			total = 0;
		} finally {
			if (id === reqId) {
				loading = false;
				firstLoad = false;
			}
		}
	}

	// Re-run whenever any query input changes (deps read synchronously here).
	$effect(() => {
		runQuery({
			columns: visibleCols,
			search: searchTerm,
			filters,
			sort,
			offset: page * pageSize,
			limit: pageSize
		});
	});

	function toggleSort(name: string) {
		if (!sort || sort.col !== name) sort = { col: name, dir: 'asc' };
		else if (sort.dir === 'asc') sort = { col: name, dir: 'desc' };
		else sort = null;
		page = 0;
	}

	function openFilter(e: MouseEvent, name: string) {
		e.stopPropagation();
		openFilterCol = openFilterCol === name ? null : name;
	}

	function applyFilter(name: string, f: ColumnFilter | null) {
		const next = { ...filters };
		if (f) next[name] = f;
		else delete next[name];
		filters = next;
		page = 0;
		openFilterCol = null;
	}

	function clearAll() {
		filters = {};
		searchInput = '';
		searchTerm = '';
		sort = null;
		page = 0;
	}

	function goto(p: number) {
		page = Math.min(Math.max(0, p), totalPages - 1);
	}

	const hasActiveView = $derived(!!searchTerm || activeFilterCount > 0);

	function triggerDownload(bytes: Uint8Array, filename: string, mime: string) {
		const blob = new Blob([bytes], { type: mime });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = filename;
		document.body.appendChild(a);
		a.click();
		a.remove();
		URL.revokeObjectURL(url);
	}

	async function downloadCsv(scope: 'view' | 'full') {
		if (exporting) return;
		exporting = true;
		error = null;
		try {
			const bytes = await exportCsv({
				columns: scope === 'full' ? COLUMNS.map((c) => c.name) : visibleCols,
				search: scope === 'full' ? '' : searchTerm,
				filters: scope === 'full' ? {} : filters,
				sort: scope === 'full' ? null : sort
			});
			const bom = new Uint8Array([0xef, 0xbb, 0xbf]);
			const withBom = new Uint8Array(bom.length + bytes.length);
			withBom.set(bom, 0);
			withBom.set(bytes, bom.length);
			const name =
				scope === 'full' ? 'pnab_dados_abertos_completo.csv' : 'pnab_dados_abertos_selecao.csv';
			triggerDownload(withBom, name, 'text/csv;charset=utf-8');
		} catch (e) {
			error = (e as Error).message;
		} finally {
			exporting = false;
			downloadOpen = false;
		}
	}

	function onDownloadWindowClick(e: MouseEvent) {
		if (downloadOpen && downloadEl && !downloadEl.contains(e.target as Node)) downloadOpen = false;
	}

	const brl = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
	const num = new Intl.NumberFormat('pt-BR');

	function display(name: string, v: string | number | null): string | null {
		if (v == null || v === '') return null;
		const meta = COLUMN_BY_NAME[name];
		if (meta?.type === 'number') {
			if (name === 'valor_transacao_total_bbagil') return brl.format(Number(v));
			return num.format(Number(v));
		}
		return String(v);
	}
</script>

<svelte:window onclick={onDownloadWindowClick} />

<div class="wrap">
	<div class="toolbar">
		<div class="search">
			<span class="search-icon" aria-hidden="true"></span>
			<input
				type="search"
				placeholder="Buscar em todas as colunas visíveis…"
				value={searchInput}
				oninput={(e) => onSearch(e.currentTarget.value)}
			/>
		</div>
		<div class="toolbar-right">
			{#if activeFilterCount > 0 || searchTerm || sort}
				<button class="clear-btn" onclick={clearAll}>Limpar filtros</button>
			{/if}

			<div class="download" bind:this={downloadEl}>
				<button
					class="dl-trigger"
					onclick={() => (downloadOpen = !downloadOpen)}
					aria-expanded={downloadOpen}
					disabled={exporting}
				>
					{#if exporting}
						<span class="spinner" aria-hidden="true"></span> Gerando…
					{:else}
						<span class="dl-icon" aria-hidden="true"></span> Baixar
					{/if}
				</button>
				{#if downloadOpen}
					<div class="dl-menu" role="menu">
						<button
							role="menuitem"
							onclick={() => downloadCsv('view')}
							title="Linhas filtradas/buscadas e apenas as colunas visíveis"
						>
							<span class="dl-title">Visão atual (CSV)</span>
							<span class="dl-sub"
								>{num.format(total)} linhas · {visibleCols.length}
								{visibleCols.length === 1 ? 'coluna' : 'colunas'}{hasActiveView
									? ' · com filtros'
									: ''}</span
							>
						</button>
						<button role="menuitem" onclick={() => downloadCsv('full')}>
							<span class="dl-title">Base completa (CSV)</span>
							<span class="dl-sub"
								>{grandTotal != null ? num.format(grandTotal) : '167.817'} linhas · 59 colunas</span
							>
						</button>
					</div>
				{/if}
			</div>

			<ColumnPicker {visible} onChange={(next) => (visible = next)} />
		</div>
	</div>

	<div class="status-row">
		{#if error}
			<span class="err">⚠ {error}</span>
		{:else if firstLoad}
			<span class="muted">Carregando base de dados…</span>
		{:else}
			<span class="muted">
				<strong>{num.format(total)}</strong>
				{total === 1 ? 'registro' : 'registros'}
				{#if grandTotal != null && total !== grandTotal}
					<span class="of">de {num.format(grandTotal)}</span>
				{/if}
				{#if loading}<span class="spinner" aria-label="carregando"></span>{/if}
			</span>
		{/if}
	</div>

	<div class="table-scroll" class:dim={loading}>
		{#if visibleMetas.length === 0}
			<p class="empty">Selecione ao menos uma coluna.</p>
		{:else}
			<table>
				<thead>
					<tr>
						{#each visibleMetas as c}
							<th class:num={c.type === 'number'} class:sorted={sort?.col === c.name}>
								<div class="th-inner">
									<button class="th-label" onclick={() => toggleSort(c.name)} title={c.name}>
										<span>{c.label}</span>
										<span class="sort-ind">
											{#if sort?.col === c.name}{sort.dir === 'asc' ? '▲' : '▼'}{/if}
										</span>
									</button>
									<button
										class="filter-btn"
										class:active={!!filters[c.name]}
										aria-label={`Filtrar ${c.label}`}
										onclick={(e) => openFilter(e, c.name)}
									>
										<span class="funnel" aria-hidden="true"></span>
									</button>
									{#if openFilterCol === c.name}
										<ColumnFilterPopover
											column={c}
											current={filters[c.name]}
											onApply={(f) => applyFilter(c.name, f)}
											onClose={() => (openFilterCol = null)}
										/>
									{/if}
								</div>
							</th>
						{/each}
					</tr>
				</thead>
				<tbody>
					{#if rows.length === 0 && !firstLoad}
						<tr class="no-rows">
							<td colspan={visibleMetas.length}>Nenhum registro encontrado.</td>
						</tr>
					{/if}
					{#each rows as row}
						<tr>
							{#each visibleMetas as c}
								{@const v = display(c.name, row[c.name])}
								<td class:num={c.type === 'number'}>
									{#if v == null}<span class="nil">—</span>{:else}{v}{/if}
								</td>
							{/each}
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}
	</div>

	<div class="pager">
		<div class="page-size">
			Linhas por página:
			<select bind:value={pageSize} onchange={() => (page = 0)}>
				{#each PAGE_SIZES as s}<option value={s}>{s}</option>{/each}
			</select>
		</div>
		<div class="page-nav">
			<button onclick={() => goto(0)} disabled={page === 0} aria-label="Primeira página">«</button>
			<button onclick={() => goto(page - 1)} disabled={page === 0} aria-label="Página anterior"
				>‹</button
			>
			<span class="page-of">Página {num.format(page + 1)} de {num.format(totalPages)}</span>
			<button
				onclick={() => goto(page + 1)}
				disabled={page >= totalPages - 1}
				aria-label="Próxima página">›</button
			>
			<button
				onclick={() => goto(totalPages - 1)}
				disabled={page >= totalPages - 1}
				aria-label="Última página">»</button
			>
		</div>
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
	</div>
</div>

<style>
	.wrap {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	/* ── toolbar ── */
	.toolbar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		flex-wrap: wrap;
	}
	.search {
		position: relative;
		flex: 1 1 320px;
		max-width: 480px;
	}
	.search-icon {
		position: absolute;
		left: 0.7rem;
		top: 50%;
		transform: translateY(-50%);
		width: 13px;
		height: 13px;
		border: 1.6px solid #8a93a6;
		border-radius: 50%;
	}
	.search-icon::after {
		content: '';
		position: absolute;
		right: -5px;
		bottom: -3px;
		width: 6px;
		height: 1.6px;
		background: #8a93a6;
		transform: rotate(45deg);
	}
	.search input {
		width: 100%;
		box-sizing: border-box;
		padding: 0.55rem 0.7rem 0.55rem 2rem;
		border: 1px solid #d5dceb;
		border-radius: 6px;
		font-size: 0.9rem;
	}
	.search input:focus {
		outline: none;
		border-color: #4271b5;
	}
	.toolbar-right {
		display: flex;
		align-items: center;
		gap: 0.6rem;
	}
	.clear-btn {
		background: none;
		border: 1px solid #e2e8f5;
		border-radius: 6px;
		padding: 0.5rem 0.75rem;
		font-size: 0.83rem;
		font-weight: 600;
		color: #ab4723;
		cursor: pointer;
	}
	.clear-btn:hover {
		background: #fdf3ee;
	}

	/* ── download ── */
	.download {
		position: relative;
	}
	.dl-trigger {
		display: inline-flex;
		align-items: center;
		gap: 0.45rem;
		padding: 0.5rem 0.8rem;
		background: #4271b5;
		border: 1px solid #4271b5;
		border-radius: 6px;
		font-size: 0.85rem;
		font-weight: 600;
		color: #fff;
		cursor: pointer;
	}
	.dl-trigger:hover:not(:disabled) {
		background: #2e4e8a;
		border-color: #2e4e8a;
	}
	.dl-trigger:disabled {
		opacity: 0.7;
		cursor: default;
	}
	.dl-trigger .spinner {
		border-color: rgba(255, 255, 255, 0.5);
		border-top-color: #fff;
	}
	.dl-icon {
		width: 12px;
		height: 12px;
		position: relative;
	}
	.dl-icon::before {
		content: '';
		position: absolute;
		left: 5px;
		top: 0;
		width: 2px;
		height: 8px;
		background: currentColor;
	}
	.dl-icon::after {
		content: '';
		position: absolute;
		left: 2px;
		top: 4px;
		width: 8px;
		height: 8px;
		border-right: 2px solid currentColor;
		border-bottom: 2px solid currentColor;
		transform: rotate(45deg);
		transform-origin: center;
	}
	.dl-menu {
		position: absolute;
		top: calc(100% + 6px);
		right: 0;
		z-index: 40;
		width: 250px;
		background: #fff;
		border: 1px solid #d5dceb;
		border-radius: 8px;
		box-shadow: 0 12px 28px rgba(15, 21, 64, 0.14);
		padding: 0.35rem;
		display: flex;
		flex-direction: column;
	}
	.dl-menu button {
		display: flex;
		flex-direction: column;
		gap: 0.1rem;
		width: 100%;
		text-align: left;
		background: none;
		border: none;
		border-radius: 6px;
		padding: 0.55rem 0.65rem;
		cursor: pointer;
		text-decoration: none;
		color: inherit;
	}
	.dl-menu button:hover:not(:disabled) {
		background: #f4f6fb;
	}
	.dl-menu button:disabled {
		opacity: 0.5;
		cursor: default;
	}
	.dl-title {
		font-size: 0.85rem;
		font-weight: 600;
		color: #1b1b1b;
	}
	.dl-sub {
		font-size: 0.72rem;
		color: #8a93a6;
	}

	/* ── status ── */
	.status-row {
		font-size: 0.85rem;
		min-height: 1.2rem;
	}
	.muted {
		color: #555;
	}
	.of {
		color: #8a93a6;
	}
	.err {
		color: #ab4723;
		font-weight: 600;
	}
	.spinner {
		display: inline-block;
		width: 12px;
		height: 12px;
		margin-left: 0.5rem;
		border: 2px solid #cfd8ea;
		border-top-color: #4271b5;
		border-radius: 50%;
		vertical-align: -2px;
		animation: spin 0.7s linear infinite;
	}
	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	/* ── table ── */
	.table-scroll {
		overflow-x: auto;
		border: 1px solid #e5e9f0;
		border-radius: 8px;
		background: #fff;
		max-height: 68vh;
		overflow-y: auto;
		transition: opacity 0.15s ease;
	}
	.table-scroll.dim {
		opacity: 0.55;
	}
	table {
		border-collapse: separate;
		border-spacing: 0;
		width: 100%;
		font-size: 0.83rem;
	}
	thead th {
		position: sticky;
		top: 0;
		z-index: 5;
		background: #f4f6fb;
		border-bottom: 1px solid #d5dceb;
		text-align: left;
		white-space: nowrap;
		vertical-align: top;
	}
	th.num {
		text-align: right;
	}
	.th-inner {
		position: relative;
		display: flex;
		align-items: center;
		gap: 0.25rem;
		padding: 0.5rem 0.6rem;
	}
	th.num .th-inner {
		justify-content: flex-end;
	}
	.th-label {
		display: inline-flex;
		align-items: center;
		gap: 0.3rem;
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
		font-size: 0.8rem;
		font-weight: 700;
		color: #1b1b1b;
		white-space: nowrap;
	}
	.th-label:hover {
		color: #4271b5;
	}
	.sort-ind {
		font-size: 0.6rem;
		color: #4271b5;
		width: 0.7em;
	}
	.filter-btn {
		display: inline-flex;
		background: none;
		border: none;
		padding: 0.15rem;
		cursor: pointer;
		color: #b0b8c9;
		border-radius: 3px;
	}
	.filter-btn:hover {
		color: #4271b5;
		background: #e8eefb;
	}
	.filter-btn.active {
		color: #4271b5;
	}
	.funnel {
		width: 11px;
		height: 11px;
		clip-path: polygon(0 0, 100% 0, 60% 50%, 60% 100%, 40% 85%, 40% 50%);
		background: currentColor;
	}
	tbody td {
		padding: 0.45rem 0.6rem;
		border-bottom: 1px solid #eef1f6;
		white-space: nowrap;
		max-width: 340px;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	td.num {
		text-align: right;
		font-variant-numeric: tabular-nums;
	}
	tbody tr:hover td {
		background: #f9fbfe;
	}
	.nil {
		color: #c3c9d6;
	}
	.no-rows td,
	.empty {
		text-align: center;
		color: #8a93a6;
		padding: 2rem;
	}

	/* ── pager ── */
	.pager {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
		flex-wrap: wrap;
		font-size: 0.85rem;
		color: #555;
	}
	.page-size select {
		margin-left: 0.4rem;
		padding: 0.3rem 0.4rem;
		border: 1px solid #d5dceb;
		border-radius: 5px;
	}
	.page-nav {
		display: flex;
		align-items: center;
		gap: 0.3rem;
	}
	.page-nav button {
		min-width: 2rem;
		padding: 0.35rem 0.5rem;
		border: 1px solid #d5dceb;
		background: #fff;
		border-radius: 5px;
		cursor: pointer;
		font-size: 0.9rem;
		color: #2e4e8a;
	}
	.page-nav button:disabled {
		color: #c3c9d6;
		cursor: default;
	}
	.page-nav button:not(:disabled):hover {
		background: #eef2fb;
	}
	.page-of {
		padding: 0 0.6rem;
		white-space: nowrap;
	}
	
	.footer-band {
		width: 100%;
		color: #000;
	}

	.footer {
		text-align: center;
	}

	/* On narrow screens the download menu is a right-anchored dropdown that can
	   spill outside the viewport; pin it to the bottom of the screen instead. */
	@media (max-width: 560px) {
		.dl-menu {
			position: fixed;
			left: 1rem;
			right: 1rem;
			top: auto;
			bottom: 1rem;
			width: auto;
			z-index: 60;
		}
	}
</style>
