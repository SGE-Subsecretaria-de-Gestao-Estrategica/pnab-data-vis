<script lang="ts">
	import { blue } from 'sniic-design-system';
	import { base } from '$app/paths';

	let { active }: { active: 'painel' | 'dados' } = $props();
</script>

<div class="top-tabs" style:--accent={blue}>
	<a
		class="top-tab"
		class:active={active === 'painel'}
		href={base + '/'}
		aria-current={active === 'painel' ? 'page' : undefined}>Painel de dados</a
	>
	<a
		class="top-tab"
		class:active={active === 'dados'}
		href={base + '/dados-abertos'}
		aria-current={active === 'dados' ? 'page' : undefined}>Dados abertos</a
	>
</div>

<style>
	.top-tabs {
		display: flex;
		gap: 1.5rem;
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 2rem;
		border-bottom: 1px solid #e5e9f0;
	}

	.top-tab {
		padding: 0.9rem 0;
		font-size: 0.9rem;
		font-weight: 700;
		color: #555;
		text-decoration: none;
		border-bottom: 2px solid transparent;
		transition: color 0.15s ease, border-color 0.15s ease;
	}

	.top-tab:hover {
		color: var(--accent);
	}

	.top-tab.active {
		color: var(--accent);
		border-bottom-color: var(--accent);
	}
</style>
