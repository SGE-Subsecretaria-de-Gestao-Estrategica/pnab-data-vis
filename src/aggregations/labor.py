import pandas as pd
import numpy as np

def aggregate_vinculo_formal_labor(
    df_cubo: pd.DataFrame,
    col_vinculo: str = "tipo_vinculo_agregado_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
    col_tipo_documento: str = "tipo_documento",
) -> pd.DataFrame:
    """
    Cria um DataFrame de uma linha com quantidade, valor pago e percentuais
    por existência de vínculo formal de trabalho.

    Regras:
    - Com vínculo formal: tipo_vinculo_agregado_rais preenchida
    - Sem vínculo formal: tipo_vinculo_agregado_rais nula ou vazia
    - Considera apenas registros de CPF
    """

    df = df_cubo.copy()

    # Mantém apenas CPF
    df = df[df[col_tipo_documento] == "CPF"].copy()

    # Trata strings vazias como missing
    vinculo_preenchido = (
        df[col_vinculo]
        .notna()
        & df[col_vinculo].astype(str).str.strip().ne("")
    )

    com_vinculo = vinculo_preenchido
    sem_vinculo = ~vinculo_preenchido

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

    cols_percentuais = [
        "percentual_contemplados_sem_vinculo_trabalho_formal",
        "percentual_contemplados_com_vinculo_trabalho_formal",
        "percentual_valor_pago_sem_vinculo_trabalho_formal",
        "percentual_valor_pago_com_vinculo_trabalho_formal",
    ]
    resultado[cols_percentuais] = resultado[cols_percentuais].round(3)

    return resultado

