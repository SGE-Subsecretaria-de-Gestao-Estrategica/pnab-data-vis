// Shared dashboard filter state (Svelte 5 runes)

import { siglaToName, regionMap } from '$lib/data/section1';

export type Visao = 'uf' | 'estados' | 'municipios';
export type Regiao = 'Todas' | 'Norte' | 'Nordeste' | 'Centro-Oeste' | 'Sudeste' | 'Sul';

export const REGIOES: Regiao[] = ['Todas', 'Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'];
export const UF_LIST = Object.keys(siglaToName).sort();

export function createFilters() {
	let visao = $state<Visao>('uf');
	let regiao = $state<Regiao>('Todas');
	let uf = $state<string>('Todas');

	const ufsForRegiao = $derived(
		regiao === 'Todas'
			? UF_LIST
			: UF_LIST.filter((u) => regionMap[u] === regiao)
	);

	const filteredUFs = $derived(
		uf !== 'Todas' ? [uf] : ufsForRegiao
	);

	function reset() {
		visao = 'uf';
		regiao = 'Todas';
		uf = 'Todas';
	}

	return {
		get visao() { return visao; },
		set visao(v: Visao) { visao = v; },
		get regiao() { return regiao; },
		set regiao(v: Regiao) {
			regiao = v;
			if (uf !== 'Todas' && v !== 'Todas' && regionMap[uf] !== v) {
				uf = 'Todas';
			}
		},
		get uf() { return uf; },
		set uf(v: string) { uf = v; },
		get ufsForRegiao() { return ufsForRegiao; },
		get filteredUFs() { return filteredUFs; },
		reset,
	};
}
