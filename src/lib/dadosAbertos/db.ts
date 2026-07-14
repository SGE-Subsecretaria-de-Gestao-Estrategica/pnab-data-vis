// DuckDB-WASM client for the /dados-abertos microdata table.
//
// The whole Parquet file (~4 MB) is fetched once and registered in WASM memory
// the first time the page needs it; every subsequent search / filter / sort /
// page is a SQL query over columnar data, so it stays fast and low-memory.
//
// SQL safety: column names only ever come from the whitelist in ./columns
// (isKnownColumn) and are double-quoted; user-provided *values* are escaped as
// SQL string literals or validated as finite numbers before being inlined.

import * as duckdb from '@duckdb/duckdb-wasm';
import mvp_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import mvp_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
import eh_wasm from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';
import { base } from '$app/paths';
import { isKnownColumn } from './columns';

const TABLE = 'dados';
const PARQUET_FILE = 'dados_abertos.parquet';

export type ColumnFilter =
	| { kind: 'in'; values: string[]; includeNull?: boolean }
	| { kind: 'contains'; text: string }
	| { kind: 'range'; min: number | null; max: number | null };

export interface QueryOptions {
	columns: string[]; // visible columns to SELECT and to search across
	search: string; // global search term
	filters: Record<string, ColumnFilter>; // keyed by column name
	sort: { col: string; dir: 'asc' | 'desc' } | null;
	offset: number;
	limit: number;
}

export type Row = Record<string, string | number | null>;

// ── connection (lazy singleton) ────────────────────────────────────────────
let ready: Promise<duckdb.AsyncDuckDBConnection> | null = null;
let dbInstance: duckdb.AsyncDuckDB | null = null;

export function initDados(): Promise<duckdb.AsyncDuckDBConnection> {
	if (!ready) ready = boot();
	return ready;
}

async function boot(): Promise<duckdb.AsyncDuckDBConnection> {
	const bundle = await duckdb.selectBundle({
		mvp: { mainModule: mvp_wasm, mainWorker: mvp_worker },
		eh: { mainModule: eh_wasm, mainWorker: eh_worker }
	});

	const worker = new Worker(bundle.mainWorker!);
	const logger = new duckdb.ConsoleLogger(duckdb.LogLevel.WARNING);
	const db = new duckdb.AsyncDuckDB(logger, worker);
	await db.instantiate(bundle.mainModule, bundle.pthreadWorker);

	const url = `${base}/data/${PARQUET_FILE}`;
	const resp = await fetch(url);
	if (!resp.ok) throw new Error(`Não foi possível carregar os dados (HTTP ${resp.status}).`);
	await db.registerFileBuffer(PARQUET_FILE, new Uint8Array(await resp.arrayBuffer()));

	const conn = await db.connect();
	await conn.query(`CREATE OR REPLACE VIEW ${TABLE} AS SELECT * FROM read_parquet('${PARQUET_FILE}')`);
	dbInstance = db;
	return conn;
}

// ── SQL literal helpers ─────────────────────────────────────────────────────
function col(name: string): string {
	return `"${name.replace(/"/g, '""')}"`;
}
function litStr(v: string): string {
	return `'${v.replace(/'/g, "''")}'`;
}
function litNum(v: number): string {
	if (!Number.isFinite(v)) throw new Error('Valor numérico inválido.');
	return String(v);
}
// Escape LIKE wildcards so search treats them literally (paired with ESCAPE '\').
function likePattern(term: string): string {
	return '%' + term.replace(/[\\%_]/g, '\\$&') + '%';
}
function ilike(colExpr: string, term: string): string {
	return `${colExpr} ILIKE ${litStr(likePattern(term))} ESCAPE '\\'`;
}

function buildWhere(opts: QueryOptions): string {
	const clauses: string[] = [];

	for (const [name, f] of Object.entries(opts.filters)) {
		if (!isKnownColumn(name)) continue;
		const c = col(name);
		if (f.kind === 'in') {
			const vals = f.values.filter((v) => v != null);
			const parts: string[] = [];
			if (vals.length) parts.push(`CAST(${c} AS VARCHAR) IN (${vals.map(litStr).join(', ')})`);
			if (f.includeNull) parts.push(`${c} IS NULL`);
			if (parts.length) clauses.push(parts.length > 1 ? `(${parts.join(' OR ')})` : parts[0]);
		} else if (f.kind === 'contains') {
			const t = f.text.trim();
			if (t) clauses.push(ilike(`CAST(${c} AS VARCHAR)`, t));
		} else if (f.kind === 'range') {
			if (f.min != null) clauses.push(`${c} >= ${litNum(f.min)}`);
			if (f.max != null) clauses.push(`${c} <= ${litNum(f.max)}`);
		}
	}

	const term = opts.search.trim();
	if (term) {
		const cols = opts.columns.filter(isKnownColumn);
		if (cols.length) {
			const ors = cols.map((n) => ilike(`CAST(${col(n)} AS VARCHAR)`, term));
			clauses.push(`(${ors.join(' OR ')})`);
		}
	}

	return clauses.length ? 'WHERE ' + clauses.join(' AND ') : '';
}

function normalize(v: unknown): string | number | null {
	if (v == null) return null;
	if (typeof v === 'bigint') return Number(v);
	if (typeof v === 'number' || typeof v === 'string') return v;
	return String(v);
}

