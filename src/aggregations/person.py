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