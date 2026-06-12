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
# import pandas as pd

# import pandas as pd


# def aggregate_vinculo_formal_labor_by_uf(
#     df_cubo: pd.DataFrame,
#     df_rais_uf: pd.DataFrame,
#     col_uf: str = "uf",
#     col_vinculo: str = "tipo_vinculo_agregado_rais",
#     col_quantidade: str = "quantidade",
#     col_valor: str = "valor_transacao",
#     col_uf_rais: str = "uf",
#     col_qtd_rais: str = "qtd_vinculos_formais_rais_2024",
# ) -> pd.DataFrame:
#     """
#     Cria um DataFrame com uma linha por UF, contendo:
#     - quantidade de contemplados PNAB com e sem vínculo formal
#     - valor pago com e sem vínculo formal
#     - percentuais dentro da própria UF
#     - participação da UF no total PNAB
#     - participação da UF no total PNAB por tipo de vínculo
#     - participação da UF no total Brasil da RAIS 2024

#     Regras:
#     - Considera apenas tipo_documento == "CPF"
#     - Sem vínculo formal: tipo_vinculo_agregado_rais missing, nulo ou vazio
#     - Com vínculo formal: tipo_vinculo_agregado_rais preenchido

#     A coluna percentual_vinculos_formais_rais_2024_brasil responde:
#     - De todos os vínculos formais da RAIS 2024 no Brasil, quanto está em cada UF.
#     """

#     required_columns_cubo = [
#         "tipo_documento",
#         col_uf,
#         col_vinculo,
#         col_quantidade,
#         col_valor,
#     ]

#     missing_columns_cubo = [
#         col for col in required_columns_cubo if col not in df_cubo.columns
#     ]

#     if missing_columns_cubo:
#         raise ValueError(
#             f"As seguintes colunas não existem no df_cubo: {missing_columns_cubo}"
#         )

#     required_columns_rais = [
#         col_uf_rais,
#         col_qtd_rais,
#     ]

#     missing_columns_rais = [
#         col for col in required_columns_rais if col not in df_rais_uf.columns
#     ]

#     if missing_columns_rais:
#         raise ValueError(
#             f"As seguintes colunas não existem no df_rais_uf: {missing_columns_rais}"
#         )

#     # ------------------------------------------------------------
#     # 1. Filtra apenas CPF na PNAB
#     # ------------------------------------------------------------
#     df = df_cubo.copy()

#     df = df.loc[
#         df["tipo_documento"].eq("CPF")
#     ].copy()

#     # ------------------------------------------------------------
#     # 2. Classifica vínculo formal na PNAB
#     # ------------------------------------------------------------
#     vinculo_preenchido = (
#         df[col_vinculo].notna()
#         & df[col_vinculo].astype(str).str.strip().ne("")
#     )

#     df["situacao_vinculo_formal"] = "sem_vinculo_trabalho_formal"

#     df.loc[
#         vinculo_preenchido,
#         "situacao_vinculo_formal"
#     ] = "com_vinculo_trabalho_formal"

#     # ------------------------------------------------------------
#     # 3. Agrega PNAB por UF e situação de vínculo
#     # ------------------------------------------------------------
#     resumo = (
#         df
#         .groupby([col_uf, "situacao_vinculo_formal"], dropna=False)
#         .agg(
#             numero_contemplados=(col_quantidade, "sum"),
#             valor_pago=(col_valor, "sum"),
#         )
#         .reset_index()
#     )

#     tabela = (
#         resumo
#         .pivot(
#             index=col_uf,
#             columns="situacao_vinculo_formal",
#             values=["numero_contemplados", "valor_pago"],
#         )
#     )

#     tabela.columns = [
#         f"{metrica}_{situacao}"
#         for metrica, situacao in tabela.columns
#     ]

#     tabela = tabela.reset_index().fillna(0)

#     colunas_esperadas = [
#         "numero_contemplados_sem_vinculo_trabalho_formal",
#         "numero_contemplados_com_vinculo_trabalho_formal",
#         "valor_pago_sem_vinculo_trabalho_formal",
#         "valor_pago_com_vinculo_trabalho_formal",
#     ]

#     for col in colunas_esperadas:
#         if col not in tabela.columns:
#             tabela[col] = 0

#     # ------------------------------------------------------------
#     # 4. Totais PNAB por UF
#     # ------------------------------------------------------------
#     tabela["numero_contemplados_total"] = (
#         tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
#         + tabela["numero_contemplados_com_vinculo_trabalho_formal"]
#     )

