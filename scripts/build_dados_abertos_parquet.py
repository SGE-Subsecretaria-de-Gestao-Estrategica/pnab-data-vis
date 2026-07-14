#!/usr/bin/env python3
"""Merge the 6 anonymised microdata CSVs into a single Parquet file.

Output: static/data/dados_abertos.parquet (ZSTD + dictionary-encoded),
consumed at runtime by DuckDB-WASM on the /dados-abertos page.

Run:  python3 scripts/build_dados_abertos_parquet.py
"""

from __future__ import annotations

import glob
import os
import sys

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_GLOB = os.path.join(ROOT, "data", "data_table", "df_aux_anonimizado__parte_*.csv")
OUT_DIR = os.path.join(ROOT, "static", "data")
OUT_PATH = os.path.join(OUT_DIR, "dados_abertos.parquet")

# Columns that must be typed numerically (everything else stays text so that
# codes such as cod_ibge / codigo_municipio keep their leading zeros).
FLOAT_COLS = ["valor_transacao_total_bbagil"]
INT_COLS = ["idade_receita_cpf", "populacao_ibge"]


def main() -> int:
    files = sorted(glob.glob(SRC_GLOB))
    if not files:
        print(f"No source CSVs matched {SRC_GLOB}", file=sys.stderr)
        return 1
    print(f"Reading {len(files)} files…")

    frames = []
    for f in files:
        # utf-8-sig strips the BOM; keep everything as string, treat "" as NA
        # so numeric casts and DuckDB see real NULLs.
        df = pd.read_csv(
            f,
            sep=";",
            encoding="utf-8-sig",
            dtype=str,
            keep_default_na=False,
            na_values=[""],
        )
        frames.append(df)
        print(f"  {os.path.basename(f)}: {len(df):,} rows")

    df = pd.concat(frames, ignore_index=True)
    print(f"Merged: {len(df):,} rows × {len(df.columns)} cols")

    for c in FLOAT_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64")
    for c in INT_COLS:
        # nullable integer so NaN survives as NULL rather than becoming float
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")

    table = pa.Table.from_pandas(df, preserve_index=False)

    os.makedirs(OUT_DIR, exist_ok=True)
    pq.write_table(
        table,
        OUT_PATH,
        compression="zstd",
        compression_level=19,
        use_dictionary=True,
        data_page_size=1 << 20,
    )

    size_mb = os.path.getsize(OUT_PATH) / (1024 * 1024)
    print(f"Wrote {OUT_PATH} — {len(df):,} rows, {size_mb:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
