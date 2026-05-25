import pandas as pd
import numpy as np


import numpy as np
import pandas as pd


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