#     tabela["valor_pago_total"] = (
#         tabela["valor_pago_sem_vinculo_trabalho_formal"]
#         + tabela["valor_pago_com_vinculo_trabalho_formal"]
#     )

#     # ------------------------------------------------------------
#     # 5. Percentuais PNAB dentro da UF
#     # ------------------------------------------------------------
#     tabela["percentual_contemplados_sem_vinculo_trabalho_formal"] = (
#         tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
#         .div(
#             tabela["numero_contemplados_total"]
#             .where(tabela["numero_contemplados_total"].ne(0))
#         )
#         .fillna(0)
#     )

#     tabela["percentual_contemplados_com_vinculo_trabalho_formal"] = (
#         tabela["numero_contemplados_com_vinculo_trabalho_formal"]
#         .div(
#             tabela["numero_contemplados_total"]
#             .where(tabela["numero_contemplados_total"].ne(0))
#         )
#         .fillna(0)
#     )

#     tabela["percentual_valor_pago_sem_vinculo_trabalho_formal"] = (
#         tabela["valor_pago_sem_vinculo_trabalho_formal"]
#         .div(
#             tabela["valor_pago_total"]
#             .where(tabela["valor_pago_total"].ne(0))
#         )
#         .fillna(0)
#     )

#     tabela["percentual_valor_pago_com_vinculo_trabalho_formal"] = (
#         tabela["valor_pago_com_vinculo_trabalho_formal"]
#         .div(
#             tabela["valor_pago_total"]
#             .where(tabela["valor_pago_total"].ne(0))
#         )
#         .fillna(0)
#     )

#     # ------------------------------------------------------------
#     # 6. Totais Brasil PNAB
#     # ------------------------------------------------------------
#     total_numero_contemplados_brasil = tabela["numero_contemplados_total"].sum()
#     total_valor_pago_brasil = tabela["valor_pago_total"].sum()

#     total_numero_sem_vinculo_brasil = (
#         tabela["numero_contemplados_sem_vinculo_trabalho_formal"].sum()
#     )

#     total_numero_com_vinculo_brasil = (
#         tabela["numero_contemplados_com_vinculo_trabalho_formal"].sum()
#     )

#     total_valor_sem_vinculo_brasil = (
#         tabela["valor_pago_sem_vinculo_trabalho_formal"].sum()
#     )

#     total_valor_com_vinculo_brasil = (
#         tabela["valor_pago_com_vinculo_trabalho_formal"].sum()
#     )

#     # ------------------------------------------------------------
#     # 7. Participações PNAB no total Brasil
#     # ------------------------------------------------------------
#     tabela["percentual_numero_contemplados_no_total_geral"] = (
#         tabela["numero_contemplados_total"] / total_numero_contemplados_brasil
#         if total_numero_contemplados_brasil > 0
#         else 0
#     )

#     tabela["percentual_valor_pago_no_total_geral"] = (
#         tabela["valor_pago_total"] / total_valor_pago_brasil
#         if total_valor_pago_brasil > 0
#         else 0
#     )

#     tabela["percentual_numero_contemplados_sem_vinculo_no_total_geral"] = (
#         tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
#         / total_numero_sem_vinculo_brasil
#         if total_numero_sem_vinculo_brasil > 0
#         else 0
#     )

#     tabela["percentual_numero_contemplados_com_vinculo_no_total_geral"] = (
#         tabela["numero_contemplados_com_vinculo_trabalho_formal"]
#         / total_numero_com_vinculo_brasil
#         if total_numero_com_vinculo_brasil > 0
#         else 0
#     )

#     tabela["percentual_valor_pago_sem_vinculo_no_total_geral"] = (
#         tabela["valor_pago_sem_vinculo_trabalho_formal"]
#         / total_valor_sem_vinculo_brasil
#         if total_valor_sem_vinculo_brasil > 0
#         else 0
#     )

#     tabela["percentual_valor_pago_com_vinculo_no_total_geral"] = (
#         tabela["valor_pago_com_vinculo_trabalho_formal"]
#         / total_valor_com_vinculo_brasil
#         if total_valor_com_vinculo_brasil > 0
#         else 0
#     )

#     # ------------------------------------------------------------
#     # 8. Calcula participação da UF na RAIS 2024 Brasil
#     # ------------------------------------------------------------
#     df_rais = df_rais_uf[[col_uf_rais, col_qtd_rais]].copy()

#     df_rais = df_rais.rename(
#         columns={
#             col_uf_rais: col_uf,
#             col_qtd_rais: "qtd_vinculos_formais_rais_2024",
#         }
#     )