def aggregate_vinculo_formal_labor_by_region(
    df_cubo: pd.DataFrame,
    col_regiao: str = "regiao",
    col_vinculo: str = "tipo_vinculo_agregado_rais",
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

    Regras:
    - Sem vínculo formal: tipo_vinculo_agregado_rais missing, nulo ou vazio
    - Com vínculo formal: tipo_vinculo_agregado_rais preenchido
    """

    df = df_cubo.copy()

    df = df[df["tipo_documento"] == "CPF"].copy()

    # Preenchido = com vínculo formal
    vinculo_preenchido = (
        df[col_vinculo].notna()
        & df[col_vinculo].astype(str).str.strip().ne("")
    )

    df["situacao_vinculo_formal"] = "sem_vinculo_trabalho_formal"
    df.loc[vinculo_preenchido, "situacao_vinculo_formal"] = "com_vinculo_trabalho_formal"

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
    col_vinculo: str = "tipo_vinculo_agregado_rais",
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

    Regras:
    - Sem vínculo formal: tipo_vinculo_agregado_rais missing, nulo ou vazio
    - Com vínculo formal: tipo_vinculo_agregado_rais preenchido
    """

    df = df_cubo.copy()

    df = df[df["tipo_documento"] == "CPF"].copy()

    vinculo_preenchido = (
        df[col_vinculo].notna()
        & df[col_vinculo].astype(str).str.strip().ne("")
    )

    df["situacao_vinculo_formal"] = "sem_vinculo_trabalho_formal"
    df.loc[vinculo_preenchido, "situacao_vinculo_formal"] = "com_vinculo_trabalho_formal"

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

    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

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
import pandas as pd


def aggregate_vinculo_formal_labor_by_sexo(
    df_cubo: pd.DataFrame,
    col_sexo: str = "Sexo",
    col_vinculo: str = "tipo_vinculo_agregado_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria um DataFrame com uma linha por Sexo, comparando contemplados
    com e sem vínculo formal de trabalho.

    Considera apenas:
    - tipo_documento == CPF
    - Sexo == Masculino ou Feminino

    Regras:
    - Sem vínculo formal: tipo_vinculo_agregado_rais missing, nulo ou vazio
    - Com vínculo formal: tipo_vinculo_agregado_rais preenchido
    """

    df = df_cubo.copy()

    df = df[df["tipo_documento"] == "CPF"].copy()

    df = df.loc[
        df[col_sexo].isin(["Masculino", "Feminino"])
    ].copy()

    vinculo_preenchido = (
        df[col_vinculo].notna()
        & df[col_vinculo].astype(str).str.strip().ne("")
    )

    df["situacao_vinculo_formal"] = "sem_vinculo_trabalho_formal"
    df.loc[vinculo_preenchido, "situacao_vinculo_formal"] = "com_vinculo_trabalho_formal"

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

    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

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
    col_vinculo: str = "tipo_vinculo_agregado_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria um DataFrame com uma linha por faixa etária, comparando contemplados
    com e sem vínculo formal de trabalho.

    Considera apenas:
    - tipo_documento == CPF
    - faixa_etaria não nula

    Regras:
    - Sem vínculo formal: tipo_vinculo_agregado_rais missing, nulo ou vazio
    - Com vínculo formal: tipo_vinculo_agregado_rais preenchido
    """

    df = df_cubo.copy()

    df = df[df["tipo_documento"] == "CPF"].copy()

    df = df.loc[
        df[col_faixa_etaria].notna()
    ].copy()

    vinculo_preenchido = (
        df[col_vinculo].notna()
        & ~df[col_vinculo]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["", "nan", "none", "null", "<na>"])
    )

    df["situacao_vinculo_formal"] = "sem_vinculo_trabalho_formal"
    df.loc[vinculo_preenchido, "situacao_vinculo_formal"] = "com_vinculo_trabalho_formal"

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

    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

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


def aggregate_vinculo_formal_labor_by_raca_cor(
    df_cubo: pd.DataFrame,
    col_raca_cor: str = "raca_cor_desc_description",
    col_vinculo: str = "tipo_vinculo_agregado_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria um DataFrame com uma linha por raça/cor, comparando contemplados
    com e sem vínculo formal de trabalho.

    Considera apenas:
    - tipo_documento == CPF
    - raca_cor_desc_description não nula
    - raca_cor_desc_description != "Não informado"

    Regras:
    - Sem vínculo formal: tipo_vinculo_agregado_rais missing, nulo ou vazio
    - Com vínculo formal: tipo_vinculo_agregado_rais preenchido
    """

    df = df_cubo.copy()

    df = df[df["tipo_documento"] == "CPF"].copy()

    # Remove raça/cor sem informação
    df = df.loc[
        df[col_raca_cor].notna()
        & df[col_raca_cor].astype(str).str.strip().str.lower().ne("não informado")
    ].copy()

    # NÃO filtrar missing em col_vinculo.
    # Missing em tipo_vinculo_agregado_rais significa "sem vínculo".
    vinculo_preenchido = (
        df[col_vinculo].notna()
        & ~df[col_vinculo]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["", "nan", "none", "null", "<na>"])
    )

    df["situacao_vinculo_formal"] = "sem_vinculo_trabalho_formal"
    df.loc[vinculo_preenchido, "situacao_vinculo_formal"] = "com_vinculo_trabalho_formal"

    resumo = (
        df
        .groupby([col_raca_cor, "situacao_vinculo_formal"], dropna=False)
        .agg(
            numero_contemplados=(col_quantidade, "sum"),
            valor_pago=(col_valor, "sum"),
        )
        .reset_index()
    )

    tabela = (
        resumo
        .pivot(
            index=col_raca_cor,
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

    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

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
        col_raca_cor,

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
        .sort_values(col_raca_cor)
        .reset_index(drop=True)
    )


def aggregate_raca_cor_vinculo_formal_labor_by_sexo(
    df_cubo: pd.DataFrame,
    col_raca_cor: str = "raca_cor_desc_description",
    col_sexo: str = "Sexo",
    col_flag: str = "flag_join_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria uma visão por raça/cor, combinando:

    1. Relação com vínculo formal de trabalho:
       - contemplados com vínculo
       - contemplados sem vínculo
       - valor pago com vínculo
       - valor pago sem vínculo

    2. Recorte por Sexo dentro de cada raça/cor:
       - quantidade Masculino
       - quantidade Feminino
       - percentual Masculino/Feminino dentro da raça/cor
       - valor Masculino
       - valor Feminino
       - percentual do valor Masculino/Feminino dentro da raça/cor

    Considera apenas:
    - raça/cor não nula
    - flag_join_rais não nula
    - Sexo igual a Masculino ou Feminino
    """

    df = df_cubo.copy()

    df = df[df['tipo_documento'] == 'CPF']
   
    df = df.loc[
        df[col_raca_cor].notna()
        & df[col_flag].notna()
        & df[col_sexo].isin(["Masculino", "Feminino"])
    ].copy()

    df["situacao_vinculo_formal"] = df[col_flag].map({
        False: "sem_vinculo_trabalho_formal",
        True: "com_vinculo_trabalho_formal",
    })

    # =========================
    # 1. Visão por vínculo formal
    # =========================

    resumo_vinculo = (
        df
        .groupby([col_raca_cor, "situacao_vinculo_formal"], dropna=False)
        .agg(
            numero_contemplados=(col_quantidade, "sum"),
            valor_pago=(col_valor, "sum"),
        )
        .reset_index()
    )

    tabela_vinculo = (
        resumo_vinculo
        .pivot(
            index=col_raca_cor,
            columns="situacao_vinculo_formal",
            values=["numero_contemplados", "valor_pago"],
        )
    )

    tabela_vinculo.columns = [
        f"{metrica}_{situacao}"
        for metrica, situacao in tabela_vinculo.columns
    ]

    tabela_vinculo = tabela_vinculo.reset_index().fillna(0)

    colunas_vinculo_esperadas = [
        "numero_contemplados_sem_vinculo_trabalho_formal",
        "numero_contemplados_com_vinculo_trabalho_formal",
        "valor_pago_sem_vinculo_trabalho_formal",
        "valor_pago_com_vinculo_trabalho_formal",
    ]

    for col in colunas_vinculo_esperadas:
        if col not in tabela_vinculo.columns:
            tabela_vinculo[col] = 0

    tabela_vinculo["numero_contemplados_total"] = (
        tabela_vinculo["numero_contemplados_sem_vinculo_trabalho_formal"]
        + tabela_vinculo["numero_contemplados_com_vinculo_trabalho_formal"]
    )

    tabela_vinculo["valor_pago_total"] = (
        tabela_vinculo["valor_pago_sem_vinculo_trabalho_formal"]
        + tabela_vinculo["valor_pago_com_vinculo_trabalho_formal"]
    )

    tabela_vinculo["percentual_contemplados_sem_vinculo_trabalho_formal"] = (
        tabela_vinculo["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela_vinculo["numero_contemplados_total"]
    ).fillna(0)

    tabela_vinculo["percentual_contemplados_com_vinculo_trabalho_formal"] = (
        tabela_vinculo["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela_vinculo["numero_contemplados_total"]
    ).fillna(0)

    tabela_vinculo["percentual_valor_pago_sem_vinculo_trabalho_formal"] = (
        tabela_vinculo["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela_vinculo["valor_pago_total"]
    ).fillna(0)

    tabela_vinculo["percentual_valor_pago_com_vinculo_trabalho_formal"] = (
        tabela_vinculo["valor_pago_com_vinculo_trabalho_formal"]
        / tabela_vinculo["valor_pago_total"]
    ).fillna(0)

    # =========================
    # 2. Visão por Sexo
    # =========================

    resumo_sexo = (
        df
        .groupby([col_raca_cor, col_sexo], dropna=False)
        .agg(
            numero_contemplados=(col_quantidade, "sum"),
            valor_pago=(col_valor, "sum"),
        )
        .reset_index()
    )

    tabela_sexo = (
        resumo_sexo
        .pivot(
            index=col_raca_cor,
            columns=col_sexo,
            values=["numero_contemplados", "valor_pago"],
        )
    )

    tabela_sexo.columns = [
        f"{metrica}_{sexo.lower()}"
        for metrica, sexo in tabela_sexo.columns
    ]

    tabela_sexo = tabela_sexo.reset_index().fillna(0)

    colunas_sexo_esperadas = [
        "numero_contemplados_masculino",
        "numero_contemplados_feminino",
        "valor_pago_masculino",
        "valor_pago_feminino",
    ]

    for col in colunas_sexo_esperadas:
        if col not in tabela_sexo.columns:
            tabela_sexo[col] = 0

    tabela_sexo["numero_contemplados_total_sexo"] = (
        tabela_sexo["numero_contemplados_masculino"]
        + tabela_sexo["numero_contemplados_feminino"]
    )

    tabela_sexo["valor_pago_total_sexo"] = (
        tabela_sexo["valor_pago_masculino"]
        + tabela_sexo["valor_pago_feminino"]
    )

    tabela_sexo["percentual_contemplados_masculino"] = (
        tabela_sexo["numero_contemplados_masculino"]
        / tabela_sexo["numero_contemplados_total_sexo"]
    ).fillna(0)

    tabela_sexo["percentual_contemplados_feminino"] = (
        tabela_sexo["numero_contemplados_feminino"]
        / tabela_sexo["numero_contemplados_total_sexo"]
    ).fillna(0)

    tabela_sexo["percentual_valor_pago_masculino"] = (
        tabela_sexo["valor_pago_masculino"]
        / tabela_sexo["valor_pago_total_sexo"]
    ).fillna(0)

    tabela_sexo["percentual_valor_pago_feminino"] = (
        tabela_sexo["valor_pago_feminino"]
        / tabela_sexo["valor_pago_total_sexo"]
    ).fillna(0)

    # =========================
    # 3. Junta as duas visões
    # =========================

    tabela = tabela_vinculo.merge(
        tabela_sexo,
        on=col_raca_cor,
        how="left",
    ).fillna(0)

    # Participação da raça/cor no total geral
    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

    colunas_finais = [
        col_raca_cor,

        # Vínculo formal
        "numero_contemplados_sem_vinculo_trabalho_formal",
        "numero_contemplados_com_vinculo_trabalho_formal",
        "numero_contemplados_total",
        "percentual_contemplados_sem_vinculo_trabalho_formal",
        "percentual_contemplados_com_vinculo_trabalho_formal",
        "percentual_numero_contemplados_no_total_geral",

        "valor_pago_sem_vinculo_trabalho_formal",
        "valor_pago_com_vinculo_trabalho_formal",
        "valor_pago_total",
        "percentual_valor_pago_sem_vinculo_trabalho_formal",
        "percentual_valor_pago_com_vinculo_trabalho_formal",
        "percentual_valor_pago_no_total_geral",

        # Sexo
        "numero_contemplados_masculino",
        "numero_contemplados_feminino",
        "numero_contemplados_total_sexo",
        "percentual_contemplados_masculino",
        "percentual_contemplados_feminino",

        "valor_pago_masculino",
        "valor_pago_feminino",
        "valor_pago_total_sexo",
        "percentual_valor_pago_masculino",
        "percentual_valor_pago_feminino",
    ]

    return (
        tabela[colunas_finais]
        .sort_values(col_raca_cor)
        .reset_index(drop=True)
    )


def aggregate_vinculo_formal_labor_by_escolaridade(
    df_cubo: pd.DataFrame,
    col_escolaridade: str = "escolaridade_agregado_rais",
    col_flag: str = "flag_join_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
    preencher_sem_informacao: bool = True,
) -> pd.DataFrame:
    """
    Cria uma visão por escolaridade agregada da RAIS, comparando:
    - contemplados com vínculo formal
    - contemplados sem vínculo formal
    - valor pago com vínculo formal
    - valor pago sem vínculo formal
    - percentuais dentro da escolaridade
    - percentuais no total geral
    - percentuais no total geral por tipo de vínculo

    Observação:
    Como a escolaridade vem da RAIS, registros sem vínculo formal podem aparecer
    com escolaridade nula. Por padrão, esses casos são classificados como
    'Sem informação'.
    """

    df = df_cubo.copy()

    df = df[df['tipo_documento'] == 'CPF']

    df = df.loc[df[col_flag].notna()].copy()

    if preencher_sem_informacao:
        df[col_escolaridade] = df[col_escolaridade].fillna("Sem informação")
    else:
        df = df.loc[df[col_escolaridade].notna()].copy()

    df["situacao_vinculo_formal"] = df[col_flag].map({
        False: "sem_vinculo_trabalho_formal",
        True: "com_vinculo_trabalho_formal",
    })

    resumo = (
        df
        .groupby([col_escolaridade, "situacao_vinculo_formal"], dropna=False)
        .agg(
            numero_contemplados=(col_quantidade, "sum"),
            valor_pago=(col_valor, "sum"),
        )
        .reset_index()
    )

    tabela = (
        resumo
        .pivot(
            index=col_escolaridade,
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

    # Percentuais dentro da própria escolaridade
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

    # Participação da escolaridade no total geral
    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

    # Participação da escolaridade no total geral com/sem vínculo
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
        col_escolaridade,

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
        .sort_values("numero_contemplados_total", ascending=False)
        .reset_index(drop=True)
    )




def aggregate_vinculo_trabalho_formal_by_escolaridade_sem_sem_informacao(
    df_cubo: pd.DataFrame,
    col_escolaridade: str = "escolaridade_agregado_rais",
    col_flag: str = "flag_join_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria uma visão por escolaridade agregada da RAIS, comparando:
    - contemplados com vínculo formal
    - contemplados sem vínculo formal
    - valor pago com vínculo formal
    - valor pago sem vínculo formal
    - percentuais dentro da escolaridade
    - percentuais no total geral
    - percentuais no total geral por tipo de vínculo

    Esta versão exclui:
    - escolaridade_agregado_rais == "Sem informação"
    - escolaridade_agregado_rais nula
    - flag_join_rais nula
    """

    df = df_cubo.copy()

    df = df[df['tipo_documento'] == 'CPF']

    df = df.loc[
        df[col_flag].notna()
        & df[col_escolaridade].notna()
        & (df[col_escolaridade] != "Sem informação")
    ].copy()

    df["situacao_vinculo_formal"] = df[col_flag].map({
        False: "sem_vinculo_trabalho_formal",
        True: "com_vinculo_trabalho_formal",
    })

    resumo = (
        df
        .groupby([col_escolaridade, "situacao_vinculo_formal"], dropna=False)
        .agg(
            numero_contemplados=(col_quantidade, "sum"),
            valor_pago=(col_valor, "sum"),
        )
        .reset_index()
    )

    tabela = (
        resumo
        .pivot(
            index=col_escolaridade,
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

    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

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
        col_escolaridade,

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
        .sort_values("numero_contemplados_total", ascending=False)
        .reset_index(drop=True)
    )


def aggregate_cbo_rais(df_cubo: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega quantidade de contemplados e valor recebido por CBO_2002_RAIS.

    Filtros aplicados:
    - tipo_documento == "CPF"
    - flag_join_rais == True

    Retorna:
    - CBO_2002_RAIS
    - soma_quantidade
    - percentual_quantidade
    - soma_valor
    - percentual_valor
    """
    df_cubo_cbo = df_cubo[['cbo_codigo', 'cbo_descricao']].drop_duplicates()
    df_cubo_cbo = df_cubo_cbo[~(df_cubo_cbo['cbo_codigo'].isna())]
    df_cubo_cbo = df_cubo_cbo.rename(columns={
        'cbo_descricao': 'cbo_descricao_rais'
    })

    df_cubo_rais_raw = df_cubo[df_cubo['flag_join_rais'] == True]

    df_cubo_rais = df_cubo_rais_raw.merge(
    how='left',
    right=df_cubo_cbo,
    left_on='CBO_2002_RAIS',
    right_on='cbo_codigo'
    )


    df = df_cubo_rais.copy()

    df_filtrado = df.loc[
        (df["tipo_documento"].eq("CPF"))
        & (df["flag_join_rais"].eq(True))
    ].copy()

    df_resultado = (
        df_filtrado
        .groupby("cbo_descricao_rais", dropna=False)
        .agg(
            soma_quantidade=("quantidade", "sum"),
            soma_valor=("valor_transacao", "sum"),
        )
        .reset_index()
    )

    total_quantidade = df_resultado["soma_quantidade"].sum()
    total_valor = df_resultado["soma_valor"].sum()

    df_resultado["percentual_quantidade"] = (
        df_resultado["soma_quantidade"] / total_quantidade
        if total_quantidade > 0
        else 0
    )

    df_resultado["percentual_valor"] = (
        df_resultado["soma_valor"] / total_valor
        if total_valor > 0
        else 0
    )

    df_resultado = df_resultado[
        [
            "cbo_descricao_rais",
            "soma_quantidade",
            "percentual_quantidade",
            "soma_valor",
            "percentual_valor",
        ]
    ].sort_values(
        by="soma_valor",
        ascending=False
    ).reset_index(drop=True)

    return df_resultado


def aggregate_vinculo_formal_labor_by_age_group(
    df_cubo: pd.DataFrame,
    col_faixa_etaria: str = "faixa_etaria",
    col_vinculo: str = "tipo_vinculo_agregado_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Cria um DataFrame com uma linha por faixa etária, comparando contemplados
    com e sem vínculo formal de trabalho.

    Considera apenas:
    - tipo_documento == CPF
    - faixa_etaria não nula

    Regras:
    - Sem vínculo formal: tipo_vinculo_agregado_rais missing, nulo ou vazio
    - Com vínculo formal: tipo_vinculo_agregado_rais preenchido
    """

    df = df_cubo.copy()

    df = df[df["tipo_documento"] == "CPF"].copy()

    df = df.loc[
        df[col_faixa_etaria].notna()
    ].copy()

    vinculo_preenchido = (
        df[col_vinculo].notna()
        & ~df[col_vinculo]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["", "nan", "none", "null", "<na>"])
    )

    df["situacao_vinculo_formal"] = "sem_vinculo_trabalho_formal"
    df.loc[vinculo_preenchido, "situacao_vinculo_formal"] = "com_vinculo_trabalho_formal"

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

    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).fillna(0)

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


def resumo_raca_cor_com_vinculo_rais(
    df_cubo: pd.DataFrame,
    col_raca: str = "raca_cor_desc_description",
    col_vinculo: str = "tipo_vinculo_agregado_rais",
    col_qtd: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Retorna resumo por raça/cor considerando apenas contemplados com vínculo RAIS.

    Regras:
    - 'Não informado' é desconsiderado da análise;
    - valores NaN em raça/cor também são desconsiderados;
    - vínculo RAIS = tipo_vinculo_agregado_rais não missing;
    - percentuais são calculados apenas sobre as categorias válidas.
    """

    df = df_cubo.copy()

    # Remove raça/cor não informada e missing
    df = df[
        df[col_raca].notna()
        & (df[col_raca].astype(str).str.strip() != "Não informado")
    ].copy()

    # Mantém apenas contemplados com vínculo RAIS
    df = df[df[col_vinculo].notna()].copy()

    # Agrega por raça/cor
    resumo = (
        df
        .groupby(col_raca, dropna=False)
        .agg(
            qtd_contemplados_com_vinculo=(col_qtd, "sum"),
            valor_transacao_com_vinculo=(col_valor, "sum"),
        )
        .reset_index()
    )

    # Totais válidos para cálculo dos percentuais
    total_qtd = resumo["qtd_contemplados_com_vinculo"].sum()
    total_valor = resumo["valor_transacao_com_vinculo"].sum()

    resumo["perc_qtd_contemplados_com_vinculo"] = np.where(
        total_qtd > 0,
        resumo["qtd_contemplados_com_vinculo"] / total_qtd ,
        0
    )

    resumo["perc_valor_transacao_com_vinculo"] = np.where(
        total_valor > 0,
        resumo["valor_transacao_com_vinculo"] / total_valor ,
        0
    )

    # Ordena da maior para menor participação em quantidade
    resumo = resumo.sort_values(
        "qtd_contemplados_com_vinculo",
        ascending=False
    ).reset_index(drop=True)

    return resumo
import pandas as pd
import numpy as np

def resumo_escolaridade_com_vinculo_rais(
    df_cubo: pd.DataFrame,
    col_escolaridade: str = "escolaridade_agregado_rais",
    col_vinculo: str = "tipo_vinculo_agregado_rais",
    col_qtd: str = "quantidade",
    col_valor: str = "valor_transacao",
) -> pd.DataFrame:
    """
    Retorna resumo por escolaridade considerando apenas contemplados com vínculo RAIS.

    Regras:
    - vínculo RAIS = tipo_vinculo_agregado_rais não missing;
    - categorias de escolaridade missing são desconsideradas;
    - percentuais são calculados sobre o total de contemplados com vínculo;
    - valor médio = soma do valor da categoria / quantidade de contemplados da categoria.
    """

    ordem_escolaridade = [
        "Sem instrução e fundamental incompleto",
        "Fundamental completo e médio incompleto",
        "Médio completo e superior incompleto",
        "Superior completo",
        "Mestrado ou doutorado completo",
    ]

    df = df_cubo.copy()

    # Remove escolaridade missing
    df = df[df[col_escolaridade].notna()].copy()

    # Mantém apenas categorias esperadas
    df = df[df[col_escolaridade].isin(ordem_escolaridade)].copy()

    # Mantém apenas contemplados com vínculo RAIS
    df = df[df[col_vinculo].notna()].copy()

    resumo = (
        df
        .groupby(col_escolaridade)
        .agg(
            qtd_contemplados_com_vinculo=(col_qtd, "sum"),
            valor_transacao_com_vinculo=(col_valor, "sum"),
        )
        .reindex(ordem_escolaridade)
        .fillna(0)
        .reset_index()
    )

    total_qtd = resumo["qtd_contemplados_com_vinculo"].sum()
    total_valor = resumo["valor_transacao_com_vinculo"].sum()

    resumo["perc_qtd_contemplados_com_vinculo"] = np.where(
        total_qtd > 0,
        resumo["qtd_contemplados_com_vinculo"] / total_qtd * 100,
        0
    )

    resumo["perc_valor_transacao_com_vinculo"] = np.where(
        total_valor > 0,
        resumo["valor_transacao_com_vinculo"] / total_valor * 100,
        0
    )

    resumo["valor_medio_transacao_com_vinculo"] = np.where(
        resumo["qtd_contemplados_com_vinculo"] > 0,
        resumo["valor_transacao_com_vinculo"] / resumo["qtd_contemplados_com_vinculo"],
        0
    )

    return resumo