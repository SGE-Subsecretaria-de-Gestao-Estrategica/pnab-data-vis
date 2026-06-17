<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title: string;
		subtitle?: string;
		/** Optional tab labels for switching views within the card */
		tabs?: string[];
		activeTab?: number;
		ontabchange?: (index: number) => void;
		children: Snippet;
	}

	let { title, subtitle, tabs, activeTab = 0, ontabchange, children }: Props = $props();
</script>

<div class="card">
	<div class="card-header">
		<h3>{title}</h3>
		{#if subtitle}
			<p class="subtitle">{subtitle}</p>
		{/if}
		{#if tabs && tabs.length > 1}
			<div class="tabs">
				{#each tabs as tab, i}
					<button
						class="tab"
						class:active={activeTab === i}
						onclick={() => ontabchange?.(i)}
					>
						{tab}
					</button>
				{/each}
			</div>
		{/if}
	</div>
	<div class="card-body">
		{@render children()}
	</div>
</div>

<style>
	.card {
		background: transparent;
		border-radius: 0.75rem;
		border: 1px solid rgba(0, 0, 0, 0.09);
		overflow: hidden;
	}

	.card-header {
		padding: 1.25rem 1.5rem 0.75rem;
		border-bottom: 1px solid rgba(0, 0, 0, 0.07);
	}

	h3 {
		margin: 0;
		font-size: 1rem;
		font-weight: 700;
		color: #1B1B1B;
		line-height: 1.3;
	}

	.subtitle {
		margin: 0.25rem 0 0;
		font-size: 0.8rem;
		color: #666;
		line-height: 1.4;
	}

	.tabs {
		display: flex;
		gap: 0;
		margin-top: 0.75rem;
		border-bottom: 2px solid #e0e0e0;
	}

	.tab {
		font-family: 'Rawline', 'Raleway', system-ui, sans-serif;
		font-size: 0.78rem;
		font-weight: 500;
		padding: 0.5rem 1rem;
		border: none;
		background: none;
		color: #666;
		cursor: pointer;
		border-bottom: 2px solid transparent;
		margin-bottom: -2px;
		transition: color 0.15s, border-color 0.15s;
		white-space: nowrap;
	}

	.tab:hover {
		color: #333;
	}

	.tab.active {
		color: #1351B4;
		border-bottom-color: #1351B4;
		font-weight: 600;
	}

	.card-body {
		padding: 1.25rem 1.5rem;
	}
</style>
