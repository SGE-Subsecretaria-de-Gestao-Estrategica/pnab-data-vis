import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import type { Plugin } from 'vite';

const base = process.env.BASE_PATH ?? '';

function rebaseFontPaths(): Plugin {
	return {
		name: 'rebase-font-paths',
		generateBundle(_opts, bundle) {
			if (!base) return;
			for (const chunk of Object.values(bundle)) {
				if (chunk.type === 'asset' && typeof chunk.source === 'string') {
					chunk.source = chunk.source.replaceAll("url('/fonts/", `url('${base}/fonts/`);
				}
			}
		}
	};
}

export default defineConfig({
	plugins: [sveltekit(), rebaseFontPaths()]
});