#     total_vinculos_formais_rais_2024_brasil = (
#         df_rais["qtd_vinculos_formais_rais_2024"].sum()
#     )

#     df_rais["percentual_vinculos_formais_rais_2024_brasil"] = (
#         df_rais["qtd_vinculos_formais_rais_2024"]
#         / total_vinculos_formais_rais_2024_brasil
#         if total_vinculos_formais_rais_2024_brasil > 0
#         else 0
#     )

#     # ------------------------------------------------------------
#     # 9. Junta RAIS 2024 na tabela PNAB
#     # ------------------------------------------------------------
#     tabela = tabela.merge(
#         df_rais,
#         on=col_uf,
#         how="left"
#     )

#     tabela[
#         [
#             "qtd_vinculos_formais_rais_2024",
#             "percentual_vinculos_formais_rais_2024_brasil",
#         ]
#     ] = tabela[
#         [
#             "qtd_vinculos_formais_rais_2024",
#             "percentual_vinculos_formais_rais_2024_brasil",
#         ]
#     ].fillna(0)

#     # ------------------------------------------------------------
#     # 10. Ordem final das colunas
#     # ------------------------------------------------------------
#     colunas_finais = [
#         col_uf,

#         "numero_contemplados_sem_vinculo_trabalho_formal",
#         "numero_contemplados_com_vinculo_trabalho_formal",
#         "numero_contemplados_total",

#         "percentual_contemplados_sem_vinculo_trabalho_formal",
#         "percentual_contemplados_com_vinculo_trabalho_formal",
#         "percentual_numero_contemplados_no_total_geral",
#         "percentual_numero_contemplados_sem_vinculo_no_total_geral",
#         "percentual_numero_contemplados_com_vinculo_no_total_geral",

#         "qtd_vinculos_formais_rais_2024",
#         "percentual_vinculos_formais_rais_2024_brasil",

#         "valor_pago_sem_vinculo_trabalho_formal",
#         "valor_pago_com_vinculo_trabalho_formal",
#         "valor_pago_total",

#         "percentual_valor_pago_sem_vinculo_trabalho_formal",
#         "percentual_valor_pago_com_vinculo_trabalho_formal",
#         "percentual_valor_pago_no_total_geral",
#         "percentual_valor_pago_sem_vinculo_no_total_geral",
#         "percentual_valor_pago_com_vinculo_no_total_geral",
#     ]

#     return (
#         tabela[colunas_finais]
#         .sort_values(col_uf)
#         .reset_index(drop=True)
#     )

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



