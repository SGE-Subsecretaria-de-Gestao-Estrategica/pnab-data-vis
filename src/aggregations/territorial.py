import pandas as pd

def executed_value_n_contemplados_qty_by(df_cubo, by_filter):
    """
    Recebe df_cubo e agrega valores e quantidade de contemplados por:
    - ESTADO
    - MUNICIPIO
    - UF, considerando ESTADO + MUNICIPIO nos valores executados

    Para by_filter == 'UF', a população de referência é a população do ESTADO

    Entra também quantidade de contemplados por faixa de valor;
    Entra também o valor executado percapita
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

    df_tabela_uf = (
        df
        .groupby("uf", as_index=False)
        .agg(
            valor_executado_rs=("valor_transacao", "sum"),
            qtde_contemplados=("quantidade", "sum"),
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


def aggregate_execution_by_region(
    df_cubo: pd.DataFrame,
    by_filter: str = "ESTADO"
) -> pd.DataFrame:
    """
    Agrega valor executado, quantidade de contemplados e população por região.

    Parâmetros
    ----------
    df_cubo : pd.DataFrame
        Base principal.

    by_filter : str
        Recorte territorial usado no cálculo.

        Opções:
        - "ESTADO": considera apenas registros estaduais.
        - "MUNICIPIO": considera apenas registros municipais.
        - "UF": considera ESTADO + MUNICIPIO para valor e contemplados,
          mas usa apenas a população dos ESTADOS como referência.

    Retorna
    -------
    pd.DataFrame
        Tabela agregada por região.
    """

    by_filter = by_filter.upper()

    if by_filter == "ESTADO":
        df_valores = df_cubo[df_cubo["tipo_ente"] == "ESTADO"].copy()
        df_populacao_base = df_valores.copy()

    elif by_filter == "MUNICIPIO":
        df_valores = df_cubo[df_cubo["tipo_ente"] == "MUNICIPIO"].copy()
        df_populacao_base = df_valores.copy()

    elif by_filter == "UF":
        # Valor e contemplados consideram ESTADO + MUNICIPIO
        df_valores = df_cubo.copy()

        # População de referência vem apenas dos ESTADOS
        df_populacao_base = df_cubo[df_cubo["tipo_ente"] == "ESTADO"].copy()

    else:
        raise ValueError("by_filter deve ser 'ESTADO', 'MUNICIPIO' ou 'UF'.")

    df_valor_region = (
        df_valores
        .groupby("regiao", as_index=False)
        .agg(
            valor_executado_rs=("valor_transacao", "sum"),
            qtde_contemplados=("quantidade", "sum"),
            min_valor=("valor_transacao", "min"),
            mediana_valor=("valor_transacao", "median"),
            max_valor=("valor_transacao", "max"),
            media_valor=("valor_transacao", "mean")
        )
    )

    df_populacao_region = (
        df_populacao_base
        .groupby(["regiao", "uf"], as_index=False)
        .agg(
            populacao=("sum_populacao", "max")
        )
        .groupby("regiao", as_index=False)
        .agg(
            populacao=("populacao", "sum")
        )
    )

    df_tabela_region = df_valor_region.merge(
        df_populacao_region,
        on="regiao",
        how="left"
    )

    df_tabela_region["perc_valor_executado"] = (
        df_tabela_region["valor_executado_rs"]
        / df_tabela_region["valor_executado_rs"].sum()
    )

    df_tabela_region["perc_qtde_contemplados"] = (
        df_tabela_region["qtde_contemplados"]
        / df_tabela_region["qtde_contemplados"].sum()
    )

    df_tabela_region["perc_populacao"] = (
        df_tabela_region["populacao"]
        / df_tabela_region["populacao"].sum()
    )

    df_tabela_region["perc_contemplados_populacao"] = (
        df_tabela_region["qtde_contemplados"]
        / df_tabela_region["populacao"]
    )

    return df_tabela_region