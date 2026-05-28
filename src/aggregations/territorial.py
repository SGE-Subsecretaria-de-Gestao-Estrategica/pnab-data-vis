import pandas as pd
import numpy as np


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
            columns="faixa_vlr_pago",
            values="quantidade",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
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


def aggregate_capital_interior_summary(
    df_cubo: pd.DataFrame
) -> pd.DataFrame:
    """
    Gera resumo agregado de valor e quantidade para capitais e interior.

    Considera apenas registros de MUNICIPIO.
    Divide os municípios entre:
    - capital
    - interior

    Também calcula quantidade e percentual de contemplados por Sexo:
    - Feminino
    - Masculino

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

    df_municipios["sexo_norm"] = (
        df_municipios["Sexo"]
        .fillna("Não informado")
        .astype(str)
        .str.upper()
        .str.strip()
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

    quantidade_feminino_capital = (
        df_capital
        .loc[df_capital["sexo_norm"].eq("FEMININO"), "quantidade"]
        .sum()
    )

    quantidade_masculino_capital = (
        df_capital
        .loc[df_capital["sexo_norm"].eq("MASCULINO"), "quantidade"]
        .sum()
    )

    quantidade_feminino_interior = (
        df_interior
        .loc[df_interior["sexo_norm"].eq("FEMININO"), "quantidade"]
        .sum()
    )

    quantidade_masculino_interior = (
        df_interior
        .loc[df_interior["sexo_norm"].eq("MASCULINO"), "quantidade"]
        .sum()
    )

    df_resultado = pd.DataFrame({
        "valor_total_capital": [valor_total_capital],
        "quantidade_total_capital": [quantidade_total_capital],
        "percentual_valor_capital": [
            valor_total_capital / valor_total_geral * 100
            if valor_total_geral > 0 else np.nan
        ],
        "percentual_quantidade_capital": [
            quantidade_total_capital / quantidade_total_geral * 100
            if quantidade_total_geral > 0 else np.nan
        ],

        "quantidade_feminino_capital": [quantidade_feminino_capital],
        "percentual_feminino_capital": [
            quantidade_feminino_capital / quantidade_total_capital * 100
            if quantidade_total_capital > 0 else np.nan
        ],
        "quantidade_masculino_capital": [quantidade_masculino_capital],
        "percentual_masculino_capital": [
            quantidade_masculino_capital / quantidade_total_capital * 100
            if quantidade_total_capital > 0 else np.nan
        ],

        "valor_total_interior": [valor_total_interior],
        "quantidade_total_interior": [quantidade_total_interior],
        "percentual_valor_interior": [
            valor_total_interior / valor_total_geral * 100
            if valor_total_geral > 0 else np.nan
        ],
        "percentual_quantidade_interior": [
            quantidade_total_interior / quantidade_total_geral * 100
            if quantidade_total_geral > 0 else np.nan
        ],

        "quantidade_feminino_interior": [quantidade_feminino_interior],
        "percentual_feminino_interior": [
            quantidade_feminino_interior / quantidade_total_interior * 100
            if quantidade_total_interior > 0 else np.nan
        ],
        "quantidade_masculino_interior": [quantidade_masculino_interior],
        "percentual_masculino_interior": [
            quantidade_masculino_interior / quantidade_total_interior * 100
            if quantidade_total_interior > 0 else np.nan
        ],
    })

    colunas_valor = [
        "valor_total_capital",
        "valor_total_interior"
    ]

    colunas_quantidade = [
        "quantidade_total_capital",
        "quantidade_feminino_capital",
        "quantidade_masculino_capital",
        "quantidade_total_interior",
        "quantidade_feminino_interior",
        "quantidade_masculino_interior"
    ]

    colunas_percentual = [
        "percentual_valor_capital",
        "percentual_quantidade_capital",
        "percentual_feminino_capital",
        "percentual_masculino_capital",
        "percentual_valor_interior",
        "percentual_quantidade_interior",
        "percentual_feminino_interior",
        "percentual_masculino_interior"
    ]

    df_resultado[colunas_valor] = (
        np.ceil(df_resultado[colunas_valor])
        .astype("Int64")
    )

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
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

    Também acrescenta:
    - quantidade de contemplados por faixa_vlr_pago;
    - quantidade por tipo_documento;
    - valor total por tipo_documento;
    - valor mínimo, mediana, máximo e média por tipo_documento;
    - quantidade por Sexo;
    - valor por Sexo;
    - percentual de quantidade por Sexo;
    - percentual de valor por Sexo.

    Observação:
    - a regra de manter apenas Sexo válido é aplicada somente nas agregações de Sexo;
    - o restante da função usa a base completa conforme os filtros originais.
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

    df["faixa_vlr_pago_tratada"] = (
        df["faixa_vlr_pago"]
        .fillna("Não informado")
    )

    df["tipo_documento_tratado"] = (
        df["tipo_documento"]
        .fillna("Não informado")
        .astype(str)
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

    df["sexo_tratado"] = df["sexo_norm"].map({
        "FEMININO": "Feminino",
        "MASCULINO": "Masculino"
    })

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
    # 6. Quantidade de contemplados por faixa de valor - municípios
    # ------------------------------------------------------------

    df_faixa_municipios = (
        df_municipios
        .pivot_table(
            index="porte_populacional",
            columns="faixa_vlr_pago_tratada",
            values="quantidade",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    # ------------------------------------------------------------
    # 7. Função auxiliar para pivot por tipo_documento
    # ------------------------------------------------------------

    def pivot_tipo_documento_por_porte(
        df_base: pd.DataFrame,
        values: str,
        aggfunc: str,
        prefixo_coluna: str
    ) -> pd.DataFrame:
        df_pivot = (
            df_base
            .pivot_table(
                index="porte_populacional",
                columns="tipo_documento_tratado",
                values=values,
                aggfunc=aggfunc,
                fill_value=0
            )
            .reset_index()
        )

        df_pivot = df_pivot.rename(
            columns={
                col: f"{prefixo_coluna}_tipo_documento_{col}"
                for col in df_pivot.columns
                if col != "porte_populacional"
            }
        )

        return df_pivot

    # ------------------------------------------------------------
    # 8. Função auxiliar para pivot por Sexo
    # ------------------------------------------------------------

    def pivot_sexo_por_porte(
        df_base: pd.DataFrame,
        values: str,
        aggfunc: str,
        prefixo_coluna: str
    ) -> pd.DataFrame:
        df_pivot = (
            df_base
            .pivot_table(
                index="porte_populacional",
                columns="sexo_tratado",
                values=values,
                aggfunc=aggfunc,
                fill_value=0
            )
            .reset_index()
        )

        df_pivot = df_pivot.rename(
            columns={
                col: f"{prefixo_coluna}_sexo_{col}"
                for col in df_pivot.columns
                if col != "porte_populacional"
            }
        )

        return df_pivot

    # ------------------------------------------------------------
    # 9. Tipo_documento - municípios
    # ------------------------------------------------------------

    df_qtd_tipo_doc_municipios = pivot_tipo_documento_por_porte(
        df_base=df_municipios,
        values="quantidade",
        aggfunc="sum",
        prefixo_coluna="qtd"
    )

    df_valor_tipo_doc_municipios = pivot_tipo_documento_por_porte(
        df_base=df_municipios,
        values="valor_transacao",
        aggfunc="sum",
        prefixo_coluna="valor"
    )

    df_min_valor_tipo_doc_municipios = pivot_tipo_documento_por_porte(
        df_base=df_municipios,
        values="valor_transacao",
        aggfunc="min",
        prefixo_coluna="min_valor"
    )

    df_mediana_valor_tipo_doc_municipios = pivot_tipo_documento_por_porte(
        df_base=df_municipios,
        values="valor_transacao",
        aggfunc="median",
        prefixo_coluna="mediana_valor"
    )

    df_max_valor_tipo_doc_municipios = pivot_tipo_documento_por_porte(
        df_base=df_municipios,
        values="valor_transacao",
        aggfunc="max",
        prefixo_coluna="max_valor"
    )

    df_media_valor_tipo_doc_municipios = pivot_tipo_documento_por_porte(
        df_base=df_municipios,
        values="valor_transacao",
        aggfunc="mean",
        prefixo_coluna="media_valor"
    )

    # ------------------------------------------------------------
    # 10. Sexo - municípios
    # Mantém apenas Sexo válido somente nesta agregação
    # ------------------------------------------------------------

    df_municipios_sexo = df_municipios[
        df_municipios["sexo_tratado"].isin(["Feminino", "Masculino"])
    ].copy()

    df_qtd_sexo_municipios = pivot_sexo_por_porte(
        df_base=df_municipios_sexo,
        values="quantidade",
        aggfunc="sum",
        prefixo_coluna="qtd"
    )

    df_valor_sexo_municipios = pivot_sexo_por_porte(
        df_base=df_municipios_sexo,
        values="valor_transacao",
        aggfunc="sum",
        prefixo_coluna="valor"
    )

    df_total_sexo_municipios = (
        df_municipios_sexo
        .groupby("porte_populacional", dropna=False, as_index=False)
        .agg(
            total_qtd_sexo_valido=("quantidade", "sum"),
            total_valor_sexo_valido=("valor_transacao", "sum")
        )
    )

    # ------------------------------------------------------------
    # 11. Criar linha agregada dos estados
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
    # 12. Base dos estados com porte_populacional = -99
    # ------------------------------------------------------------

    df_estados_base = df_estados.copy()
    df_estados_base["porte_populacional"] = -99

    # ------------------------------------------------------------
    # 13. Quantidade de contemplados por faixa de valor - estados
    # ------------------------------------------------------------

    df_faixa_estado = (
        df_estados_base
        .pivot_table(
            index="porte_populacional",
            columns="faixa_vlr_pago_tratada",
            values="quantidade",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    # ------------------------------------------------------------
    # 14. Tipo_documento - estados
    # ------------------------------------------------------------

    df_qtd_tipo_doc_estado = pivot_tipo_documento_por_porte(
        df_base=df_estados_base,
        values="quantidade",
        aggfunc="sum",
        prefixo_coluna="qtd"
    )

    df_valor_tipo_doc_estado = pivot_tipo_documento_por_porte(
        df_base=df_estados_base,
        values="valor_transacao",
        aggfunc="sum",
        prefixo_coluna="valor"
    )

    df_min_valor_tipo_doc_estado = pivot_tipo_documento_por_porte(
        df_base=df_estados_base,
        values="valor_transacao",
        aggfunc="min",
        prefixo_coluna="min_valor"
    )

    df_mediana_valor_tipo_doc_estado = pivot_tipo_documento_por_porte(
        df_base=df_estados_base,
        values="valor_transacao",
        aggfunc="median",
        prefixo_coluna="mediana_valor"
    )

    df_max_valor_tipo_doc_estado = pivot_tipo_documento_por_porte(
        df_base=df_estados_base,
        values="valor_transacao",
        aggfunc="max",
        prefixo_coluna="max_valor"
    )

    df_media_valor_tipo_doc_estado = pivot_tipo_documento_por_porte(
        df_base=df_estados_base,
        values="valor_transacao",
        aggfunc="mean",
        prefixo_coluna="media_valor"
    )

    # ------------------------------------------------------------
    # 15. Sexo - estados
    # Mantém apenas Sexo válido somente nesta agregação
    # ------------------------------------------------------------

    df_estados_sexo = df_estados_base[
        df_estados_base["sexo_tratado"].isin(["Feminino", "Masculino"])
    ].copy()

    df_qtd_sexo_estado = pivot_sexo_por_porte(
        df_base=df_estados_sexo,
        values="quantidade",
        aggfunc="sum",
        prefixo_coluna="qtd"
    )

    df_valor_sexo_estado = pivot_sexo_por_porte(
        df_base=df_estados_sexo,
        values="valor_transacao",
        aggfunc="sum",
        prefixo_coluna="valor"
    )

    df_total_sexo_estado = (
        df_estados_sexo
        .groupby("porte_populacional", dropna=False, as_index=False)
        .agg(
            total_qtd_sexo_valido=("quantidade", "sum"),
            total_valor_sexo_valido=("valor_transacao", "sum")
        )
    )

    # ------------------------------------------------------------
    # 16. Juntar municípios por porte + linha de estados
    # ------------------------------------------------------------

    df_porte = pd.concat(
        [df_porte_municipios, df_estado],
        ignore_index=True
    )

    df_faixa = pd.concat(
        [df_faixa_municipios, df_faixa_estado],
        ignore_index=True
    )

    df_qtd_tipo_doc = pd.concat(
        [df_qtd_tipo_doc_municipios, df_qtd_tipo_doc_estado],
        ignore_index=True
    )

    df_valor_tipo_doc = pd.concat(
        [df_valor_tipo_doc_municipios, df_valor_tipo_doc_estado],
        ignore_index=True
    )

    df_min_valor_tipo_doc = pd.concat(
        [df_min_valor_tipo_doc_municipios, df_min_valor_tipo_doc_estado],
        ignore_index=True
    )

    df_mediana_valor_tipo_doc = pd.concat(
        [df_mediana_valor_tipo_doc_municipios, df_mediana_valor_tipo_doc_estado],
        ignore_index=True
    )

    df_max_valor_tipo_doc = pd.concat(
        [df_max_valor_tipo_doc_municipios, df_max_valor_tipo_doc_estado],
        ignore_index=True
    )

    df_media_valor_tipo_doc = pd.concat(
        [df_media_valor_tipo_doc_municipios, df_media_valor_tipo_doc_estado],
        ignore_index=True
    )

    df_qtd_sexo = pd.concat(
        [df_qtd_sexo_municipios, df_qtd_sexo_estado],
        ignore_index=True
    )

    df_valor_sexo = pd.concat(
        [df_valor_sexo_municipios, df_valor_sexo_estado],
        ignore_index=True
    )

    df_total_sexo = pd.concat(
        [df_total_sexo_municipios, df_total_sexo_estado],
        ignore_index=True
    )

    df_porte = (
        df_porte
        .merge(df_faixa, on="porte_populacional", how="left")
        .merge(df_qtd_tipo_doc, on="porte_populacional", how="left")
        .merge(df_valor_tipo_doc, on="porte_populacional", how="left")
        .merge(df_min_valor_tipo_doc, on="porte_populacional", how="left")
        .merge(df_mediana_valor_tipo_doc, on="porte_populacional", how="left")
        .merge(df_max_valor_tipo_doc, on="porte_populacional", how="left")
        .merge(df_media_valor_tipo_doc, on="porte_populacional", how="left")
        .merge(df_qtd_sexo, on="porte_populacional", how="left")
        .merge(df_valor_sexo, on="porte_populacional", how="left")
        .merge(df_total_sexo, on="porte_populacional", how="left")
    )

    # ------------------------------------------------------------
    # 17. Calcular percentuais gerais
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
    # 18. Calcular percentuais por Sexo
    # Denominador: apenas registros com Sexo válido
    # ------------------------------------------------------------

    colunas_qtd_sexo = [
        col for col in df_porte.columns
        if col.startswith("qtd_sexo_")
    ]

    colunas_valor_sexo = [
        col for col in df_porte.columns
        if col.startswith("valor_sexo_")
    ]

    for coluna in colunas_qtd_sexo:
        nome_percentual = coluna.replace("qtd_sexo_", "percentual_qtd_sexo_")

        df_porte[nome_percentual] = np.where(
            df_porte["total_qtd_sexo_valido"].fillna(0).ne(0),
            df_porte[coluna] / df_porte["total_qtd_sexo_valido"],
            np.nan
        )

    for coluna in colunas_valor_sexo:
        nome_percentual = coluna.replace("valor_sexo_", "percentual_valor_sexo_")

        df_porte[nome_percentual] = np.where(
            df_porte["total_valor_sexo_valido"].fillna(0).ne(0),
            df_porte[coluna] / df_porte["total_valor_sexo_valido"],
            np.nan
        )

    # ------------------------------------------------------------
    # 19. Identificar colunas
    # ------------------------------------------------------------

    colunas_base = [
        "porte_populacional",
        "numero_municipios",
        "valor_total_por_porte",
        "valor_urbano_por_porte",
        "valor_rural_por_porte",
        "quantidade_contemplados_por_porte",
        "quantidade_contemplados_urbano",
        "quantidade_contemplados_rural",
        "percentual_valor_urbano_por_porte",
        "percentual_valor_rural_por_porte",
        "percentual_valor_por_porte",
        "percentual_quantidade_por_porte",
        "total_qtd_sexo_valido",
        "total_valor_sexo_valido",
    ]

    colunas_qtd_tipo_documento = [
        col for col in df_porte.columns
        if col.startswith("qtd_tipo_documento_")
    ]

    colunas_valor_tipo_documento = [
        col for col in df_porte.columns
        if col.startswith("valor_tipo_documento_")
    ]

    colunas_min_valor_tipo_documento = [
        col for col in df_porte.columns
        if col.startswith("min_valor_tipo_documento_")
    ]

    colunas_mediana_valor_tipo_documento = [
        col for col in df_porte.columns
        if col.startswith("mediana_valor_tipo_documento_")
    ]

    colunas_max_valor_tipo_documento = [
        col for col in df_porte.columns
        if col.startswith("max_valor_tipo_documento_")
    ]

    colunas_media_valor_tipo_documento = [
        col for col in df_porte.columns
        if col.startswith("media_valor_tipo_documento_")
    ]

    colunas_qtd_sexo = [
        col for col in df_porte.columns
        if col.startswith("qtd_sexo_")
    ]

    colunas_valor_sexo = [
        col for col in df_porte.columns
        if col.startswith("valor_sexo_")
    ]

    colunas_percentual_qtd_sexo = [
        col for col in df_porte.columns
        if col.startswith("percentual_qtd_sexo_")
    ]

    colunas_percentual_valor_sexo = [
        col for col in df_porte.columns
        if col.startswith("percentual_valor_sexo_")
    ]

    colunas_faixa_vlr_pago = [
        col for col in df_porte.columns
        if col not in (
            colunas_base
            + colunas_qtd_tipo_documento
            + colunas_valor_tipo_documento
            + colunas_min_valor_tipo_documento
            + colunas_mediana_valor_tipo_documento
            + colunas_max_valor_tipo_documento
            + colunas_media_valor_tipo_documento
            + colunas_qtd_sexo
            + colunas_valor_sexo
            + colunas_percentual_qtd_sexo
            + colunas_percentual_valor_sexo
        )
    ]

    # ------------------------------------------------------------
    # 20. Converter tipos sem arredondar valores monetários
    # ------------------------------------------------------------

    colunas_valor = [
        "valor_total_por_porte",
        "valor_urbano_por_porte",
        "valor_rural_por_porte",
        "total_valor_sexo_valido",
    ]

    colunas_valor_tipo_documento_todas = (
        colunas_valor_tipo_documento
        + colunas_min_valor_tipo_documento
        + colunas_mediana_valor_tipo_documento
        + colunas_max_valor_tipo_documento
        + colunas_media_valor_tipo_documento
    )

    colunas_valor_todas = (
        colunas_valor
        + colunas_valor_tipo_documento_todas
        + colunas_valor_sexo
    )

    # Mantém valores monetários como decimal, sem ceil, sem round e sem converter para inteiro
    df_porte[colunas_valor_todas] = (
        df_porte[colunas_valor_todas]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .astype("Float64")
    )

    colunas_quantidade = [
        "numero_municipios",
        "quantidade_contemplados_por_porte",
        "quantidade_contemplados_urbano",
        "quantidade_contemplados_rural",
        "total_qtd_sexo_valido",
    ]

    colunas_quantidade_todas = (
        colunas_quantidade
        + colunas_faixa_vlr_pago
        + colunas_qtd_tipo_documento
        + colunas_qtd_sexo
    )

    # Quantidades continuam como inteiros
    df_porte[colunas_quantidade_todas] = (
        df_porte[colunas_quantidade_todas]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .astype("Int64")
    )

    # ------------------------------------------------------------
    # 21. Ordenar tabela
    # ------------------------------------------------------------

    df_porte = (
        df_porte
        .sort_values("valor_total_por_porte", ascending=False)
        .reset_index(drop=True)
    )

    return df_porte

def aggregate_special_territories_by(
    df_cubo: pd.DataFrame,
    categories: list[str],
    by_filter: str = "MUNICIPIO",
) -> pd.DataFrame:
    """
    Agrega valor executado e quantidade de contemplados por tipo de território especial.

    A variável de referência é cod_tipo_nome.

    Também acrescenta, por tipo_documento:
    - quantidade;
    - valor total;
    - valor mínimo;
    - mediana;
    - valor máximo;
    - média.

    Parâmetros
    ----------
    df_cubo : pd.DataFrame
        Base principal.

    by_filter : str
        Recorte territorial usado na agregação.

        Opções:
        - "MUNICIPIO": considera apenas registros municipais.
        - "ESTADO": considera apenas registros estaduais.
        - "UF": considera ESTADO + MUNICIPIO.

    categories : list[str]
        Lista de categorias que devem aparecer no resultado final,
        mesmo quando não houver registros.

    Retorna
    -------
    pd.DataFrame
        Tabela agregada por cod_tipo_nome, com valor, quantidade,
        percentuais e indicadores por tipo_documento.
    """

    by_filter = by_filter.upper()

    df = df_cubo.copy()

    df["tipo_ente_norm"] = (
        df["tipo_ente"]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    if by_filter == "MUNICIPIO":
        df = df[df["tipo_ente_norm"].eq("MUNICIPIO")].copy()

    elif by_filter == "ESTADO":
        df = df[df["tipo_ente_norm"].eq("ESTADO")].copy()

    elif by_filter == "UF":
        df = df[df["tipo_ente_norm"].isin(["ESTADO", "MUNICIPIO"])].copy()

    else:
        raise ValueError("by_filter deve ser 'MUNICIPIO', 'ESTADO' ou 'UF'.")

    df["cod_tipo_nome_tratado"] = (
        df["cod_tipo_nome"]
        .fillna("Não informado")
    )

    df["tipo_documento_tratado"] = (
        df["tipo_documento"]
        .fillna("Não informado")
        .astype(str)
    )

    # ------------------------------------------------------------
    # Agregação principal por território
    # ------------------------------------------------------------

    df_agg = (
        df
        .groupby("cod_tipo_nome_tratado", dropna=False, as_index=False)
        .agg(
            valor_transacao=("valor_transacao", "sum"),
            quantidade_contemplados=("quantidade", "sum")
        )
    )

    df_agg = (
        df_agg
        .set_index("cod_tipo_nome_tratado")
        .reindex(categories, fill_value=0)
        .reset_index()
    )

    # ------------------------------------------------------------
    # Função auxiliar para pivot por tipo_documento
    # ------------------------------------------------------------

    def pivot_tipo_documento_por_territorio(
        df_base: pd.DataFrame,
        values: str,
        aggfunc: str,
        prefixo_coluna: str
    ) -> pd.DataFrame:
        if df_base.empty:
            return pd.DataFrame({"cod_tipo_nome_tratado": categories})

        df_pivot = (
            df_base
            .pivot_table(
                index="cod_tipo_nome_tratado",
                columns="tipo_documento_tratado",
                values=values,
                aggfunc=aggfunc,
                fill_value=0
            )
            .reset_index()
        )

        df_pivot = (
            df_pivot
            .set_index("cod_tipo_nome_tratado")
            .reindex(categories, fill_value=0)
            .reset_index()
        )

        df_pivot = df_pivot.rename(
            columns={
                col: f"{prefixo_coluna}_tipo_documento_{col}"
                for col in df_pivot.columns
                if col != "cod_tipo_nome_tratado"
            }
        )

        return df_pivot

    # ------------------------------------------------------------
    # Tipo_documento
    # ------------------------------------------------------------

    df_qtd_tipo_documento = pivot_tipo_documento_por_territorio(
        df_base=df,
        values="quantidade",
        aggfunc="sum",
        prefixo_coluna="qtd"
    )

    df_valor_tipo_documento = pivot_tipo_documento_por_territorio(
        df_base=df,
        values="valor_transacao",
        aggfunc="sum",
        prefixo_coluna="valor"
    )

    df_min_valor_tipo_documento = pivot_tipo_documento_por_territorio(
        df_base=df,
        values="valor_transacao",
        aggfunc="min",
        prefixo_coluna="min_valor"
    )

    df_mediana_valor_tipo_documento = pivot_tipo_documento_por_territorio(
        df_base=df,
        values="valor_transacao",
        aggfunc="median",
        prefixo_coluna="mediana_valor"
    )

    df_max_valor_tipo_documento = pivot_tipo_documento_por_territorio(
        df_base=df,
        values="valor_transacao",
        aggfunc="max",
        prefixo_coluna="max_valor"
    )

    df_media_valor_tipo_documento = pivot_tipo_documento_por_territorio(
        df_base=df,
        values="valor_transacao",
        aggfunc="mean",
        prefixo_coluna="media_valor"
    )

    # ------------------------------------------------------------
    # Juntar agregação principal + tipo_documento
    # ------------------------------------------------------------

    df_agg = (
        df_agg
        .merge(df_qtd_tipo_documento, on="cod_tipo_nome_tratado", how="left")
        .merge(df_valor_tipo_documento, on="cod_tipo_nome_tratado", how="left")
        .merge(df_min_valor_tipo_documento, on="cod_tipo_nome_tratado", how="left")
        .merge(df_mediana_valor_tipo_documento, on="cod_tipo_nome_tratado", how="left")
        .merge(df_max_valor_tipo_documento, on="cod_tipo_nome_tratado", how="left")
        .merge(df_media_valor_tipo_documento, on="cod_tipo_nome_tratado", how="left")
    )

    # ------------------------------------------------------------
    # Percentuais
    # ------------------------------------------------------------

    valor_total = df_agg["valor_transacao"].sum()
    quantidade_total = df_agg["quantidade_contemplados"].sum()

    df_agg["perc_valor_transacao"] = np.where(
        valor_total > 0,
        df_agg["valor_transacao"] / valor_total,
        0
    )

    df_agg["perc_quantidade_contemplados"] = np.where(
        quantidade_total > 0,
        df_agg["quantidade_contemplados"] / quantidade_total,
        0
    )

    # ------------------------------------------------------------
    # Identificar colunas por tipo
    # ------------------------------------------------------------

    colunas_qtd_tipo_documento = [
        col for col in df_agg.columns
        if col.startswith("qtd_tipo_documento_")
    ]

    colunas_valor_tipo_documento = [
        col for col in df_agg.columns
        if col.startswith("valor_tipo_documento_")
    ]

    colunas_min_valor_tipo_documento = [
        col for col in df_agg.columns
        if col.startswith("min_valor_tipo_documento_")
    ]

    colunas_mediana_valor_tipo_documento = [
        col for col in df_agg.columns
        if col.startswith("mediana_valor_tipo_documento_")
    ]

    colunas_max_valor_tipo_documento = [
        col for col in df_agg.columns
        if col.startswith("max_valor_tipo_documento_")
    ]

    colunas_media_valor_tipo_documento = [
        col for col in df_agg.columns
        if col.startswith("media_valor_tipo_documento_")
    ]

    colunas_valor = (
        ["valor_transacao"]
        + colunas_valor_tipo_documento
        + colunas_min_valor_tipo_documento
        + colunas_mediana_valor_tipo_documento
        + colunas_max_valor_tipo_documento
        + colunas_media_valor_tipo_documento
    )

    colunas_quantidade = (
        ["quantidade_contemplados"]
        + colunas_qtd_tipo_documento
    )

    # ------------------------------------------------------------
    # Formatação
    # ------------------------------------------------------------

    df_agg[colunas_valor] = (
        np.ceil(df_agg[colunas_valor])
        .fillna(0)
        .astype("Int64")
    )

    df_agg[colunas_quantidade] = (
        df_agg[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    df_agg[[
        "perc_valor_transacao",
        "perc_quantidade_contemplados"
    ]] = (
        df_agg[[
            "perc_valor_transacao",
            "perc_quantidade_contemplados"
        ]]
        .round(4)
    )

    # ------------------------------------------------------------
    # Renomear e ordenar colunas
    # ------------------------------------------------------------

    df_agg = df_agg.rename(
        columns={"cod_tipo_nome_tratado": "cod_tipo_nome"}
    )

    colunas_finais = [
        "cod_tipo_nome",
        "valor_transacao",
        "perc_valor_transacao",
        "quantidade_contemplados",
        "perc_quantidade_contemplados",
    ] + (
        colunas_qtd_tipo_documento
        + colunas_valor_tipo_documento
        + colunas_min_valor_tipo_documento
        + colunas_mediana_valor_tipo_documento
        + colunas_max_valor_tipo_documento
        + colunas_media_valor_tipo_documento
    )

    df_agg = df_agg[colunas_finais]

    return df_agg

def generate_special_territories_brazil_view(
    df_cubo: pd.DataFrame
) -> pd.DataFrame:
    """
    Gera visão Brasil para territórios especiais selecionados.

    Considera:
    - valor total Brasil = ESTADO + MUNICIPIO;
    - população Brasil = população dos ESTADOS, uma vez por UF;
    - territórios:
        - Favela e Comunidade Urbana
        - Agrupamento quilombola
        - Agrupamento indígena
    """

    # ------------------------------------------------------------
    # 1. Copiar base
    # ------------------------------------------------------------

    df_territorio = df_cubo.copy()

    # ------------------------------------------------------------
    # 2. Normalizar tipo_ente e tratar cod_tipo_nome
    # ------------------------------------------------------------

    df_territorio["tipo_ente_norm"] = (
        df_territorio["tipo_ente"]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df_territorio["cod_tipo_nome_tratado"] = (
        df_territorio["cod_tipo_nome"]
        .fillna("Não informado")
    )

    # ------------------------------------------------------------
    # 3. Categorias de interesse
    # ------------------------------------------------------------

    categorias_territorio = [
        "Favela e Comunidade Urbana",
        "Agrupamento quilombola",
        "Agrupamento indígena"
    ]

    # ------------------------------------------------------------
    # 4. Percentual fixo da população no território - IBGE
    # ------------------------------------------------------------

    dict_perc_populacao_territorio = {
        "Favela e Comunidade Urbana": 8.00,
        "Agrupamento quilombola": 0.70,
        "Agrupamento indígena": 0.83
    }

    # ------------------------------------------------------------
    # 5. Valor total Brasil
    # Estado + municípios
    # ------------------------------------------------------------

    valor_total_brasil = df_territorio["valor_transacao"].sum()

    # ------------------------------------------------------------
    # 6. População total Brasil
    # Usando sum_populacao das linhas de ESTADO
    # Uma vez por UF, para evitar duplicação
    # ------------------------------------------------------------

    populacao_brasil = (
        df_territorio
        .loc[df_territorio["tipo_ente_norm"].eq("ESTADO")]
        .groupby("uf", as_index=False)
        .agg(populacao_uf=("sum_populacao", "max"))
        ["populacao_uf"]
        .sum()
    )

    # ------------------------------------------------------------
    # 7. Agregar Brasil por tipo de território
    # Estado + municípios
    # ------------------------------------------------------------

    df_vis_territorio_brasil = (
        df_territorio
        .loc[df_territorio["cod_tipo_nome_tratado"].isin(categorias_territorio)]
        .groupby("cod_tipo_nome_tratado", as_index=False)
        .agg(
            valor=("valor_transacao", "sum"),
            quantidade_contemplados=("quantidade", "sum")
        )
    )

    # ------------------------------------------------------------
    # 8. Garantir que as 3 linhas apareçam
    # ------------------------------------------------------------

    df_vis_territorio_brasil = (
        df_vis_territorio_brasil
        .set_index("cod_tipo_nome_tratado")
        .reindex(categorias_territorio, fill_value=0)
        .reset_index()
    )

    # ------------------------------------------------------------
    # 9. Calcular percentuais
    # ------------------------------------------------------------

    df_vis_territorio_brasil["perc_recurso_total"] = np.where(
        valor_total_brasil > 0,
        df_vis_territorio_brasil["valor"] / valor_total_brasil,
        0
    )

    df_vis_territorio_brasil["perc_agentes_contemplados"] = np.where(
        populacao_brasil > 0,
        df_vis_territorio_brasil["quantidade_contemplados"] / populacao_brasil,
        0
    )

    df_vis_territorio_brasil["perc_populacao_no_territorio"] = (
        df_vis_territorio_brasil["cod_tipo_nome_tratado"]
        .map(dict_perc_populacao_territorio)
    )

    # ------------------------------------------------------------
    # 10. Formatar valores
    # ------------------------------------------------------------

    df_vis_territorio_brasil["valor"] = (
        np.ceil(df_vis_territorio_brasil["valor"])
        .astype("Int64")
    )

    df_vis_territorio_brasil["quantidade_contemplados"] = (
        df_vis_territorio_brasil["quantidade_contemplados"]
        .fillna(0)
        .astype("Int64")
    )

    df_vis_territorio_brasil["perc_recurso_total"] = (
        df_vis_territorio_brasil["perc_recurso_total"] * 100
    ).round(2)

    df_vis_territorio_brasil["perc_agentes_contemplados"] = (
        df_vis_territorio_brasil["perc_agentes_contemplados"] * 100
    ).round(2)

    # ------------------------------------------------------------
    # 11. Renomear colunas finais
    # ------------------------------------------------------------

    df_vis_territorio_brasil = (
        df_vis_territorio_brasil
        .rename(columns={
            "cod_tipo_nome_tratado": "territorio",
            "valor": "Valor (R$)",
            "quantidade_contemplados": "Quantidade de contemplados",
            "perc_recurso_total": "% recurso total",
            "perc_agentes_contemplados": "% de agentes contemplados",
            "perc_populacao_no_territorio": "% população no território"
        })
        [
            [
                "territorio",
                "Valor (R$)",
                "Quantidade de contemplados",
                "% recurso total",
                "% de agentes contemplados",
                "% população no território"
            ]
        ]
    )

    return df_vis_territorio_brasil


def aggregate_faixa_valor_by(
    df_cubo: pd.DataFrame,
    by_filter: str = "UF"
) -> pd.DataFrame:
    """
    Agrega quantidade de contemplados por faixa de valor pago.

    Parâmetros
    ----------
    df_cubo : pd.DataFrame
        Base principal.

    by_filter : str
        Recorte territorial usado na agregação.

        Opções:
        - "ESTADO": considera apenas registros estaduais.
        - "MUNICIPIO": considera apenas registros municipais.
        - "UF": considera ESTADO + MUNICIPIO.

    Retorna
    -------
    pd.DataFrame
        Tabela com quantidade e percentual de contemplados por faixa de valor.
    """

    by_filter = by_filter.upper()

    # ------------------------------------------------------------
    # 1. Copiar base
    # ------------------------------------------------------------

    df_faixa = df_cubo.copy()

    # ------------------------------------------------------------
    # 2. Normalizar tipo_ente
    # ------------------------------------------------------------

    df_faixa["tipo_ente_norm"] = (
        df_faixa["tipo_ente"]
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
        df_faixa = df_faixa[
            df_faixa["tipo_ente_norm"].eq("ESTADO")
        ].copy()

    elif by_filter == "MUNICIPIO":
        df_faixa = df_faixa[
            df_faixa["tipo_ente_norm"].eq("MUNICIPIO")
        ].copy()

    elif by_filter == "UF":
        df_faixa = df_faixa[
            df_faixa["tipo_ente_norm"].isin(["ESTADO", "MUNICIPIO"])
        ].copy()

    else:
        raise ValueError("by_filter deve ser 'ESTADO', 'MUNICIPIO' ou 'UF'.")

    # ------------------------------------------------------------
    # 4. Ordem desejada das faixas
    # ------------------------------------------------------------

    ordem_faixa_vlr_pago = [
        "Até 2 mil",
        "2 a 10 mil",
        "10 a 50 mil",
        "50 a 200 mil",
        "200 a 500 mil",
        "500 mil a 1 milhão",
        "1 milhão a 10 milhões",
        "Acima de 10 milhões"
    ]

    # ------------------------------------------------------------
    # 5. Tratar faixa_vlr_pago
    # ------------------------------------------------------------

    df_faixa["faixa_vlr_pago_tratada"] = (
        df_faixa["faixa_vlr_pago"]
        .fillna("Não informado")
    )

    # ------------------------------------------------------------
    # 6. Agregar por faixa de valor
    # ------------------------------------------------------------

    df_faixa_vlr = (
        df_faixa
        .groupby("faixa_vlr_pago_tratada", as_index=False)
        .agg(
            quantidade_contemplados=("quantidade", "sum")
        )
    )

    # ------------------------------------------------------------
    # 7. Garantir que todas as faixas apareçam
    # ------------------------------------------------------------

    df_faixa_vlr = (
        df_faixa_vlr
        .set_index("faixa_vlr_pago_tratada")
        .reindex(ordem_faixa_vlr_pago, fill_value=0)
        .reset_index()
    )

    # ------------------------------------------------------------
    # 8. Calcular percentual
    # ------------------------------------------------------------

    total_contemplados = df_faixa_vlr["quantidade_contemplados"].sum()

    df_faixa_vlr["perc_quantidade_contemplados"] = np.where(
        total_contemplados > 0,
        df_faixa_vlr["quantidade_contemplados"] / total_contemplados,
        0
    )

    # ------------------------------------------------------------
    # 9. Formatar valores
    # ------------------------------------------------------------

    df_faixa_vlr["quantidade_contemplados"] = (
        df_faixa_vlr["quantidade_contemplados"]
        .fillna(0)
        .astype("Int64")
    )

    # ------------------------------------------------------------
    # 10. Renomear colunas finais
    # ------------------------------------------------------------

    df_faixa_vlr = (
        df_faixa_vlr
        .rename(columns={
            "faixa_vlr_pago_tratada": "faixa_vlr_pago",
            "quantidade_contemplados": "Quantidade de contemplados",
            "perc_quantidade_contemplados": "% de contemplados"
        })
    )

    return df_faixa_vlr


def aggregate_execution_by_person_type(
    df_cubo: pd.DataFrame,
    by_filter: str = "UF"
) -> pd.DataFrame:

    """
    Agrega valor executado e quantidade de contemplados por tipo_documento.

    Também acrescenta a quantidade de contemplados por faixa_vlr_pago,
    com cada faixa aparecendo como uma coluna.

    Parâmetros
    ----------
    df_cubo : pd.DataFrame
        Base principal.

    by_filter : str
        Recorte territorial usado na agregação.

        Opções:
        - "ESTADO": considera apenas registros estaduais.
        - "MUNICIPIO": considera apenas registros municipais.
        - "UF": considera ESTADO + MUNICIPIO.

    Retorna
    -------
    pd.DataFrame
        Tabela agregada por tipo_documento, com valores absolutos,
        percentuais, estatísticas de valor e faixas de valor pago.
    """

    by_filter = by_filter.upper()

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
    # 2. Aplicar filtro territorial
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
    # 3. Tratar tipo_documento e faixa_vlr_pago
    # ------------------------------------------------------------

    df["tipo_documento_tratado"] = (
        df["tipo_documento"]
        .fillna("Não informado")
    )

    df["faixa_vlr_pago_tratada"] = (
        df["faixa_vlr_pago"]
        .fillna("Não informado")
    )

    ordem_faixa_vlr_pago = [
        "Até 2 mil",
        "2 a 10 mil",
        "10 a 50 mil",
        "50 a 200 mil",
        "200 a 500 mil",
        "500 mil a 1 milhão",
        "1 milhão a 10 milhões",
        "Acima de 10 milhões"
    ]

    # ------------------------------------------------------------
    # 4. Agregar por tipo_documento
    # ------------------------------------------------------------

    df_tipo_documento = (
        df
        .groupby("tipo_documento_tratado", dropna=False, as_index=False)
        .agg(
            valor_executado_rs=("valor_transacao", "sum"),
            qtde_contemplados=("quantidade", "sum"),
            min_valor=("valor_transacao", "min"),
            mediana_valor=("valor_transacao", "median"),
            max_valor=("valor_transacao", "max"),
            media_valor=("valor_transacao", "mean")
        )
    )

    # ------------------------------------------------------------
    # 5. Quantidade de contemplados por faixa_vlr_pago
    # ------------------------------------------------------------

    df_faixa_vlr_pago = (
        df
        .pivot_table(
            index="tipo_documento_tratado",
            columns="faixa_vlr_pago_tratada",
            values="quantidade",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    # Garantir ordem das colunas de faixa quando existirem
    colunas_faixa_existentes = [
        coluna
        for coluna in ordem_faixa_vlr_pago
        if coluna in df_faixa_vlr_pago.columns
    ]

    df_faixa_vlr_pago = df_faixa_vlr_pago[
        ["tipo_documento_tratado"] + colunas_faixa_existentes
    ]

    # ------------------------------------------------------------
    # 6. Juntar tabela principal com faixas
    # ------------------------------------------------------------

    df_tipo_documento = df_tipo_documento.merge(
        df_faixa_vlr_pago,
        on="tipo_documento_tratado",
        how="left"
    )

    # ------------------------------------------------------------
    # 7. Calcular percentuais
    # ------------------------------------------------------------

    valor_total = df_tipo_documento["valor_executado_rs"].sum()
    quantidade_total = df_tipo_documento["qtde_contemplados"].sum()

    df_tipo_documento["perc_valor_executado"] = np.where(
        valor_total > 0,
        df_tipo_documento["valor_executado_rs"] / valor_total,
        0
    )

    df_tipo_documento["perc_qtde_contemplados"] = np.where(
        quantidade_total > 0,
        df_tipo_documento["qtde_contemplados"] / quantidade_total,
        0
    )

    # ------------------------------------------------------------
    # 8. Formatar valores
    # ------------------------------------------------------------

    colunas_valor = [
        "valor_executado_rs",
        "min_valor",
        "mediana_valor",
        "max_valor",
        "media_valor"
    ]

    df_tipo_documento[colunas_valor] = (
        np.ceil(df_tipo_documento[colunas_valor])
        .astype("Int64")
    )

    colunas_quantidade = [
        "qtde_contemplados"
    ] + colunas_faixa_existentes

    df_tipo_documento[colunas_quantidade] = (
        df_tipo_documento[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    # ------------------------------------------------------------
    # 9. Renomear e ordenar
    # ------------------------------------------------------------

    colunas_finais = [
        "tipo_documento",
        "valor_executado_rs",
        "perc_valor_executado",
        "qtde_contemplados",
        "perc_qtde_contemplados",
        "min_valor",
        "mediana_valor",
        "max_valor",
        "media_valor",
    ] + colunas_faixa_existentes

    df_tipo_documento = (
        df_tipo_documento
        .rename(columns={
            "tipo_documento_tratado": "tipo_documento"
        })
        [colunas_finais]
        .sort_values("valor_executado_rs", ascending=False)
        .reset_index(drop=True)
    )

    return df_tipo_documento


def aggregate_execution_by_region(
    df_cubo: pd.DataFrame,
    by_filter: str = "ESTADO"
) -> pd.DataFrame:
    """
    Agrega valor executado, quantidade de contemplados e população por região.

    Também acrescenta, por tipo_documento:
    - quantidade;
    - valor total;
    - valor mínimo;
    - mediana;
    - valor máximo;
    - média.

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

    # ------------------------------------------------------------
    # Tratar tipo_documento
    # ------------------------------------------------------------

    df_valores["tipo_documento_tratado"] = (
        df_valores["tipo_documento"]
        .fillna("Não informado")
        .astype(str)
    )

    # ------------------------------------------------------------
    # Tabela principal por região
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # População por região
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # Percentuais gerais
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # Função auxiliar para pivot por tipo_documento
    # ------------------------------------------------------------

    def pivot_tipo_documento_por_regiao(
        df_base: pd.DataFrame,
        values: str,
        aggfunc: str,
        prefixo_coluna: str
    ) -> pd.DataFrame:
        df_pivot = (
            df_base
            .pivot_table(
                index="regiao",
                columns="tipo_documento_tratado",
                values=values,
                aggfunc=aggfunc,
                fill_value=0
            )
            .reset_index()
        )

        df_pivot = df_pivot.rename(
            columns={
                col: f"{prefixo_coluna}_tipo_documento_{col}"
                for col in df_pivot.columns
                if col != "regiao"
            }
        )

        return df_pivot

    # ------------------------------------------------------------
    # Tipo_documento por região
    # ------------------------------------------------------------

    df_qtd_tipo_documento = pivot_tipo_documento_por_regiao(
        df_base=df_valores,
        values="quantidade",
        aggfunc="sum",
        prefixo_coluna="qtd"
    )

    df_valor_tipo_documento = pivot_tipo_documento_por_regiao(
        df_base=df_valores,
        values="valor_transacao",
        aggfunc="sum",
        prefixo_coluna="valor"
    )

    df_min_valor_tipo_documento = pivot_tipo_documento_por_regiao(
        df_base=df_valores,
        values="valor_transacao",
        aggfunc="min",
        prefixo_coluna="min_valor"
    )

    df_mediana_valor_tipo_documento = pivot_tipo_documento_por_regiao(
        df_base=df_valores,
        values="valor_transacao",
        aggfunc="median",
        prefixo_coluna="mediana_valor"
    )

    df_max_valor_tipo_documento = pivot_tipo_documento_por_regiao(
        df_base=df_valores,
        values="valor_transacao",
        aggfunc="max",
        prefixo_coluna="max_valor"
    )

    df_media_valor_tipo_documento = pivot_tipo_documento_por_regiao(
        df_base=df_valores,
        values="valor_transacao",
        aggfunc="mean",
        prefixo_coluna="media_valor"
    )

    # ------------------------------------------------------------
    # Juntar tudo
    # ------------------------------------------------------------

    df_tabela_region = (
        df_tabela_region
        .merge(df_qtd_tipo_documento, on="regiao", how="left")
        .merge(df_valor_tipo_documento, on="regiao", how="left")
        .merge(df_min_valor_tipo_documento, on="regiao", how="left")
        .merge(df_mediana_valor_tipo_documento, on="regiao", how="left")
        .merge(df_max_valor_tipo_documento, on="regiao", how="left")
        .merge(df_media_valor_tipo_documento, on="regiao", how="left")
    )

    return df_tabela_region