def aggregate_vinculo_formal_labor_by_uf(
    df_cubo: pd.DataFrame,
    col_uf: str = "uf",
    col_vinculo: str = "tipo_vinculo_agregado_rais",
    col_quantidade: str = "quantidade",
    col_valor: str = "valor_transacao",
    col_tipo_documento: str = "tipo_documento",
    col_tipo_ente: str | None = None,
    filtro_tipo_ente: str | None = None,
) -> pd.DataFrame:
    """
    Cria um DataFrame com uma linha por UF, contendo:
    - quantidade de contemplados com e sem vínculo formal
    - valor pago com e sem vínculo formal
    - percentuais dentro da própria UF
    - participação da UF no total geral
    - participação da UF no total geral por tipo de vínculo
    - população IBGE 2024
    - total de vínculos formais RAIS 2024 por UF
    - percentual da população da UF com vínculo formal RAIS 2024

    Regras:
    - Considera apenas CPF
    - Sem vínculo formal: tipo_vinculo_agregado_rais missing, nulo ou vazio
    - Com vínculo formal: tipo_vinculo_agregado_rais preenchido

    Parâmetros opcionais:
    - col_tipo_ente: coluna usada para filtrar tipo de ente, ex.: "tipo_ente" ou "tipo_ente_bbagil"
    - filtro_tipo_ente: valor a ser filtrado, ex.: "ESTADO", "MUNICIPIO"
    """

    df = df_cubo.copy()

    # ------------------------------------------------------------
    # 1. Filtra apenas CPF
    # ------------------------------------------------------------
    df = df[df[col_tipo_documento].eq("CPF")].copy()

    # ------------------------------------------------------------
    # 2. Filtro opcional por tipo de ente
    #    Ex.: col_tipo_ente="tipo_ente", filtro_tipo_ente="ESTADO"
    # ------------------------------------------------------------
    if col_tipo_ente is not None and filtro_tipo_ente is not None:
        df = df[df[col_tipo_ente].eq(filtro_tipo_ente)].copy()

    # ------------------------------------------------------------
    # 3. Classifica com / sem vínculo formal
    # ------------------------------------------------------------
    vinculo_preenchido = (
        df[col_vinculo].notna()
        & df[col_vinculo].astype(str).str.strip().ne("")
    )

    df["situacao_vinculo_formal"] = "sem_vinculo_trabalho_formal"
    df.loc[vinculo_preenchido, "situacao_vinculo_formal"] = "com_vinculo_trabalho_formal"

    # ------------------------------------------------------------
    # 4. Agrega por UF e situação de vínculo
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

    # ------------------------------------------------------------
    # 5. Garante colunas esperadas
    # ------------------------------------------------------------
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
    # 6. Totais
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
    # 7. Percentuais dentro da própria UF
    # ------------------------------------------------------------
    tabela["percentual_contemplados_sem_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_total"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    tabela["percentual_contemplados_com_vinculo_trabalho_formal"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_total"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    tabela["percentual_valor_pago_sem_vinculo_trabalho_formal"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela["valor_pago_total"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    tabela["percentual_valor_pago_com_vinculo_trabalho_formal"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / tabela["valor_pago_total"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    # ------------------------------------------------------------
    # 8. Percentuais no total geral
    # ------------------------------------------------------------
    tabela["percentual_numero_contemplados_no_total_geral"] = (
        tabela["numero_contemplados_total"]
        / tabela["numero_contemplados_total"].sum()
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    tabela["percentual_valor_pago_no_total_geral"] = (
        tabela["valor_pago_total"]
        / tabela["valor_pago_total"].sum()
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    tabela["percentual_numero_contemplados_sem_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_sem_vinculo_trabalho_formal"].sum()
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    tabela["percentual_numero_contemplados_com_vinculo_no_total_geral"] = (
        tabela["numero_contemplados_com_vinculo_trabalho_formal"]
        / tabela["numero_contemplados_com_vinculo_trabalho_formal"].sum()
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    tabela["percentual_valor_pago_sem_vinculo_no_total_geral"] = (
        tabela["valor_pago_sem_vinculo_trabalho_formal"]
        / tabela["valor_pago_sem_vinculo_trabalho_formal"].sum()
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    tabela["percentual_valor_pago_com_vinculo_no_total_geral"] = (
        tabela["valor_pago_com_vinculo_trabalho_formal"]
        / tabela["valor_pago_com_vinculo_trabalho_formal"].sum()
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    # ------------------------------------------------------------
    # 9. Base externa: população IBGE 2024 + vínculos RAIS 2024
    # ------------------------------------------------------------
    df_pop_vinculos_uf = pd.DataFrame({
        "codigo_uf": [
            11, 12, 13, 14, 15, 16, 17,
            21, 22, 23, 24, 25, 26, 27, 28, 29,
            31, 32, 33, 35,
            41, 42, 43,
            50, 51, 52, 53
        ],
        "uf": [
            "RO", "AC", "AM", "RR", "PA", "AP", "TO",
            "MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA",
            "MG", "ES", "RJ", "SP",
            "PR", "SC", "RS",
            "MS", "MT", "GO", "DF"
        ],
        "unidade_da_federacao": [
            "Rondônia", "Acre", "Amazonas", "Roraima", "Pará", "Amapá", "Tocantins",
            "Maranhão", "Piauí", "Ceará", "Rio Grande do Norte", "Paraíba",
            "Pernambuco", "Alagoas", "Sergipe", "Bahia",
            "Minas Gerais", "Espírito Santo", "Rio de Janeiro", "São Paulo",
            "Paraná", "Santa Catarina", "Rio Grande do Sul",
            "Mato Grosso do Sul", "Mato Grosso", "Goiás", "Distrito Federal"
        ],
        "populacao_ibge_2024": [
            1746227, 880631, 4281209, 716793, 8664306, 802837, 1577342,
            7010960, 3375646, 9233656, 3446071, 4145040, 9539029, 3220104,
            2291077, 14850513,
            21322691, 4102129, 17219679, 45973194,
            11824665, 8058441, 11229915,
            2901895, 3836399, 7350483, 2982818
        ],
        "total_vinculos_a_rais_2024": [
            413955, 180093, 801349, 148049, 1445663, 154926, 408312,
            977685, 568830, 1871093, 709350, 811007, 1919501, 636259,
            467807, 2774157,
            6094585, 1101019, 4744216, 15994587,
            3717135, 2863776, 3287525,
            831160, 1209870, 1950312, 1707305
        ],
    })

    df_pop_vinculos_uf["percentual_populacao_com_vinculo_rais_2024"] = (
        df_pop_vinculos_uf["total_vinculos_a_rais_2024"]
        / df_pop_vinculos_uf["populacao_ibge_2024"]
    )

    # ------------------------------------------------------------
    # 10. Cria chave de UF robusta
    #     Funciona se col_uf vier como:
    #     - sigla: "SP"
    #     - código IBGE: 35
    #     - nome: "São Paulo"
    # ------------------------------------------------------------
    mapa_nome_para_sigla = dict(
        zip(
            df_pop_vinculos_uf["unidade_da_federacao"],
            df_pop_vinculos_uf["uf"]
        )
    )

    mapa_codigo_para_sigla = dict(
        zip(
            df_pop_vinculos_uf["codigo_uf"].astype(str),
            df_pop_vinculos_uf["uf"]
        )
    )

    def normaliza_uf(valor):
        if pd.isna(valor):
            return np.nan

        valor_str = str(valor).strip()

        # Caso seja código IBGE como 35, 35.0 ou "35"
        valor_codigo = valor_str.replace(".0", "")
        if valor_codigo in mapa_codigo_para_sigla:
            return mapa_codigo_para_sigla[valor_codigo]

        # Caso seja nome da UF
        if valor_str in mapa_nome_para_sigla:
            return mapa_nome_para_sigla[valor_str]

        # Caso já seja sigla
        return valor_str.upper()

    tabela["uf_merge"] = tabela[col_uf].apply(normaliza_uf)

    df_pop_vinculos_uf_merge = df_pop_vinculos_uf.rename(
        columns={"uf": "uf_merge"}
    )

    tabela = tabela.merge(
        df_pop_vinculos_uf_merge,
        how="left",
        on="uf_merge"
    )

    tabela = tabela.drop(columns=["uf_merge"], errors="ignore")

    # ------------------------------------------------------------
    # 11. Comparações entre a PNAB e a proporção geral da UF
    # ------------------------------------------------------------
    tabela["diferenca_pp_contemplados_com_vinculo_vs_populacao_uf"] = (
        tabela["percentual_contemplados_com_vinculo_trabalho_formal"]
        - tabela["percentual_populacao_com_vinculo_rais_2024"]
    )

    tabela["razao_contemplados_com_vinculo_vs_populacao_uf"] = (
        tabela["percentual_contemplados_com_vinculo_trabalho_formal"]
        / tabela["percentual_populacao_com_vinculo_rais_2024"]
    ).replace([np.inf, -np.inf], np.nan).fillna(0)

    # ------------------------------------------------------------
    # 12. Ordem final das colunas
    # ------------------------------------------------------------
    colunas_finais = [
        col_uf,
        "codigo_uf",
        "unidade_da_federacao",

        "populacao_ibge_2024",
        "total_vinculos_a_rais_2024",
        "percentual_populacao_com_vinculo_rais_2024",

        "numero_contemplados_sem_vinculo_trabalho_formal",
        "numero_contemplados_com_vinculo_trabalho_formal",
        "numero_contemplados_total",

        "percentual_contemplados_sem_vinculo_trabalho_formal",
        "percentual_contemplados_com_vinculo_trabalho_formal",

        "diferenca_pp_contemplados_com_vinculo_vs_populacao_uf",
        "razao_contemplados_com_vinculo_vs_populacao_uf",

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

# def aggregate_vinculo_formal_labor_by_uf(
#     df_cubo: pd.DataFrame,
#     df_rais_uf: pd.DataFrame,
#     col_uf: str = "uf",
#     col_vinculo: str = "tipo_vinculo_agregado_rais",
#     col_quantidade: str = "quantidade",
#     col_valor: str = "valor_transacao",
#     col_uf_rais: str = "uf",
#     col_qtd_rais: str = "qtd_vinculos_formais_rais_2024",
# ) -> pd.DataFrame:
#     """
#     Cria um DataFrame com uma linha por UF, contendo:
#     - quantidade de contemplados PNAB com e sem vínculo formal
#     - valor pago com e sem vínculo formal
#     - percentuais dentro da própria UF
#     - participação da UF no total PNAB
#     - participação da UF no total PNAB por tipo de vínculo
#     - participação da UF no total Brasil da RAIS 2024

#     Regras:
#     - Considera apenas tipo_documento == "CPF"
#     - Sem vínculo formal: tipo_vinculo_agregado_rais missing, nulo ou vazio
#     - Com vínculo formal: tipo_vinculo_agregado_rais preenchido

#     A coluna percentual_vinculos_formais_rais_2024_brasil responde:
#     - De todos os vínculos formais da RAIS 2024 no Brasil, quanto está em cada UF.
#     """

#     required_columns_cubo = [
#         "tipo_documento",
#         col_uf,
#         col_vinculo,
#         col_quantidade,
#         col_valor,
#     ]

#     missing_columns_cubo = [
#         col for col in required_columns_cubo if col not in df_cubo.columns
#     ]

#     if missing_columns_cubo:
#         raise ValueError(
#             f"As seguintes colunas não existem no df_cubo: {missing_columns_cubo}"
#         )

#     required_columns_rais = [
#         col_uf_rais,
#         col_qtd_rais,
#     ]

#     missing_columns_rais = [
#         col for col in required_columns_rais if col not in df_rais_uf.columns
#     ]

#     if missing_columns_rais:
#         raise ValueError(
#             f"As seguintes colunas não existem no df_rais_uf: {missing_columns_rais}"
#         )

#     # ------------------------------------------------------------
#     # 1. Filtra apenas CPF na PNAB
#     # ------------------------------------------------------------
#     df = df_cubo.copy()

#     df = df.loc[
#         df["tipo_documento"].eq("CPF")
#     ].copy()

#     # ------------------------------------------------------------
#     # 2. Classifica vínculo formal na PNAB
#     # ------------------------------------------------------------
#     vinculo_preenchido = (
#         df[col_vinculo].notna()
#         & df[col_vinculo].astype(str).str.strip().ne("")
#     )

#     df["situacao_vinculo_formal"] = "sem_vinculo_trabalho_formal"

#     df.loc[
#         vinculo_preenchido,
#         "situacao_vinculo_formal"
#     ] = "com_vinculo_trabalho_formal"

#     # ------------------------------------------------------------
#     # 3. Agrega PNAB por UF e situação de vínculo
#     # ------------------------------------------------------------
#     resumo = (
#         df
#         .groupby([col_uf, "situacao_vinculo_formal"], dropna=False)
#         .agg(
#             numero_contemplados=(col_quantidade, "sum"),
#             valor_pago=(col_valor, "sum"),
#         )
#         .reset_index()
#     )

#     tabela = (
#         resumo
#         .pivot(
#             index=col_uf,
#             columns="situacao_vinculo_formal",
#             values=["numero_contemplados", "valor_pago"],
#         )
#     )

#     tabela.columns = [
#         f"{metrica}_{situacao}"
#         for metrica, situacao in tabela.columns
#     ]

#     tabela = tabela.reset_index().fillna(0)

#     colunas_esperadas = [
#         "numero_contemplados_sem_vinculo_trabalho_formal",
#         "numero_contemplados_com_vinculo_trabalho_formal",
#         "valor_pago_sem_vinculo_trabalho_formal",
#         "valor_pago_com_vinculo_trabalho_formal",
#     ]

#     for col in colunas_esperadas:
#         if col not in tabela.columns:
#             tabela[col] = 0

#     # ------------------------------------------------------------
#     # 4. Totais PNAB por UF
#     # ------------------------------------------------------------
#     tabela["numero_contemplados_total"] = (
#         tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
#         + tabela["numero_contemplados_com_vinculo_trabalho_formal"]
#     )

#     tabela["valor_pago_total"] = (
#         tabela["valor_pago_sem_vinculo_trabalho_formal"]
#         + tabela["valor_pago_com_vinculo_trabalho_formal"]
#     )

#     # ------------------------------------------------------------
#     # 5. Percentuais PNAB dentro da UF
#     # ------------------------------------------------------------
#     tabela["percentual_contemplados_sem_vinculo_trabalho_formal"] = (
#         tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
#         .div(
#             tabela["numero_contemplados_total"]
#             .where(tabela["numero_contemplados_total"].ne(0))
#         )
#         .fillna(0)
#     )

#     tabela["percentual_contemplados_com_vinculo_trabalho_formal"] = (
#         tabela["numero_contemplados_com_vinculo_trabalho_formal"]
#         .div(
#             tabela["numero_contemplados_total"]
#             .where(tabela["numero_contemplados_total"].ne(0))
#         )
#         .fillna(0)
#     )

#     tabela["percentual_valor_pago_sem_vinculo_trabalho_formal"] = (
#         tabela["valor_pago_sem_vinculo_trabalho_formal"]
#         .div(
#             tabela["valor_pago_total"]
#             .where(tabela["valor_pago_total"].ne(0))
#         )
#         .fillna(0)
#     )

#     tabela["percentual_valor_pago_com_vinculo_trabalho_formal"] = (
#         tabela["valor_pago_com_vinculo_trabalho_formal"]
#         .div(
#             tabela["valor_pago_total"]
#             .where(tabela["valor_pago_total"].ne(0))
#         )
#         .fillna(0)
#     )

#     # ------------------------------------------------------------
#     # 6. Totais Brasil PNAB
#     # ------------------------------------------------------------
#     total_numero_contemplados_brasil = tabela["numero_contemplados_total"].sum()
#     total_valor_pago_brasil = tabela["valor_pago_total"].sum()

#     total_numero_sem_vinculo_brasil = (
#         tabela["numero_contemplados_sem_vinculo_trabalho_formal"].sum()
#     )

#     total_numero_com_vinculo_brasil = (
#         tabela["numero_contemplados_com_vinculo_trabalho_formal"].sum()
#     )

#     total_valor_sem_vinculo_brasil = (
#         tabela["valor_pago_sem_vinculo_trabalho_formal"].sum()
#     )

#     total_valor_com_vinculo_brasil = (
#         tabela["valor_pago_com_vinculo_trabalho_formal"].sum()
#     )

#     # ------------------------------------------------------------
#     # 7. Participações PNAB no total Brasil
#     # ------------------------------------------------------------
#     tabela["percentual_numero_contemplados_no_total_geral"] = (
#         tabela["numero_contemplados_total"] / total_numero_contemplados_brasil
#         if total_numero_contemplados_brasil > 0
#         else 0
#     )

#     tabela["percentual_valor_pago_no_total_geral"] = (
#         tabela["valor_pago_total"] / total_valor_pago_brasil
#         if total_valor_pago_brasil > 0
#         else 0
#     )

#     tabela["percentual_numero_contemplados_sem_vinculo_no_total_geral"] = (
#         tabela["numero_contemplados_sem_vinculo_trabalho_formal"]
#         / total_numero_sem_vinculo_brasil
#         if total_numero_sem_vinculo_brasil > 0
#         else 0
#     )

#     tabela["percentual_numero_contemplados_com_vinculo_no_total_geral"] = (
#         tabela["numero_contemplados_com_vinculo_trabalho_formal"]
#         / total_numero_com_vinculo_brasil
#         if total_numero_com_vinculo_brasil > 0
#         else 0
#     )

#     tabela["percentual_valor_pago_sem_vinculo_no_total_geral"] = (
#         tabela["valor_pago_sem_vinculo_trabalho_formal"]
#         / total_valor_sem_vinculo_brasil
#         if total_valor_sem_vinculo_brasil > 0
#         else 0
#     )

#     tabela["percentual_valor_pago_com_vinculo_no_total_geral"] = (
#         tabela["valor_pago_com_vinculo_trabalho_formal"]
#         / total_valor_com_vinculo_brasil
#         if total_valor_com_vinculo_brasil > 0
#         else 0
#     )

#     # ------------------------------------------------------------
#     # 8. Calcula participação da UF na RAIS 2024 Brasil
#     # ------------------------------------------------------------
#     df_rais = df_rais_uf[[col_uf_rais, col_qtd_rais]].copy()

#     df_rais = df_rais.rename(
#         columns={
#             col_uf_rais: col_uf,
#             col_qtd_rais: "qtd_vinculos_formais_rais_2024",
#         }
#     )

#     total_vinculos_formais_rais_2024_brasil = (
#         df_rais["qtd_vinculos_formais_rais_2024"].sum()
#     )

#     df_rais["percentual_vinculos_formais_rais_2024_brasil"] = (
#         df_rais["qtd_vinculos_formais_rais_2024"]
#         / total_vinculos_formais_rais_2024_brasil
#         if total_vinculos_formais_rais_2024_brasil > 0
#         else 0
#     )

#     # ------------------------------------------------------------
#     # 9. Junta RAIS 2024 na tabela PNAB
#     # ------------------------------------------------------------
#     tabela = tabela.merge(
#         df_rais,
#         on=col_uf,
#         how="left"
#     )

#     tabela[
#         [
#             "qtd_vinculos_formais_rais_2024",
#             "percentual_vinculos_formais_rais_2024_brasil",
#         ]
#     ] = tabela[
#         [
#             "qtd_vinculos_formais_rais_2024",
#             "percentual_vinculos_formais_rais_2024_brasil",
#         ]
#     ].fillna(0)

#     # ------------------------------------------------------------
#     # 10. Ordem final das colunas
#     # ------------------------------------------------------------
#     colunas_finais = [
#         col_uf,

#         "numero_contemplados_sem_vinculo_trabalho_formal",
#         "numero_contemplados_com_vinculo_trabalho_formal",
#         "numero_contemplados_total",

#         "percentual_contemplados_sem_vinculo_trabalho_formal",
#         "percentual_contemplados_com_vinculo_trabalho_formal",
#         "percentual_numero_contemplados_no_total_geral",
#         "percentual_numero_contemplados_sem_vinculo_no_total_geral",
#         "percentual_numero_contemplados_com_vinculo_no_total_geral",

#         "qtd_vinculos_formais_rais_2024",
#         "percentual_vinculos_formais_rais_2024_brasil",

#         "valor_pago_sem_vinculo_trabalho_formal",
#         "valor_pago_com_vinculo_trabalho_formal",
#         "valor_pago_total",

#         "percentual_valor_pago_sem_vinculo_trabalho_formal",
#         "percentual_valor_pago_com_vinculo_trabalho_formal",
#         "percentual_valor_pago_no_total_geral",
#         "percentual_valor_pago_sem_vinculo_no_total_geral",
#         "percentual_valor_pago_com_vinculo_no_total_geral",
#     ]

#     return (
#         tabela[colunas_finais]
#         .sort_values(col_uf)
#         .reset_index(drop=True)
#     )



def aggregate_vinculo_formal_cpf(
    df_cubo: pd.DataFrame,
    coluna_tipo_documento: str = "tipo_documento",
    coluna_vinculo: str = "tipo_vinculo_description",
    coluna_valor: str = "valor_transacao",
    coluna_quantidade: str = "quantidade",
) -> pd.DataFrame:
    """
    Agrega contemplados CPF segundo presença ou ausência de vínculo formal.

    Regras:
    - considera apenas tipo_documento == CPF;
    - cria flag_vinculo_formal:
        True  = tipo_vinculo_description preenchido;
        False = tipo_vinculo_description vazio/nulo;
    - quantidade de contemplados = soma da coluna quantidade;
    - valor pago = soma da coluna valor_transacao.
    """

    df = df_cubo.copy()

    # Filtra apenas CPF
    df = df.loc[
        df[coluna_tipo_documento].astype(str).str.upper().eq("CPF")
    ].copy()

    # Garante valores numéricos
    df[coluna_valor] = pd.to_numeric(df[coluna_valor], errors="coerce").fillna(0)
    df[coluna_quantidade] = pd.to_numeric(df[coluna_quantidade], errors="coerce").fillna(0)

    # Cria flag de vínculo formal
    vinculo_norm = (
        df[coluna_vinculo]
        .astype("string")
        .str.strip()
    )

    df["flag_vinculo_formal"] = (
        vinculo_norm.notna()
        & ~vinculo_norm.eq("")
        & ~vinculo_norm.str.upper().eq("VAZIO")
    )

    # Agregações
    numero_com_vinculo = df.loc[
        df["flag_vinculo_formal"],
        coluna_quantidade
    ].sum()

    numero_sem_vinculo = df.loc[
        ~df["flag_vinculo_formal"],
        coluna_quantidade
    ].sum()

    valor_com_vinculo = df.loc[
        df["flag_vinculo_formal"],
        coluna_valor
    ].sum()

    valor_sem_vinculo = df.loc[
        ~df["flag_vinculo_formal"],
        coluna_valor
    ].sum()

    numero_total = numero_com_vinculo + numero_sem_vinculo
    valor_total = valor_com_vinculo + valor_sem_vinculo

    resultado = pd.DataFrame({
        "numero_contemplados_sem_vinculo_trabalho_formal": [numero_sem_vinculo],
        "numero_contemplados_com_vinculo_trabalho_formal": [numero_com_vinculo],
        "numero_contemplados_total": [numero_total],

        "percentual_contemplados_sem_vinculo_trabalho_formal": [
            numero_sem_vinculo / numero_total if numero_total != 0 else 0
        ],
        "percentual_contemplados_com_vinculo_trabalho_formal": [
            numero_com_vinculo / numero_total if numero_total != 0 else 0
        ],

        "valor_pago_sem_vinculo_trabalho_formal": [valor_sem_vinculo],
        "valor_pago_com_vinculo_trabalho_formal": [valor_com_vinculo],
        "valor_pago_total": [valor_total],

        "percentual_valor_pago_sem_vinculo_trabalho_formal": [
            valor_sem_vinculo / valor_total if valor_total != 0 else 0
        ],
        "percentual_valor_pago_com_vinculo_trabalho_formal": [
            valor_com_vinculo / valor_total if valor_total != 0 else 0
        ],
    })

    return resultado