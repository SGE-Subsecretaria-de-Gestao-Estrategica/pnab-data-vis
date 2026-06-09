import pandas as pd

import pandas as pd


def aggregate_cadunico_summary(
    df_cubo: pd.DataFrame,
    qtd_documentos_unicos_cadunico: int = 57_338,
    corte_media_aparada: float = 0.01,
) -> pd.DataFrame:
    """
    Resume a participação de contemplados CPF que estão no CadÚnico.

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera como CadÚnico pessoaCad_cadunico == 1.0
    - Usa a coluna quantidade como número de contemplados
    - Usa a coluna valor_transacao como valor recebido
    - O número de documentos únicos no CadÚnico é informado externamente,
      pois não está disponível em df_cubo.

    Métricas de média:
    - media_valor_recebido_cadunico:
        valor total recebido pelo público CadÚnico / quantidade de contemplados CadÚnico

    - media_aparada_valor_recebido_cadunico:
        média ponderada pelo número de contemplados, removendo o topo da distribuição
        conforme corte_media_aparada. Por padrão, remove o 1% superior.

    Retorna uma tabela com uma linha.
    """

    required_columns = [
        "tipo_documento",
        "pessoaCad_cadunico",
        "quantidade",
        "valor_transacao",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    def calcular_media_aparada_ponderada(
        df: pd.DataFrame,
        col_valor_medio: str,
        col_peso: str,
        corte_superior: float = 0.01,
    ) -> float:
        """
        Calcula média aparada ponderada, removendo o topo da distribuição.

        Exemplo:
        - corte_superior = 0.01 remove o 1% superior.
        """

        df_aux = df[[col_valor_medio, col_peso]].dropna().copy()

        df_aux = df_aux.loc[
            df_aux[col_peso].gt(0)
        ].copy()

        if df_aux.empty:
            return 0

        total_peso = df_aux[col_peso].sum()

        if total_peso <= 0:
            return 0

        limite_peso = total_peso * (1 - corte_superior)

        df_aux = df_aux.sort_values(col_valor_medio).reset_index(drop=True)
        df_aux["peso_acumulado"] = df_aux[col_peso].cumsum()

        valor_corte = df_aux.loc[
            df_aux["peso_acumulado"].ge(limite_peso),
            col_valor_medio,
        ].iloc[0]

        df_aparado = df_aux.loc[
            df_aux[col_valor_medio].le(valor_corte)
        ].copy()

        peso_aparado = df_aparado[col_peso].sum()

        if peso_aparado <= 0:
            return 0

        return (
            df_aparado[col_valor_medio]
            .mul(df_aparado[col_peso])
            .sum()
            / peso_aparado
        )

    # ------------------------------------------------------------
    # 1. Filtra apenas CPF
    # ------------------------------------------------------------
    df_cpf = df_cubo.loc[
        df_cubo["tipo_documento"].eq("CPF")
    ].copy()

    # ------------------------------------------------------------
    # 2. Filtra CPF no CadÚnico
    # ------------------------------------------------------------
    df_cpf_cadunico = df_cpf.loc[
        df_cpf["pessoaCad_cadunico"].eq(1.0)
    ].copy()

    # ------------------------------------------------------------
    # 3. Totais gerais de CPF
    # ------------------------------------------------------------
    total_contemplados_cpf = df_cpf["quantidade"].sum()
    total_valor_cpf = df_cpf["valor_transacao"].sum()

    # ------------------------------------------------------------
    # 4. Totais CadÚnico
    # ------------------------------------------------------------
    qtd_contemplados_cadunico = df_cpf_cadunico["quantidade"].sum()
    valor_recebido_cadunico = df_cpf_cadunico["valor_transacao"].sum()

    # ------------------------------------------------------------
    # 5. Percentuais
    # ------------------------------------------------------------
    perc_contemplados_cadunico = (
        qtd_contemplados_cadunico / total_contemplados_cpf
        if total_contemplados_cpf > 0
        else 0
    )

    perc_valor_cadunico = (
        valor_recebido_cadunico / total_valor_cpf
        if total_valor_cpf > 0
        else 0
    )

    # ------------------------------------------------------------
    # 6. Média simples do valor recebido pelo público CadÚnico
    # ------------------------------------------------------------
    media_valor_recebido_cadunico = (
        valor_recebido_cadunico / qtd_contemplados_cadunico
        if qtd_contemplados_cadunico > 0
        else 0
    )

    # ------------------------------------------------------------
    # 7. Média aparada do valor recebido pelo público CadÚnico
    # ------------------------------------------------------------
    df_cpf_cadunico["valor_medio_por_contemplado_linha"] = (
        df_cpf_cadunico["valor_transacao"]
        .div(
            df_cpf_cadunico["quantidade"]
            .where(df_cpf_cadunico["quantidade"].ne(0))
        )
        .fillna(0)
    )

    media_aparada_valor_recebido_cadunico = calcular_media_aparada_ponderada(
        df=df_cpf_cadunico,
        col_valor_medio="valor_medio_por_contemplado_linha",
        col_peso="quantidade",
        corte_superior=corte_media_aparada,
    )

    # ------------------------------------------------------------
    # 8. Resultado final
    # ------------------------------------------------------------
    df_resultado = pd.DataFrame(
        {
            "perc_contemplados_cadunico": [perc_contemplados_cadunico],
            "qtd_contemplados_cadunico": [qtd_contemplados_cadunico],
            "qtd_documentos_unicos_cadunico": [qtd_documentos_unicos_cadunico],
            "valor_recebido_cadunico": [valor_recebido_cadunico],
            "perc_valor_cadunico": [perc_valor_cadunico],
            "media_valor_recebido_cadunico": [media_valor_recebido_cadunico],
            "media_aparada_valor_recebido_cadunico": [
                media_aparada_valor_recebido_cadunico
            ],
        }
    )

    return df_resultado

def aggregate_cadunico_profile_summary(df_cubo: pd.DataFrame) -> pd.DataFrame:
    """
    Gera um resumo do perfil dos contemplados CPF que estão no CadÚnico.

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera apenas pessoaCad_cadunico == 1.0
    - Usa a coluna quantidade como número de contemplados
    - Calcula percentuais sobre o total de contemplados CPF no CadÚnico

    Retorna um DataFrame com:
    - dimensão analisada
    - categoria
    - soma_quantidade
    - percentual_contemplados_cadunico
    """

    required_columns = [
        "tipo_documento",
        "pessoaCad_cadunico",
        "Sexo",
        "faixa_etaria",
        "quantidade",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    df_cadunico = df_cubo.loc[
        (df_cubo["tipo_documento"].eq("CPF"))
        & (df_cubo["pessoaCad_cadunico"].eq(1.0))
    ].copy()

    total_contemplados_cadunico = df_cadunico["quantidade"].sum()

    df_sexo = (
        df_cadunico
        .loc[df_cadunico["Sexo"].isin(["Feminino", "Masculino"])]
        .groupby("Sexo", dropna=False)
        .agg(soma_quantidade=("quantidade", "sum"))
        .reset_index()
        .rename(columns={"Sexo": "categoria"})
    )

    df_sexo["dimensao"] = "Sexo"

    faixas_ordenadas = [
        "15-24 anos",
        "25-54 anos",
        "55-64 anos",
        "65+ anos",
    ]

    df_faixa_etaria = (
        df_cadunico
        .loc[df_cadunico["faixa_etaria"].isin(faixas_ordenadas)]
        .groupby("faixa_etaria", dropna=False)
        .agg(soma_quantidade=("quantidade", "sum"))
        .reset_index()
        .rename(columns={"faixa_etaria": "categoria"})
    )

    df_faixa_etaria["dimensao"] = "Faixa etária"

    df_resultado = pd.concat(
        [df_sexo, df_faixa_etaria],
        ignore_index=True
    )

    df_resultado["percentual_contemplados_cadunico"] = (
        df_resultado["soma_quantidade"] / total_contemplados_cadunico
        if total_contemplados_cadunico > 0
        else 0
    )

    df_resultado["categoria"] = pd.Categorical(
        df_resultado["categoria"],
        categories=["Feminino", "Masculino"] + faixas_ordenadas,
        ordered=True
    )

    df_resultado = (
        df_resultado
        .sort_values(["dimensao", "categoria"])
        .reset_index(drop=True)
    )

    return df_resultado[
        [
            "dimensao",
            "categoria",
            "soma_quantidade",
            "percentual_contemplados_cadunico",
        ]
    ]


def aggregate_cadunico_faixa_etaria_by_sexo(df_cubo: pd.DataFrame) -> pd.DataFrame:
    """
    Para cada faixa etária, calcula valor recebido e quantidade de contemplados
    por sexo entre contemplados CPF que estão no CadÚnico.

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera apenas pessoaCad_cadunico == 1.0
    - Considera apenas Sexo == "Feminino" ou "Masculino"
    - Usa quantidade como número de contemplados
    - Usa valor_transacao como valor recebido

    Os percentuais são calculados dentro de cada faixa etária.
    Ou seja, em cada linha, Feminino + Masculino = 100%, salvo ausência de dados.
    """

    required_columns = [
        "tipo_documento",
        "pessoaCad_cadunico",
        "faixa_etaria",
        "Sexo",
        "quantidade",
        "valor_transacao",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    faixas_ordenadas = [
        "15-24 anos",
        "25-54 anos",
        "55-64 anos",
        "65+ anos",
    ]

    sexos_validos = ["Feminino", "Masculino"]

    df = df_cubo.loc[
        (df_cubo["tipo_documento"].eq("CPF"))
        & (df_cubo["pessoaCad_cadunico"].eq(1.0))
        & (df_cubo["Sexo"].isin(sexos_validos))
        & (df_cubo["faixa_etaria"].isin(faixas_ordenadas))
    ].copy()

    df_agg = (
        df
        .groupby(["faixa_etaria", "Sexo"], dropna=False)
        .agg(
            quantidade=("quantidade", "sum"),
            valor=("valor_transacao", "sum"),
        )
        .reset_index()
    )

    df_pivot = (
        df_agg
        .pivot_table(
            index="faixa_etaria",
            columns="Sexo",
            values=["quantidade", "valor"],
            aggfunc="sum",
            fill_value=0,
        )
    )

    df_pivot.columns = [
        f"{metrica}_{sexo.lower()}"
        for metrica, sexo in df_pivot.columns
    ]

    df_pivot = df_pivot.reset_index()

    for sexo in ["feminino", "masculino"]:
        if f"quantidade_{sexo}" not in df_pivot.columns:
            df_pivot[f"quantidade_{sexo}"] = 0

        if f"valor_{sexo}" not in df_pivot.columns:
            df_pivot[f"valor_{sexo}"] = 0

    df_pivot["total_quantidade_faixa_etaria"] = (
        df_pivot["quantidade_feminino"]
        + df_pivot["quantidade_masculino"]
    )

    df_pivot["total_valor_faixa_etaria"] = (
        df_pivot["valor_feminino"]
        + df_pivot["valor_masculino"]
    )

    df_pivot["perc_quantidade_feminino"] = (
        df_pivot["quantidade_feminino"]
        / df_pivot["total_quantidade_faixa_etaria"]
    ).fillna(0)

    df_pivot["perc_quantidade_masculino"] = (
        df_pivot["quantidade_masculino"]
        / df_pivot["total_quantidade_faixa_etaria"]
    ).fillna(0)

    df_pivot["perc_valor_feminino"] = (
        df_pivot["valor_feminino"]
        / df_pivot["total_valor_faixa_etaria"]
    ).fillna(0)

    df_pivot["perc_valor_masculino"] = (
        df_pivot["valor_masculino"]
        / df_pivot["total_valor_faixa_etaria"]
    ).fillna(0)

    df_pivot["faixa_etaria"] = pd.Categorical(
        df_pivot["faixa_etaria"],
        categories=faixas_ordenadas,
        ordered=True,
    )

    df_resultado = (
        df_pivot
        .sort_values("faixa_etaria")
        .reset_index(drop=True)
    )

    return df_resultado[
        [
            "faixa_etaria",
            "valor_feminino",
            "perc_valor_feminino",
            "quantidade_feminino",
            "perc_quantidade_feminino",
            "valor_masculino",
            "perc_valor_masculino",
            "quantidade_masculino",
            "perc_quantidade_masculino",
            "total_valor_faixa_etaria",
            "total_quantidade_faixa_etaria",
        ]
    ]


def aggregate_cadunico_by_situacao_renda(df_cubo: pd.DataFrame, tipo_agg: str = 'situacao_renda_cadunico') -> pd.DataFrame:
    """
    Agrega quantidade de contemplados e valor recebido por situação de renda
    entre contemplados CPF que estão no CadÚnico.

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera apenas pessoaCad_cadunico == 1.0
    - Considera apenas as categorias válidas de situacao_renda_cadunico
    - Usa quantidade como número de contemplados
    - Usa valor_transacao como valor recebido
    """

    required_columns = [
        "tipo_documento",
        "pessoaCad_cadunico",
        tipo_agg,
        "quantidade",
        "valor_transacao",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    categorias_validas = [
        "Pobreza",
        "Baixa renda",
        "Acima de 1/2 salário mínimo",
    ]

    df = df_cubo.loc[
        (df_cubo["tipo_documento"].eq("CPF"))
        & (df_cubo["pessoaCad_cadunico"].eq(1.0))
        & (df_cubo[tipo_agg].isin(categorias_validas))
    ].copy()

    df_resultado = (
        df
        .groupby(tipo_agg, dropna=False)
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

    df_resultado[tipo_agg] = pd.Categorical(
        df_resultado[tipo_agg],
        categories=categorias_validas,
        ordered=True,
    )

    df_resultado = (
        df_resultado
        .sort_values(tipo_agg)
        .reset_index(drop=True)
    )

    return df_resultado[
        [
            tipo_agg,
            "soma_quantidade",
            "percentual_quantidade",
            "soma_valor",
            "percentual_valor",
        ]
    ]


def aggregate_cadunico_by_fx_renda_per_capita(df_cubo: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega quantidade de contemplados e valor recebido por faixa de renda per capita
    entre contemplados CPF que estão no CadÚnico.

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera apenas pessoaCad_cadunico == 1.0
    - Considera apenas as categorias válidas de fxRendaPerCapita_desc_cadunico
    - Usa quantidade como número de contemplados
    - Usa valor_transacao como valor recebido
    """

    required_columns = [
        "tipo_documento",
        "pessoaCad_cadunico",
        "fxRendaPerCapita_desc_cadunico",
        "quantidade",
        "valor_transacao",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    categorias_validas = [
        "De 0 até R$ 109",
        "De R$ 109,01 até R$ 218",
        "De R$ 218,01 até meio salário mínimo",
        "De meio salário mínimo a um salário mínimo",
        "Superior a um salário mínimo",
    ]

    df = df_cubo.loc[
        (df_cubo["tipo_documento"].eq("CPF"))
        & (df_cubo["pessoaCad_cadunico"].eq(1.0))
        & (df_cubo["fxRendaPerCapita_desc_cadunico"].isin(categorias_validas))
    ].copy()

    df_resultado = (
        df
        .groupby("fxRendaPerCapita_desc_cadunico", dropna=False)
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

    df_resultado["fxRendaPerCapita_desc_cadunico"] = pd.Categorical(
        df_resultado["fxRendaPerCapita_desc_cadunico"],
        categories=categorias_validas,
        ordered=True,
    )

    df_resultado = (
        df_resultado
        .sort_values("fxRendaPerCapita_desc_cadunico")
        .reset_index(drop=True)
    )

    return df_resultado[
        [
            "fxRendaPerCapita_desc_cadunico",
            "soma_quantidade",
            "percentual_quantidade",
            "soma_valor",
            "percentual_valor",
        ]
    ]


def aggregate_cadunico_by_situacao_domicilio(df_cubo: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega quantidade de contemplados e valor recebido por situação do domicílio
    entre contemplados CPF que estão no CadÚnico.

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera apenas pessoaCad_cadunico == 1.0
    - Usa quantidade como número de contemplados
    - Usa valor_transacao como valor recebido
    - Valores NaN em SITUACAO são contabilizados como "Não informado"
    """

    required_columns = [
        "tipo_documento",
        "pessoaCad_cadunico",
        "SITUACAO",
        "quantidade",
        "valor_transacao",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    categorias_ordenadas = [
        "Urbana",
        "Rural",
        "Não informado",
    ]

    df = df_cubo.loc[
        (df_cubo["tipo_documento"].eq("CPF"))
        & (df_cubo["pessoaCad_cadunico"].eq(1.0))
    ].copy()

    df["SITUACAO"] = df["SITUACAO"].fillna("Não informado")

    df = df.loc[
        df["SITUACAO"].isin(categorias_ordenadas)
    ].copy()

    df_resultado = (
        df
        .groupby("SITUACAO", dropna=False)
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

    df_resultado["SITUACAO"] = pd.Categorical(
        df_resultado["SITUACAO"],
        categories=categorias_ordenadas,
        ordered=True,
    )

    df_resultado = (
        df_resultado
        .sort_values("SITUACAO")
        .reset_index(drop=True)
    )

    return df_resultado[
        [
            "SITUACAO",
            "soma_quantidade",
            "percentual_quantidade",
            "soma_valor",
            "percentual_valor",
        ]
    ]


def aggregate_cadunico_by_population_size(df_cubo: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega quantidade de contemplados e valor recebido por porte populacional
    entre contemplados CPF que estão no CadÚnico.

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera apenas pessoaCad_cadunico == 1.0
    - Remove porte_populacional == "-99", pois se refere a estados
    - Usa quantidade como número de contemplados
    - Usa valor_transacao como valor recebido
    """

    required_columns = [
        "tipo_documento",
        "pessoaCad_cadunico",
        "porte_populacional",
        "quantidade",
        "valor_transacao",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    categorias_ordenadas = [
        "1_pequeno_i",
        "2_pequeno_ii",
        "3_medio",
        "4_grande",
    ]

    df = df_cubo.loc[
        (df_cubo["tipo_documento"].eq("CPF"))
        & (df_cubo["pessoaCad_cadunico"].eq(1.0))
        & (df_cubo["porte_populacional"].isin(categorias_ordenadas))
    ].copy()

    df_resultado = (
        df
        .groupby("porte_populacional", dropna=False)
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

    df_resultado["porte_populacional"] = pd.Categorical(
        df_resultado["porte_populacional"],
        categories=categorias_ordenadas,
        ordered=True,
    )

    df_resultado = (
        df_resultado
        .sort_values("porte_populacional")
        .reset_index(drop=True)
    )

    return df_resultado[
        [
            "porte_populacional",
            "soma_quantidade",
            "percentual_quantidade",
            "soma_valor",
            "percentual_valor",
        ]
    ]


def aggregate_cadunico_by_uf(df_cubo: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega, por UF, quantidade e valor de contemplados no CadÚnico
    em comparação com o total de contemplados CPF da UF.

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera CadÚnico quando pessoaCad_cadunico == 1.0
    - Usa quantidade como número de contemplados
    - Usa valor_transacao como valor recebido

    Percentuais calculados:
    - percentual de contemplados CPF da UF que estão no CadÚnico
    - participação da UF no total Brasil de contemplados CadÚnico
    - participação da UF no total Brasil de contemplados CPF
    - participação da UF no valor Brasil de contemplados CadÚnico
    - participação da UF no valor Brasil de contemplados CPF
    """

    required_columns = [
        "tipo_documento",
        "pessoaCad_cadunico",
        "uf",
        "quantidade",
        "valor_transacao",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    # ------------------------------------------------------------
    # 1. Filtra apenas CPF
    # ------------------------------------------------------------
    df_cpf = df_cubo.loc[
        df_cubo["tipo_documento"].eq("CPF")
    ].copy()

    df_cpf["uf"] = df_cpf["uf"].fillna("Não informado")

    # ------------------------------------------------------------
    # 2. Total de contemplados CPF por UF
    # ------------------------------------------------------------
    df_total_uf = (
        df_cpf
        .groupby("uf", dropna=False)
        .agg(
            qtd_contemplados_total_uf=("quantidade", "sum"),
            valor_contemplados_total_uf=("valor_transacao", "sum"),
        )
        .reset_index()
    )

    # ------------------------------------------------------------
    # 3. Total de contemplados CPF no CadÚnico por UF
    # ------------------------------------------------------------
    df_cadunico_uf = (
        df_cpf
        .loc[df_cpf["pessoaCad_cadunico"].eq(1.0)]
        .groupby("uf", dropna=False)
        .agg(
            qtd_contemplados_cadunico=("quantidade", "sum"),
            valor_contemplados_cadunico=("valor_transacao", "sum"),
        )
        .reset_index()
    )

    # ------------------------------------------------------------
    # 4. Junta total CPF com total CadÚnico
    # ------------------------------------------------------------
    df_resultado = df_total_uf.merge(
        df_cadunico_uf,
        on="uf",
        how="left",
    )

    df_resultado[
        [
            "qtd_contemplados_cadunico",
            "valor_contemplados_cadunico",
        ]
    ] = df_resultado[
        [
            "qtd_contemplados_cadunico",
            "valor_contemplados_cadunico",
        ]
    ].fillna(0)

    # ------------------------------------------------------------
    # 5. Totais Brasil
    # ------------------------------------------------------------
    total_qtd_cadunico_brasil = df_resultado["qtd_contemplados_cadunico"].sum()
    total_qtd_geral_brasil = df_resultado["qtd_contemplados_total_uf"].sum()

    total_valor_cadunico_brasil = df_resultado["valor_contemplados_cadunico"].sum()
    total_valor_geral_brasil = df_resultado["valor_contemplados_total_uf"].sum()

    # ------------------------------------------------------------
    # 6. Percentual de contemplados da UF que estão no CadÚnico
    # ------------------------------------------------------------
    df_resultado["perc_qtd_cadunico_na_uf"] = (
        df_resultado["qtd_contemplados_cadunico"]
        .div(
            df_resultado["qtd_contemplados_total_uf"]
            .where(df_resultado["qtd_contemplados_total_uf"].ne(0))
        )
        .fillna(0)
    )

    # ------------------------------------------------------------
    # 7. Participação da UF no total Brasil
    # ------------------------------------------------------------
    df_resultado["perc_qtd_cadunico_brasil"] = (
        df_resultado["qtd_contemplados_cadunico"] / total_qtd_cadunico_brasil
        if total_qtd_cadunico_brasil > 0
        else 0
    )

    df_resultado["perc_qtd_total_brasil"] = (
        df_resultado["qtd_contemplados_total_uf"] / total_qtd_geral_brasil
        if total_qtd_geral_brasil > 0
        else 0
    )

    df_resultado["perc_valor_cadunico_brasil"] = (
        df_resultado["valor_contemplados_cadunico"] / total_valor_cadunico_brasil
        if total_valor_cadunico_brasil > 0
        else 0
    )

    df_resultado["perc_valor_total_brasil"] = (
        df_resultado["valor_contemplados_total_uf"] / total_valor_geral_brasil
        if total_valor_geral_brasil > 0
        else 0
    )

    # ------------------------------------------------------------
    # 8. Ordenação final
    # ------------------------------------------------------------
    df_resultado = (
        df_resultado
        .sort_values("qtd_contemplados_cadunico", ascending=False)
        .reset_index(drop=True)
    )

    return df_resultado[
        [
            "uf",
            "qtd_contemplados_cadunico",
            "qtd_contemplados_total_uf",
            "perc_qtd_cadunico_na_uf",
            "perc_qtd_cadunico_brasil",
            "perc_qtd_total_brasil",
            "valor_contemplados_cadunico",
            "valor_contemplados_total_uf",
            "perc_valor_cadunico_brasil",
            "perc_valor_total_brasil",
        ]
    ]


def aggregate_cadunico_by_value_group(df_cubo: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega a quantidade de contemplados no CadÚnico por faixa de valor pago.

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera apenas pessoaCad_cadunico == 1.0
    - Usa quantidade como número de contemplados
    - Agrupa pela coluna faixa_vlr_pago_ju_bbagil
    - Calcula o percentual que cada faixa representa no total de contemplados
      CPF do CadÚnico
    """

    required_columns = [
        "tipo_documento",
        "pessoaCad_cadunico",
        "faixa_vlr_pago_ju_bbagil",
        "quantidade",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    categorias_ordenadas = [
        "Até 2 mil",
        "De 2 a 10 mil",
        "De 10 a 50 mil",
        "De 50 a 200 mil",
        "Acima de 200 mil",
    ]

    df = df_cubo.loc[
        (df_cubo["tipo_documento"].eq("CPF"))
        & (df_cubo["pessoaCad_cadunico"].eq(1.0))
        & (df_cubo["faixa_vlr_pago_ju_bbagil"].isin(categorias_ordenadas))
    ].copy()

    df_resultado = (
        df
        .groupby("faixa_vlr_pago_ju_bbagil", dropna=False)
        .agg(
            soma_quantidade=("quantidade", "sum")
        )
        .reindex(categorias_ordenadas, fill_value=0)
        .reset_index()
    )

    total_quantidade = df_resultado["soma_quantidade"].sum()

    df_resultado["percentual_quantidade"] = (
        df_resultado["soma_quantidade"] / total_quantidade
        if total_quantidade > 0
        else 0
    )

    return df_resultado[
        [
            "faixa_vlr_pago_ju_bbagil",
            "soma_quantidade",
            "percentual_quantidade",
        ]
    ]


def aggregate_bolsa_familia_summary(df_cubo: pd.DataFrame) -> pd.DataFrame:
    """
    Resume a participação dos contemplados CPF que são beneficiários do Bolsa Família.

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera beneficiário do Bolsa Família quando familiaPBF_cadunico == 1.0
    - Usa quantidade como número de contemplados
    - Usa valor_transacao como valor recebido

    Retorna uma tabela com uma linha.
    """

    required_columns = [
        "tipo_documento",
        "familiaPBF_cadunico",
        "quantidade",
        "valor_transacao",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    df_cpf = df_cubo.loc[
        df_cubo["tipo_documento"].eq("CPF")
    ].copy()

    df_pbf = df_cpf.loc[
        df_cpf["familiaPBF_cadunico"].eq(1.0)
    ].copy()

    total_contemplados_cpf = df_cpf["quantidade"].sum()
    total_valor_cpf = df_cpf["valor_transacao"].sum()

    qtd_contemplados_pbf = df_pbf["quantidade"].sum()
    valor_recebido_pbf = df_pbf["valor_transacao"].sum()

    perc_contemplados_pbf = (
        qtd_contemplados_pbf / total_contemplados_cpf 
        if total_contemplados_cpf > 0
        else 0
    )

    perc_valor_pbf = (
        valor_recebido_pbf / total_valor_cpf 
        if total_valor_cpf > 0
        else 0
    )

    df_resultado = pd.DataFrame(
        {
            "qtd_contemplados_bolsa_familia": [qtd_contemplados_pbf],
            "perc_contemplados_bolsa_familia": [perc_contemplados_pbf],
            "valor_recebido_bolsa_familia": [valor_recebido_pbf],
            "perc_valor_bolsa_familia": [perc_valor_pbf],
            "qtd_contemplados_cpf_total": [total_contemplados_cpf],
            "valor_cpf_total": [total_valor_cpf],
        }
    )

    return df_resultado

def aggregate_bpc_summary(df_cubo: pd.DataFrame) -> pd.DataFrame:
    """
    Resume a participação dos contemplados CPF que recebem
    Benefício de Prestação Continuada (BPC).

    Regras:
    - Considera apenas tipo_documento == "CPF"
    - Considera beneficiário do BPC quando pertence_bpc == 1.0
    - Usa quantidade como número de contemplados
    - Usa valor_transacao como valor recebido

    Retorna uma tabela com uma linha.
    """

    required_columns = [
        "tipo_documento",
        "pertence_bpc",
        "quantidade",
        "valor_transacao",
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    df_cpf = df_cubo.loc[
        df_cubo["tipo_documento"].eq("CPF")
    ].copy()

    df_bpc = df_cpf.loc[
        df_cpf["pertence_bpc"].eq(1.0)
    ].copy()

    total_contemplados_cpf = df_cpf["quantidade"].sum()
    total_valor_cpf = df_cpf["valor_transacao"].sum()

    qtd_contemplados_bpc = df_bpc["quantidade"].sum()
    valor_recebido_bpc = df_bpc["valor_transacao"].sum()

    perc_contemplados_bpc = (
        qtd_contemplados_bpc / total_contemplados_cpf 
        if total_contemplados_cpf > 0
        else 0
    )

    perc_valor_bpc = (
        valor_recebido_bpc / total_valor_cpf 
        if total_valor_cpf > 0
        else 0
    )

    df_resultado = pd.DataFrame(
        {
            "qtd_contemplados_bpc": [qtd_contemplados_bpc],
            "perc_contemplados_bpc": [perc_contemplados_bpc],
            "valor_recebido_bpc": [valor_recebido_bpc],
            "perc_valor_bpc": [perc_valor_bpc],
            "qtd_contemplados_cpf_total": [total_contemplados_cpf],
            "valor_cpf_total": [total_valor_cpf],
        }
    )

    return df_resultado



def aggregate_cadunico_representacao_by_uf(
    df_cubo: pd.DataFrame,
    col_uf: str = "uf",
    col_tipo_documento: str = "tipo_documento",
    col_cadunico: str = "pessoaCad_cadunico",
    col_quantidade: str = "quantidade",
) -> pd.DataFrame:
    """
    Calcula, por UF, a comparação entre:

    1. A distribuição da população cadastrada no CadÚnico no Brasil;
    2. A distribuição dos contemplados PNAB que estão no CadÚnico.

    Regras:
    - Considera apenas tipo_documento == "CPF";
    - Considera contemplado no CadÚnico quando pessoaCad_cadunico == 1.0;
    - Usa a coluna quantidade como número de contemplados;
    - Percentuais retornam em escala decimal, ou seja:
        0.10 = 10%.

    Principais colunas calculadas:
    - perc_qtd_cadunico_brasil:
        quanto a UF representa no total de pessoas cadastradas no CadÚnico no Brasil.

    - perc_qtd_contemplados_cadunico:
        quanto a UF representa no total de contemplados PNAB que estão no CadÚnico.

    - razao_representacao_pnab_cadunico:
        compara a participação da UF entre os contemplados PNAB no CadÚnico
        com a participação da UF na população total do CadÚnico.
        Valores acima de 1 indicam sobrerrepresentação na PNAB.
    """

    required_columns = [
        col_uf,
        col_tipo_documento,
        col_cadunico,
        col_quantidade,
    ]

    missing_columns = [
        col for col in required_columns if col not in df_cubo.columns
    ]

    if missing_columns:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {missing_columns}"
        )

    # ------------------------------------------------------------
    # 1. Base de referência: população e CadÚnico por UF
    # ------------------------------------------------------------
    df_ref_uf = pd.DataFrame({
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
        "qtd_pessoas_cadunico_uf": [
            873792, 571102, 2716758, 412078, 5601544, 525802, 916427,
            4633794, 2222147, 5745101, 2035308, 2568796, 5810408, 2046130,
            1416112, 9426922,
            8835783, 1801725, 6939360, 14214700,
            4409296, 1822770, 3733440,
            1426684, 1730035, 3332959, 959621
        ],
    })

    # ------------------------------------------------------------
    # 2. Filtra apenas CPF e contemplados no CadÚnico
    # ------------------------------------------------------------
    df_cpf_cadunico = df_cubo.loc[
        df_cubo[col_tipo_documento].eq("CPF")
        & df_cubo[col_cadunico].eq(1.0)
    ].copy()

    df_cpf_cadunico[col_uf] = df_cpf_cadunico[col_uf].fillna("Não informado")

    # ------------------------------------------------------------
    # 3. Agrega contemplados PNAB no CadÚnico por UF
    # ------------------------------------------------------------
    df_pnab_cadunico_uf = (
        df_cpf_cadunico
        .groupby(col_uf, dropna=False)
        .agg(
            qtd_contemplados_cadunico=(col_quantidade, "sum")
        )
        .reset_index()
        .rename(columns={col_uf: "uf"})
    )

    # ------------------------------------------------------------
    # 4. Junta referência CadÚnico com contemplados PNAB
    # ------------------------------------------------------------
    df_resultado = df_ref_uf.merge(
        df_pnab_cadunico_uf,
        on="uf",
        how="left"
    )

    df_resultado["qtd_contemplados_cadunico"] = (
        df_resultado["qtd_contemplados_cadunico"]
        .fillna(0)
    )

    # ------------------------------------------------------------
    # 5. Totais Brasil
    # ------------------------------------------------------------
    total_pessoas_cadunico_brasil = (
        df_resultado["qtd_pessoas_cadunico_uf"].sum()
    )

    total_contemplados_cadunico_brasil = (
        df_resultado["qtd_contemplados_cadunico"].sum()
    )

    # ------------------------------------------------------------
    # 6. Percentuais principais
    # ------------------------------------------------------------
    df_resultado["perc_qtd_cadunico_brasil"] = (
        df_resultado["qtd_pessoas_cadunico_uf"]
        / total_pessoas_cadunico_brasil
        if total_pessoas_cadunico_brasil > 0
        else 0
    )

    df_resultado["perc_qtd_contemplados_cadunico"] = (
        df_resultado["qtd_contemplados_cadunico"]
        / total_contemplados_cadunico_brasil
        if total_contemplados_cadunico_brasil > 0
        else 0
    )

    # ------------------------------------------------------------
    # 7. Métricas auxiliares úteis
    # ------------------------------------------------------------

    # Percentual da população da UF que está no CadÚnico
    df_resultado["perc_populacao_uf_no_cadunico"] = (
        df_resultado["qtd_pessoas_cadunico_uf"]
        .div(
            df_resultado["populacao_ibge_2024"]
            .where(df_resultado["populacao_ibge_2024"].ne(0))
        )
        .fillna(0)
    )

    # Percentual de pessoas do CadÚnico da UF contempladas pela PNAB
    df_resultado["perc_cadunico_uf_contemplado_pnab"] = (
        df_resultado["qtd_contemplados_cadunico"]
        .div(
            df_resultado["qtd_pessoas_cadunico_uf"]
            .where(df_resultado["qtd_pessoas_cadunico_uf"].ne(0))
        )
        .fillna(0)
    )

    # Razão de representação:
    # participação da UF entre contemplados PNAB CadÚnico /
    # participação da UF no CadÚnico Brasil
    df_resultado["razao_representacao_pnab_cadunico"] = (
        df_resultado["perc_qtd_contemplados_cadunico"]
        .div(
            df_resultado["perc_qtd_cadunico_brasil"]
            .where(df_resultado["perc_qtd_cadunico_brasil"].ne(0))
        )
        .fillna(0)
    )

    # ------------------------------------------------------------
    # 8. Ordenação final
    # ------------------------------------------------------------
    df_resultado = (
        df_resultado
        .sort_values("qtd_contemplados_cadunico", ascending=False)
        .reset_index(drop=True)
    )

    return df_resultado[
        [
            "codigo_uf",
            "uf",
            "unidade_da_federacao",
            "populacao_ibge_2024",
            "qtd_pessoas_cadunico_uf",
            "qtd_contemplados_cadunico",
            "perc_qtd_cadunico_brasil",
            "perc_qtd_contemplados_cadunico",
            "perc_populacao_uf_no_cadunico",
            "perc_cadunico_uf_contemplado_pnab",
            "razao_representacao_pnab_cadunico",
        ]
    ]

import numpy as np
import pandas as pd


def aggregate_pf_cadunico_by_faixa_valor_ju(
    df_cubo: pd.DataFrame,
    by_filter: str = "UF",
    coluna_tipo_ente: str = "tipo_ente",
    coluna_tipo_documento: str = "tipo_documento",
    coluna_faixa: str = "faixa_vlr_pago_ju_bbagil",
    coluna_quantidade: str = "quantidade",
    coluna_valor: str = "valor_transacao",
    coluna_cadunico: str = "pessoaCad_cadunico"
) -> pd.DataFrame:
    """
    Agrega Pessoas Físicas por faixa de valor pago.

    Linhas:
    - categorias da coluna faixa_vlr_pago_ju_bbagil.

    Filtros:
    - considera apenas tipo_documento == CPF;
    - opcionalmente filtra por tipo_ente:
        - "ESTADO": apenas tipo_ente == ESTADO;
        - "MUNICIPIO": apenas tipo_ente == MUNICIPIO;
        - "UF": considera ESTADO + MUNICIPIO.

    Para cada faixa, calcula:
    - quantidade geral de contemplados PF;
    - percentual da quantidade geral no total de PF;
    - valor geral;
    - percentual do valor geral no total de PF;
    - quantidade de contemplados PF no CadÚnico;
    - percentual da quantidade CadÚnico no total de PF no CadÚnico;
    - percentual da quantidade CadÚnico no total geral de PF;
    - valor de contemplados PF no CadÚnico;
    - percentual do valor CadÚnico no total de PF no CadÚnico;
    - percentual do valor CadÚnico no total geral de PF.

    Percentuais retornam em escala decimal:
    - 0.25 = 25%

    Não há arredondamento dos valores.
    """

    by_filter = by_filter.upper().strip()

    # ------------------------------------------------------------
    # 1. Copiar base
    # ------------------------------------------------------------

    df = df_cubo.copy()

    # ------------------------------------------------------------
    # 2. Normalizar tipo_ente
    # ------------------------------------------------------------

    df["tipo_ente_norm"] = (
        df[coluna_tipo_ente]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    # ------------------------------------------------------------
    # 3. Aplicar filtro territorial
    # ------------------------------------------------------------

    if by_filter == "ESTADO":
        df = df[df["tipo_ente_norm"].eq("ESTADO")].copy()

    elif by_filter == "MUNICIPIO":
        df = df[df["tipo_ente_norm"].eq("MUNICIPIO")].copy()

    elif by_filter == "UF":
        df = df[df["tipo_ente_norm"].isin(["ESTADO", "MUNICIPIO"])].copy()

    else:
        raise ValueError("by_filter deve ser 'ESTADO', 'MUNICIPIO' ou 'UF'.")

    # ------------------------------------------------------------
    # 4. Filtrar apenas Pessoa Física
    # ------------------------------------------------------------

    df["tipo_documento_norm"] = (
        df[coluna_tipo_documento]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df = df[df["tipo_documento_norm"].eq("CPF")].copy()

    # ------------------------------------------------------------
    # 5. Definir ordem das faixas
    # ------------------------------------------------------------

    ordem_faixa_vlr_pago = [
        "Até 2 mil",
        "De 2 a 10 mil",
        "De 10 a 50 mil",
        "De 50 a 200 mil",
        "Acima de 200 mil"
    ]

    df["faixa_vlr_pago_ju_bbagil_tratada"] = (
        df[coluna_faixa]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    df = df[
        df["faixa_vlr_pago_ju_bbagil_tratada"].isin(ordem_faixa_vlr_pago)
    ].copy()

    # ------------------------------------------------------------
    # 6. Garantir tipos numéricos
    # ------------------------------------------------------------

    df[coluna_quantidade] = pd.to_numeric(
        df[coluna_quantidade],
        errors="coerce"
    ).fillna(0)

    df[coluna_valor] = pd.to_numeric(
        df[coluna_valor],
        errors="coerce"
    ).fillna(0)

    # ------------------------------------------------------------
    # 7. Criar flag CadÚnico
    # ------------------------------------------------------------

    df["flag_cadunico"] = df[coluna_cadunico].eq(1.0)

    # ------------------------------------------------------------
    # 8. Calcular totais gerais
    # ------------------------------------------------------------

    total_qtd_geral = df[coluna_quantidade].sum()
    total_valor_geral = df[coluna_valor].sum()

    total_qtd_cadunico = df.loc[
        df["flag_cadunico"],
        coluna_quantidade
    ].sum()

    total_valor_cadunico = df.loc[
        df["flag_cadunico"],
        coluna_valor
    ].sum()

    # ------------------------------------------------------------
    # 9. Agregar geral por faixa
    # ------------------------------------------------------------

    df_geral = (
        df
        .groupby("faixa_vlr_pago_ju_bbagil_tratada", as_index=False)
        .agg(
            qtd_contemplados_geral=(coluna_quantidade, "sum"),
            valor_total_geral=(coluna_valor, "sum")
        )
    )

    # ------------------------------------------------------------
    # 10. Agregar CadÚnico por faixa
    # ------------------------------------------------------------

    df_cadunico = (
        df
        .loc[df["flag_cadunico"]]
        .groupby("faixa_vlr_pago_ju_bbagil_tratada", as_index=False)
        .agg(
            qtd_contemplados_cadunico=(coluna_quantidade, "sum"),
            valor_total_cadunico=(coluna_valor, "sum")
        )
    )

    # ------------------------------------------------------------
    # 11. Montar base final
    # ------------------------------------------------------------

    df_resultado = pd.DataFrame({
        "faixa_vlr_pago_ju_bbagil": ordem_faixa_vlr_pago
    })

    df_resultado = df_resultado.merge(
        df_geral,
        left_on="faixa_vlr_pago_ju_bbagil",
        right_on="faixa_vlr_pago_ju_bbagil_tratada",
        how="left"
    )

    df_resultado = df_resultado.merge(
        df_cadunico,
        left_on="faixa_vlr_pago_ju_bbagil",
        right_on="faixa_vlr_pago_ju_bbagil_tratada",
        how="left",
        suffixes=("", "_cad")
    )

    df_resultado = df_resultado.drop(
        columns=[
            col for col in [
                "faixa_vlr_pago_ju_bbagil_tratada",
                "faixa_vlr_pago_ju_bbagil_tratada_cad"
            ]
            if col in df_resultado.columns
        ]
    )

    # ------------------------------------------------------------
    # 12. Preencher ausentes
    # ------------------------------------------------------------

    colunas_quantidade = [
        "qtd_contemplados_geral",
        "qtd_contemplados_cadunico"
    ]

    colunas_valor = [
        "valor_total_geral",
        "valor_total_cadunico"
    ]

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
    )

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .fillna(0)
    )

    # ------------------------------------------------------------
    # 13. Calcular percentuais
    # ------------------------------------------------------------

    df_resultado["perc_qtd_geral_no_total_pf"] = np.where(
        total_qtd_geral != 0,
        df_resultado["qtd_contemplados_geral"] / total_qtd_geral,
        np.nan
    )

    df_resultado["perc_valor_geral_no_total_pf"] = np.where(
        total_valor_geral != 0,
        df_resultado["valor_total_geral"] / total_valor_geral,
        np.nan
    )

    df_resultado["perc_qtd_cadunico_no_total_cadunico"] = np.where(
        total_qtd_cadunico != 0,
        df_resultado["qtd_contemplados_cadunico"] / total_qtd_cadunico,
        np.nan
    )

    df_resultado["perc_valor_cadunico_no_total_cadunico"] = np.where(
        total_valor_cadunico != 0,
        df_resultado["valor_total_cadunico"] / total_valor_cadunico,
        np.nan
    )

    df_resultado["perc_qtd_cadunico_no_total_pf"] = np.where(
        total_qtd_geral != 0,
        df_resultado["qtd_contemplados_cadunico"] / total_qtd_geral,
        np.nan
    )

    df_resultado["perc_valor_cadunico_no_total_pf"] = np.where(
        total_valor_geral != 0,
        df_resultado["valor_total_cadunico"] / total_valor_geral,
        np.nan
    )

    # ------------------------------------------------------------
    # 14. Adicionar totais de referência
    # ------------------------------------------------------------

    df_resultado["total_contemplados_pf"] = total_qtd_geral
    df_resultado["valor_total_pf"] = total_valor_geral

    df_resultado["total_contemplados_pf_cadunico"] = total_qtd_cadunico
    df_resultado["valor_total_pf_cadunico"] = total_valor_cadunico

    # ------------------------------------------------------------
    # 15. Ordenar colunas finais
    # ------------------------------------------------------------

    colunas_finais = [
        "faixa_vlr_pago_ju_bbagil",

        "qtd_contemplados_geral",
        "perc_qtd_geral_no_total_pf",
        "valor_total_geral",
        "perc_valor_geral_no_total_pf",

        "qtd_contemplados_cadunico",
        "perc_qtd_cadunico_no_total_cadunico",
        "perc_qtd_cadunico_no_total_pf",
        "valor_total_cadunico",
        "perc_valor_cadunico_no_total_cadunico",
        "perc_valor_cadunico_no_total_pf",

        "total_contemplados_pf",
        "valor_total_pf",
        "total_contemplados_pf_cadunico",
        "valor_total_pf_cadunico"
    ]

    df_resultado = df_resultado[colunas_finais].copy()

    # ------------------------------------------------------------
    # 16. Ajustar tipos
    # ------------------------------------------------------------

    colunas_int = [
        "qtd_contemplados_geral",
        "qtd_contemplados_cadunico",
        "total_contemplados_pf",
        "total_contemplados_pf_cadunico"
    ]

    colunas_float = [
        col for col in df_resultado.columns
        if col not in ["faixa_vlr_pago_ju_bbagil"] + colunas_int
    ]

    df_resultado[colunas_int] = (
        df_resultado[colunas_int]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_float] = (
        df_resultado[colunas_float]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    return df_resultado