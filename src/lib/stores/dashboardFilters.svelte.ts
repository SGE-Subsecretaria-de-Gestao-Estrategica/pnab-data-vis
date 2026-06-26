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
	// Segundo estado, opcional, para comparar dois estados lado a lado. 'Todas' = nenhum.
	let uf2 = $state<string>('Todas');

	const ufsForRegiao = $derived(
		regiao === 'Todas' ? UF_LIST : UF_LIST.filter((u) => regionMap[u] === regiao)
	);

	// UFs currently in scope (for aggregating the left-side panel).
	// Com um segundo estado selecionado, o escopo passa a comparar os dois.
	const filteredUFs = $derived(
		uf !== 'Todas' ? (uf2 !== 'Todas' ? [uf, uf2] : [uf]) : ufsForRegiao
	);

	return {
		get visao() { return visao; },
		set visao(v: Visao) {
			visao = v;
			// Leaving "regioes" with a stale single-UF selection would be confusing.
			if (v === 'regioes') { uf = 'Todas'; uf2 = 'Todas'; }
		},
		get regiao() { return regiao; },
		set regiao(v: RegiaoFilter) {
			regiao = v;
			if (uf !== 'Todas' && v !== 'Todas' && regionMap[uf] !== v) uf = 'Todas';
			if (uf2 !== 'Todas' && v !== 'Todas' && regionMap[uf2] !== v) uf2 = 'Todas';
		},
		get uf() { return uf; },
		set uf(v: string) {
			uf = v;
			// Sem estado primário (ou se o comparado virou o primário) não há comparação.
			if (v === 'Todas' || v === uf2) uf2 = 'Todas';
		},
		get uf2() { return uf2; },
		set uf2(v: string) { uf2 = v; },
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
			uf2 = 'Todas';
		},
	};
}

export type DashboardFilters = ReturnType<typeof createDashboardFilters>;
