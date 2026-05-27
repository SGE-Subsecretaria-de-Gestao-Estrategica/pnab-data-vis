import pandas as pd


def aggregate_cadunico_summary(
    df_cubo: pd.DataFrame,
    qtd_documentos_unicos_cadunico: int = 57_338
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

    df_cpf = df_cubo.loc[
        df_cubo["tipo_documento"].eq("CPF")
    ].copy()

    df_cpf_cadunico = df_cpf[df_cpf["pessoaCad_cadunico"].notna()]

    total_contemplados_cpf = df_cpf["quantidade"].sum()
    total_valor_cpf = df_cpf["valor_transacao"].sum()

    qtd_contemplados_cadunico = df_cpf_cadunico["quantidade"].sum()
    valor_recebido_cadunico = df_cpf_cadunico["valor_transacao"].sum()

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

    df_resultado = pd.DataFrame(
        {
            "perc_contemplados_cadunico": [perc_contemplados_cadunico],
            "qtd_contemplados_cadunico": [qtd_contemplados_cadunico],
            "qtd_documentos_unicos_cadunico": [qtd_documentos_unicos_cadunico],
            "valor_recebido_cadunico": [valor_recebido_cadunico],
            "perc_valor_cadunico": [perc_valor_cadunico],
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
        df_resultado["soma_quantidade"] / total_quantidade * 100
        if total_quantidade > 0
        else 0
    )

    df_resultado["percentual_valor"] = (
        df_resultado["soma_valor"] / total_valor * 100
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