import { base } from '$app/paths';

// The sniic-design-system `loadBrazilGeoJSON` fetches `/geo/brazil-states.geojson`
// with an absolute path baked into its dist, which 404s when the app is deployed
// under a base path (e.g. GitHub Pages at /pnab-data-vis/). This local loader
// respects SvelteKit's `base` so the asset resolves correctly in every deploy.

let cache: unknown = null;
let inflight: Promise<unknown> | null = null;

export function loadBrazilGeoJSON(): Promise<unknown> {
	if (cache) return Promise.resolve(cache);
	if (!inflight) {
		inflight = fetch(`${base}/geo/brazil-states.geojson`)
			.then((r) => r.json())
			.then((d) => {
				cache = d;
				inflight = null;
				return d;
			});
	}
	return inflight;
}
