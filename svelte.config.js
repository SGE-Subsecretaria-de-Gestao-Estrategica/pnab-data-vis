import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: 'index.html',
			precompress: false,
			strict: true
		}),
		paths: {
			base: process.env.BASE_PATH ?? ''
		},
		prerender: {
			handleHttpError: ({ path, message }) => {
				// Font preloads 404 in the prerender crawler (it can't fetch the
				// binary static assets), but they resolve fine at runtime. The path
				// is base-prefixed (e.g. /pnab-data-vis/fonts/...), so match anywhere.
				if (path.includes('/fonts/')) return;
				throw new Error(message);
			}
		}
	}
};

export default config;