// ── queries ─────────────────────────────────────────────────────────────────
export async function totalRows(): Promise<number> {
	const conn = await initDados();
	const res = await conn.query(`SELECT COUNT(*)::BIGINT AS n FROM ${TABLE}`);
	return Number((res.get(0) as { n: bigint } | null)?.n ?? 0);
}

export async function queryPage(opts: QueryOptions): Promise<{ rows: Row[]; total: number }> {
	const conn = await initDados();
	const cols = opts.columns.filter(isKnownColumn);
	if (!cols.length) return { rows: [], total: 0 };

	const where = buildWhere(opts);
	const limit = Math.max(1, Math.min(opts.limit, 500));
	const offset = Math.max(0, opts.offset);

	let orderBy = '';
	if (opts.sort && isKnownColumn(opts.sort.col)) {
		const dir = opts.sort.dir === 'desc' ? 'DESC' : 'ASC';
		orderBy = `ORDER BY ${col(opts.sort.col)} ${dir} NULLS LAST`;
	}

	const countRes = await conn.query(`SELECT COUNT(*)::BIGINT AS n FROM ${TABLE} ${where}`);
	const total = Number((countRes.get(0) as { n: bigint } | null)?.n ?? 0);

	const selectList = cols.map(col).join(', ');
	const dataRes = await conn.query(
		`SELECT ${selectList} FROM ${TABLE} ${where} ${orderBy} LIMIT ${limit} OFFSET ${offset}`
	);

	const rows = dataRes.toArray().map((r) => {
		const o: Row = {};
		for (const c of cols) o[c] = normalize((r as Record<string, unknown>)[c]);
		return o;
	});
	return { rows, total };
}

// Distinct values for a categorical filter, most frequent first.
export async function distinctValues(
	name: string,
	limit = 300
): Promise<{ values: string[]; hasNull: boolean; truncated: boolean }> {
	if (!isKnownColumn(name)) return { values: [], hasNull: false, truncated: false };
	const conn = await initDados();
	const c = col(name);
	const res = await conn.query(
		`SELECT CAST(${c} AS VARCHAR) AS v, COUNT(*)::BIGINT AS n FROM ${TABLE}
		 WHERE ${c} IS NOT NULL GROUP BY 1 ORDER BY n DESC, v ASC LIMIT ${limit + 1}`
	);
	const arr = res.toArray() as { v: string }[];
	const truncated = arr.length > limit;
	const values = arr.slice(0, limit).map((r) => String(r.v));
	const nullRes = await conn.query(`SELECT COUNT(*)::BIGINT AS n FROM ${TABLE} WHERE ${c} IS NULL`);
	const hasNull = Number((nullRes.get(0) as { n: bigint } | null)?.n ?? 0) > 0;
	return { values, hasNull, truncated };
}

// Distinct cardinality — used to pick between a checkbox list and a text filter.
export async function distinctCount(name: string): Promise<number> {
	if (!isKnownColumn(name)) return 0;
	const conn = await initDados();
	const res = await conn.query(`SELECT COUNT(DISTINCT ${col(name)})::BIGINT AS n FROM ${TABLE}`);
	return Number((res.get(0) as { n: bigint } | null)?.n ?? 0);
}

export async function numericRange(name: string): Promise<{ min: number; max: number }> {
	if (!isKnownColumn(name)) return { min: 0, max: 0 };
	const conn = await initDados();
	const c = col(name);
	const res = await conn.query(`SELECT MIN(${c}) AS lo, MAX(${c}) AS hi FROM ${TABLE}`);
	const r = res.get(0) as { lo: unknown; hi: unknown } | null;
	return { min: Number(r?.lo ?? 0), max: Number(r?.hi ?? 0) };
}

// Export rows (respecting search/filters/sort) to a UTF-8 CSV byte buffer, using
// DuckDB's COPY into the in-WASM filesystem. `;` delimiter + BOM (added by the
// caller) make it open cleanly in pt-BR Excel.
export async function exportCsv(opts: {
	columns: string[];
	search: string;
	filters: Record<string, ColumnFilter>;
	sort: { col: string; dir: 'asc' | 'desc' } | null;
}): Promise<Uint8Array> {
	const conn = await initDados();
	if (!dbInstance) throw new Error('Base de dados não inicializada.');
	const cols = opts.columns.filter(isKnownColumn);
	if (!cols.length) throw new Error('Selecione ao menos uma coluna.');

	const where = buildWhere({ ...opts, offset: 0, limit: 1 });
	let orderBy = '';
	if (opts.sort && isKnownColumn(opts.sort.col)) {
		const dir = opts.sort.dir === 'desc' ? 'DESC' : 'ASC';
		orderBy = `ORDER BY ${col(opts.sort.col)} ${dir} NULLS LAST`;
	}

	const fname = `export_${Date.now()}.csv`;
	const select = `SELECT ${cols.map(col).join(', ')} FROM ${TABLE} ${where} ${orderBy}`;
	try {
		await conn.query(
			`COPY (${select}) TO '${fname}' (FORMAT CSV, HEADER, DELIMITER ';')`
		);
		return await dbInstance.copyFileToBuffer(fname);
	} finally {
		await dbInstance.dropFile(fname).catch(() => {});
	}
}
