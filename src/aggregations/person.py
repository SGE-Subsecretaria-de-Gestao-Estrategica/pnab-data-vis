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
    df_cubo: pd.DataFrame,
    proporcao_aparada: float = 0.99
) -> pd.DataFrame:
    """
    Calcula a proporção da quantidade e do valor de contemplados por Sexo.

    Filtros aplicados:
    - considera apenas registros com tipo_documento == CPF;
    - considera apenas CPFs com Sexo marcado como Masculino ou Feminino.

    Usa:
    - quantidade como contagem de contemplados;
    - valor_transacao como valor executado.

    Também calcula:
    - valor médio geral;
    - valor médio por sexo;
    - valor médio aparado geral;
    - valor médio aparado por sexo.

    Percentuais retornam em escala decimal:
    0.55 = 55%.

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

    df["valor_transacao"] = pd.to_numeric(
        df["valor_transacao"],
        errors="coerce"
    )

    df["quantidade"] = pd.to_numeric(
        df["quantidade"],
        errors="coerce"
    )

    df["valor_medio_linha"] = np.where(
        df["quantidade"].fillna(0).ne(0),
        df["valor_transacao"] / df["quantidade"],
        np.nan
    )

    def calcular_valor_medio_aparado(
        df_base: pd.DataFrame,
        proporcao: float = proporcao_aparada
    ) -> float:
        """
        Calcula média aparada ponderada.

        Remove o 1% superior dos valores médios por linha
        e calcula:

        soma(valor_transacao aparado) / soma(quantidade aparada)
        """

        base = df_base.copy()

        base = base[
            base["valor_medio_linha"].notna()
            & base["valor_transacao"].notna()
            & base["quantidade"].notna()
            & base["quantidade"].gt(0)
        ].copy()

        if base.empty:
            return np.nan

        limite = base["valor_medio_linha"].quantile(proporcao)

        base_aparada = base[
            base["valor_medio_linha"] <= limite
        ].copy()

        if base_aparada.empty:
            return np.nan

        quantidade_aparada = base_aparada["quantidade"].sum()

        if quantidade_aparada == 0:
            return np.nan

        return (
            base_aparada["valor_transacao"].sum()
            / quantidade_aparada
        )

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

    valor_medio_contemplados = (
        valor_contemplados / quantidade_contemplados
        if quantidade_contemplados > 0 else np.nan
    )

    valor_medio_contemplados_feminino = (
        valor_contemplados_feminino / quantidade_contemplados_feminino
        if quantidade_contemplados_feminino > 0 else np.nan
    )

    valor_medio_contemplados_masculino = (
        valor_contemplados_masculino / quantidade_contemplados_masculino
        if quantidade_contemplados_masculino > 0 else np.nan
    )

    valor_medio_aparado_contemplados = calcular_valor_medio_aparado(df)

    valor_medio_aparado_contemplados_feminino = calcular_valor_medio_aparado(
        df[df["sexo_norm"].eq("FEMININO")]
    )

    valor_medio_aparado_contemplados_masculino = calcular_valor_medio_aparado(
        df[df["sexo_norm"].eq("MASCULINO")]
    )

    df_resultado = pd.DataFrame({
        "quantidade_contemplados": [quantidade_contemplados],
        "perc_quantidade_contemplados": [1],

        "valor_contemplados": [valor_contemplados],
        "perc_valor_contemplados": [1],
        "valor_medio_contemplados": [valor_medio_contemplados],
        "valor_medio_aparado_contemplados": [
            valor_medio_aparado_contemplados
        ],

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
        "valor_medio_contemplados_feminino": [
            valor_medio_contemplados_feminino
        ],
        "valor_medio_aparado_contemplados_feminino": [
            valor_medio_aparado_contemplados_feminino
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
        "valor_medio_contemplados_masculino": [
            valor_medio_contemplados_masculino
        ],
        "valor_medio_aparado_contemplados_masculino": [
            valor_medio_aparado_contemplados_masculino
        ],
    })

    colunas_quantidade = [
        "quantidade_contemplados",
        "quantidade_contemplados_feminino",
        "quantidade_contemplados_masculino",
    ]

    colunas_valor = [
        "valor_contemplados",
        "valor_medio_contemplados",
        "valor_medio_aparado_contemplados",

        "valor_contemplados_feminino",
        "valor_medio_contemplados_feminino",
        "valor_medio_aparado_contemplados_feminino",

        "valor_contemplados_masculino",
        "valor_medio_contemplados_masculino",
        "valor_medio_aparado_contemplados_masculino",
    ]

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    return df_resultado




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

def aggregate_cnpj_natureza_juridica_por_regiao(
    df_cubo: pd.DataFrame,
    coluna_regiao: str = "regiao",
    coluna_natureza: str = "naturezajuridica_agrupada_receita_cnpj",
    coluna_valor: str = "valor_transacao",
    coluna_quantidade: str = "quantidade",
    coluna_tipo_documento: str = "tipo_documento"
) -> pd.DataFrame:
    """
    Agrega apenas CNPJs por região e natureza jurídica.

    Para cada região, mostra quanto cada categoria de natureza jurídica representa
    em quantidade de contemplados e em valor recebido.

    Percentuais principais:
    - perc_quantidade_contemplados_na_regiao:
        quantidade da linha / total de quantidade da região da linha

    - perc_valor_contemplados_na_regiao:
        valor da linha / total de valor da região da linha

    Percentuais retornam em escala decimal:
    0.25 = 25%
    """

    required_columns = [
        coluna_regiao,
        coluna_natureza,
        coluna_valor,
        coluna_quantidade,
        coluna_tipo_documento,
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    regioes = [
        "Norte",
        "Nordeste",
        "Centro-Oeste",
        "Sudeste",
        "Sul"
    ]

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

    # ------------------------------------------------------------
    # 1. Considera apenas CNPJ
    # ------------------------------------------------------------
    df = df[df["tipo_documento_norm"].eq("CNPJ")].copy()

    df[coluna_valor] = pd.to_numeric(
        df[coluna_valor],
        errors="coerce"
    ).fillna(0)

    df[coluna_quantidade] = pd.to_numeric(
        df[coluna_quantidade],
        errors="coerce"
    ).fillna(0)

    df[coluna_regiao] = (
        df[coluna_regiao]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    df[coluna_natureza] = (
        df[coluna_natureza]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------------
    # 2. Mantém apenas regiões e naturezas desejadas
    # ------------------------------------------------------------
    df = df[
        df[coluna_regiao].isin(regioes)
        & df[coluna_natureza].isin(categorias_natureza)
    ].copy()

    df[coluna_regiao] = pd.Categorical(
        df[coluna_regiao],
        categories=regioes,
        ordered=True
    )

    df[coluna_natureza] = pd.Categorical(
        df[coluna_natureza],
        categories=categorias_natureza,
        ordered=True
    )

    # ------------------------------------------------------------
    # 3. Agrega por região e natureza jurídica
    # ------------------------------------------------------------
    df_resultado = (
        df
        .groupby([coluna_regiao, coluna_natureza], observed=False)
        .agg(
            quantidade_contemplados=(coluna_quantidade, "sum"),
            valor_contemplados=(coluna_valor, "sum")
        )
        .reset_index()
        .rename(columns={
            coluna_regiao: "regiao",
            coluna_natureza: "natureza_juridica"
        })
    )

    # ------------------------------------------------------------
    # 4. Calcula totais da região da linha
    # ------------------------------------------------------------
    totais_regiao = (
        df_resultado
        .groupby("regiao", observed=False)
        .agg(
            total_quantidade_regiao=("quantidade_contemplados", "sum"),
            total_valor_regiao=("valor_contemplados", "sum")
        )
        .reset_index()
    )

    df_resultado = df_resultado.merge(
        totais_regiao,
        on="regiao",
        how="left"
    )

    # ------------------------------------------------------------
    # 5. Percentuais dentro da região da linha
    # ------------------------------------------------------------
    df_resultado["perc_quantidade_contemplados_na_regiao"] = np.where(
        df_resultado["total_quantidade_regiao"] > 0,
        df_resultado["quantidade_contemplados"]
        / df_resultado["total_quantidade_regiao"],
        np.nan
    )

    df_resultado["perc_valor_contemplados_na_regiao"] = np.where(
        df_resultado["total_valor_regiao"] > 0,
        df_resultado["valor_contemplados"]
        / df_resultado["total_valor_regiao"],
        np.nan
    )

    # Mantém também os nomes antigos, caso você já esteja usando em gráficos
    df_resultado["perc_quantidade_contemplados"] = (
        df_resultado["perc_quantidade_contemplados_na_regiao"]
    )

    df_resultado["perc_valor_contemplados"] = (
        df_resultado["perc_valor_contemplados_na_regiao"]
    )

    # ------------------------------------------------------------
    # 6. Ajustes de tipos
    # ------------------------------------------------------------
    df_resultado["quantidade_contemplados"] = (
        df_resultado["quantidade_contemplados"]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado["total_quantidade_regiao"] = (
        df_resultado["total_quantidade_regiao"]
        .fillna(0)
        .astype("Int64")
    )

    colunas_valor = [
        "valor_contemplados",
        "total_valor_regiao"
    ]

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .fillna(0)
        .astype("Float64")
    )

    colunas_percentual = [
        "perc_quantidade_contemplados_na_regiao",
        "perc_valor_contemplados_na_regiao",
        "perc_quantidade_contemplados",
        "perc_valor_contemplados",
    ]

    df_resultado[colunas_percentual] = (
        df_resultado[colunas_percentual]
        .astype("Float64")
    )

    # ------------------------------------------------------------
    # 7. Ordenação final
    # ------------------------------------------------------------
    df_resultado = (
        df_resultado
        .sort_values(["regiao", "natureza_juridica"])
        .reset_index(drop=True)
    )

    return df_resultado


def top_cnaes_cnpj(
    df_cubo: pd.DataFrame,
    top_n: int = 20,
    apenas_cnae_cultural: bool = True,
    valor_flag_cnae_cultural: str = "CNAE CULTURAL",
    coluna_tipo_documento: str = "tipo_documento",
    coluna_cnae: str = "descr_cnae_principal_receita_cnpj",
    coluna_flag_cnae: str = "flag_cnae_cultural",
    coluna_valor: str = "valor_transacao",
    coluna_quantidade: str = "quantidade"
) -> pd.DataFrame:
    """
    Retorna os top CNAEs de CNPJs que mais receberam recursos.

    Regras:
    - filtra apenas tipo_documento == "CNPJ";
    - se apenas_cnae_cultural=True, mostra apenas CNAEs culturais;
    - se apenas_cnae_cultural=False, mostra CNAEs gerais;
    - os percentuais são SEMPRE calculados em relação ao total de todos os CNAEs de CNPJs,
      e não apenas em relação aos CNAEs culturais.

    Percentuais retornam em escala decimal:
    0.25 = 25%
    """

    def normalizar_texto(valor):
        valor = str(valor).upper().strip()
        valor = unicodedata.normalize("NFKD", valor)
        valor = valor.encode("ascii", errors="ignore").decode("utf-8")
        return valor

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

    # Filtra apenas CNPJ
    df = df[df["tipo_documento_norm"].eq("CNPJ")].copy()

    df[coluna_valor] = pd.to_numeric(
        df[coluna_valor],
        errors="coerce"
    ).fillna(0)

    df[coluna_quantidade] = pd.to_numeric(
        df[coluna_quantidade],
        errors="coerce"
    ).fillna(0)

    df[coluna_cnae] = (
        df[coluna_cnae]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------------
    # Denominador: TODOS os CNAEs de CNPJs
    # ------------------------------------------------------------

    total_quantidade_todos_cnaes = df[coluna_quantidade].sum()
    total_valor_todos_cnaes = df[coluna_valor].sum()

    # ------------------------------------------------------------
    # Filtro opcional: apenas CNAE cultural
    # ------------------------------------------------------------

    if apenas_cnae_cultural:
        df["flag_cnae_norm"] = (
            df[coluna_flag_cnae]
            .fillna("Não informado")
            .astype(str)
            .str.upper()
            .str.strip()
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )

        valor_flag_norm = normalizar_texto(valor_flag_cnae_cultural)

        df = df[df["flag_cnae_norm"].eq(valor_flag_norm)].copy()

    # ------------------------------------------------------------
    # Agregação dos CNAEs exibidos
    # ------------------------------------------------------------

    df_agg = (
        df
        .groupby(coluna_cnae, dropna=False)
        .agg(
            quantidade_contemplados=(coluna_quantidade, "sum"),
            valor_transacao=(coluna_valor, "sum")
        )
        .reset_index()
        .rename(columns={coluna_cnae: "cnae_principal"})
    )

    # Percentuais em relação ao TODO dos CNAEs de CNPJs
    df_agg["perc_quantidade_contemplados"] = np.where(
        total_quantidade_todos_cnaes > 0,
        df_agg["quantidade_contemplados"] / total_quantidade_todos_cnaes,
        np.nan
    )

    df_agg["perc_valor_transacao"] = np.where(
        total_valor_todos_cnaes > 0,
        df_agg["valor_transacao"] / total_valor_todos_cnaes,
        np.nan
    )

    df_resultado = (
        df_agg
        .sort_values("valor_transacao", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    df_resultado.insert(0, "ranking_valor", range(1, len(df_resultado) + 1))

    df_resultado["visao_cnae"] = np.where(
        apenas_cnae_cultural,
        "CNAE cultural",
        "CNAE geral"
    )

    df_resultado["total_quantidade_todos_cnaes"] = total_quantidade_todos_cnaes
    df_resultado["total_valor_todos_cnaes"] = total_valor_todos_cnaes

    df_resultado["quantidade_contemplados"] = (
        df_resultado["quantidade_contemplados"]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado["total_quantidade_todos_cnaes"] = (
        df_resultado["total_quantidade_todos_cnaes"]
        .fillna(0)
        .astype("Int64")
    )

    colunas_valor = [
        "valor_transacao",
        "total_valor_todos_cnaes"
    ]

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .astype("Float64")
    )

    colunas_percentual = [
        "perc_quantidade_contemplados",
        "perc_valor_transacao"
    ]

    df_resultado[colunas_percentual] = (
        df_resultado[colunas_percentual]
        .astype("Float64")
    )

    return df_resultado


def aggregate_vinculo_formal_labor_by_uf(
    df_cubo: pd.DataFrame,
    df_rais_uf: pd.DataFrame,
    col_uf: str = "uf",
    col_vinculo: str = "tipo_vinculo_agregado_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
    col_uf_rais: str = "uf",
    col_qtd_rais: str = "qtd_vinculos_formais_rais_2024",
) -> pd.DataFrame:
    """
    Cria um DataFrame com uma linha por UF, contendo:
    - quantidade de contemplados PNAB com e sem vínculo formal
    - valor pago com e sem vínculo formal
    - percentuais dentro da própria UF
    - participação da UF no total PNAB
    - participação da UF no total PNAB por tipo de vínculo
    - participação da UF no total Brasil da RAIS 2024

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Sem vínculo formal: tipo_vinculo_agregado_rais missing, nulo ou vazio
    - Com vínculo formal: tipo_vinculo_agregado_rais preenchido

    A coluna percentual_vinculos_formais_rais_2024_brasil responde:
    - De todos os vínculos formais da RAIS 2024 no Brasil, quanto está em cada UF.
    """

    required_columns_cubo = [
        "tipo_documento",
        col_uf,
        col_vinculo,
        col_quantidade,
        col_valor,
    ]

    missing_columns_cubo = [
        col for col in required_columns_cubo if col not in df_cubo.columns
    ]

    if missing_columns_cubo:
        raise ValueError(
            f"As seguintes colunas não existem no df_cubo: {missing_columns_cubo}"
        )

    required_columns_rais = [
        col_uf_rais,
        col_qtd_rais,
    ]

    missing_columns_rais = [
        col for col in required_columns_rais if col not in df_rais_uf.columns
    ]

    if missing_columns_rais:
        raise ValueError(
            f"As seguintes colunas não existem no df_rais_uf: {missing_columns_rais}"
        )

    # ------------------------------------------------------------
    # 1. Filtra apenas CPF na PNAB
    # ------------------------------------------------------------
    df = df_cubo.copy()

    df = df.loc[
        df["tipo_documento"].eq("CPF")
    ].copy()

    # ------------------------------------------------------------
    # 2. Classifica vínculo formal na PNAB
    # ------------------------------------------------------------
    vinculo_preenchido = (
        df[col_vinculo].notna()
        & df[col_vinculo].astype(str).str.strip().ne("")
    )

    df["situacao_vinculo_formal"] = "sem_vinculo_trabalho_formal"

    df.loc[
        vinculo_preenchido,
        "situacao_vinculo_formal"
    ] = "com_vinculo_trabalho_formal"

    # ------------------------------------------------------------
    # 3. Agrega PNAB por UF e situação de vínculo
    # ------------------------------------------------------------
    resumo = (
        df
        .groupby([col_uf, "situacao_vinculo_formal"], dropna=False)
        .agg(
            numero_contemplados=(col_quantidade, "sum"),
            valor_pago=(col_valor, "sum"),
        )
        .reset_index()
    )

    tabela = (
        resumo
        .pivot(
            index=col_uf,
            columns="situacao_vinculo_formal",
            values=["numero_contemplados", "valor_pago"],
        )
    )

    tabela.columns = [
        f"{metrica}_{situacao}"
        for metrica, situacao in tabela.columns
    ]

    tabela = tabela.reset_index().fillna(0)

    colunas_esperadas = [
        "numero_contemplados_sem_vinculo_trabalho_formal",
        "numero_contemplados_com_vinculo_trabalho_formal",
        "valor_pago_sem_vinculo_trabalho_formal",
        "valor_pago_com_vinculo_trabalho_formal",
    ]

    for col in colunas_esperadas:
        if col not in tabela.columns:
            tabela[col] = 0

    # ------------------------------------------------------------
    # 4. Totais PNAB por UF
    # ------------------------------------------------------------
    tabela["numero_contemplados_total"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        + tabela["numero_contemplados_com_vinculo_trabalho_formal"]
    )

    tabela["valor_pago_total"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        + tabela["valor_pago_com_vinculo_trabalho_formal"]
    )

    # ------------------------------------------------------------
    # 5. Percentuais PNAB dentro da UF
    # ------------------------------------------------------------
    tabela["percentual_contemplados_sem_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        .div(
            tabela["numero_contemplados_total"]
            .where(tabela["numero_contemplados_total"].ne(0))
        )
        .fillna(0)
    )

    tabela["percentual_contemplados_com_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        .div(
            tabela["numero_contemplados_total"]
            .where(tabela["numero_contemplados_total"].ne(0))
        )
        .fillna(0)
    )

    tabela["percentual_valor_pago_sem_vinculo_trabalho_formal"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        .div(
            tabela["valor_pago_total"]
            .where(tabela["valor_pago_total"].ne(0))
        )
        .fillna(0)
    )

    tabela["percentual_valor_pago_com_vinculo_trabalho_formal"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        .div(
            tabela["valor_pago_total"]
            .where(tabela["valor_pago_total"].ne(0))
        )
        .fillna(0)
    )

    # ------------------------------------------------------------
    # 6. Totais Brasil PNAB
    # ------------------------------------------------------------
    total_numero_contemplados_brasil = tabela["numero_contemplados_total"].sum()
    total_valor_pago_brasil = tabela["valor_pago_total"].sum()

    total_numero_sem_vinculo_brasil = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"].sum()
    )

    total_numero_com_vinculo_brasil = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"].sum()
    )

    total_valor_sem_vinculo_brasil = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"].sum()
    )

    total_valor_com_vinculo_brasil = (
        tabela["valor_pago_com_vinculo_trabalho_formal"].sum()
    )

    # ------------------------------------------------------------
    # 7. Participações PNAB no total Brasil
    # ------------------------------------------------------------
    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"] / total_numero_contemplados_brasil
        if total_numero_contemplados_brasil > 0
        else 0
    )

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"] / total_valor_pago_brasil
        if total_valor_pago_brasil > 0
        else 0
    )

    tabela["percentual_numero_contemplados_sem_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / total_numero_sem_vinculo_brasil
        if total_numero_sem_vinculo_brasil > 0
        else 0
    )

    tabela["percentual_numero_contemplados_com_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / total_numero_com_vinculo_brasil
        if total_numero_com_vinculo_brasil > 0
        else 0
    )

    tabela["percentual_valor_pago_sem_vinculo_no_total_geral"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / total_valor_sem_vinculo_brasil
        if total_valor_sem_vinculo_brasil > 0
        else 0
    )

    tabela["percentual_valor_pago_com_vinculo_no_total_geral"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / total_valor_com_vinculo_brasil
        if total_valor_com_vinculo_brasil > 0
        else 0
    )

    # ------------------------------------------------------------
    # 8. Calcula participação da UF na RAIS 2024 Brasil
    # ------------------------------------------------------------
    df_rais = df_rais_uf[[col_uf_rais, col_qtd_rais]].copy()

    df_rais = df_rais.rename(
        columns={
            col_uf_rais: col_uf,
            col_qtd_rais: "qtd_vinculos_formais_rais_2024",
        }
    )

    total_vinculos_formais_rais_2024_brasil = (
        df_rais["qtd_vinculos_formais_rais_2024"].sum()
    )

    df_rais["percentual_vinculos_formais_rais_2024_brasil"] = (
        df_rais["qtd_vinculos_formais_rais_2024"]
        / total_vinculos_formais_rais_2024_brasil
        if total_vinculos_formais_rais_2024_brasil > 0
        else 0
    )

    # ------------------------------------------------------------
    # 9. Junta RAIS 2024 na tabela PNAB
    # ------------------------------------------------------------
    tabela = tabela.merge(
        df_rais,
        on=col_uf,
        how="left"
    )

    tabela[
        [
            "qtd_vinculos_formais_rais_2024",
            "percentual_vinculos_formais_rais_2024_brasil",
        ]
    ] = tabela[
        [
            "qtd_vinculos_formais_rais_2024",
            "percentual_vinculos_formais_rais_2024_brasil",
        ]
    ].fillna(0)

    # ------------------------------------------------------------
    # 10. Ordem final das colunas
    # ------------------------------------------------------------
    colunas_finais = [
        col_uf,

        "numero_contemplados_sem_vinculo_trabalho_formal",
        "numero_contemplados_com_vinculo_trabalho_formal",
        "numero_contemplados_total",

        "percentual_contemplados_sem_vinculo_trabalho_formal",
        "percentual_contemplados_com_vinculo_trabalho_formal",
        "percentual_numero_contemplados_no_total_geral",
        "percentual_numero_contemplados_sem_vinculo_no_total_geral",
        "percentual_numero_contemplados_com_vinculo_no_total_geral",

        "qtd_vinculos_formais_rais_2024",
        "percentual_vinculos_formais_rais_2024_brasil",

        "valor_pago_sem_vinculo_trabalho_formal",
        "valor_pago_com_vinculo_trabalho_formal",
        "valor_pago_total",

        "percentual_valor_pago_sem_vinculo_trabalho_formal",
        "percentual_valor_pago_com_vinculo_trabalho_formal",
        "percentual_valor_pago_no_total_geral",
        "percentual_valor_pago_sem_vinculo_no_total_geral",
        "percentual_valor_pago_com_vinculo_no_total_geral",
    ]

    return (
        tabela[colunas_finais]
        .sort_values(col_uf)
        .reset_index(drop=True)
    )


def make_df_media_aparada_sexo_capitais_cpf(
    df_cubo: pd.DataFrame,
    col_tipo_documento: str = "tipo_documento",
    col_sexo: str = "Sexo",
    col_flag_capital: str = "flag_capital",
    col_valor: str = "valor_transacao",
    col_quantidade: str = "quantidade",
    proporcao_aparada: float = 0.99
) -> pd.DataFrame:
    """
    Retorna um DataFrame com valor médio e média aparada por Sexo,
    considerando apenas:
    - tipo_documento == CPF;
    - flag_capital == True;
    - Sexo igual a Masculino ou Feminino.

    A média simples é calculada como:
    soma(valor_transacao) / soma(quantidade)

    A média aparada remove o 1% superior dos valores médios por linha,
    dentro de cada Sexo, e depois recalcula:
    soma(valor_transacao aparado) / soma(quantidade aparada)
    """

    df = df_cubo.copy()

    # ------------------------------------------------------------
    # 1. Normalizações
    # ------------------------------------------------------------

    df["tipo_documento_norm"] = (
        df[col_tipo_documento]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
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

    df["sexo_tratado"] = df["sexo_norm"].map({
        "FEMININO": "Feminino",
        "MASCULINO": "Masculino"
    })

    df[col_valor] = pd.to_numeric(df[col_valor], errors="coerce")
    df[col_quantidade] = pd.to_numeric(df[col_quantidade], errors="coerce")

    # ------------------------------------------------------------
    # 2. Filtros: CPF + capitais + sexo válido
    # ------------------------------------------------------------

    df = df[
        df["tipo_documento_norm"].eq("CPF")
        & df[col_flag_capital].eq(True)
        & df["sexo_tratado"].isin(["Feminino", "Masculino"])
    ].copy()

    # ------------------------------------------------------------
    # 3. Valor médio por linha
    # ------------------------------------------------------------

    df["valor_medio_linha"] = np.where(
        df[col_quantidade].fillna(0).ne(0),
        df[col_valor] / df[col_quantidade],
        np.nan
    )

    # ------------------------------------------------------------
    # 4. Função auxiliar: média aparada ponderada
    # ------------------------------------------------------------

    def calcular_media_aparada(grupo: pd.DataFrame) -> float:
        grupo = grupo[
            grupo["valor_medio_linha"].notna()
            & grupo[col_valor].notna()
            & grupo[col_quantidade].notna()
            & grupo[col_quantidade].gt(0)
        ].copy()

        if grupo.empty:
            return np.nan

        limite = grupo["valor_medio_linha"].quantile(proporcao_aparada)

        grupo_aparado = grupo[
            grupo["valor_medio_linha"] <= limite
        ].copy()

        if grupo_aparado.empty:
            return np.nan

        qtd_aparada = grupo_aparado[col_quantidade].sum()

        if qtd_aparada == 0:
            return np.nan

        return grupo_aparado[col_valor].sum() / qtd_aparada

    # ------------------------------------------------------------
    # 5. Agregação final por sexo
    # ------------------------------------------------------------

    df_resultado = (
        df
        .groupby("sexo_tratado", as_index=False)
        .agg(
            quantidade_contemplados=(col_quantidade, "sum"),
            valor_contemplados=(col_valor, "sum")
        )
        .rename(columns={"sexo_tratado": "Sexo"})
    )

    df_resultado["valor_medio"] = np.where(
        df_resultado["quantidade_contemplados"].fillna(0).ne(0),
        df_resultado["valor_contemplados"] / df_resultado["quantidade_contemplados"],
        np.nan
    )

    df_media_aparada = (
        df
        .groupby("sexo_tratado")
        .apply(calcular_media_aparada)
        .reset_index(name="valor_medio_aparado")
        .rename(columns={"sexo_tratado": "Sexo"})
    )

    df_resultado = df_resultado.merge(
        df_media_aparada,
        on="Sexo",
        how="left"
    )

    # ------------------------------------------------------------
    # 6. Tipagem
    # ------------------------------------------------------------

    df_resultado["quantidade_contemplados"] = (
        df_resultado["quantidade_contemplados"]
        .fillna(0)
        .astype("Int64")
    )

    colunas_valor = [
        "valor_contemplados",
        "valor_medio",
        "valor_medio_aparado"
    ]

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    df_resultado = (
        df_resultado
        .sort_values("Sexo")
        .reset_index(drop=True)
    )

    return df_resultado