def aggregate_execution_summary_by_scope(
    df_cubo: pd.DataFrame,
    scope: str = "MUNICIPIO"
) -> pd.DataFrame:
    """
    Agrega número de entes, valor total, quantidade de contemplados
    e valor médio por ente para diferentes recortes territoriais.

    Parâmetros
    ----------
    df_cubo : pd.DataFrame
        Base principal.

    scope : str
        Recorte desejado.

        Opções:
        - "MUNICIPIO": considera todos os municípios.
        - "CAPITAL": considera apenas municípios com flag_capital == True.
        - "ESTADO": considera apenas estados.

    Retorna
    -------
    pd.DataFrame
        Tabela com uma linha agregada para o recorte escolhido.
    """

    scope = scope.upper()

    tipo_ente_normalizado = (
        df_cubo["tipo_ente"]
        .astype(str)
        .str.upper()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    if scope == "MUNICIPIO":
        df = df_cubo[tipo_ente_normalizado.eq("MUNICIPIO")].copy()
        categoria = "municipios"

    elif scope == "CAPITAL":
        flag_capital_normalizada = (
            df_cubo["flag_capital"]
            .astype(str)
            .str.upper()
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )

        df = df_cubo[
            tipo_ente_normalizado.eq("MUNICIPIO")
            & flag_capital_normalizada.isin(["TRUE", "1", "SIM", "S"])
        ].copy()

        categoria = "capitais"

    elif scope == "ESTADO":
        df = df_cubo[tipo_ente_normalizado.eq("ESTADO")].copy()
        categoria = "estados"

    else:
        raise ValueError("scope deve ser 'MUNICIPIO', 'CAPITAL' ou 'ESTADO'.")

    df_agregado = pd.DataFrame({
        "categoria": [categoria],
        "numero_entes": [df["ente"].nunique()],
        "valor_total": [df["valor_transacao"].sum()],
        "contemplados_total": [df["quantidade"].sum()]
    })

    df_agregado["valor_total_dividido_numero_entes"] = (
        df_agregado["valor_total"]
        / df_agregado["numero_entes"]
    )

    colunas_valor = [
        "valor_total",
        "valor_total_dividido_numero_entes"
    ]

    df_agregado[colunas_valor] = (
        np.ceil(df_agregado[colunas_valor])
        .astype("Int64")
    )

    df_agregado["contemplados_total"] = (
        df_agregado["contemplados_total"]
        .astype("Int64")
    )

    df_agregado["numero_entes"] = (
        df_agregado["numero_entes"]
        .astype("Int64")
    )

    return df_agregado


def resumo_valor_por_porte_municipio(
    df_cubo: pd.DataFrame,
    filtrar_municipios: bool = True
) -> pd.DataFrame:
    """
    Gera resumo por porte populacional do município.

    Colunas retornadas:
    - Tipo de município
    - Quantidade de municípios por Porte
    - Valor total por Porte
    - Valor médio por município

    Parâmetros
    ----------
    df_cubo : pd.DataFrame
        Base principal contendo as colunas:
        - porte_populacional
        - ente
        - valor_transacao
        - tipo_ente, caso filtrar_municipios=True

    filtrar_municipios : bool
        Se True, mantém apenas registros em que tipo_ente == 'MUNICIPIO'.
    """

    df = df_cubo.copy()

    if filtrar_municipios and "tipo_ente" in df.columns:
        df = df[df["tipo_ente"].eq("MUNICIPIO")].copy()

    resumo = (
        df
        .groupby("porte_populacional", dropna=False)
        .agg(
            quantidade_municipios_por_porte=("ente", "nunique"),
            valor_total_por_porte=("valor_transacao", "sum")
        )
        .reset_index()
    )

    resumo["valor_medio_por_municipio"] = (
        resumo["valor_total_por_porte"] / resumo["quantidade_municipios_por_porte"]
    )

    resumo = resumo.rename(columns={
        "porte_populacional": "Tipo de município",
        "quantidade_municipios_por_porte": "Quantidade de municípios por Porte",
        "valor_total_por_porte": "Valor total por Porte",
        "valor_medio_por_municipio": "Valor médio por município"
    })

    return resumo