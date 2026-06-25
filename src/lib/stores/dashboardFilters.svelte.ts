// Shared dashboard filter state (Svelte 5 runes).
//
// `visao` is the entity level (uf / estados / municipios / regioes).
// `regiao` and `uf` are scoping selections. Clicking a UF on the map sets `uf`
// (or `regiao`, when the visão is `regioes`), so map clicks and the dropdowns
// stay in sync.

import { regionMap, UF_LIST, REGIOES } from '$lib/data/dashboard';
import type { Visao, Regiao } from '$lib/data/dashboard';

export type RegiaoFilter = 'Todas' | Regiao;
export const REGIAO_OPTIONS: RegiaoFilter[] = ['Todas', ...REGIOES];

export const VISAO_LABELS: Record<Visao, string> = {
	uf: 'UF (Estado + Municípios)',
	estados: 'Estados',
	municipios: 'Municípios',
	regioes: 'Regiões',
};

export function createDashboardFilters(initialVisao: Visao = 'uf') {
	let visao = $state<Visao>(initialVisao);
	let regiao = $state<RegiaoFilter>('Todas');
	let uf = $state<string>('Todas');

	const ufsForRegiao = $derived(
		regiao === 'Todas' ? UF_LIST : UF_LIST.filter((u) => regionMap[u] === regiao)
	);

	// UFs currently in scope (for aggregating the left-side panel).
	const filteredUFs = $derived(uf !== 'Todas' ? [uf] : ufsForRegiao);

	return {
		get visao() { return visao; },
		set visao(v: Visao) {
			visao = v;
			// Leaving "regioes" with a stale single-UF selection would be confusing.
			if (v === 'regioes') uf = 'Todas';
		},
		get regiao() { return regiao; },
		set regiao(v: RegiaoFilter) {
			regiao = v;
			if (uf !== 'Todas' && v !== 'Todas' && regionMap[uf] !== v) uf = 'Todas';
		},
		get uf() { return uf; },
		set uf(v: string) { uf = v; },
		get ufsForRegiao() { return ufsForRegiao; },
		get filteredUFs() { return filteredUFs; },

		/** Map click handler — selects a UF (or its region, in `regioes` visão). */
		selectUf(sigla: string) {
			if (visao === 'regioes') {
				const r = regionMap[sigla] as RegiaoFilter | undefined;
				regiao = regiao === r ? 'Todas' : (r ?? 'Todas');
				uf = 'Todas';
			} else {
				uf = uf === sigla ? 'Todas' : sigla;
			}
		},

		reset() {
			visao = initialVisao;
			regiao = 'Todas';
			uf = 'Todas';
		},
	};
}

export type DashboardFilters = ReturnType<typeof createDashboardFilters>;
