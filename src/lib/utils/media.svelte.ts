import { browser } from '$app/environment';

/**
 * Matcher reativo de media query para os runes do Svelte 5.
 * Use no topo do <script> de um componente:
 *   const isMobile = createMediaQuery('(max-width: 768px)');
 *   ... isMobile.matches ...
 */
export function createMediaQuery(query: string) {
	let matches = $state(false);

	$effect(() => {
		if (!browser) return;
		const mql = window.matchMedia(query);
		matches = mql.matches;
		const onChange = (e: MediaQueryListEvent) => (matches = e.matches);
		mql.addEventListener('change', onChange);
		return () => mql.removeEventListener('change', onChange);
	});

	return {
		get matches() {
			return matches;
		},
	};
}
