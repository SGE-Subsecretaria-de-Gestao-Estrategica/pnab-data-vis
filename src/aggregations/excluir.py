
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
    - valores e quantidades por zona urbana/rural;
    - valor e quantidade por tipo_documento;
    - valor e quantidade por Sexo, considerando apenas tipo_documento == CPF.
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
        df = df_cubo.copy()

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
    # Tratar tipo_documento
    # ------------------------------------------------------------

    df["tipo_documento_tratado"] = (
        df["tipo_documento"]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # ------------------------------------------------------------
    # Tratar Sexo
    # ------------------------------------------------------------

    df["sexo_tratado"] = (
        df["Sexo"]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
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
            columns="faixa_vlr_pago_ju_bbagil",
            values="quantidade",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )
    
    df_exec_uf_faixa_vlr = df_exec_uf_faixa_vlr.rename(
        columns={
            'faixa_vlr_pago_ju_bbagil': 'faixa_vlr_pago'
        }
    )

    # ------------------------------------------------------------
    # Quantidade por tipo_documento
    # ------------------------------------------------------------

    df_qtd_tipo_documento = (
        df
        .pivot_table(
            index="uf",
            columns="tipo_documento_tratado",
            values="quantidade",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    df_qtd_tipo_documento = df_qtd_tipo_documento.rename(
        columns={
            col: f"qtd_tipo_documento_{col}"
            for col in df_qtd_tipo_documento.columns
            if col != "uf"
        }
    )

    # ------------------------------------------------------------
    # Valor por tipo_documento: soma, mínimo, mediana, máximo e média
    # ------------------------------------------------------------

    def pivot_valor_tipo_documento(df_base, aggfunc, prefixo_coluna):
        df_pivot = (
            df_base
            .pivot_table(
                index="uf",
                columns="tipo_documento_tratado",
                values="valor_transacao",
                aggfunc=aggfunc,
                fill_value=0
            )
            .reset_index()
        )

        df_pivot = df_pivot.rename(
            columns={
                col: f"{prefixo_coluna}_tipo_documento_{col}"
                for col in df_pivot.columns
                if col != "uf"
            }
        )

        return df_pivot

    df_valor_tipo_documento = pivot_valor_tipo_documento(
        df_base=df,
        aggfunc="sum",
        prefixo_coluna="valor"
    )

    df_min_valor_tipo_documento = pivot_valor_tipo_documento(
        df_base=df,
        aggfunc="min",
        prefixo_coluna="min_valor"
    )

    df_mediana_valor_tipo_documento = pivot_valor_tipo_documento(
        df_base=df,
        aggfunc="median",
        prefixo_coluna="mediana_valor"
    )

    df_max_valor_tipo_documento = pivot_valor_tipo_documento(
        df_base=df,
        aggfunc="max",
        prefixo_coluna="max_valor"
    )

    df_media_valor_tipo_documento = pivot_valor_tipo_documento(
        df_base=df,
        aggfunc="mean",
        prefixo_coluna="media_valor"
    )

    # ------------------------------------------------------------
    # Quantidade e valor por Sexo
    # Apenas tipo_documento == CPF
    # ------------------------------------------------------------

    df_sexo_base = df[
        df["tipo_documento_tratado"].eq("CPF")
    ].copy()

    df_qtd_sexo = (
        df_sexo_base
        .pivot_table(
            index="uf",
            columns="sexo_tratado",
            values="quantidade",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    df_qtd_sexo = df_qtd_sexo.rename(
        columns={
            col: f"qtd_sexo_{col}"
            for col in df_qtd_sexo.columns
            if col != "uf"
        }
    )

    df_valor_sexo = (
        df_sexo_base
        .pivot_table(
            index="uf",
            columns="sexo_tratado",
            values="valor_transacao",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    df_valor_sexo = df_valor_sexo.rename(
        columns={
            col: f"valor_sexo_{col}"
            for col in df_valor_sexo.columns
            if col != "uf"
        }
    )

    total_qtd_cpf_por_uf = (
        df_sexo_base
        .groupby("uf", as_index=False)
        .agg(total_qtd_cpf=("quantidade", "sum"))
    )

    total_valor_cpf_por_uf = (
        df_sexo_base
        .groupby("uf", as_index=False)
        .agg(total_valor_cpf=("valor_transacao", "sum"))
    )

    # ------------------------------------------------------------
    # Juntar tudo
    # ------------------------------------------------------------

    df_final = (
        df_tabela_uf
        .merge(
            right=df_exec_uf_faixa_vlr,
            on="uf",
            how="left"
        )
        .merge(
            right=df_qtd_tipo_documento,
            on="uf",
            how="left"
        )
        .merge(
            right=df_valor_tipo_documento,
            on="uf",
            how="left"
        )
        .merge(
            right=df_min_valor_tipo_documento,
            on="uf",
            how="left"
        )
        .merge(
            right=df_mediana_valor_tipo_documento,
            on="uf",
            how="left"
        )
        .merge(
            right=df_max_valor_tipo_documento,
            on="uf",
            how="left"
        )
        .merge(
            right=df_media_valor_tipo_documento,
            on="uf",
            how="left"
        )
        .merge(
            right=df_qtd_sexo,
            on="uf",
            how="left"
        )
        .merge(
            right=df_valor_sexo,
            on="uf",
            how="left"
        )
        .merge(
            right=total_qtd_cpf_por_uf,
            on="uf",
            how="left"
        )
        .merge(
            right=total_valor_cpf_por_uf,
            on="uf",
            how="left"
        )
    )

    # ------------------------------------------------------------
    # Percentuais por Sexo dentro da UF
    # Apenas entre pessoas físicas CPF
    # ------------------------------------------------------------

    colunas_qtd_sexo = [
        col for col in df_final.columns
        if col.startswith("qtd_sexo_")
    ]

    colunas_valor_sexo = [
        col for col in df_final.columns
        if col.startswith("valor_sexo_")
    ]

    for coluna in colunas_qtd_sexo:
        nome_percentual = coluna.replace("qtd_sexo_", "percentual_qtd_sexo_")

        df_final[nome_percentual] = np.where(
            df_final["total_qtd_cpf"].fillna(0).ne(0),
            df_final[coluna] / df_final["total_qtd_cpf"],
            np.nan
        )

    for coluna in colunas_valor_sexo:
        nome_percentual = coluna.replace("valor_sexo_", "percentual_valor_sexo_")

        df_final[nome_percentual] = np.where(
            df_final["total_valor_cpf"].fillna(0).ne(0),
            df_final[coluna] / df_final["total_valor_cpf"],
            np.nan
        )

    return df_final