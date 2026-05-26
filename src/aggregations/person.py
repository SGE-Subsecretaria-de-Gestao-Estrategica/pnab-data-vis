import pandas as pd
import numpy as np
import re
import unicodedata
from pathlib import Path


def aggregate_contemplados_pf_pj_proportion(
    df_cubo: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcula a proporção entre quantidade de contemplados pessoas físicas e
    pessoas jurídicas.

    Usa:
    - CPF como pessoa física;
    - CNPJ como pessoa jurídica;
    - quantidade como coluna de contagem de contemplados.

    Retorna uma tabela com uma linha.
    """

    df = df_cubo.copy()

    df["tipo_documento_norm"] = (
        df["tipo_documento"]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    quantidade_contemplados = df["quantidade"].sum()

    quantidade_contemplados_pf = (
        df
        .loc[df["tipo_documento_norm"].eq("CPF"), "quantidade"]
        .sum()
    )

    quantidade_contemplados_pj = (
        df
        .loc[df["tipo_documento_norm"].eq("CNPJ"), "quantidade"]
        .sum()
    )

    df_resultado = pd.DataFrame({
        "quantidade_contemplados": [quantidade_contemplados],
        "perc_quantidade_contemplados": [1],
        "quantidade_contemplados_pf": [quantidade_contemplados_pf],
        "perc_quantidade_contemplados_pf": [
            quantidade_contemplados_pf / quantidade_contemplados
            if quantidade_contemplados > 0 else np.nan
        ],
        "quantidade_contemplados_pj": [quantidade_contemplados_pj],
        "perc_quantidade_contemplados_pj": [
            quantidade_contemplados_pj / quantidade_contemplados
            if quantidade_contemplados > 0 else np.nan
        ],
    })

    colunas_quantidade = [
        "quantidade_contemplados",
        "quantidade_contemplados_pf",
        "quantidade_contemplados_pj",
    ]

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    return df_resultado


def aggregate_contemplados_by_sexo_proportion(
    df_cubo: pd.DataFrame
) -> pd.DataFrame:
    """
    Calcula a proporção da quantidade e do valor de contemplados por Sexo.

    Filtros aplicados:
    - considera apenas registros com tipo_documento == CPF;
    - considera apenas CPFs com Sexo marcado como Masculino ou Feminino.

    Usa:
    - quantidade como contagem de contemplados;
    - valor_transacao como valor executado.

    Retorna uma tabela com uma linha.
    """

    df = df_cubo.copy()

    df["tipo_documento_norm"] = (
        df["tipo_documento"]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df["sexo_norm"] = (
        df["Sexo"]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df = df[
        df["tipo_documento_norm"].eq("CPF")
        & df["sexo_norm"].isin(["FEMININO", "MASCULINO"])
    ].copy()

    quantidade_contemplados = df["quantidade"].sum()
    valor_contemplados = df["valor_transacao"].sum()

    quantidade_contemplados_feminino = (
        df
        .loc[df["sexo_norm"].eq("FEMININO"), "quantidade"]
        .sum()
    )

    quantidade_contemplados_masculino = (
        df
        .loc[df["sexo_norm"].eq("MASCULINO"), "quantidade"]
        .sum()
    )

    valor_contemplados_feminino = (
        df
        .loc[df["sexo_norm"].eq("FEMININO"), "valor_transacao"]
        .sum()
    )

    valor_contemplados_masculino = (
        df
        .loc[df["sexo_norm"].eq("MASCULINO"), "valor_transacao"]
        .sum()
    )

    df_resultado = pd.DataFrame({
        "quantidade_contemplados": [quantidade_contemplados],
        "perc_quantidade_contemplados": [1],

        "valor_contemplados": [valor_contemplados],
        "perc_valor_contemplados": [1],

        "quantidade_contemplados_feminino": [
            quantidade_contemplados_feminino
        ],
        "perc_quantidade_contemplados_feminino": [
            quantidade_contemplados_feminino / quantidade_contemplados
            if quantidade_contemplados > 0 else np.nan
        ],

        "valor_contemplados_feminino": [
            valor_contemplados_feminino
        ],
        "perc_valor_contemplados_feminino": [
            valor_contemplados_feminino / valor_contemplados
            if valor_contemplados > 0 else np.nan
        ],

        "quantidade_contemplados_masculino": [
            quantidade_contemplados_masculino
        ],
        "perc_quantidade_contemplados_masculino": [
            quantidade_contemplados_masculino / quantidade_contemplados
            if quantidade_contemplados > 0 else np.nan
        ],

        "valor_contemplados_masculino": [
            valor_contemplados_masculino
        ],
        "perc_valor_contemplados_masculino": [
            valor_contemplados_masculino / valor_contemplados
            if valor_contemplados > 0 else np.nan
        ],
    })

    colunas_quantidade = [
        "quantidade_contemplados",
        "quantidade_contemplados_feminino",
        "quantidade_contemplados_masculino",
    ]

    colunas_valor = [
        "valor_contemplados",
        "valor_contemplados_feminino",
        "valor_contemplados_masculino",
    ]

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_valor] = (
        np.ceil(df_resultado[colunas_valor])
        .fillna(0)
        .astype("Int64")
    )

    return df_resultado


import numpy as np
import pandas as pd


def aggregate_valor_quantity_by_age_group_sexo_wide(
    df_cubo: pd.DataFrame
) -> pd.DataFrame:
    """
    Agrega valor recebido e quantidade de contemplados por faixa_etaria,
    abrindo Sexo em colunas.

    Filtros aplicados:
    - considera apenas tipo_documento == CPF;
    - considera apenas Sexo válido: Feminino ou Masculino.

    Retorna uma linha por faixa_etaria.
    """

    df = df_cubo.copy()

    # ------------------------------------------------------------
    # 1. Normalizar tipo_documento
    # ------------------------------------------------------------

    df["tipo_documento_norm"] = (
        df["tipo_documento"]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    # ------------------------------------------------------------
    # 2. Normalizar Sexo
    # ------------------------------------------------------------

    df["sexo_norm"] = (
        df["Sexo"]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df["sexo_tratado"] = df["sexo_norm"].map({
        "FEMININO": "feminino",
        "MASCULINO": "masculino"
    })

    # ------------------------------------------------------------
    # 3. Filtrar CPF com Sexo válido
    # ------------------------------------------------------------

    df = df[
        df["tipo_documento_norm"].eq("CPF")
        & df["sexo_tratado"].isin(["feminino", "masculino"])
    ].copy()

    # ------------------------------------------------------------
    # 4. Tratar faixa_etaria
    # ------------------------------------------------------------

    df["faixa_etaria_tratada"] = (
        df["faixa_etaria"]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------------
    # 5. Pivot de valor recebido por Sexo
    # ------------------------------------------------------------

    df_valor = (
        df
        .pivot_table(
            index="faixa_etaria_tratada",
            columns="sexo_tratado",
            values="valor_transacao",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    df_valor = df_valor.rename(columns={
        "feminino": "valor_recebido_feminino",
        "masculino": "valor_recebido_masculino"
    })

    # Garantir colunas mesmo quando algum sexo não existir
    for coluna in [
        "valor_recebido_feminino",
        "valor_recebido_masculino"
    ]:
        if coluna not in df_valor.columns:
            df_valor[coluna] = 0

    # ------------------------------------------------------------
    # 6. Pivot de quantidade de contemplados por Sexo
    # ------------------------------------------------------------

    df_quantidade = (
        df
        .pivot_table(
            index="faixa_etaria_tratada",
            columns="sexo_tratado",
            values="quantidade",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    df_quantidade = df_quantidade.rename(columns={
        "feminino": "quantidade_contemplados_feminino",
        "masculino": "quantidade_contemplados_masculino"
    })

    # Garantir colunas mesmo quando algum sexo não existir
    for coluna in [
        "quantidade_contemplados_feminino",
        "quantidade_contemplados_masculino"
    ]:
        if coluna not in df_quantidade.columns:
            df_quantidade[coluna] = 0

    # ------------------------------------------------------------
    # 7. Juntar valor e quantidade
    # ------------------------------------------------------------

    df_resultado = df_valor.merge(
        df_quantidade,
        on="faixa_etaria_tratada",
        how="left"
    )

    # ------------------------------------------------------------
    # 8. Totais por faixa_etaria
    # ------------------------------------------------------------

    df_resultado["valor_recebido_total"] = (
        df_resultado["valor_recebido_feminino"]
        + df_resultado["valor_recebido_masculino"]
    )

    df_resultado["quantidade_contemplados_total"] = (
        df_resultado["quantidade_contemplados_feminino"]
        + df_resultado["quantidade_contemplados_masculino"]
    )

    # ------------------------------------------------------------
    # 9. Percentuais dentro da faixa_etaria
    # ------------------------------------------------------------

    df_resultado["perc_valor_feminino_na_faixa"] = np.where(
        df_resultado["valor_recebido_total"].ne(0),
        df_resultado["valor_recebido_feminino"]
        / df_resultado["valor_recebido_total"],
        np.nan
    )

    df_resultado["perc_valor_masculino_na_faixa"] = np.where(
        df_resultado["valor_recebido_total"].ne(0),
        df_resultado["valor_recebido_masculino"]
        / df_resultado["valor_recebido_total"],
        np.nan
    )

    df_resultado["perc_quantidade_feminino_na_faixa"] = np.where(
        df_resultado["quantidade_contemplados_total"].ne(0),
        df_resultado["quantidade_contemplados_feminino"]
        / df_resultado["quantidade_contemplados_total"],
        np.nan
    )

    df_resultado["perc_quantidade_masculino_na_faixa"] = np.where(
        df_resultado["quantidade_contemplados_total"].ne(0),
        df_resultado["quantidade_contemplados_masculino"]
        / df_resultado["quantidade_contemplados_total"],
        np.nan
    )

    # ------------------------------------------------------------
    # 10. Percentuais da faixa no total geral
    # ------------------------------------------------------------

    valor_total_geral = df_resultado["valor_recebido_total"].sum()
    quantidade_total_geral = df_resultado["quantidade_contemplados_total"].sum()

    df_resultado["perc_valor_total_geral"] = np.where(
        valor_total_geral > 0,
        df_resultado["valor_recebido_total"] / valor_total_geral,
        np.nan
    )

    df_resultado["perc_quantidade_total_geral"] = np.where(
        quantidade_total_geral > 0,
        df_resultado["quantidade_contemplados_total"] / quantidade_total_geral,
        np.nan
    )

    # ------------------------------------------------------------
    # 11. Formatar valores
    # ------------------------------------------------------------

    colunas_valor = [
        "valor_recebido_feminino",
        "valor_recebido_masculino",
        "valor_recebido_total"
    ]

    colunas_quantidade = [
        "quantidade_contemplados_feminino",
        "quantidade_contemplados_masculino",
        "quantidade_contemplados_total"
    ]

    df_resultado[colunas_valor] = (
        np.ceil(df_resultado[colunas_valor])
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    # ------------------------------------------------------------
    # 12. Renomear e ordenar colunas
    # ------------------------------------------------------------

    df_resultado = (
        df_resultado
        .rename(columns={
            "faixa_etaria_tratada": "faixa_etaria"
        })
        [
            [
                "faixa_etaria",

                "valor_recebido_feminino",
                "valor_recebido_masculino",
                "valor_recebido_total",
                "perc_valor_feminino_na_faixa",
                "perc_valor_masculino_na_faixa",
                "perc_valor_total_geral",

                "quantidade_contemplados_feminino",
                "quantidade_contemplados_masculino",
                "quantidade_contemplados_total",
                "perc_quantidade_feminino_na_faixa",
                "perc_quantidade_masculino_na_faixa",
                "perc_quantidade_total_geral",
            ]
        ]
        .sort_values("faixa_etaria")
        .reset_index(drop=True)
    )

    return df_resultado



def _normalize_suffix(value: str) -> str:
    """
    Normaliza textos para uso em nomes de colunas.
    Exemplo: 'Centro-Oeste' -> 'centro_oeste'
    """
    value = str(value)

    value = (
        unicodedata
        .normalize("NFKD", value)
        .encode("ascii", errors="ignore")
        .decode("utf-8")
    )

    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = value.strip("_")

    return value or "nao_informado"


def aggregate_value_quantity_by_age_group_region_wide(
    df_cubo: pd.DataFrame,
    output_csv_path: str | Path | None = None,
    percent_as_100: bool = False
) -> pd.DataFrame:
    """
    Agrega valor recebido e quantidade de contemplados por faixa_etaria e região.

    Filtro aplicado:
    - considera apenas tipo_documento == CPF.

    Retorna uma linha por faixa_etaria, com regiões abertas em colunas.

    Parâmetros
    ----------
    df_cubo : pd.DataFrame
        Base principal.

    output_csv_path : str | Path | None
        Caminho opcional para salvar o CSV.

    percent_as_100 : bool
        Se True, transforma proporções em percentuais de 0 a 100.
        Se False, mantém proporções de 0 a 1.
    """

    df = df_cubo.copy()

    # ------------------------------------------------------------
    # 1. Normalizar tipo_documento
    # ------------------------------------------------------------

    df["tipo_documento_norm"] = (
        df["tipo_documento"]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    # ------------------------------------------------------------
    # 2. Filtrar apenas CPF
    # ------------------------------------------------------------

    df = df[df["tipo_documento_norm"].eq("CPF")].copy()

    # ------------------------------------------------------------
    # 3. Tratar faixa_etaria e regiao
    # ------------------------------------------------------------

    df["faixa_etaria_tratada"] = (
        df["faixa_etaria"]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    df["regiao_tratada"] = (
        df["regiao"]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    df["regiao_col"] = df["regiao_tratada"].apply(_normalize_suffix)

    regioes_padrao = [
        "centro_oeste",
        "nordeste",
        "norte",
        "sudeste",
        "sul",
    ]

    regioes_existentes = list(df["regiao_col"].dropna().unique())

    regioes_ordenadas = (
        [regiao for regiao in regioes_padrao if regiao in regioes_existentes]
        + sorted([
            regiao
            for regiao in regioes_existentes
            if regiao not in regioes_padrao
        ])
    )

    # ------------------------------------------------------------
    # 4. Pivot de valor recebido por região
    # ------------------------------------------------------------

    df_valor = (
        df
        .pivot_table(
            index="faixa_etaria_tratada",
            columns="regiao_col",
            values="valor_transacao",
            aggfunc="sum",
            fill_value=0
        )
        .reindex(columns=regioes_ordenadas, fill_value=0)
        .reset_index()
    )

    df_valor = df_valor.rename(
        columns={
            regiao: f"valor_recebido_{regiao}"
            for regiao in regioes_ordenadas
        }
    )

    # ------------------------------------------------------------
    # 5. Pivot de quantidade de contemplados por região
    # ------------------------------------------------------------

    df_quantidade = (
        df
        .pivot_table(
            index="faixa_etaria_tratada",
            columns="regiao_col",
            values="quantidade",
            aggfunc="sum",
            fill_value=0
        )
        .reindex(columns=regioes_ordenadas, fill_value=0)
        .reset_index()
    )

    df_quantidade = df_quantidade.rename(
        columns={
            regiao: f"quantidade_contemplados_{regiao}"
            for regiao in regioes_ordenadas
        }
    )

    # ------------------------------------------------------------
    # 6. Juntar valor e quantidade
    # ------------------------------------------------------------

    df_resultado = df_valor.merge(
        df_quantidade,
        on="faixa_etaria_tratada",
        how="left"
    )

    colunas_valor_regiao = [
        f"valor_recebido_{regiao}"
        for regiao in regioes_ordenadas
    ]

    colunas_quantidade_regiao = [
        f"quantidade_contemplados_{regiao}"
        for regiao in regioes_ordenadas
    ]

    # ------------------------------------------------------------
    # 7. Totais por faixa_etaria
    # ------------------------------------------------------------

    df_resultado["valor_recebido_total"] = (
        df_resultado[colunas_valor_regiao].sum(axis=1)
    )

    df_resultado["quantidade_contemplados_total"] = (
        df_resultado[colunas_quantidade_regiao].sum(axis=1)
    )

    valor_total_geral = df_resultado["valor_recebido_total"].sum()
    quantidade_total_geral = df_resultado["quantidade_contemplados_total"].sum()

    # ------------------------------------------------------------
    # 8. Percentuais de valor
    # ------------------------------------------------------------

    for regiao in regioes_ordenadas:
        coluna_valor = f"valor_recebido_{regiao}"

        df_resultado[f"perc_valor_total_geral_{regiao}"] = np.where(
            valor_total_geral > 0,
            df_resultado[coluna_valor] / valor_total_geral,
            np.nan
        )

        df_resultado[f"perc_valor_na_faixa_{regiao}"] = np.where(
            df_resultado["valor_recebido_total"].ne(0),
            df_resultado[coluna_valor] / df_resultado["valor_recebido_total"],
            np.nan
        )

    df_resultado["perc_valor_total_geral"] = np.where(
        valor_total_geral > 0,
        df_resultado["valor_recebido_total"] / valor_total_geral,
        np.nan
    )

    # ------------------------------------------------------------
    # 9. Percentuais de quantidade
    # ------------------------------------------------------------

    for regiao in regioes_ordenadas:
        coluna_quantidade = f"quantidade_contemplados_{regiao}"

        df_resultado[f"perc_quantidade_total_geral_{regiao}"] = np.where(
            quantidade_total_geral > 0,
            df_resultado[coluna_quantidade] / quantidade_total_geral,
            np.nan
        )

        df_resultado[f"perc_quantidade_na_faixa_{regiao}"] = np.where(
            df_resultado["quantidade_contemplados_total"].ne(0),
            (
                df_resultado[coluna_quantidade]
                / df_resultado["quantidade_contemplados_total"]
            ),
            np.nan
        )

    df_resultado["perc_quantidade_total_geral"] = np.where(
        quantidade_total_geral > 0,
        df_resultado["quantidade_contemplados_total"] / quantidade_total_geral,
        np.nan
    )

    # ------------------------------------------------------------
    # 10. Converter percentuais para 0-100, se desejado
    # ------------------------------------------------------------

    colunas_percentuais = [
        coluna
        for coluna in df_resultado.columns
        if coluna.startswith("perc_")
    ]

    if percent_as_100:
        df_resultado[colunas_percentuais] = (
            df_resultado[colunas_percentuais] * 100
        )

    # ------------------------------------------------------------
    # 11. Formatar valores
    # ------------------------------------------------------------

    colunas_valor = colunas_valor_regiao + ["valor_recebido_total"]

    colunas_quantidade = (
        colunas_quantidade_regiao
        + ["quantidade_contemplados_total"]
    )

    df_resultado[colunas_valor] = (
        np.ceil(df_resultado[colunas_valor])
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    # ------------------------------------------------------------
    # 12. Renomear coluna principal
    # ------------------------------------------------------------

    df_resultado = df_resultado.rename(
        columns={"faixa_etaria_tratada": "faixa_etaria"}
    )

    # ------------------------------------------------------------
    # 13. Ordenar colunas
    # ------------------------------------------------------------

    colunas_finais = (
        ["faixa_etaria"]
        + colunas_valor_regiao
        + ["valor_recebido_total"]
        + [
            f"perc_valor_total_geral_{regiao}"
            for regiao in regioes_ordenadas
        ]
        + ["perc_valor_total_geral"]
        + [
            f"perc_valor_na_faixa_{regiao}"
            for regiao in regioes_ordenadas
        ]
        + colunas_quantidade_regiao
        + ["quantidade_contemplados_total"]
        + [
            f"perc_quantidade_total_geral_{regiao}"
            for regiao in regioes_ordenadas
        ]
        + ["perc_quantidade_total_geral"]
        + [
            f"perc_quantidade_na_faixa_{regiao}"
            for regiao in regioes_ordenadas
        ]
    )

    df_resultado = (
        df_resultado[colunas_finais]
        .sort_values("faixa_etaria")
        .reset_index(drop=True)
    )

    # ------------------------------------------------------------
    # 14. Salvar CSV, se informado
    # ------------------------------------------------------------

    if output_csv_path is not None:
        output_csv_path = Path(output_csv_path)
        output_csv_path.parent.mkdir(parents=True, exist_ok=True)

        df_resultado.to_csv(
            output_csv_path,
            index=False,
            encoding="utf-8-sig"
        )

    return df_resultado