import pandas as pd
import numpy as np

import numpy as np
import pandas as pd


def executed_value_n_contemplados_qty_by(df_cubo, by_filter):
    """
    Recebe df_cubo e agrega valores e quantidade de contemplados por:
    - ESTADO
    - MUNICIPIO
    - UF, considerando ESTADO + MUNICIPIO nos valores executados.

    Para by_filter == 'UF', a população de referência é a população do ESTADO.

    Inclui:
    - valor executado total;
    - quantidade de contemplados;
    - população;
    - percentual de contemplados pela população;
    - valor executado per capita;
    - estatísticas de valor: mínimo, mediana, máximo e média;
    - quantidade de contemplados por faixa de valor;
    - valores e quantidades por zona urbana/rural.
    """

    by_filter = by_filter.upper()

    if by_filter == "ESTADO":
        df = df_cubo[df_cubo["tipo_ente"] == "ESTADO"].copy()

        df_populacao = (
            df
            .groupby("uf", as_index=False)
            .agg(sum_populacao=("sum_populacao", "max"))
        )

    elif by_filter == "MUNICIPIO":
        df = df_cubo[df_cubo["tipo_ente"] == "MUNICIPIO"].copy()

        df_populacao = (
            df
            .groupby("uf", as_index=False)
            .agg(sum_populacao=("sum_populacao", "max"))
        )

    elif by_filter == "UF":
        # Aqui entram valores de ESTADO + MUNICIPIO
        df = df_cubo.copy()

        # Mas a população de referência vem somente do ESTADO
        df_populacao = (
            df_cubo
            .loc[df_cubo["tipo_ente"] == "ESTADO"]
            .groupby("uf", as_index=False)
            .agg(sum_populacao=("sum_populacao", "max"))
        )

    else:
        raise ValueError("by_filter deve ser 'ESTADO', 'MUNICIPIO' ou 'UF'.")

    # ------------------------------------------------------------
    # Normalizar coluna SITUACAO
    # ------------------------------------------------------------

    df["situacao_norm"] = (
        df["SITUACAO"]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    mask_urbano = df["situacao_norm"].isin(["URBANA", "URBANO"])
    mask_rural = df["situacao_norm"].isin(["RURAL"])

    # ------------------------------------------------------------
    # Criar colunas auxiliares de valor e quantidade
    # ------------------------------------------------------------

    df["valor_urbano"] = np.where(
        mask_urbano,
        df["valor_transacao"],
        0
    )

    df["valor_rural"] = np.where(
        mask_rural,
        df["valor_transacao"],
        0
    )

    df["qtde_urbano"] = np.where(
        mask_urbano,
        df["quantidade"],
        0
    )

    df["qtde_rural"] = np.where(
        mask_rural,
        df["quantidade"],
        0
    )

    # ------------------------------------------------------------
    # Tabela principal por UF
    # ------------------------------------------------------------

    df_tabela_uf = (
        df
        .groupby("uf", as_index=False)
        .agg(
            valor_executado_rs=("valor_transacao", "sum"),
            qtde_contemplados=("quantidade", "sum"),
            valor_urbano=("valor_urbano", "sum"),
            valor_rural=("valor_rural", "sum"),
            qtde_urbano=("qtde_urbano", "sum"),
            qtde_rural=("qtde_rural", "sum"),
            min_valor=("valor_transacao", "min"),
            mediana_valor=("valor_transacao", "median"),
            max_valor=("valor_transacao", "max"),
            media_valor=("valor_transacao", "mean")
        )
    )

    df_tabela_uf = df_tabela_uf.merge(
        df_populacao,
        on="uf",
        how="left"
    )

    # ------------------------------------------------------------
    # Percentuais gerais
    # ------------------------------------------------------------

    df_tabela_uf["valor_executado_perc"] = (
        df_tabela_uf["valor_executado_rs"]
        / df_tabela_uf["valor_executado_rs"].sum()
    )

    df_tabela_uf["perc_contemplados_populacao"] = (
        df_tabela_uf["qtde_contemplados"]
        / df_tabela_uf["sum_populacao"]
    )

    df_tabela_uf["valor_executado_percapita"] = (
        df_tabela_uf["valor_executado_rs"]
        / df_tabela_uf["sum_populacao"]
    )

    # ------------------------------------------------------------
    # Percentuais urbano/rural dentro da UF
    # ------------------------------------------------------------

    df_tabela_uf["perc_valor_urbano"] = np.where(
        df_tabela_uf["valor_executado_rs"].ne(0),
        df_tabela_uf["valor_urbano"] / df_tabela_uf["valor_executado_rs"],
        np.nan
    )

    df_tabela_uf["perc_valor_rural"] = np.where(
        df_tabela_uf["valor_executado_rs"].ne(0),
        df_tabela_uf["valor_rural"] / df_tabela_uf["valor_executado_rs"],
        np.nan
    )

    df_tabela_uf["perc_qtde_urbano"] = np.where(
        df_tabela_uf["qtde_contemplados"].ne(0),
        df_tabela_uf["qtde_urbano"] / df_tabela_uf["qtde_contemplados"],
        np.nan
    )

    df_tabela_uf["perc_qtde_rural"] = np.where(
        df_tabela_uf["qtde_contemplados"].ne(0),
        df_tabela_uf["qtde_rural"] / df_tabela_uf["qtde_contemplados"],
        np.nan
    )

    # ------------------------------------------------------------
    # Quantidade por faixa de valor
    # ------------------------------------------------------------

    df_exec_uf_faixa_vlr = (
        df
        .pivot_table(
            index="uf",
            columns="faixa_vlr_pago",
            values="quantidade",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    df_final = df_tabela_uf.merge(
        right=df_exec_uf_faixa_vlr,
        on="uf",
        how="left"
    )

    return df_final


def aggregate_capital_interior_summary(
    df_cubo: pd.DataFrame
) -> pd.DataFrame:
    """
    Gera resumo agregado de valor e quantidade para capitais e interior.

    Considera apenas registros de MUNICIPIO.
    Divide os municípios entre:
    - capital
    - interior

    Retorna uma tabela com uma linha.
    """

    tipo_ente_normalizado = (
        df_cubo["tipo_ente"]
        .astype(str)
        .str.upper()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df_municipios = df_cubo[
        tipo_ente_normalizado.eq("MUNICIPIO")
    ].copy()

    flag_capital_normalizada = (
        df_municipios["flag_capital"]
        .astype(str)
        .str.upper()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df_capital = df_municipios[
        flag_capital_normalizada.isin(["TRUE", "1", "SIM", "S"])
    ].copy()

    df_interior = df_municipios[
        ~flag_capital_normalizada.isin(["TRUE", "1", "SIM", "S"])
    ].copy()

    valor_total_capital = df_capital["valor_transacao"].sum()
    quantidade_total_capital = df_capital["quantidade"].sum()

    valor_total_interior = df_interior["valor_transacao"].sum()
    quantidade_total_interior = df_interior["quantidade"].sum()

    valor_total_geral = valor_total_capital + valor_total_interior
    quantidade_total_geral = quantidade_total_capital + quantidade_total_interior

    df_resultado = pd.DataFrame({
        "valor_total_capital": [valor_total_capital],
        "quantidade_total_capital": [quantidade_total_capital],
        "percentual_valor_capital": [
            valor_total_capital / valor_total_geral * 100
        ],
        "percentual_quantidade_capital": [
            quantidade_total_capital / quantidade_total_geral * 100
        ],
        "valor_total_interior": [valor_total_interior],
        "quantidade_total_interior": [quantidade_total_interior],
        "percentual_valor_interior": [
            valor_total_interior / valor_total_geral * 100
        ],
        "percentual_quantidade_interior": [
            quantidade_total_interior / quantidade_total_geral * 100
        ]
    })

    colunas_valor = [
        "valor_total_capital",
        "valor_total_interior"
    ]

    colunas_quantidade = [
        "quantidade_total_capital",
        "quantidade_total_interior"
    ]

    colunas_percentual = [
        "percentual_valor_capital",
        "percentual_quantidade_capital",
        "percentual_valor_interior",
        "percentual_quantidade_interior"
    ]

    df_resultado[colunas_valor] = (
        np.ceil(df_resultado[colunas_valor])
        .astype("Int64")
    )

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .astype("Int64")
    )

    df_resultado[colunas_percentual] = (
        df_resultado[colunas_percentual]
        .round(2)
    )

    return df_resultado


def aggregate_execution_by_porte_with_estado(
    df_cubo: pd.DataFrame
) -> pd.DataFrame:
    """
    Agrega valores, quantidades e percentuais por porte populacional dos municípios,
    acrescentando uma linha agregada para ESTADO.

    A linha de ESTADO usa porte_populacional = -99.

    Retorna
    -------
    pd.DataFrame
        Tabela agregada com municípios por porte populacional e uma linha para estados.
    """

    df = df_cubo.copy()

    # ------------------------------------------------------------
    # 1. Normalizar tipo_ente
    # ------------------------------------------------------------

    df["tipo_ente_norm"] = (
        df["tipo_ente"]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    # ------------------------------------------------------------
    # 2. Normalizar SITUACAO
    # ------------------------------------------------------------

    df["situacao_norm"] = (
        df["SITUACAO"]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    mask_urbano = df["situacao_norm"].isin(["URBANA", "URBANO"])
    mask_rural = df["situacao_norm"].isin(["RURAL"])

    # ------------------------------------------------------------
    # 3. Criar colunas auxiliares
    # ------------------------------------------------------------

    df["valor_urbano"] = np.where(
        mask_urbano,
        df["valor_transacao"],
        0
    )

    df["valor_rural"] = np.where(
        mask_rural,
        df["valor_transacao"],
        0
    )

    df["quantidade_urbano"] = np.where(
        mask_urbano,
        df["quantidade"],
        0
    )

    df["quantidade_rural"] = np.where(
        mask_rural,
        df["quantidade"],
        0
    )

    # ------------------------------------------------------------
    # 4. Separar municípios e estados
    # ------------------------------------------------------------

    df_municipios = df[df["tipo_ente_norm"].eq("MUNICIPIO")].copy()
    df_estados = df[df["tipo_ente_norm"].eq("ESTADO")].copy()

    # ------------------------------------------------------------
    # 5. Agregar municípios por porte populacional
    # ------------------------------------------------------------

    df_porte_municipios = (
        df_municipios
        .groupby("porte_populacional", dropna=False, as_index=False)
        .agg(
            numero_municipios=("ente", "nunique"),
            valor_total_por_porte=("valor_transacao", "sum"),
            valor_urbano_por_porte=("valor_urbano", "sum"),
            valor_rural_por_porte=("valor_rural", "sum"),
            quantidade_contemplados_por_porte=("quantidade", "sum"),
            quantidade_contemplados_urbano=("quantidade_urbano", "sum"),
            quantidade_contemplados_rural=("quantidade_rural", "sum"),
        )
    )

    # ------------------------------------------------------------
    # 6. Criar linha agregada dos estados
    # ------------------------------------------------------------

    df_estado = pd.DataFrame({
        "porte_populacional": [-99],
        "numero_municipios": [df_estados["ente"].nunique()],
        "valor_total_por_porte": [df_estados["valor_transacao"].sum()],
        "valor_urbano_por_porte": [df_estados["valor_urbano"].sum()],
        "valor_rural_por_porte": [df_estados["valor_rural"].sum()],
        "quantidade_contemplados_por_porte": [df_estados["quantidade"].sum()],
        "quantidade_contemplados_urbano": [df_estados["quantidade_urbano"].sum()],
        "quantidade_contemplados_rural": [df_estados["quantidade_rural"].sum()],
    })

    # ------------------------------------------------------------
    # 7. Juntar municípios por porte + linha de estados
    # ------------------------------------------------------------

    df_porte = pd.concat(
        [df_porte_municipios, df_estado],
        ignore_index=True
    )

    # ------------------------------------------------------------
    # 8. Calcular percentuais
    # ------------------------------------------------------------

    valor_total_geral = df_porte["valor_total_por_porte"].sum()
    quantidade_total_geral = df_porte["quantidade_contemplados_por_porte"].sum()

    df_porte["percentual_valor_urbano_por_porte"] = np.where(
        df_porte["valor_total_por_porte"].ne(0),
        df_porte["valor_urbano_por_porte"] / df_porte["valor_total_por_porte"],
        np.nan
    )

    df_porte["percentual_valor_rural_por_porte"] = np.where(
        df_porte["valor_total_por_porte"].ne(0),
        df_porte["valor_rural_por_porte"] / df_porte["valor_total_por_porte"],
        np.nan
    )

    df_porte["percentual_valor_por_porte"] = np.where(
        valor_total_geral != 0,
        df_porte["valor_total_por_porte"] / valor_total_geral,
        np.nan
    )

    df_porte["percentual_quantidade_por_porte"] = np.where(
        quantidade_total_geral != 0,
        df_porte["quantidade_contemplados_por_porte"] / quantidade_total_geral,
        np.nan
    )

    # ------------------------------------------------------------
    # 9. Arredondar valores monetários para cima
    # ------------------------------------------------------------

    colunas_valor = [
        "valor_total_por_porte",
        "valor_urbano_por_porte",
        "valor_rural_por_porte",
    ]

    df_porte[colunas_valor] = (
        np.ceil(df_porte[colunas_valor])
        .astype("Int64")
    )

    colunas_quantidade = [
        "numero_municipios",
        "quantidade_contemplados_por_porte",
        "quantidade_contemplados_urbano",
        "quantidade_contemplados_rural",
    ]

    df_porte[colunas_quantidade] = (
        df_porte[colunas_quantidade]
        .astype("Int64")
    )

    # ------------------------------------------------------------
    # 10. Ordenar tabela
    # ------------------------------------------------------------

    df_porte = (
        df_porte
        .sort_values("valor_total_por_porte", ascending=False)
        .reset_index(drop=True)
    )

    return df_porte

