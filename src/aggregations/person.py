import pandas as pd
import numpy as np
import re
import unicodedata
from pathlib import Path


def aggregate_contemplados_pf_pj_proportion(
    df_cubo: pd.DataFrame,
    coluna_valor: str = "valor_transacao",
    by_filter: str = 'UF'
) -> pd.DataFrame:
    """
    Calcula a proporção entre quantidade e valor recebido por
    pessoas físicas e pessoas jurídicas.

    Usa:
    - CPF como pessoa física;
    - CNPJ como pessoa jurídica;
    - quantidade como coluna de contagem de contemplados;
    - valor_transacao como coluna de valor, por padrão.

    Retorna uma tabela com uma linha.
    """

    def media_aparada_1pct_superior(x):
        """
        Calcula a média removendo os 1% maiores valores do grupo.
        """
        x = pd.to_numeric(x, errors="coerce").dropna()

        if x.empty:
            return np.nan

        limite_superior = x.quantile(0.99)

        return x[x <= limite_superior].mean()

    df = df_cubo.copy()

    if by_filter == 'ESTADO':
        df = df[df['tipo_ente'] == 'ESTADO']
    elif by_filter == 'MUNICIPIO':
        df = df[df['tipo_ente'] == 'MUNICIPIO']
    else:
        df = df.copy()

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

    df[coluna_valor] = pd.to_numeric(
        df[coluna_valor],
        errors="coerce"
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

    valor_contemplados = df[coluna_valor].sum()

    valor_contemplados_pf = (
        df
        .loc[df["tipo_documento_norm"].eq("CPF"), coluna_valor]
        .sum()
    )

    valor_contemplados_pj = (
        df
        .loc[df["tipo_documento_norm"].eq("CNPJ"), coluna_valor]
        .sum()
    )

    valor_medio_contemplados_pf = (
        valor_contemplados_pf / quantidade_contemplados_pf
        if quantidade_contemplados_pf > 0 else np.nan
    )

    valor_medio_contemplados_pj = (
        valor_contemplados_pj / quantidade_contemplados_pj
        if quantidade_contemplados_pj > 0 else np.nan
    )

    media_aparada_1pct_valor_pf = media_aparada_1pct_superior(
        df.loc[df["tipo_documento_norm"].eq("CPF"), coluna_valor]
    )

    media_aparada_1pct_valor_pj = media_aparada_1pct_superior(
        df.loc[df["tipo_documento_norm"].eq("CNPJ"), coluna_valor]
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

        "valor_contemplados": [valor_contemplados],
        "perc_valor_contemplados": [1],

        "valor_contemplados_pf": [valor_contemplados_pf],
        "perc_valor_contemplados_pf": [
            valor_contemplados_pf / valor_contemplados
            if valor_contemplados > 0 else np.nan
        ],

        "valor_contemplados_pj": [valor_contemplados_pj],
        "perc_valor_contemplados_pj": [
            valor_contemplados_pj / valor_contemplados
            if valor_contemplados > 0 else np.nan
        ],

        "valor_medio_contemplados_pf": [valor_medio_contemplados_pf],
        "media_aparada_1pct_valor_pf": [media_aparada_1pct_valor_pf],

        "valor_medio_contemplados_pj": [valor_medio_contemplados_pj],
        "media_aparada_1pct_valor_pj": [media_aparada_1pct_valor_pj],
    })

    colunas_quantidade = [
        "quantidade_contemplados",
        "quantidade_contemplados_pf",
        "quantidade_contemplados_pj",
    ]

    colunas_valor = [
        "valor_contemplados",
        "valor_contemplados_pf",
        "valor_contemplados_pj",
        "valor_medio_contemplados_pf",
        "media_aparada_1pct_valor_pf",
        "valor_medio_contemplados_pj",
        "media_aparada_1pct_valor_pj",
    ]

    colunas_percentual = [
        "perc_quantidade_contemplados",
        "perc_quantidade_contemplados_pf",
        "perc_quantidade_contemplados_pj",
        "perc_valor_contemplados",
        "perc_valor_contemplados_pf",
        "perc_valor_contemplados_pj",
    ]

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .fillna(0)
        .astype("Float64")
    )

    df_resultado[colunas_percentual] = (
        df_resultado[colunas_percentual]
        .astype("Float64")
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




def aggregate_cnpj_mei_proportion(
    df_cubo: pd.DataFrame,
    coluna_valor: str = "valor_transacao",
    coluna_quantidade: str = "quantidade",
    coluna_tipo_documento: str = "tipo_documento",
    coluna_mei: str = "cnpj_optante_mei",
    by_filter: str = "UF"
) -> pd.DataFrame:
    """
    Calcula, apenas entre CNPJs, a proporção de MEIs em quantidade de contemplados
    e em valor recebido.

    Regra:
    - Considera apenas tipo_documento == "CNPJ"
    - Considera MEI quando cnpj_optante_mei == 1

    Retorna:
    - quantidade de CNPJs contemplados
    - quantidade de MEIs contemplados
    - quantidade de não MEIs contemplados
    - valor recebido por CNPJs
    - valor recebido por MEIs
    - valor recebido por não MEIs
    - percentuais de quantidade e valor
    - valor médio
    - média aparada de 1%, removendo os maiores 1% valores

    Percentuais retornam em escala decimal:
    - 0.25 = 25%
    """

    def media_aparada_1pct_superior(x):
        """
        Calcula a média removendo os 1% maiores valores do grupo.
        """
        x = pd.to_numeric(x, errors="coerce").dropna()

        if x.empty:
            return np.nan

        limite_superior = x.quantile(0.99)

        return x[x <= limite_superior].mean()

    df = df_cubo.copy()

    if by_filter == 'ESTADO':
        df = df[df['tipo_ente'] == 'ESTADO']
    elif by_filter == 'MUNICIPIO':
        df = df[df['tipo_ente'] == 'MUNICIPIO']
    else:
        df = df.copy()

    df["tipo_documento_norm"] = (
        df[coluna_tipo_documento]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df = df[df["tipo_documento_norm"].eq("CNPJ")].copy()

    df[coluna_valor] = pd.to_numeric(
        df[coluna_valor],
        errors="coerce"
    ).fillna(0)

    df[coluna_quantidade] = pd.to_numeric(
        df[coluna_quantidade],
        errors="coerce"
    ).fillna(0)

    df["is_mei"] = df[coluna_mei].eq(1)

    quantidade_contemplados_cnpj = df[coluna_quantidade].sum()

    quantidade_contemplados_mei = (
        df
        .loc[df["is_mei"], coluna_quantidade]
        .sum()
    )

    quantidade_contemplados_nao_mei = (
        df
        .loc[~df["is_mei"], coluna_quantidade]
        .sum()
    )

    valor_contemplados_cnpj = df[coluna_valor].sum()

    valor_contemplados_mei = (
        df
        .loc[df["is_mei"], coluna_valor]
        .sum()
    )

    valor_contemplados_nao_mei = (
        df
        .loc[~df["is_mei"], coluna_valor]
        .sum()
    )

    valor_medio_contemplados_cnpj = (
        valor_contemplados_cnpj / quantidade_contemplados_cnpj
        if quantidade_contemplados_cnpj > 0 else np.nan
    )

    valor_medio_contemplados_mei = (
        valor_contemplados_mei / quantidade_contemplados_mei
        if quantidade_contemplados_mei > 0 else np.nan
    )

    valor_medio_contemplados_nao_mei = (
        valor_contemplados_nao_mei / quantidade_contemplados_nao_mei
        if quantidade_contemplados_nao_mei > 0 else np.nan
    )

    media_aparada_1pct_valor_cnpj = media_aparada_1pct_superior(
        df[coluna_valor]
    )

    media_aparada_1pct_valor_mei = media_aparada_1pct_superior(
        df.loc[df["is_mei"], coluna_valor]
    )

    media_aparada_1pct_valor_nao_mei = media_aparada_1pct_superior(
        df.loc[~df["is_mei"], coluna_valor]
    )

    df_resultado = pd.DataFrame({
        "quantidade_contemplados_cnpj": [quantidade_contemplados_cnpj],
        "perc_quantidade_contemplados_cnpj": [1],

        "quantidade_contemplados_mei": [quantidade_contemplados_mei],
        "perc_quantidade_contemplados_mei": [
            quantidade_contemplados_mei / quantidade_contemplados_cnpj
            if quantidade_contemplados_cnpj > 0 else np.nan
        ],

        "quantidade_contemplados_nao_mei": [quantidade_contemplados_nao_mei],
        "perc_quantidade_contemplados_nao_mei": [
            quantidade_contemplados_nao_mei / quantidade_contemplados_cnpj
            if quantidade_contemplados_cnpj > 0 else np.nan
        ],

        "valor_contemplados_cnpj": [valor_contemplados_cnpj],
        "perc_valor_contemplados_cnpj": [1],

        "valor_contemplados_mei": [valor_contemplados_mei],
        "perc_valor_contemplados_mei": [
            valor_contemplados_mei / valor_contemplados_cnpj
            if valor_contemplados_cnpj > 0 else np.nan
        ],

        "valor_contemplados_nao_mei": [valor_contemplados_nao_mei],
        "perc_valor_contemplados_nao_mei": [
            valor_contemplados_nao_mei / valor_contemplados_cnpj
            if valor_contemplados_cnpj > 0 else np.nan
        ],

        "valor_medio_contemplados_cnpj": [valor_medio_contemplados_cnpj],
        "valor_medio_contemplados_mei": [valor_medio_contemplados_mei],
        "valor_medio_contemplados_nao_mei": [valor_medio_contemplados_nao_mei],

        "media_aparada_1pct_valor_cnpj": [media_aparada_1pct_valor_cnpj],
        "media_aparada_1pct_valor_mei": [media_aparada_1pct_valor_mei],
        "media_aparada_1pct_valor_nao_mei": [media_aparada_1pct_valor_nao_mei],
    })

    colunas_quantidade = [
        "quantidade_contemplados_cnpj",
        "quantidade_contemplados_mei",
        "quantidade_contemplados_nao_mei",
    ]

    colunas_valor = [
        "valor_contemplados_cnpj",
        "valor_contemplados_mei",
        "valor_contemplados_nao_mei",
        "valor_medio_contemplados_cnpj",
        "valor_medio_contemplados_mei",
        "valor_medio_contemplados_nao_mei",
        "media_aparada_1pct_valor_cnpj",
        "media_aparada_1pct_valor_mei",
        "media_aparada_1pct_valor_nao_mei",
    ]

    colunas_percentual = [
        "perc_quantidade_contemplados_cnpj",
        "perc_quantidade_contemplados_mei",
        "perc_quantidade_contemplados_nao_mei",
        "perc_valor_contemplados_cnpj",
        "perc_valor_contemplados_mei",
        "perc_valor_contemplados_nao_mei",
    ]

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .fillna(0)
        .astype("Float64")
    )

    df_resultado[colunas_percentual] = (
        df_resultado[colunas_percentual]
        .astype("Float64")
    )

    return df_resultado

import pandas as pd
import numpy as np

def aggregate_sexo_uf_ibge_pnab(
    df_cubo: pd.DataFrame,
    col_uf: str = "uf",
    col_sexo: str = "Sexo",
    col_tipo_documento: str = "tipo_documento",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Retorna uma tabela por UF comparando:

    - proporção masculina e feminina da população residente segundo IBGE 2022;
    - quantidade de contemplados masculinos e femininos;
    - percentual de contemplados masculinos e femininos dentro da UF;
    - valor recebido por masculinos e femininos;
    - percentual do valor recebido por masculinos e femininos dentro da UF.

    Regras:
    - considera apenas tipo_documento == 'CPF';
    - considera apenas Sexo == Masculino ou Feminino/Femenino;
    - percentuais da PNAB retornam em escala decimal:
      0.52 = 52%;
    - percentuais do IBGE também são convertidos para escala decimal.
    """

    df_ibge_sexo_uf = pd.DataFrame({
        "uf": [
            "RJ", "DF", "PE", "SE", "AL", "SP", "PB", "RS", "BA",
            "RN", "CE", "PR", "MG", "ES", "PI", "MA", "GO", "MS",
            "SC", "AP", "RO", "AM", "PA", "AC", "TO", "RR", "MT"
        ],
        "perc_ibge_masculino": [
            47.2, 47.7, 47.7, 47.9, 47.9, 48.2, 48.3, 48.3, 48.3,
            48.4, 48.4, 48.7, 48.8, 48.8, 48.9, 49.1, 49.1, 49.2,
            49.3, 49.7, 49.8, 49.9, 49.9, 50.0, 50.1, 50.3, 50.3
        ],
        "perc_ibge_feminino": [
            52.8, 52.3, 52.3, 52.1, 52.1, 51.8, 51.7, 51.7, 51.7,
            51.6, 51.6, 51.3, 51.2, 51.2, 51.1, 50.9, 50.9, 50.8,
            50.7, 50.3, 50.2, 50.1, 50.1, 50.0, 49.9, 49.7, 49.7
        ]
    })

    # Converte IBGE para escala decimal
    df_ibge_sexo_uf["perc_ibge_masculino"] = (
        df_ibge_sexo_uf["perc_ibge_masculino"] / 100
    )

    df_ibge_sexo_uf["perc_ibge_feminino"] = (
        df_ibge_sexo_uf["perc_ibge_feminino"] / 100
    )

    df = df_cubo.copy()

    df[col_uf] = (
        df[col_uf]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["tipo_documento_norm"] = (
        df[col_tipo_documento]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["sexo_norm"] = (
        df[col_sexo]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df["sexo_norm"] = df["sexo_norm"].replace({
        "FEMENINO": "FEMININO"
    })

    df = df[
        (df["tipo_documento_norm"].eq("CPF")) &
        (df["sexo_norm"].isin(["MASCULINO", "FEMININO"]))
    ].copy()

    df[col_quantidade] = pd.to_numeric(
        df[col_quantidade],
        errors="coerce"
    ).fillna(0)

    df[col_valor] = pd.to_numeric(
        df[col_valor],
        errors="coerce"
    ).fillna(0)

    df_agg = (
        df
        .groupby([col_uf, "sexo_norm"], as_index=False)
        .agg(
            quantidade_contemplados=(col_quantidade, "sum"),
            valor_recebido=(col_valor, "sum")
        )
    )

    df_qtd = (
        df_agg
        .pivot_table(
            index=col_uf,
            columns="sexo_norm",
            values="quantidade_contemplados",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    df_valor = (
        df_agg
        .pivot_table(
            index=col_uf,
            columns="sexo_norm",
            values="valor_recebido",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    df_resultado = df_qtd.merge(
        df_valor,
        on=col_uf,
        how="outer",
        suffixes=("_qtd", "_valor")
    )

    colunas_esperadas = [
        "MASCULINO_qtd",
        "FEMININO_qtd",
        "MASCULINO_valor",
        "FEMININO_valor"
    ]

    for coluna in colunas_esperadas:
        if coluna not in df_resultado.columns:
            df_resultado[coluna] = 0

    df_resultado = df_resultado.rename(columns={
        col_uf: "uf",
        "MASCULINO_qtd": "quantidade_contemplados_masculino",
        "FEMININO_qtd": "quantidade_contemplados_feminino",
        "MASCULINO_valor": "valor_masculino",
        "FEMININO_valor": "valor_feminino",
    })

    df_resultado["quantidade_contemplados_total"] = (
        df_resultado["quantidade_contemplados_masculino"] +
        df_resultado["quantidade_contemplados_feminino"]
    )

    df_resultado["valor_total"] = (
        df_resultado["valor_masculino"] +
        df_resultado["valor_feminino"]
    )

    df_resultado["perc_quantidade_contemplados_masculino"] = np.where(
        df_resultado["quantidade_contemplados_total"] > 0,
        df_resultado["quantidade_contemplados_masculino"] /
        df_resultado["quantidade_contemplados_total"],
        np.nan
    )

    df_resultado["perc_quantidade_contemplados_feminino"] = np.where(
        df_resultado["quantidade_contemplados_total"] > 0,
        df_resultado["quantidade_contemplados_feminino"] /
        df_resultado["quantidade_contemplados_total"],
        np.nan
    )

    df_resultado["perc_valor_masculino"] = np.where(
        df_resultado["valor_total"] > 0,
        df_resultado["valor_masculino"] / df_resultado["valor_total"],
        np.nan
    )

    df_resultado["perc_valor_feminino"] = np.where(
        df_resultado["valor_total"] > 0,
        df_resultado["valor_feminino"] / df_resultado["valor_total"],
        np.nan
    )

    df_resultado = df_resultado.merge(
        df_ibge_sexo_uf,
        on="uf",
        how="left"
    )

    df_resultado = df_resultado[
        [
            "uf",

            "perc_ibge_masculino",
            "perc_ibge_feminino",

            "quantidade_contemplados_total",
            "quantidade_contemplados_masculino",
            "perc_quantidade_contemplados_masculino",
            "quantidade_contemplados_feminino",
            "perc_quantidade_contemplados_feminino",

            "valor_total",
            "valor_masculino",
            "perc_valor_masculino",
            "valor_feminino",
            "perc_valor_feminino",
        ]
    ]

    colunas_quantidade = [
        "quantidade_contemplados_total",
        "quantidade_contemplados_masculino",
        "quantidade_contemplados_feminino"
    ]

    colunas_valor = [
        "valor_total",
        "valor_masculino",
        "valor_feminino"
    ]

    colunas_percentual = [
        "perc_ibge_masculino",
        "perc_ibge_feminino",
        "perc_quantidade_contemplados_masculino",
        "perc_quantidade_contemplados_feminino",
        "perc_valor_masculino",
        "perc_valor_feminino"
    ]

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .fillna(0)
        .astype("Float64")
    )

    df_resultado[colunas_percentual] = (
        df_resultado[colunas_percentual]
        .astype("Float64")
    )

    df_resultado = (
        df_resultado
        .sort_values("uf")
        .reset_index(drop=True)
    )

    return df_resultado


def aggregate_cnpj_natureza_juridica(
    df_cubo: pd.DataFrame,
    coluna_natureza: str = "naturezajuridica_agrupada_receita_cnpj",
    coluna_valor: str = "valor_transacao",
    coluna_quantidade: str = "quantidade",
    coluna_tipo_documento: str = "tipo_documento"
) -> pd.DataFrame:
    """
    Agrega apenas CNPJs por natureza jurídica agrupada.

    Para cada categoria, retorna:
    - quantidade de contemplados;
    - percentual da quantidade sobre o total de CNPJs;
    - valor recebido;
    - percentual do valor sobre o total de CNPJs.

    Percentuais retornam em escala decimal:
    0.25 = 25%
    """

    categorias_natureza = [
        "Microempresa-ME",
        "MEI",
        "Empresa de Pequeno Porte (EPP)",
        "Administração Pública",
        "Entidades sem fins lucrativos",
        "Entidades Empresariais",
    ]

    df = df_cubo.copy()

    df["tipo_documento_norm"] = (
        df[coluna_tipo_documento]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df = df[df["tipo_documento_norm"].eq("CNPJ")].copy()

    df[coluna_valor] = pd.to_numeric(
        df[coluna_valor],
        errors="coerce"
    ).fillna(0)

    df[coluna_quantidade] = pd.to_numeric(
        df[coluna_quantidade],
        errors="coerce"
    ).fillna(0)

    df[coluna_natureza] = (
        df[coluna_natureza]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    df = df[df[coluna_natureza].isin(categorias_natureza)].copy()

    df[coluna_natureza] = pd.Categorical(
        df[coluna_natureza],
        categories=categorias_natureza,
        ordered=True
    )

    df_resultado = (
        df
        .groupby(coluna_natureza, observed=False)
        .agg(
            quantidade_contemplados=(coluna_quantidade, "sum"),
            valor_contemplados=(coluna_valor, "sum")
        )
        .reset_index()
        .rename(columns={coluna_natureza: "natureza_juridica"})
    )

    total_quantidade = df_resultado["quantidade_contemplados"].sum()
    total_valor = df_resultado["valor_contemplados"].sum()

    df_resultado["perc_quantidade_contemplados"] = np.where(
        total_quantidade > 0,
        df_resultado["quantidade_contemplados"] / total_quantidade,
        np.nan
    )

    df_resultado["perc_valor_contemplados"] = np.where(
        total_valor > 0,
        df_resultado["valor_contemplados"] / total_valor,
        np.nan
    )

    df_resultado["quantidade_contemplados"] = (
        df_resultado["quantidade_contemplados"]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado["valor_contemplados"] = (
        df_resultado["valor_contemplados"]
        .fillna(0)
        .astype("Float64")
    )

    df_resultado["perc_quantidade_contemplados"] = (
        df_resultado["perc_quantidade_contemplados"]
        .astype("Float64")
    )

    df_resultado["perc_valor_contemplados"] = (
        df_resultado["perc_valor_contemplados"]
        .astype("Float64")
    )

    df_resultado = (
        df_resultado
        .sort_values("natureza_juridica")
        .reset_index(drop=True)
    )

    return df_resultado