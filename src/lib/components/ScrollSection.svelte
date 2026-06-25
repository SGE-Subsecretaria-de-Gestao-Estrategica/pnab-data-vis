<script lang="ts">
	import { type Snippet } from 'svelte';

	interface Props {
		id: string;
		children: Snippet;
	}

	let { id, children }: Props = $props();
	let visible = $state(false);
	let sectionEl: HTMLElement;

	$effect(() => {
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						visible = true;
					}
				});
			},
			{ threshold: 0.2 }
		);

		observer.observe(sectionEl);

		return () => observer.disconnect();
	});
</script>

<section bind:this={sectionEl} {id} class="scroll-section" class:visible>
	{@render children()}
</section>

<style>
	.scroll-section {
		min-height: 100vh;
		max-width: var(--section-max-width);
		margin: 0 auto;
		padding: var(--section-padding);
		display: flex;
		flex-direction: column;
		justify-content: center;
		opacity: 0;
		transform: translateY(30px);
		transition:
			opacity 0.6s ease,
			transform 0.6s ease;
	}

	:global(.scroll-section h1),
	:global(.scroll-section h2),
	:global(.scroll-section h3),
	:global(.scroll-section h4),
	:global(.scroll-section p),
	:global(.scroll-section li) {
		font-family: 'Rawline', system-ui, sans-serif;
	}

	.scroll-section.visible {
		opacity: 1;
		transform: translateY(0);
	}
</style>
