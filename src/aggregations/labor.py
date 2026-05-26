import pandas as pd


def aggregate_vinculo_formal_labor(
    df_cubo: pd.DataFrame,
    col_flag: str = "flag_join_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria um DataFrame de uma linha com quantidade, valor pago e percentuais
    por existência de vínculo formal de trabalho.

    Regras:
    - Sem vínculo formal: flag_join_rais == False
    - Com vínculo formal: flag_join_rais == True
    - Valores nulos na flag são desconsiderados
    """

    df = df_cubo.copy()

    df = df[df['tipo_documento'] == 'CPF']

    sem_vinculo = df[col_flag] == False
    com_vinculo = df[col_flag] == True

    qtd_sem_vinculo = df.loc[sem_vinculo, col_quantidade].sum()
    qtd_com_vinculo = df.loc[com_vinculo, col_quantidade].sum()
    qtd_total = qtd_sem_vinculo + qtd_com_vinculo

    valor_sem_vinculo = df.loc[sem_vinculo, col_valor].sum()
    valor_com_vinculo = df.loc[com_vinculo, col_valor].sum()
    valor_total = valor_sem_vinculo + valor_com_vinculo

    resultado = pd.DataFrame([{
        "numero_contemplados_sem_vinculo_trabalho_formal": qtd_sem_vinculo,
        "numero_contemplados_com_vinculo_trabalho_formal": qtd_com_vinculo,
        "numero_contemplados_total": qtd_total,

        "percentual_contemplados_sem_vinculo_trabalho_formal": (
            qtd_sem_vinculo / qtd_total if qtd_total else 0
        ),
        "percentual_contemplados_com_vinculo_trabalho_formal": (
            qtd_com_vinculo / qtd_total if qtd_total else 0
        ),

        "valor_pago_sem_vinculo_trabalho_formal": valor_sem_vinculo,
        "valor_pago_com_vinculo_trabalho_formal": valor_com_vinculo,
        "valor_pago_total": valor_total,

        "percentual_valor_pago_sem_vinculo_trabalho_formal": (
            valor_sem_vinculo / valor_total if valor_total else 0
        ),
        "percentual_valor_pago_com_vinculo_trabalho_formal": (
            valor_com_vinculo / valor_total if valor_total else 0
        ),
    }])

    return resultado


def aggregate_vinculo_formal_labor_by_region(
    df_cubo: pd.DataFrame,
    col_regiao: str = "regiao",
    col_flag: str = "flag_join_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria um DataFrame com uma linha por região, contendo:
    - quantidade de contemplados com e sem vínculo formal
    - valor pago com e sem vínculo formal
    - percentuais dentro da própria região
    - participação da região no total geral
    - participação da região no total geral por tipo de vínculo
    """

    df = df_cubo.copy()

    df = df[df['tipo_documento'] == 'CPF']

    # Mantém apenas casos em que a informação de vínculo existe
    df = df.loc[df[col_flag].notna()].copy()

    df["situacao_vinculo_formal"] = df[col_flag].map({
        False: "sem_vinculo_trabalho_formal",
        True: "com_vinculo_trabalho_formal",
    })

    resumo = (
        df
        .groupby([col_regiao, "situacao_vinculo_formal"], dropna=False)
        .agg(
            numero_contemplados=(col_quantidade, "sum"),
            valor_pago=(col_valor, "sum"),
        )
        .reset_index()
    )

    tabela = (
        resumo
        .pivot(
            index=col_regiao,
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

    tabela["numero_contemplados_total"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        + tabela["numero_contemplados_com_vinculo_trabalho_formal"]
    )

    tabela["valor_pago_total"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        + tabela["valor_pago_com_vinculo_trabalho_formal"]
    )

    # Percentuais dentro da própria região
    tabela["percentual_contemplados_sem_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_total"]
    ).fillna(0)

    tabela["percentual_contemplados_com_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_total"]
    ).fillna(0)

    tabela["percentual_valor_pago_sem_vinculo_trabalho_formal"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela["valor_pago_total"]
    ).fillna(0)

    tabela["percentual_valor_pago_com_vinculo_trabalho_formal"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / tabela["valor_pago_total"]
    ).fillna(0)

    # Participação da região no total geral, independentemente do vínculo
    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

    # Participação da região no total geral de contemplados com/sem vínculo
    tabela["percentual_numero_contemplados_sem_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_sem_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    tabela["percentual_numero_contemplados_com_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_com_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    # Participação da região no total geral de valor pago com/sem vínculo
    tabela["percentual_valor_pago_sem_vinculo_no_total_geral"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela["valor_pago_sem_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_com_vinculo_no_total_geral"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / tabela["valor_pago_com_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    colunas_finais = [
        col_regiao,

        "numero_contemplados_sem_vinculo_trabalho_formal",
        "numero_contemplados_com_vinculo_trabalho_formal",
        "numero_contemplados_total",

        "percentual_contemplados_sem_vinculo_trabalho_formal",
        "percentual_contemplados_com_vinculo_trabalho_formal",
        "percentual_numero_contemplados_no_total_geral",
        "percentual_numero_contemplados_sem_vinculo_no_total_geral",
        "percentual_numero_contemplados_com_vinculo_no_total_geral",

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
        .sort_values(col_regiao)
        .reset_index(drop=True)
    )


def aggregate_vinculo_formal_labor_by_uf(
    df_cubo: pd.DataFrame,
    col_uf: str = "uf",
    col_flag: str = "flag_join_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria um DataFrame com uma linha por UF, contendo:
    - quantidade de contemplados com e sem vínculo formal
    - valor pago com e sem vínculo formal
    - percentuais dentro da própria UF
    - participação da UF no total geral
    - participação da UF no total geral por tipo de vínculo
    """

    df = df_cubo.copy()

    df = df[df['tipo_documento'] == 'CPF']

    # Mantém apenas casos em que a informação de vínculo existe
    df = df.loc[df[col_flag].notna()].copy()

    df["situacao_vinculo_formal"] = df[col_flag].map({
        False: "sem_vinculo_trabalho_formal",
        True: "com_vinculo_trabalho_formal",
    })

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

    tabela["numero_contemplados_total"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        + tabela["numero_contemplados_com_vinculo_trabalho_formal"]
    )

    tabela["valor_pago_total"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        + tabela["valor_pago_com_vinculo_trabalho_formal"]
    )

    # Percentuais dentro da própria UF
    tabela["percentual_contemplados_sem_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_total"]
    ).fillna(0)

    tabela["percentual_contemplados_com_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_total"]
    ).fillna(0)

    tabela["percentual_valor_pago_sem_vinculo_trabalho_formal"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela["valor_pago_total"]
    ).fillna(0)

    tabela["percentual_valor_pago_com_vinculo_trabalho_formal"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / tabela["valor_pago_total"]
    ).fillna(0)

    # Participação da UF no total geral, independentemente do vínculo
    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

    # Participação da UF no total geral de contemplados com/sem vínculo
    tabela["percentual_numero_contemplados_sem_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_sem_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    tabela["percentual_numero_contemplados_com_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_com_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    # Participação da UF no total geral de valor pago com/sem vínculo
    tabela["percentual_valor_pago_sem_vinculo_no_total_geral"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela["valor_pago_sem_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_com_vinculo_no_total_geral"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / tabela["valor_pago_com_vinculo_trabalho_formal"].sum()
    ).fillna(0)

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


def aggregate_vinculo_formal_labor_by_sexo(
    df_cubo: pd.DataFrame,
    col_sexo: str = "Sexo",
    col_flag: str = "flag_join_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria um DataFrame com uma linha por Sexo, comparando contemplados
    com e sem vínculo formal de trabalho.

    Considera apenas:
    - Sexo == Masculino ou Feminino
    - flag_join_rais não nulo
    """

    df = df_cubo.copy()

    df = df[df['tipo_documento'] == 'CPF']

    df = df.loc[
        df[col_sexo].isin(["Masculino", "Feminino"])
        & df[col_flag].notna()
    ].copy()

    df["situacao_vinculo_formal"] = df[col_flag].map({
        False: "sem_vinculo_trabalho_formal",
        True: "com_vinculo_trabalho_formal",
    })

    resumo = (
        df
        .groupby([col_sexo, "situacao_vinculo_formal"], dropna=False)
        .agg(
            numero_contemplados=(col_quantidade, "sum"),
            valor_pago=(col_valor, "sum"),
        )
        .reset_index()
    )

    tabela = (
        resumo
        .pivot(
            index=col_sexo,
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

    tabela["numero_contemplados_total"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        + tabela["numero_contemplados_com_vinculo_trabalho_formal"]
    )

    tabela["valor_pago_total"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        + tabela["valor_pago_com_vinculo_trabalho_formal"]
    )

    # Percentuais dentro do próprio Sexo
    tabela["percentual_contemplados_sem_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_total"]
    ).fillna(0)

    tabela["percentual_contemplados_com_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_total"]
    ).fillna(0)

    tabela["percentual_valor_pago_sem_vinculo_trabalho_formal"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela["valor_pago_total"]
    ).fillna(0)

    tabela["percentual_valor_pago_com_vinculo_trabalho_formal"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / tabela["valor_pago_total"]
    ).fillna(0)

    # Participação de cada Sexo no total geral
    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

    # Participação de cada Sexo no total geral com/sem vínculo
    tabela["percentual_numero_contemplados_sem_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_sem_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    tabela["percentual_numero_contemplados_com_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_com_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_sem_vinculo_no_total_geral"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela["valor_pago_sem_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_com_vinculo_no_total_geral"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / tabela["valor_pago_com_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    colunas_finais = [
        col_sexo,

        "numero_contemplados_sem_vinculo_trabalho_formal",
        "numero_contemplados_com_vinculo_trabalho_formal",
        "numero_contemplados_total",

        "percentual_contemplados_sem_vinculo_trabalho_formal",
        "percentual_contemplados_com_vinculo_trabalho_formal",
        "percentual_numero_contemplados_no_total_geral",
        "percentual_numero_contemplados_sem_vinculo_no_total_geral",
        "percentual_numero_contemplados_com_vinculo_no_total_geral",

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
        .sort_values(col_sexo)
        .reset_index(drop=True)
    )


def aggregate_vinculo_formal_labor_by_age_group(
    df_cubo: pd.DataFrame,
    col_faixa_etaria: str = "faixa_etaria",
    col_flag: str = "flag_join_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria um DataFrame com uma linha por faixa etária, comparando contemplados
    com e sem vínculo formal de trabalho.

    Considera apenas:
    - faixa_etaria não nula
    - flag_join_rais não nula
    """

    df = df_cubo.copy()

    df = df[df['tipo_documento'] == 'CPF']

    df = df.loc[
        df[col_faixa_etaria].notna()
        & df[col_flag].notna()
    ].copy()

    df["situacao_vinculo_formal"] = df[col_flag].map({
        False: "sem_vinculo_trabalho_formal",
        True: "com_vinculo_trabalho_formal",
    })

    resumo = (
        df
        .groupby([col_faixa_etaria, "situacao_vinculo_formal"], dropna=False)
        .agg(
            numero_contemplados=(col_quantidade, "sum"),
            valor_pago=(col_valor, "sum"),
        )
        .reset_index()
    )

    tabela = (
        resumo
        .pivot(
            index=col_faixa_etaria,
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

    tabela["numero_contemplados_total"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        + tabela["numero_contemplados_com_vinculo_trabalho_formal"]
    )

    tabela["valor_pago_total"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        + tabela["valor_pago_com_vinculo_trabalho_formal"]
    )

    # Percentuais dentro da própria faixa etária
    tabela["percentual_contemplados_sem_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_total"]
    ).fillna(0)

    tabela["percentual_contemplados_com_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_total"]
    ).fillna(0)

    tabela["percentual_valor_pago_sem_vinculo_trabalho_formal"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela["valor_pago_total"]
    ).fillna(0)

    tabela["percentual_valor_pago_com_vinculo_trabalho_formal"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / tabela["valor_pago_total"]
    ).fillna(0)

    # Participação de cada faixa etária no total geral
    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

    # Participação de cada faixa etária no total geral com/sem vínculo
    tabela["percentual_numero_contemplados_sem_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_sem_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    tabela["percentual_numero_contemplados_com_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_com_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_sem_vinculo_no_total_geral"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela["valor_pago_sem_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_com_vinculo_no_total_geral"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / tabela["valor_pago_com_vinculo_trabalho_formal"].sum()
    ).fillna(0)

    colunas_finais = [
        col_faixa_etaria,

        "numero_contemplados_sem_vinculo_trabalho_formal",
        "numero_contemplados_com_vinculo_trabalho_formal",
        "numero_contemplados_total",

        "percentual_contemplados_sem_vinculo_trabalho_formal",
        "percentual_contemplados_com_vinculo_trabalho_formal",
        "percentual_numero_contemplados_no_total_geral",
        "percentual_numero_contemplados_sem_vinculo_no_total_geral",
        "percentual_numero_contemplados_com_vinculo_no_total_geral",

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
        .sort_values(col_faixa_etaria)
        .reset_index(drop=True)
    )