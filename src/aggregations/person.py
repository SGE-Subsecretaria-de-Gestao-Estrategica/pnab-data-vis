import pandas as pd
import numpy as np


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

import numpy as np
import pandas as pd


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


def aggregate_value_quantity_by_sexo_age_group(
    df_cubo: pd.DataFrame
) -> pd.DataFrame:
    """
    Agrega valor recebido e quantidade de contemplados por Sexo e faixa_etaria.

    Filtros aplicados:
    - considera apenas tipo_documento == CPF;
    - considera apenas Sexo válido: Feminino ou Masculino.

    Retorna:
    - valor recebido por Sexo e faixa_etaria;
    - quantidade de contemplados por Sexo e faixa_etaria;
    - percentual do valor em relação ao total geral;
    - percentual da quantidade em relação ao total geral;
    - percentual do valor dentro da faixa_etaria;
    - percentual da quantidade dentro da faixa_etaria.
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
    # 3. Normalizar Sexo
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
        "FEMININO": "Feminino",
        "MASCULINO": "Masculino"
    })

    # ------------------------------------------------------------
    # 4. Manter apenas Sexo válido
    # ------------------------------------------------------------

    df = df[
        df["sexo_tratado"].isin(["Feminino", "Masculino"])
    ].copy()

    # ------------------------------------------------------------
    # 5. Tratar faixa_etaria
    # ------------------------------------------------------------

    df["faixa_etaria_tratada"] = (
        df["faixa_etaria"]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------------
    # 6. Agregar por faixa_etaria e Sexo
    # ------------------------------------------------------------

    df_agg = (
        df
        .groupby(
            ["faixa_etaria_tratada", "sexo_tratado"],
            dropna=False,
            as_index=False
        )
        .agg(
            valor_recebido=("valor_transacao", "sum"),
            quantidade_contemplados=("quantidade", "sum")
        )
    )

    # ------------------------------------------------------------
    # 7. Totais gerais
    # ------------------------------------------------------------

    valor_total = df_agg["valor_recebido"].sum()
    quantidade_total = df_agg["quantidade_contemplados"].sum()

    df_agg["perc_valor_total"] = np.where(
        valor_total > 0,
        df_agg["valor_recebido"] / valor_total,
        np.nan
    )

    df_agg["perc_quantidade_total"] = np.where(
        quantidade_total > 0,
        df_agg["quantidade_contemplados"] / quantidade_total,
        np.nan
    )

    # ------------------------------------------------------------
    # 8. Percentuais dentro de cada faixa_etaria
    # ------------------------------------------------------------

    df_agg["valor_total_faixa_etaria"] = (
        df_agg
        .groupby("faixa_etaria_tratada")["valor_recebido"]
        .transform("sum")
    )

    df_agg["quantidade_total_faixa_etaria"] = (
        df_agg
        .groupby("faixa_etaria_tratada")["quantidade_contemplados"]
        .transform("sum")
    )

    df_agg["perc_valor_na_faixa_etaria"] = np.where(
        df_agg["valor_total_faixa_etaria"].ne(0),
        df_agg["valor_recebido"] / df_agg["valor_total_faixa_etaria"],
        np.nan
    )

    df_agg["perc_quantidade_na_faixa_etaria"] = np.where(
        df_agg["quantidade_total_faixa_etaria"].ne(0),
        df_agg["quantidade_contemplados"]
        / df_agg["quantidade_total_faixa_etaria"],
        np.nan
    )

    # ------------------------------------------------------------
    # 9. Formatar valores
    # ------------------------------------------------------------

    colunas_valor = [
        "valor_recebido",
        "valor_total_faixa_etaria"
    ]

    colunas_quantidade = [
        "quantidade_contemplados",
        "quantidade_total_faixa_etaria"
    ]

    df_agg[colunas_valor] = (
        np.ceil(df_agg[colunas_valor])
        .fillna(0)
        .astype("Int64")
    )

    df_agg[colunas_quantidade] = (
        df_agg[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    # ------------------------------------------------------------
    # 10. Renomear e ordenar
    # ------------------------------------------------------------

    df_agg = (
        df_agg
        .rename(columns={
            "faixa_etaria_tratada": "faixa_etaria",
            "sexo_tratado": "Sexo"
        })
        [
            [
                "faixa_etaria",
                "Sexo",
                "valor_recebido",
                "quantidade_contemplados",
                "perc_valor_total",
                "perc_quantidade_total",
                "valor_total_faixa_etaria",
                "quantidade_total_faixa_etaria",
                "perc_valor_na_faixa_etaria",
                "perc_quantidade_na_faixa_etaria",
            ]
        ]
        .sort_values(
            ["faixa_etaria", "Sexo"]
        )
        .reset_index(drop=True)
    )

    return df_agg