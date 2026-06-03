import pandas as pd
import numpy as np
import unicodedata
import re



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
    - capital: definida pela coluna flag_capital;
    - interior: definido pela coluna categoria_municipio_ibge,
      quando o valor for "Interior" ou "Regiao Metropolitana".

    Também calcula quantidade e percentual de contemplados por Sexo:
    - Feminino
    - Masculino

    Retorna uma tabela com uma linha.

    Observação:
    - Percentuais retornam em escala decimal, isto é:
      0.57 = 57%.
    - Valores monetários não são arredondados.
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
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    categoria_municipio_normalizada = (
        df_municipios["categoria_municipio_ibge"]
        .astype(str)
        .str.upper()
        .str.strip()
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
        categoria_municipio_normalizada.isin([
            "INTERIOR",
            "REGIAO METROPOLITANA"
        ])
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
            valor_total_capital / valor_total_geral
            if valor_total_geral > 0 else np.nan
        ],
        "percentual_quantidade_capital": [
            quantidade_total_capital / quantidade_total_geral
            if quantidade_total_geral > 0 else np.nan
        ],

        "quantidade_feminino_capital": [quantidade_feminino_capital],
        "percentual_feminino_capital": [
            quantidade_feminino_capital / quantidade_total_capital
            if quantidade_total_capital > 0 else np.nan
        ],
        "quantidade_masculino_capital": [quantidade_masculino_capital],
        "percentual_masculino_capital": [
            quantidade_masculino_capital / quantidade_total_capital
            if quantidade_total_capital > 0 else np.nan
        ],

        "valor_total_interior": [valor_total_interior],
        "quantidade_total_interior": [quantidade_total_interior],
        "percentual_valor_interior": [
            valor_total_interior / valor_total_geral
            if valor_total_geral > 0 else np.nan
        ],
        "percentual_quantidade_interior": [
            quantidade_total_interior / quantidade_total_geral
            if quantidade_total_geral > 0 else np.nan
        ],

        "quantidade_feminino_interior": [quantidade_feminino_interior],
        "percentual_feminino_interior": [
            quantidade_feminino_interior / quantidade_total_interior
            if quantidade_total_interior > 0 else np.nan
        ],
        "quantidade_masculino_interior": [quantidade_masculino_interior],
        "percentual_masculino_interior": [
            quantidade_masculino_interior / quantidade_total_interior
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
        df_resultado[colunas_valor]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_percentual] = (
        df_resultado[colunas_percentual]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
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
    - percentual do valor entre CPF e CNPJ;
    - valor mínimo, mediana, máximo e média por tipo_documento;
    - quantidade por Sexo;
    - valor por Sexo;
    - percentual de quantidade por Sexo;
    - percentual de valor por Sexo.

    Observação:
    - perc_valor_CPF + perc_valor_CNPJ = 1 em cada linha, quando houver valor de CPF ou CNPJ;
    - os percentuais retornam em escala decimal, sem multiplicar por 100;
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
    # 18. Calcular percentuais de valor por tipo_documento
    # Denominador: CPF + CNPJ dentro da própria linha
    # ------------------------------------------------------------

    if "valor_tipo_documento_CPF" not in df_porte.columns:
        df_porte["valor_tipo_documento_CPF"] = 0

    if "valor_tipo_documento_CNPJ" not in df_porte.columns:
        df_porte["valor_tipo_documento_CNPJ"] = 0

    df_porte["valor_total_CPF_CNPJ"] = (
        df_porte["valor_tipo_documento_CPF"].fillna(0)
        + df_porte["valor_tipo_documento_CNPJ"].fillna(0)
    )

    df_porte["perc_valor_CPF"] = np.where(
        df_porte["valor_total_CPF_CNPJ"].ne(0),
        df_porte["valor_tipo_documento_CPF"] / df_porte["valor_total_CPF_CNPJ"],
        np.nan
    )

    df_porte["perc_valor_CNPJ"] = np.where(
        df_porte["valor_total_CPF_CNPJ"].ne(0),
        df_porte["valor_tipo_documento_CNPJ"] / df_porte["valor_total_CPF_CNPJ"],
        np.nan
    )

    # ------------------------------------------------------------
    # 19. Calcular percentuais por Sexo
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
    # 20. Identificar colunas
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
        "valor_total_CPF_CNPJ",
        "perc_valor_CPF",
        "perc_valor_CNPJ",
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
    # 21. Converter tipos sem arredondar valores monetários
    # ------------------------------------------------------------

    colunas_valor = [
        "valor_total_por_porte",
        "valor_urbano_por_porte",
        "valor_rural_por_porte",
        "valor_total_CPF_CNPJ",
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

    df_porte[colunas_quantidade_todas] = (
        df_porte[colunas_quantidade_todas]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .astype("Int64")
    )

    colunas_percentuais = [
        col for col in df_porte.columns
        if (
            col.startswith("percentual_")
            or col.startswith("perc_")
        )
    ]

    df_porte[colunas_percentuais] = (
        df_porte[colunas_percentuais]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    # ------------------------------------------------------------
    # 22. Ordenar tabela
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

    df_agg = df_agg[df_agg['cod_tipo_nome'].isin(["Favela e Comunidade Urbana","Agrupamento quilombola","Agrupamento indígena"])]

    return df_agg

def generate_special_territories_brazil_view(
    df_cubo: pd.DataFrame
) -> pd.DataFrame:
    """
    Gera visão Brasil para territórios especiais selecionados.

    Considera:
    - valor total Brasil = ESTADO + MUNICIPIO;
    - quantidade total de contemplados PNAB = soma da coluna quantidade;
    - população Brasil = população dos ESTADOS, uma vez por UF;
    - territórios:
        - Favela e Comunidade Urbana
        - Agrupamento quilombola
        - Agrupamento indígena

    Observação:
    - A coluna "% de agentes contemplados" representa:
      quantidade de contemplados naquela categoria /
      quantidade total de contemplados da PNAB.
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
    # 5. Valor total Brasil e quantidade total de contemplados PNAB
    # Estado + municípios
    # ------------------------------------------------------------

    valor_total_brasil = df_territorio["valor_transacao"].sum()
    quantidade_total_pnab = df_territorio["quantidade"].sum()

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
        quantidade_total_pnab > 0,
        df_vis_territorio_brasil["quantidade_contemplados"] / quantidade_total_pnab,
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
        df_vis_territorio_brasil["perc_recurso_total"]
    ).round(2)

    df_vis_territorio_brasil["perc_agentes_contemplados"] = (
        df_vis_territorio_brasil["perc_agentes_contemplados"]
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


def aggregate_by_local_residencia(
    df_cubo: pd.DataFrame,
    visao: str = "uf",
    tipo_documento: str | None = None
) -> pd.DataFrame:
    """
    Agrega quantidade de contemplados, valor total, número de municípios,
    população e percentuais por local de residência.

    A coluna sum_populacao se repete para cada município/estado que aparece.
    Por isso, para calcular população, considera-se apenas o primeiro valor
    de sum_populacao para cada combinação de:
    - local_residencia_contemplados
    - ente

    Percentuais retornam em escala decimal:
    - 0.57 = 57%
    """

    visao = visao.lower().strip()

    if visao not in ["estado", "municipio", "uf"]:
        raise ValueError("visao deve ser 'estado', 'municipio' ou 'uf'.")

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

    if tipo_documento is not None:
        tipo_documento_norm = (
            str(tipo_documento)
            .upper()
            .strip()
        )

        df["tipo_documento_norm"] = (
            df["tipo_documento"]
            .astype(str)
            .str.upper()
            .str.strip()
        )

        df = df[df["tipo_documento_norm"].eq(tipo_documento_norm)].copy()

    if visao == "estado":
        df = df[df["tipo_ente_norm"].eq("ESTADO")].copy()

    elif visao == "municipio":
        df = df[df["tipo_ente_norm"].eq("MUNICIPIO")].copy()

    categorias = [
        "Interior",
        "Regiao Metropolitana",
        "Capital"
    ]

    df["local_residencia_contemplados"] = pd.Categorical(
        df["local_residencia_contemplados"],
        categories=categorias,
        ordered=True
    )

    df_resultado = (
        df
        .groupby("local_residencia_contemplados", observed=False)
        .agg(
            numero_municipios=("ente", "nunique"),
            quantidade_contemplados=("quantidade", "sum"),
            valor_total=("valor_transacao", "sum")
        )
        .reset_index()
    )

    # População sem duplicar o mesmo ente dentro da mesma categoria
    df_populacao = (
        df
        .dropna(subset=["sum_populacao"])
        .sort_values(["local_residencia_contemplados", "ente"])
        .drop_duplicates(
            subset=["local_residencia_contemplados", "ente"],
            keep="first"
        )
        .groupby("local_residencia_contemplados", observed=False)
        .agg(
            populacao=("sum_populacao", "sum")
        )
        .reset_index()
    )

    df_resultado = df_resultado.merge(
        df_populacao,
        on="local_residencia_contemplados",
        how="left"
    )

    quantidade_total = df_resultado["quantidade_contemplados"].sum()
    valor_total_geral = df_resultado["valor_total"].sum()
    populacao_total = df_resultado["populacao"].sum()

    df_resultado["percentual_quantidade"] = np.where(
        quantidade_total > 0,
        df_resultado["quantidade_contemplados"] / quantidade_total,
        np.nan
    )

    df_resultado["percentual_valor"] = np.where(
        valor_total_geral > 0,
        df_resultado["valor_total"] / valor_total_geral,
        np.nan
    )

    df_resultado["perc_populacao"] = np.where(
        populacao_total > 0,
        df_resultado["populacao"] / populacao_total,
        np.nan
    )

    df_resultado["visao"] = visao

    df_resultado["tipo_documento_filtro"] = (
        tipo_documento if tipo_documento is not None else "Todos"
    )

    df_resultado["numero_municipios"] = (
        df_resultado["numero_municipios"]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado["quantidade_contemplados"] = (
        df_resultado["quantidade_contemplados"]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado["valor_total"] = (
        pd.to_numeric(df_resultado["valor_total"], errors="coerce")
        .fillna(0)
        .astype("Float64")
    )

    df_resultado["populacao"] = (
        pd.to_numeric(df_resultado["populacao"], errors="coerce")
        .fillna(0)
        .astype("Float64")
    )

    df_resultado["percentual_quantidade"] = (
        pd.to_numeric(df_resultado["percentual_quantidade"], errors="coerce")
        .astype("Float64")
    )

    df_resultado["percentual_valor"] = (
        pd.to_numeric(df_resultado["percentual_valor"], errors="coerce")
        .astype("Float64")
    )

    df_resultado["perc_populacao"] = (
        pd.to_numeric(df_resultado["perc_populacao"], errors="coerce")
        .astype("Float64")
    )

    return df_resultado

def aggregate_faixa_valor_ju_by(
    df_cubo: pd.DataFrame,
    by_filter: str = "UF"
) -> pd.DataFrame:
    """
    Agrega quantidade de contemplados e valor total por faixa de valor pago
    usando a coluna faixa_vlr_pago_ju_bbagil.

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
        Tabela com quantidade, valor total e percentuais por faixa de valor.
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
        "De 2 a 10 mil",
        "De 10 a 50 mil",
        "De 50 a 200 mil",
        "Acima de 200 mil"
    ]

    # ------------------------------------------------------------
    # 5. Tratar faixa_vlr_pago_ju_bbagil
    # ------------------------------------------------------------

    df_faixa["faixa_vlr_pago_ju_bbagil_tratada"] = (
        df_faixa["faixa_vlr_pago_ju_bbagil"]
        .fillna("Não informado")
    )

    # ------------------------------------------------------------
    # 6. Agregar por faixa de valor
    # ------------------------------------------------------------

    df_faixa_vlr = (
        df_faixa
        .groupby("faixa_vlr_pago_ju_bbagil_tratada", as_index=False)
        .agg(
            quantidade_contemplados=("quantidade", "sum"),
            valor_total=("valor_transacao", "sum")
        )
    )

    # ------------------------------------------------------------
    # 7. Garantir que todas as faixas apareçam
    # ------------------------------------------------------------

    df_faixa_vlr = (
        df_faixa_vlr
        .set_index("faixa_vlr_pago_ju_bbagil_tratada")
        .reindex(ordem_faixa_vlr_pago, fill_value=0)
        .reset_index()
    )

    # ------------------------------------------------------------
    # 8. Calcular percentuais
    # ------------------------------------------------------------

    total_contemplados = df_faixa_vlr["quantidade_contemplados"].sum()
    valor_total_geral = df_faixa_vlr["valor_total"].sum()

    df_faixa_vlr["perc_quantidade_contemplados"] = np.where(
        total_contemplados > 0,
        df_faixa_vlr["quantidade_contemplados"] / total_contemplados,
        0
    )

    df_faixa_vlr["perc_valor_total"] = np.where(
        valor_total_geral > 0,
        df_faixa_vlr["valor_total"] / valor_total_geral,
        0
    )

    # ------------------------------------------------------------
    # 9. Formatar tipos sem arredondar valores
    # ------------------------------------------------------------

    df_faixa_vlr["quantidade_contemplados"] = (
        df_faixa_vlr["quantidade_contemplados"]
        .fillna(0)
        .astype("Int64")
    )

    df_faixa_vlr["valor_total"] = (
        pd.to_numeric(df_faixa_vlr["valor_total"], errors="coerce")
        .fillna(0)
        .astype("Float64")
    )

    df_faixa_vlr["perc_quantidade_contemplados"] = (
        pd.to_numeric(
            df_faixa_vlr["perc_quantidade_contemplados"],
            errors="coerce"
        )
        .astype("Float64")
    )

    df_faixa_vlr["perc_valor_total"] = (
        pd.to_numeric(
            df_faixa_vlr["perc_valor_total"],
            errors="coerce"
        )
        .astype("Float64")
    )

    # ------------------------------------------------------------
    # 10. Renomear colunas finais
    # ------------------------------------------------------------

    df_faixa_vlr = (
        df_faixa_vlr
        .rename(columns={
            "faixa_vlr_pago_ju_bbagil_tratada": "faixa_vlr_pago_ju_bbagil",
            "quantidade_contemplados": "Quantidade de contemplados",
            "perc_quantidade_contemplados": "% de contemplados",
            "valor_total": "Valor total",
            "perc_valor_total": "% do valor total"
        })
    )

    return df_faixa_vlr 



def aggregate_faixa_valor_ju_by_uf(
    df_cubo: pd.DataFrame,
    by_filter: str = "UF"
) -> pd.DataFrame:
    """
    Agrega, para cada UF, a quantidade de contemplados e o valor total
    por faixa de valor pago, usando a coluna faixa_vlr_pago_ju_bbagil.

    Também calcula:
    - percentual da quantidade da faixa em relação ao total de contemplados da UF;
    - percentual do valor da faixa em relação ao valor total executado na UF.

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
        Tabela longa com UF, faixa de valor, quantidade, valor e percentuais.
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
        df["tipo_ente"]
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
        df = df[
            df["tipo_ente_norm"].eq("ESTADO")
        ].copy()

    elif by_filter == "MUNICIPIO":
        df = df[
            df["tipo_ente_norm"].eq("MUNICIPIO")
        ].copy()

    elif by_filter == "UF":
        df = df[
            df["tipo_ente_norm"].isin(["ESTADO", "MUNICIPIO"])
        ].copy()

    else:
        raise ValueError("by_filter deve ser 'ESTADO', 'MUNICIPIO' ou 'UF'.")

    # ------------------------------------------------------------
    # 4. Ordem desejada das faixas
    # ------------------------------------------------------------

    ordem_faixa_vlr_pago = [
        "Até 2 mil",
        "De 2 a 10 mil",
        "De 10 a 50 mil",
        "De 50 a 200 mil",
        "Acima de 200 mil"
    ]

    # ------------------------------------------------------------
    # 5. Tratar faixa_vlr_pago_ju_bbagil
    # ------------------------------------------------------------

    df["faixa_vlr_pago_ju_bbagil_tratada"] = (
        df["faixa_vlr_pago_ju_bbagil"]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------------
    # 6. Agregar por UF e faixa de valor
    # ------------------------------------------------------------

    df_resultado = (
        df
        .groupby(
            ["uf", "faixa_vlr_pago_ju_bbagil_tratada"],
            as_index=False
        )
        .agg(
            quantidade_contemplados=("quantidade", "sum"),
            valor_total=("valor_transacao", "sum")
        )
    )

    # ------------------------------------------------------------
    # 7. Garantir todas as combinações UF x faixa
    # ------------------------------------------------------------

    ufs = sorted(df["uf"].dropna().unique())

    index_completo = pd.MultiIndex.from_product(
        [ufs, ordem_faixa_vlr_pago],
        names=["uf", "faixa_vlr_pago_ju_bbagil_tratada"]
    )

    df_resultado = (
        df_resultado
        .set_index(["uf", "faixa_vlr_pago_ju_bbagil_tratada"])
        .reindex(index_completo, fill_value=0)
        .reset_index()
    )

    # ------------------------------------------------------------
    # 8. Calcular totais por UF
    # ------------------------------------------------------------

    df_totais_uf = (
        df_resultado
        .groupby("uf", as_index=False)
        .agg(
            total_contemplados_uf=("quantidade_contemplados", "sum"),
            valor_total_uf=("valor_total", "sum")
        )
    )

    df_resultado = df_resultado.merge(
        df_totais_uf,
        on="uf",
        how="left"
    )

    # ------------------------------------------------------------
    # 9. Calcular percentuais dentro da UF
    # ------------------------------------------------------------

    df_resultado["perc_quantidade_contemplados_uf"] = np.where(
        df_resultado["total_contemplados_uf"].ne(0),
        df_resultado["quantidade_contemplados"] / df_resultado["total_contemplados_uf"],
        np.nan
    )

    df_resultado["perc_valor_total_uf"] = np.where(
        df_resultado["valor_total_uf"].ne(0),
        df_resultado["valor_total"] / df_resultado["valor_total_uf"],
        np.nan
    )

    # ------------------------------------------------------------
    # 10. Formatar tipos sem arredondar valores
    # ------------------------------------------------------------

    df_resultado["quantidade_contemplados"] = (
        df_resultado["quantidade_contemplados"]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado["total_contemplados_uf"] = (
        df_resultado["total_contemplados_uf"]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado["valor_total"] = (
        pd.to_numeric(df_resultado["valor_total"], errors="coerce")
        .fillna(0)
        .astype("Float64")
    )

    df_resultado["valor_total_uf"] = (
        pd.to_numeric(df_resultado["valor_total_uf"], errors="coerce")
        .fillna(0)
        .astype("Float64")
    )

    df_resultado["perc_quantidade_contemplados_uf"] = (
        pd.to_numeric(
            df_resultado["perc_quantidade_contemplados_uf"],
            errors="coerce"
        )
        .astype("Float64")
    )

    df_resultado["perc_valor_total_uf"] = (
        pd.to_numeric(
            df_resultado["perc_valor_total_uf"],
            errors="coerce"
        )
        .astype("Float64")
    )

    # ------------------------------------------------------------
    # 11. Renomear colunas finais
    # ------------------------------------------------------------

    df_resultado = (
        df_resultado
        .rename(columns={
            "faixa_vlr_pago_ju_bbagil_tratada": "faixa_vlr_pago_ju_bbagil",
            "quantidade_contemplados": "Quantidade de contemplados",
            "valor_total": "Valor total da faixa",
            "total_contemplados_uf": "Total de contemplados da UF",
            "valor_total_uf": "Valor total da UF",
            "perc_quantidade_contemplados_uf": "% de contemplados na UF",
            "perc_valor_total_uf": "% do valor da UF"
        })
        [
            [
                "uf",
                "faixa_vlr_pago_ju_bbagil",
                "Quantidade de contemplados",
                "% de contemplados na UF",
                "Valor total da faixa",
                "% do valor da UF",
                "Total de contemplados da UF",
                "Valor total da UF"
            ]
        ]
    )

    return df_resultado

def aggregate_faixa_valor_ju_wide_by_uf(
    df_cubo: pd.DataFrame,
    by_filter: str = "UF"
) -> pd.DataFrame:
    """
    Agrega, para cada UF, quantidade de contemplados e valor total
    por faixa de valor pago, em formato largo.

    Usa a coluna:
    - faixa_vlr_pago_ju_bbagil

    Para cada faixa, cria colunas de:
    - quantidade;
    - percentual da quantidade dentro da UF;
    - valor;
    - percentual do valor dentro da UF.

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
        Tabela com uma linha por UF e faixas de valor como colunas.

    Observação
    ----------
    Percentuais retornam em escala decimal:
    - 0.34 = 34%

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
        df["tipo_ente"]
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
        df = df[
            df["tipo_ente_norm"].eq("ESTADO")
        ].copy()

    elif by_filter == "MUNICIPIO":
        df = df[
            df["tipo_ente_norm"].eq("MUNICIPIO")
        ].copy()

    elif by_filter == "UF":
        df = df[
            df["tipo_ente_norm"].isin(["ESTADO", "MUNICIPIO"])
        ].copy()

    else:
        raise ValueError("by_filter deve ser 'ESTADO', 'MUNICIPIO' ou 'UF'.")

    # ------------------------------------------------------------
    # 4. Definir faixas e nomes das colunas
    # ------------------------------------------------------------

    ordem_faixa_vlr_pago = [
        "Até 2 mil",
        "De 2 a 10 mil",
        "De 10 a 50 mil",
        "De 50 a 200 mil",
        "Acima de 200 mil"
    ]

    nomes_colunas_faixa = {
        "Até 2 mil": "ate_2_mil",
        "De 2 a 10 mil": "de_2_a_10_mil",
        "De 10 a 50 mil": "de_10_a_50_mil",
        "De 50 a 200 mil": "de_50_a_200_mil",
        "Acima de 200 mil": "acima_de_200_mil"
    }

    # ------------------------------------------------------------
    # 5. Tratar faixa_vlr_pago_ju_bbagil
    # ------------------------------------------------------------

    df["faixa_vlr_pago_ju_bbagil_tratada"] = (
        df["faixa_vlr_pago_ju_bbagil"]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------------
    # 6. Calcular totais por UF
    # ------------------------------------------------------------

    df_totais_uf = (
        df
        .groupby("uf", as_index=False)
        .agg(
            total_contemplados_uf=("quantidade", "sum"),
            valor_total_uf=("valor_transacao", "sum")
        )
    )

    # ------------------------------------------------------------
    # 7. Agregar por UF e faixa
    # ------------------------------------------------------------

    df_faixa_uf = (
        df
        .loc[df["faixa_vlr_pago_ju_bbagil_tratada"].isin(ordem_faixa_vlr_pago)]
        .groupby(
            ["uf", "faixa_vlr_pago_ju_bbagil_tratada"],
            as_index=False
        )
        .agg(
            quantidade_contemplados=("quantidade", "sum"),
            valor_total=("valor_transacao", "sum")
        )
    )

    # ------------------------------------------------------------
    # 8. Criar pivots de quantidade e valor
    # ------------------------------------------------------------

    df_qtd_pivot = (
        df_faixa_uf
        .pivot_table(
            index="uf",
            columns="faixa_vlr_pago_ju_bbagil_tratada",
            values="quantidade_contemplados",
            aggfunc="sum",
            fill_value=0
        )
        .reindex(columns=ordem_faixa_vlr_pago, fill_value=0)
        .reset_index()
    )

    df_valor_pivot = (
        df_faixa_uf
        .pivot_table(
            index="uf",
            columns="faixa_vlr_pago_ju_bbagil_tratada",
            values="valor_total",
            aggfunc="sum",
            fill_value=0
        )
        .reindex(columns=ordem_faixa_vlr_pago, fill_value=0)
        .reset_index()
    )

    # ------------------------------------------------------------
    # 9. Montar base final com uma linha por UF
    # ------------------------------------------------------------

    df_resultado = df_totais_uf.copy()

    df_resultado = df_resultado.merge(
        df_qtd_pivot,
        on="uf",
        how="left"
    )

    df_resultado = df_resultado.merge(
        df_valor_pivot,
        on="uf",
        how="left",
        suffixes=("_qtd", "_valor")
    )

    # ------------------------------------------------------------
    # 10. Criar colunas finais por faixa
    # ------------------------------------------------------------

    for faixa in ordem_faixa_vlr_pago:
        nome_faixa = nomes_colunas_faixa[faixa]

        coluna_qtd_origem = f"{faixa}_qtd"
        coluna_valor_origem = f"{faixa}_valor"

        if coluna_qtd_origem not in df_resultado.columns:
            df_resultado[coluna_qtd_origem] = 0

        if coluna_valor_origem not in df_resultado.columns:
            df_resultado[coluna_valor_origem] = 0

        df_resultado[f"qtd_{nome_faixa}"] = df_resultado[coluna_qtd_origem]

        df_resultado[f"perc_qtd_{nome_faixa}"] = np.where(
            df_resultado["total_contemplados_uf"].ne(0),
            df_resultado[coluna_qtd_origem] / df_resultado["total_contemplados_uf"],
            np.nan
        )

        df_resultado[f"valor_{nome_faixa}"] = df_resultado[coluna_valor_origem]

        df_resultado[f"perc_valor_{nome_faixa}"] = np.where(
            df_resultado["valor_total_uf"].ne(0),
            df_resultado[coluna_valor_origem] / df_resultado["valor_total_uf"],
            np.nan
        )

    # ------------------------------------------------------------
    # 11. Selecionar e ordenar colunas finais
    # ------------------------------------------------------------

    colunas_finais = [
        "uf",
        "total_contemplados_uf",
        "valor_total_uf"
    ]

    for faixa in ordem_faixa_vlr_pago:
        nome_faixa = nomes_colunas_faixa[faixa]

        colunas_finais.extend([
            f"qtd_{nome_faixa}",
            f"perc_qtd_{nome_faixa}",
            f"valor_{nome_faixa}",
            f"perc_valor_{nome_faixa}"
        ])

    df_resultado = df_resultado[colunas_finais].copy()

    # ------------------------------------------------------------
    # 12. Formatar tipos sem arredondar valores
    # ------------------------------------------------------------

    colunas_quantidade = [
        col for col in df_resultado.columns
        if col.startswith("qtd_") or col == "total_contemplados_uf"
    ]

    colunas_valor = [
        col for col in df_resultado.columns
        if col.startswith("valor_") or col == "valor_total_uf"
    ]

    colunas_percentual = [
        col for col in df_resultado.columns
        if col.startswith("perc_")
    ]

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .astype("Float64")
    )

    df_resultado[colunas_percentual] = (
        df_resultado[colunas_percentual]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    # ------------------------------------------------------------
    # 13. Ordenar por UF
    # ------------------------------------------------------------

    df_resultado = (
        df_resultado
        .sort_values("uf")
        .reset_index(drop=True)
    )

    return df_resultado

def make_boxplot_df_faixa_valor(
    df_aux: pd.DataFrame,
    by_filter: str = "ESTADO",
) -> pd.DataFrame:
    """
    Gera DataFrame em formato longo para montar boxplot dos valores
    recebidos e da quantidade de contemplados por faixa de valor pago.

    Como df_aux está desagrupado, cada linha representa um contemplado.
    Portanto, a quantidade de contemplados é calculada pela contagem
    de linhas em cada grupo de UF e faixa de valor.

    Parâmetros
    ----------
    df_aux : pd.DataFrame
        DataFrame com as colunas:
        - tipo_ente_bbagil
        - uf_bbagil
        - faixa_vlr_pago_ju_bbagil
        - valor_transacao_total_bbagil

    by_filter : str
        Recorte da análise:
        - "ESTADO": considera apenas tipo_ente_bbagil == "ESTADO"
        - "MUNICIPIO": considera apenas tipo_ente_bbagil == "MUNICIPIO"
        - "UF": considera ESTADO + MUNICIPIO

    Retorna
    -------
    pd.DataFrame
        DataFrame em formato longo, pronto para boxplot.

        Colunas:
        - visao
        - uf_bbagil
        - faixa_vlr_pago_ju_bbagil
        - metrica
        - valor_boxplot
        - unidade_observacao
    """

    by_filter = by_filter.upper().strip()

    df = df_aux.copy()

    colunas_obrigatorias = [
        "tipo_ente_bbagil",
        "uf_bbagil",
        "faixa_vlr_pago_ju_bbagil",
        "valor_transacao_total_bbagil",
    ]

    colunas_ausentes = [
        col for col in colunas_obrigatorias
        if col not in df.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            f"As seguintes colunas não existem no DataFrame: {colunas_ausentes}"
        )

    df["tipo_ente_norm"] = (
        df["tipo_ente_bbagil"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    if by_filter == "ESTADO":
        df = df[df["tipo_ente_norm"].eq("ESTADO")].copy()

    elif by_filter == "MUNICIPIO":
        df = df[df["tipo_ente_norm"].eq("MUNICIPIO")].copy()

    elif by_filter == "UF":
        df = df[df["tipo_ente_norm"].isin(["ESTADO", "MUNICIPIO"])].copy()

    else:
        raise ValueError("by_filter deve ser 'ESTADO', 'MUNICIPIO' ou 'UF'.")

    ordem_faixas = [
        "Até 2 mil",
        "De 2 a 10 mil",
        "De 10 a 50 mil",
        "De 50 a 200 mil",
        "Acima de 200 mil",
    ]

    df["valor_transacao_total_bbagil"] = pd.to_numeric(
        df["valor_transacao_total_bbagil"],
        errors="coerce"
    )

    df["faixa_vlr_pago_ju_bbagil"] = (
        df["faixa_vlr_pago_ju_bbagil"]
        .astype(str)
        .str.strip()
    )

    df = df[
        df["faixa_vlr_pago_ju_bbagil"].isin(ordem_faixas)
    ].copy()

    df = df.dropna(
        subset=[
            "uf_bbagil",
            "faixa_vlr_pago_ju_bbagil",
            "valor_transacao_total_bbagil",
        ]
    ).copy()

    df["faixa_vlr_pago_ju_bbagil"] = pd.Categorical(
        df["faixa_vlr_pago_ju_bbagil"],
        categories=ordem_faixas,
        ordered=True
    )

    df["visao"] = by_filter

    # --------------------------------------------------
    # 1. Base para boxplot dos valores recebidos
    #    Unidade: cada linha é um contemplado
    # --------------------------------------------------

    df_boxplot_valor = df[
        [
            "visao",
            "uf_bbagil",
            "faixa_vlr_pago_ju_bbagil",
            "valor_transacao_total_bbagil",
        ]
    ].copy()

    df_boxplot_valor = df_boxplot_valor.rename(
        columns={
            "valor_transacao_total_bbagil": "valor_boxplot"
        }
    )

    df_boxplot_valor["metrica"] = "valor_transacao_total_bbagil"
    df_boxplot_valor["unidade_observacao"] = "contemplado"

    # --------------------------------------------------
    # 2. Base para boxplot da quantidade de contemplados
    #    Unidade: UF x faixa de valor
    # --------------------------------------------------

    df_boxplot_quantidade = (
        df
        .groupby(
            ["visao", "uf_bbagil", "faixa_vlr_pago_ju_bbagil"],
            observed=True
        )
        .size()
        .reset_index(name="valor_boxplot")
    )

    df_boxplot_quantidade["metrica"] = "quantidade_contemplados"
    df_boxplot_quantidade["unidade_observacao"] = "uf_faixa"

    # --------------------------------------------------
    # Junta as duas bases em formato longo
    # --------------------------------------------------

    df_boxplot = pd.concat(
        [
            df_boxplot_valor,
            df_boxplot_quantidade,
        ],
        ignore_index=True
    )

    df_boxplot = df_boxplot[
        [
            "visao",
            "uf_bbagil",
            "faixa_vlr_pago_ju_bbagil",
            "metrica",
            "valor_boxplot",
            "unidade_observacao",
        ]
    ]

    df_boxplot = (
        df_boxplot
        .sort_values(
            [
                "metrica",
                "uf_bbagil",
                "faixa_vlr_pago_ju_bbagil",
            ]
        )
        .reset_index(drop=True)
    )

    return df_boxplot



def _slugify(texto: str) -> str:
    """
    Converte texto para formato seguro de nome de coluna.
    Ex.: 'Até 2 mil' -> 'ate_2_mil'
    """
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    texto = re.sub(r"_+", "_", texto).strip("_")
    return texto


def resumo_faixa_valor_por_porte(
    df_cubo: pd.DataFrame,
    visao: str = "UF",
    coluna_tipo_ente: str = "tipo_ente",
    coluna_porte: str = "porte_populacional",
    coluna_faixa: str = "faixa_vlr_pago_ju_bbagil",
    coluna_quantidade: str = "quantidade",
    coluna_valor: str = "valor_transacao",
    ordem_faixas: list | None = None,
    percentual_por_linha: bool = True,
) -> pd.DataFrame:
    """
    Retorna uma tabela com uma linha por porte populacional e colunas pivotadas
    por faixa de valor pago.

    Para cada faixa, cria:
    - qtd_contemplados_{faixa}
    - perc_qtd_contemplados_{faixa}
    - valor_transacao_{faixa}
    - perc_valor_transacao_{faixa}

    Parâmetros
    ----------
    df_cubo : pd.DataFrame
        DataFrame de entrada.

    visao : str, default "UF"
        Define o recorte da análise:
        - "ESTADO": filtra tipo_ente == "ESTADO"
        - "MUNICIPIO": filtra tipo_ente == "MUNICIPIO"
        - "UF": não filtra tipo_ente, considerando estados + municípios

    coluna_tipo_ente : str
        Coluna que identifica o tipo do ente.

    coluna_porte : str
        Coluna de porte populacional. Cada linha da saída será um porte.

    coluna_faixa : str
        Coluna com as faixas de valor pago.

    coluna_quantidade : str
        Coluna de quantidade de contemplados.

    coluna_valor : str
        Coluna de valor da transação.

    ordem_faixas : list | None
        Ordem desejada das faixas. Se None, usa a ordem encontrada no DataFrame.

    percentual_por_linha : bool
        Se True, calcula percentuais dentro de cada porte populacional.
        Se False, calcula percentuais sobre o total geral da visão filtrada.

    Retorno
    -------
    pd.DataFrame
        DataFrame consolidado por porte populacional.
    """

    visao = visao.upper().strip()

    if visao not in ["ESTADO", "MUNICIPIO", "UF"]:
        raise ValueError("visao deve ser 'ESTADO', 'MUNICIPIO' ou 'UF'.")

    df = df_cubo.copy()


    if visao == "ESTADO":
        df = df[df[coluna_tipo_ente] == "ESTADO"].copy()

    elif visao == "MUNICIPIO":
        df = df[df[coluna_tipo_ente] == "MUNICIPIO"].copy()

    # Remove registros sem porte ou faixa
    df = df.dropna(subset=[coluna_porte, coluna_faixa])

    if ordem_faixas is None:
        ordem_faixas = list(df[coluna_faixa].dropna().unique())

    # Agrega quantidade e valor por porte e faixa
    df_agg = (
        df
        .groupby([coluna_porte, coluna_faixa], dropna=False)
        .agg(
            qtd_contemplados=(coluna_quantidade, "sum"),
            valor_transacao=(coluna_valor, "sum"),
        )
        .reset_index()
    )

    # Totais por porte
    totais_porte = (
        df_agg
        .groupby(coluna_porte)
        .agg(
            total_qtd_contemplados=("qtd_contemplados", "sum"),
            total_valor_transacao=("valor_transacao", "sum"),
        )
        .reset_index()
    )

    df_agg = df_agg.merge(totais_porte, on=coluna_porte, how="left")

    if percentual_por_linha:
        df_agg["perc_qtd_contemplados"] = (
            df_agg["qtd_contemplados"] / df_agg["total_qtd_contemplados"]
        )

        df_agg["perc_valor_transacao"] = (
            df_agg["valor_transacao"] / df_agg["total_valor_transacao"]
        )

    else:
        total_qtd_geral = df_agg["qtd_contemplados"].sum()
        total_valor_geral = df_agg["valor_transacao"].sum()

        df_agg["perc_qtd_contemplados"] = (
            df_agg["qtd_contemplados"] / total_qtd_geral
        )

        df_agg["perc_valor_transacao"] = (
            df_agg["valor_transacao"] / total_valor_geral
        )

    # Monta tabela final em formato wide
    df_final = totais_porte.copy()

    for faixa in ordem_faixas:
        slug = _slugify(faixa)

        df_faixa = (
            df_agg[df_agg[coluna_faixa] == faixa]
            [[
                coluna_porte,
                "qtd_contemplados",
                "perc_qtd_contemplados",
                "valor_transacao",
                "perc_valor_transacao",
            ]]
            .rename(columns={
                "qtd_contemplados": f"qtd_contemplados_{slug}",
                "perc_qtd_contemplados": f"perc_qtd_contemplados_{slug}",
                "valor_transacao": f"valor_transacao_{slug}",
                "perc_valor_transacao": f"perc_valor_transacao_{slug}",
            })
        )

        df_final = df_final.merge(df_faixa, on=coluna_porte, how="left")

    # Preenche faixas inexistentes com zero
    cols_numericas = df_final.columns.drop(coluna_porte)
    df_final[cols_numericas] = df_final[cols_numericas].fillna(0)

    return df_final

def resumo_territorios_especiais_por_uf(
    df_cubo: pd.DataFrame,
    visao: str = "UF",
    coluna_uf: str = "uf",
    coluna_tipo_ente: str = "tipo_ente",
    coluna_territorio: str = "cod_tipo_nome",
    coluna_quantidade: str = "quantidade",
    coluna_valor: str = "valor_transacao",
    base_percentual: str = "total_uf",
) -> pd.DataFrame:
    """
    Gera uma visão por UF dos recursos e contemplados em territórios especiais.

    Mantém apenas:
    - Favela e Comunidade Urbana
    - Agrupamento quilombola
    - Agrupamento indígena

    Parâmetros
    ----------
    visao : str
        - "ESTADO": filtra tipo_ente == "ESTADO"
        - "UF": não filtra tipo_ente, considerando estados + municípios

    base_percentual : str
        - "total_uf": percentual de cada território em relação ao total da UF.
        - "territorios_especiais": percentual de cada território em relação apenas
          à soma dos três territórios especiais.

    Retorno
    -------
    pd.DataFrame
        DataFrame com uma linha por UF.
    """

    visao = visao.upper().strip()

    if visao not in ["ESTADO", "UF", "MUNICIPIO"]:
        raise ValueError("visao deve ser 'ESTADO' ou 'UF' ou MUNICIPIO.")

    if base_percentual not in ["total_uf", "territorios_especiais"]:
        raise ValueError(
            "base_percentual deve ser 'total_uf' ou 'territorios_especiais'."
        )

    territorios_mantidos = [
        "Favela e Comunidade Urbana",
        "Agrupamento quilombola",
        "Agrupamento indígena",
    ]

    nome_colunas = {
        "Favela e Comunidade Urbana": "favela_comunidade_urbana",
        "Agrupamento quilombola": "agrupamento_quilombola",
        "Agrupamento indígena": "agrupamento_indigena",
    }

    df = df_cubo.copy()

    if visao == "ESTADO":
        df = df[df[coluna_tipo_ente] == "ESTADO"].copy()
    

    elif visao == "MUNICIPIO":
        df = df[df[coluna_tipo_ente] == "MUNICIPIO"].copy()
    

    # Total geral da UF, antes de filtrar os territórios especiais
    total_uf = (
        df
        .groupby(coluna_uf, dropna=False)
        .agg(
            total_qtd_contemplados_uf=(coluna_quantidade, "sum"),
            total_valor_transacao_uf=(coluna_valor, "sum"),
        )
        .reset_index()
    )

    # Base apenas com os três territórios especiais
    df_terr = df[df[coluna_territorio].isin(territorios_mantidos)].copy()

    # Agrega por UF e território
    df_agg = (
        df_terr
        .groupby([coluna_uf, coluna_territorio], dropna=False)
        .agg(
            qtd_contemplados=(coluna_quantidade, "sum"),
            valor_transacao=(coluna_valor, "sum"),
        )
        .reset_index()
    )

    # Soma dos três territórios especiais por UF
    total_territorios_uf = (
        df_agg
        .groupby(coluna_uf, dropna=False)
        .agg(
            qtd_contemplados_territorios_especiais=("qtd_contemplados", "sum"),
            valor_transacao_territorios_especiais=("valor_transacao", "sum"),
        )
        .reset_index()
    )

    # DataFrame-base da saída
    df_final = (
        total_uf
        .merge(total_territorios_uf, on=coluna_uf, how="left")
    )

    df_final[
        [
            "qtd_contemplados_territorios_especiais",
            "valor_transacao_territorios_especiais",
        ]
    ] = df_final[
        [
            "qtd_contemplados_territorios_especiais",
            "valor_transacao_territorios_especiais",
        ]
    ].fillna(0)

    # Percentual da soma dos três territórios especiais dentro da UF
    df_final["perc_qtd_contemplados_territorios_especiais_uf"] = np.where(
        df_final["total_qtd_contemplados_uf"] > 0,
        df_final["qtd_contemplados_territorios_especiais"]
        / df_final["total_qtd_contemplados_uf"],
        0,
    )

    df_final["perc_valor_transacao_territorios_especiais_uf"] = np.where(
        df_final["total_valor_transacao_uf"] > 0,
        df_final["valor_transacao_territorios_especiais"]
        / df_final["total_valor_transacao_uf"],
        0,
    )

    # Junta totais para calcular os percentuais individuais
    df_agg = (
        df_agg
        .merge(total_uf, on=coluna_uf, how="left")
        .merge(total_territorios_uf, on=coluna_uf, how="left")
    )

    if base_percentual == "total_uf":
        df_agg["perc_qtd_contemplados"] = np.where(
            df_agg["total_qtd_contemplados_uf"] > 0,
            df_agg["qtd_contemplados"] / df_agg["total_qtd_contemplados_uf"],
            0,
        )

        df_agg["perc_valor_transacao"] = np.where(
            df_agg["total_valor_transacao_uf"] > 0,
            df_agg["valor_transacao"] / df_agg["total_valor_transacao_uf"],
            0,
        )

    else:
        df_agg["perc_qtd_contemplados"] = np.where(
            df_agg["qtd_contemplados_territorios_especiais"] > 0,
            df_agg["qtd_contemplados"]
            / df_agg["qtd_contemplados_territorios_especiais"],
            0,
        )

        df_agg["perc_valor_transacao"] = np.where(
            df_agg["valor_transacao_territorios_especiais"] > 0,
            df_agg["valor_transacao"]
            / df_agg["valor_transacao_territorios_especiais"],
            0,
        )

    # Cria colunas abertas para cada território especial
    for territorio, nome in nome_colunas.items():
        df_aux = (
            df_agg[df_agg[coluna_territorio] == territorio]
            [[
                coluna_uf,
                "qtd_contemplados",
                "perc_qtd_contemplados",
                "valor_transacao",
                "perc_valor_transacao",
            ]]
            .rename(columns={
                "qtd_contemplados": f"qtd_contemplados_{nome}",
                "perc_qtd_contemplados": f"perc_qtd_contemplados_{nome}",
                "valor_transacao": f"valor_transacao_{nome}",
                "perc_valor_transacao": f"perc_valor_transacao_{nome}",
            })
        )

        df_final = df_final.merge(df_aux, on=coluna_uf, how="left")

    cols_numericas = df_final.columns.drop(coluna_uf)
    df_final[cols_numericas] = df_final[cols_numericas].fillna(0)

    return df_final


def resumo_por_porte_populacional(df_aux: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna um resumo por porte populacional.

    valor_medio_por_porte:
    - média do valor recebido por contemplado.

    valor_medio_porte_municipios:
    - valor médio executado por município dentro daquele porte.
    - cálculo: valor_total_por_porte / numero_municipios.
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

    df = df_aux.copy()
    df = df[df["tipo_ente_bbagil"] == "MUNICIPIO"].copy()

    df["valor_transacao_total_bbagil"] = pd.to_numeric(
        df["valor_transacao_total_bbagil"],
        errors="coerce"
    )

    df_resumo = (
        df
        .groupby("porte_populacional", dropna=False)
        .agg(
            numero_municipios=("ente_bbagil", "nunique"),
            valor_total_por_porte=("valor_transacao_total_bbagil", "sum"),
            valor_medio_por_porte=("valor_transacao_total_bbagil", "mean"),
            media_aparada_1pct_por_porte=(
                "valor_transacao_total_bbagil",
                media_aparada_1pct_superior
            ),
            valor_mediano_por_porte=("valor_transacao_total_bbagil", "median"),
            quantidade_contemplados_por_porte=("chave", "nunique")
        )
        .reset_index()
    )

    df_resumo["valor_medio_porte_municipios"] = np.where(
        df_resumo["numero_municipios"].ne(0),
        df_resumo["valor_total_por_porte"] / df_resumo["numero_municipios"],
        np.nan
    )

    total_valor = df_resumo["valor_total_por_porte"].sum()
    total_quantidade = df_resumo["quantidade_contemplados_por_porte"].sum()

    df_resumo["percentual_valor_por_porte"] = (
        df_resumo["valor_total_por_porte"] / total_valor
    )

    df_resumo["percentual_quantidade_contemplados_por_porte"] = (
        df_resumo["quantidade_contemplados_por_porte"] / total_quantidade
    )

    ordem_portes = [
        "1_pequeno_i",
        "2_pequeno_ii",
        "3_medio",
        "4_grande"
    ]

    df_resumo["porte_populacional"] = pd.Categorical(
        df_resumo["porte_populacional"],
        categories=ordem_portes,
        ordered=True
    )

    df_resumo = (
        df_resumo
        .sort_values("porte_populacional")
        .reset_index(drop=True)
    )

    return df_resumo

def adicionar_macrorregiao_percentuais_uf(
    df_uf_cut: pd.DataFrame,
    col_uf: str = "uf"
) -> pd.DataFrame:
    """
    Adiciona macrorregião e percentuais por UF.

    Percentuais retornam em escala decimal:
    0.25 = 25%
    """

    uf_macrorregiao = {
        # Norte
        "AC": "Norte",
        "AP": "Norte",
        "AM": "Norte",
        "PA": "Norte",
        "RO": "Norte",
        "RR": "Norte",
        "TO": "Norte",

        # Nordeste
        "AL": "Nordeste",
        "BA": "Nordeste",
        "CE": "Nordeste",
        "MA": "Nordeste",
        "PB": "Nordeste",
        "PE": "Nordeste",
        "PI": "Nordeste",
        "RN": "Nordeste",
        "SE": "Nordeste",

        # Centro-Oeste
        "DF": "Centro-Oeste",
        "GO": "Centro-Oeste",
        "MT": "Centro-Oeste",
        "MS": "Centro-Oeste",

        # Sudeste
        "ES": "Sudeste",
        "MG": "Sudeste",
        "RJ": "Sudeste",
        "SP": "Sudeste",

        # Sul
        "PR": "Sul",
        "RS": "Sul",
        "SC": "Sul",
    }

    df = df_uf_cut.copy()

    # Caso a UF esteja no índice, e não em uma coluna
    if col_uf not in df.columns:
        df = df.reset_index()

        if col_uf not in df.columns:
            raise ValueError(
                f"A coluna '{col_uf}' não foi encontrada. "
                "Verifique se a UF está em uma coluna ou ajuste o parâmetro col_uf."
            )

    df[col_uf] = df[col_uf].astype(str).str.upper().str.strip()

    df["macrorregiao"] = df[col_uf].map(uf_macrorregiao)

    ufs_sem_regiao = df.loc[df["macrorregiao"].isna(), col_uf].unique()

    if len(ufs_sem_regiao) > 0:
        raise ValueError(f"UFs sem macrorregião identificada: {ufs_sem_regiao}")

    total_contemplados = df["qtde_contemplados"].sum()

    df["perc_qtde_contemplados_total"] = np.where(
        total_contemplados > 0,
        df["qtde_contemplados"] / total_contemplados,
        np.nan
    )

    total_contemplados_regiao = (
        df.groupby("macrorregiao")["qtde_contemplados"]
        .transform("sum")
    )

    df["perc_qtde_contemplados_regiao"] = np.where(
        total_contemplados_regiao > 0,
        df["qtde_contemplados"] / total_contemplados_regiao,
        np.nan
    )

    total_valor_regiao = (
        df.groupby("macrorregiao")["valor_executado_rs"]
        .transform("sum")
    )

    df["valor_executado_perc_regiao"] = np.where(
        total_valor_regiao > 0,
        df["valor_executado_rs"] / total_valor_regiao,
        np.nan
    )

    return df


def criar_df_uf_cut_from_aux(
    df_aux: pd.DataFrame,
    by_filter: str = "UF",
    col_uf: str = "uf_bbagil",
    col_valor: str = "valor_transacao_total_bbagil",
    col_chave: str = "chave",
    col_populacao: str = "populacao",
    col_tipo_ente: str = "tipo_ente_bbagil"
) -> pd.DataFrame:
    """
    Cria uma tabela agregada por UF a partir da df_aux.

    Parâmetros
    ----------
    by_filter : str
        Define a visão da análise:
        - "UF": considera todos os registros, sem filtro de tipo_ente
        - "ESTADO": considera apenas tipo_ente_bbagil == "ESTADO"

    A população da UF é obtida apenas das linhas em que tipo_ente == 'ESTADO',
    usando o primeiro valor de população encontrado para cada UF.

    Percentuais retornam em escala decimal:
    0.25 = 25%
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

    by_filter = by_filter.upper().strip()

    if by_filter not in ["UF", "ESTADO"]:
        raise ValueError("by_filter deve ser 'UF' ou 'ESTADO'.")

    df = df_aux.copy()

    df[col_uf] = df[col_uf].astype(str).str.upper().str.strip()

    df[col_tipo_ente] = (
        df[col_tipo_ente]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    # ------------------------------------------------------------
    # Filtro da visão
    # ------------------------------------------------------------

    if by_filter == "ESTADO":
        df = df[df[col_tipo_ente].eq("ESTADO")].copy()

    # Se by_filter == "UF", mantém todos os registros.

    uf_macrorregiao = {
        # Norte
        "AC": "Norte",
        "AP": "Norte",
        "AM": "Norte",
        "PA": "Norte",
        "RO": "Norte",
        "RR": "Norte",
        "TO": "Norte",

        # Nordeste
        "AL": "Nordeste",
        "BA": "Nordeste",
        "CE": "Nordeste",
        "MA": "Nordeste",
        "PB": "Nordeste",
        "PE": "Nordeste",
        "PI": "Nordeste",
        "RN": "Nordeste",
        "SE": "Nordeste",

        # Centro-Oeste
        "DF": "Centro-Oeste",
        "GO": "Centro-Oeste",
        "MT": "Centro-Oeste",
        "MS": "Centro-Oeste",

        # Sudeste
        "ES": "Sudeste",
        "MG": "Sudeste",
        "RJ": "Sudeste",
        "SP": "Sudeste",

        # Sul
        "PR": "Sul",
        "RS": "Sul",
        "SC": "Sul",
    }

    df_uf = (
        df
        .groupby(col_uf, dropna=False)
        .agg(
            valor_executado_rs=(col_valor, "sum"),
            min_valor=(col_valor, "min"),
            mediana_valor=(col_valor, "median"),
            max_valor=(col_valor, "max"),
            media_valor=(col_valor, "mean"),
            media_aparada_1pct_valor=(col_valor, media_aparada_1pct_superior),
            qtde_contemplados=(col_chave, "nunique")
        )
        .reset_index()
        .rename(columns={col_uf: "uf"})
    )

    total_valor = df_uf["valor_executado_rs"].sum()

    df_uf["valor_executado_perc"] = np.where(
        total_valor > 0,
        df_uf["valor_executado_rs"] / total_valor,
        np.nan
    )

    # ------------------------------------------------------------
    # População da UF vem sempre das linhas estaduais da base original
    # ------------------------------------------------------------

    df_pop = df_aux.copy()

    df_pop[col_uf] = df_pop[col_uf].astype(str).str.upper().str.strip()

    df_pop[col_tipo_ente] = (
        df_pop[col_tipo_ente]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df_pop_uf = (
        df_pop
        .loc[df_pop[col_tipo_ente].eq("ESTADO"), [col_uf, col_populacao]]
        .dropna(subset=[col_populacao])
        .drop_duplicates(subset=[col_uf])
        .rename(columns={
            col_uf: "uf",
            col_populacao: "populacao_uf"
        })
    )

    df_uf = df_uf.merge(
        df_pop_uf,
        on="uf",
        how="left"
    )

    df_uf["valor_executado_percapita"] = np.where(
        df_uf["populacao_uf"] > 0,
        df_uf["valor_executado_rs"] / df_uf["populacao_uf"],
        np.nan
    )

    df_uf["macrorregiao"] = df_uf["uf"].map(uf_macrorregiao)

    ufs_sem_macrorregiao = df_uf.loc[
        df_uf["macrorregiao"].isna(),
        "uf"
    ].unique()

    if len(ufs_sem_macrorregiao) > 0:
        raise ValueError(
            f"UFs sem macrorregião identificada: {ufs_sem_macrorregiao}"
        )

    total_valor_regiao = (
        df_uf
        .groupby("macrorregiao")["valor_executado_rs"]
        .transform("sum")
    )

    df_uf["valor_executado_perc_regiao"] = np.where(
        total_valor_regiao > 0,
        df_uf["valor_executado_rs"] / total_valor_regiao,
        np.nan
    )

    total_contemplados_regiao = (
        df_uf
        .groupby("macrorregiao")["qtde_contemplados"]
        .transform("sum")
    )

    df_uf["perc_qtde_contemplados_regiao"] = np.where(
        total_contemplados_regiao > 0,
        df_uf["qtde_contemplados"] / total_contemplados_regiao,
        np.nan
    )

    df_uf["visao"] = by_filter

    df_uf = df_uf[
        [
            "uf",
            "macrorregiao",
            "visao",
            "valor_executado_rs",
            "valor_executado_perc",
            "valor_executado_perc_regiao",
            "min_valor",
            "mediana_valor",
            "max_valor",
            "media_valor",
            "media_aparada_1pct_valor",
            "valor_executado_percapita",
            "qtde_contemplados",
            "perc_qtde_contemplados_regiao"
        ]
    ]

    df_uf = (
        df_uf
        .sort_values(["macrorregiao", "valor_executado_rs"], ascending=[True, False])
        .reset_index(drop=True)
    )

    return df_uf


def aggregate_estado_by_uf_local_residencia(
    df_cubo: pd.DataFrame,
    col_uf: str = "uf",
    tipo_documento: str | None = None
) -> pd.DataFrame:
    """
    Agrega, por UF, os valores executados pelos ESTADOS segundo a categoria
    de residência dos contemplados.

    Cada linha = UF
    Considera apenas tipo_ente == 'ESTADO'

    Para cada categoria:
    - quantidade_contemplados_<categoria>
    - valor_transacao_<categoria>
    - percentual_quantidade_<categoria>
    - percentual_valor_<categoria>

    Percentuais em escala decimal:
    0.25 = 25%
    """

    df = df_cubo.copy()

    if col_uf not in df.columns:
        raise ValueError(f"A coluna '{col_uf}' não foi encontrada na df_cubo.")

    df["tipo_ente_norm"] = (
        df["tipo_ente"]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df = df[df["tipo_ente_norm"].eq("ESTADO")].copy()

    if tipo_documento is not None:
        tipo_documento_norm = str(tipo_documento).upper().strip()

        df["tipo_documento_norm"] = (
            df["tipo_documento"]
            .astype(str)
            .str.upper()
            .str.strip()
        )

        df = df[df["tipo_documento_norm"].eq(tipo_documento_norm)].copy()

    categorias = [
        "Interior",
        "Regiao Metropolitana",
        "Capital"
    ]

    mapa_categorias = {
        "Interior": "interior",
        "Regiao Metropolitana": "regiao_metropolitana",
        "Capital": "capital"
    }

    df["local_residencia_contemplados"] = pd.Categorical(
        df["local_residencia_contemplados"],
        categories=categorias,
        ordered=True
    )

    df_base = (
        df
        .groupby([col_uf, "local_residencia_contemplados"], observed=False)
        .agg(
            quantidade_contemplados=("quantidade", "sum"),
            valor_transacao=("valor_transacao", "sum")
        )
        .reset_index()
    )

    totais_uf = (
        df_base
        .groupby(col_uf, as_index=False)
        .agg(
            quantidade_total_uf=("quantidade_contemplados", "sum"),
            valor_total_uf=("valor_transacao", "sum")
        )
    )

    df_base = df_base.merge(
        totais_uf,
        on=col_uf,
        how="left"
    )

    df_base["percentual_quantidade"] = np.where(
        df_base["quantidade_total_uf"] > 0,
        df_base["quantidade_contemplados"] / df_base["quantidade_total_uf"],
        np.nan
    )

    df_base["percentual_valor"] = np.where(
        df_base["valor_total_uf"] > 0,
        df_base["valor_transacao"] / df_base["valor_total_uf"],
        np.nan
    )

    dfs_pivot = []

    for categoria, sufixo in mapa_categorias.items():
        df_cat = df_base[
            df_base["local_residencia_contemplados"].eq(categoria)
        ].copy()

        df_cat = df_cat[
            [
                col_uf,
                "quantidade_contemplados",
                "valor_transacao",
                "percentual_quantidade",
                "percentual_valor"
            ]
        ].rename(
            columns={
                "quantidade_contemplados": f"quantidade_contemplados_{sufixo}",
                "valor_transacao": f"valor_transacao_{sufixo}",
                "percentual_quantidade": f"percentual_quantidade_{sufixo}",
                "percentual_valor": f"percentual_valor_{sufixo}",
            }
        )

        dfs_pivot.append(df_cat)

    df_resultado = totais_uf.copy()

    for df_cat in dfs_pivot:
        df_resultado = df_resultado.merge(
            df_cat,
            on=col_uf,
            how="left"
        )

    df_resultado = df_resultado.rename(columns={col_uf: "uf"})

    colunas_qtd = [
        col for col in df_resultado.columns
        if col.startswith("quantidade_contemplados_")
    ]

    colunas_valor = [
        col for col in df_resultado.columns
        if col.startswith("valor_transacao_")
    ]

    colunas_percentuais = [
        col for col in df_resultado.columns
        if col.startswith("percentual_")
    ]

    df_resultado[colunas_qtd] = (
        df_resultado[colunas_qtd]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .fillna(0)
        .astype("Float64")
    )

    df_resultado[colunas_percentuais] = (
        df_resultado[colunas_percentuais]
        .astype("Float64")
    )

    df_resultado["quantidade_total_uf"] = (
        df_resultado["quantidade_total_uf"]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado["valor_total_uf"] = (
        df_resultado["valor_total_uf"]
        .fillna(0)
        .astype("Float64")
    )

    df_resultado = df_resultado[
        [
            "uf",
            "quantidade_total_uf",
            "valor_total_uf",

            "quantidade_contemplados_interior",
            "valor_transacao_interior",
            "percentual_quantidade_interior",
            "percentual_valor_interior",

            "quantidade_contemplados_regiao_metropolitana",
            "valor_transacao_regiao_metropolitana",
            "percentual_quantidade_regiao_metropolitana",
            "percentual_valor_regiao_metropolitana",

            "quantidade_contemplados_capital",
            "valor_transacao_capital",
            "percentual_quantidade_capital",
            "percentual_valor_capital",
        ]
    ]

    return df_resultado.sort_values("uf").reset_index(drop=True)


def aggregate_faixa_valor_ju_wide_by_regiao(
    df_cubo: pd.DataFrame,
    by_filter: str = "UF"
) -> pd.DataFrame:
    """
    Agrega, para cada região, quantidade de contemplados e valor total
    por faixa de valor pago, em formato largo.

    Cada linha representa uma categoria da coluna 'regiao':
    - Norte
    - Nordeste
    - Centro-Oeste
    - Sudeste
    - Sul

    Usa a coluna:
    - faixa_vlr_pago_ju_bbagil

    Para cada faixa, cria colunas de:
    - quantidade;
    - percentual da quantidade dentro da região;
    - valor;
    - percentual do valor dentro da região.

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
        Tabela com uma linha por região e faixas de valor como colunas.

    Observação
    ----------
    Percentuais retornam em escala decimal:
    - 0.34 = 34%

    Não há arredondamento dos valores.
    """

    by_filter = by_filter.upper().strip()

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

    if by_filter == "ESTADO":
        df = df[df["tipo_ente_norm"].eq("ESTADO")].copy()

    elif by_filter == "MUNICIPIO":
        df = df[df["tipo_ente_norm"].eq("MUNICIPIO")].copy()

    elif by_filter == "UF":
        df = df[df["tipo_ente_norm"].isin(["ESTADO", "MUNICIPIO"])].copy()

    else:
        raise ValueError("by_filter deve ser 'ESTADO', 'MUNICIPIO' ou 'UF'.")

    ordem_regiao = [
        "Norte",
        "Nordeste",
        "Centro-Oeste",
        "Sudeste",
        "Sul"
    ]

    ordem_faixa_vlr_pago = [
        "Até 2 mil",
        "De 2 a 10 mil",
        "De 10 a 50 mil",
        "De 50 a 200 mil",
        "Acima de 200 mil"
    ]

    nomes_colunas_faixa = {
        "Até 2 mil": "ate_2_mil",
        "De 2 a 10 mil": "de_2_a_10_mil",
        "De 10 a 50 mil": "de_10_a_50_mil",
        "De 50 a 200 mil": "de_50_a_200_mil",
        "Acima de 200 mil": "acima_de_200_mil"
    }

    df["regiao"] = pd.Categorical(
        df["regiao"],
        categories=ordem_regiao,
        ordered=True
    )

    df["faixa_vlr_pago_ju_bbagil_tratada"] = (
        df["faixa_vlr_pago_ju_bbagil"]
        .fillna("Não informado")
        .astype(str)
        .str.strip()
    )

    df_totais_regiao = (
        df
        .groupby("regiao", observed=False, as_index=False)
        .agg(
            total_contemplados_uf=("quantidade", "sum"),
            valor_total_uf=("valor_transacao", "sum")
        )
    )

    df_faixa_regiao = (
        df
        .loc[df["faixa_vlr_pago_ju_bbagil_tratada"].isin(ordem_faixa_vlr_pago)]
        .groupby(
            ["regiao", "faixa_vlr_pago_ju_bbagil_tratada"],
            observed=False,
            as_index=False
        )
        .agg(
            quantidade_contemplados=("quantidade", "sum"),
            valor_total=("valor_transacao", "sum")
        )
    )

    df_qtd_pivot = (
        df_faixa_regiao
        .pivot_table(
            index="regiao",
            columns="faixa_vlr_pago_ju_bbagil_tratada",
            values="quantidade_contemplados",
            aggfunc="sum",
            fill_value=0,
            observed=False
        )
        .reindex(columns=ordem_faixa_vlr_pago, fill_value=0)
        .reset_index()
    )

    df_valor_pivot = (
        df_faixa_regiao
        .pivot_table(
            index="regiao",
            columns="faixa_vlr_pago_ju_bbagil_tratada",
            values="valor_total",
            aggfunc="sum",
            fill_value=0,
            observed=False
        )
        .reindex(columns=ordem_faixa_vlr_pago, fill_value=0)
        .reset_index()
    )

    df_resultado = df_totais_regiao.copy()

    df_resultado = df_resultado.merge(
        df_qtd_pivot,
        on="regiao",
        how="left"
    )

    df_resultado = df_resultado.merge(
        df_valor_pivot,
        on="regiao",
        how="left",
        suffixes=("_qtd", "_valor")
    )

    for faixa in ordem_faixa_vlr_pago:
        nome_faixa = nomes_colunas_faixa[faixa]

        coluna_qtd_origem = f"{faixa}_qtd"
        coluna_valor_origem = f"{faixa}_valor"

        if coluna_qtd_origem not in df_resultado.columns:
            df_resultado[coluna_qtd_origem] = 0

        if coluna_valor_origem not in df_resultado.columns:
            df_resultado[coluna_valor_origem] = 0

        df_resultado[f"qtd_{nome_faixa}"] = df_resultado[coluna_qtd_origem]

        df_resultado[f"perc_qtd_{nome_faixa}"] = np.where(
            df_resultado["total_contemplados_uf"].ne(0),
            df_resultado[coluna_qtd_origem] / df_resultado["total_contemplados_uf"],
            np.nan
        )

        df_resultado[f"valor_{nome_faixa}"] = df_resultado[coluna_valor_origem]

        df_resultado[f"perc_valor_{nome_faixa}"] = np.where(
            df_resultado["valor_total_uf"].ne(0),
            df_resultado[coluna_valor_origem] / df_resultado["valor_total_uf"],
            np.nan
        )

    colunas_finais = [
        "regiao",
        "total_contemplados_uf",
        "valor_total_uf"
    ]

    for faixa in ordem_faixa_vlr_pago:
        nome_faixa = nomes_colunas_faixa[faixa]

        colunas_finais.extend([
            f"qtd_{nome_faixa}",
            f"perc_qtd_{nome_faixa}",
            f"valor_{nome_faixa}",
            f"perc_valor_{nome_faixa}"
        ])

    df_resultado = df_resultado[colunas_finais].copy()

    colunas_quantidade = [
        col for col in df_resultado.columns
        if col.startswith("qtd_") or col == "total_contemplados_uf"
    ]

    colunas_valor = [
        col for col in df_resultado.columns
        if col.startswith("valor_") or col == "valor_total_uf"
    ]

    colunas_percentual = [
        col for col in df_resultado.columns
        if col.startswith("perc_")
    ]

    df_resultado[colunas_quantidade] = (
        df_resultado[colunas_quantidade]
        .fillna(0)
        .astype("Int64")
    )

    df_resultado[colunas_valor] = (
        df_resultado[colunas_valor]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .astype("Float64")
    )

    df_resultado[colunas_percentual] = (
        df_resultado[colunas_percentual]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    df_resultado = (
        df_resultado
        .sort_values("regiao")
        .reset_index(drop=True)
    )

    return df_resultado


def resumo_por_regiao(
    df_aux: pd.DataFrame,
    by_filter: str = "UF"
) -> pd.DataFrame:
    """
    Retorna um resumo por macrorregião.

    Cada linha = uma categoria da coluna nome_macrorregiao:
    - Norte
    - Nordeste
    - Centro-Oeste
    - Sudeste
    - Sul

    by_filter:
    - "ESTADO": considera apenas tipo_ente_bbagil == "ESTADO"
    - "MUNICIPIO": considera apenas tipo_ente_bbagil == "MUNICIPIO"
    - "UF": não aplica filtro de tipo_ente_bbagil

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

    by_filter = by_filter.upper().strip()

    if by_filter not in ["ESTADO", "MUNICIPIO", "UF"]:
        raise ValueError("by_filter deve ser 'ESTADO', 'MUNICIPIO' ou 'UF'.")

    df = df_aux.copy()

    df["tipo_ente_bbagil_norm"] = (
        df["tipo_ente_bbagil"]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    if by_filter == "ESTADO":
        df = df[df["tipo_ente_bbagil_norm"].eq("ESTADO")].copy()

    elif by_filter == "MUNICIPIO":
        df = df[df["tipo_ente_bbagil_norm"].eq("MUNICIPIO")].copy()

    ordem_regioes = [
        "Norte",
        "Nordeste",
        "Centro-Oeste",
        "Sudeste",
        "Sul"
    ]

    df["nome_macrorregiao"] = pd.Categorical(
        df["nome_macrorregiao"],
        categories=ordem_regioes,
        ordered=True
    )

    df_resumo = (
        df
        .groupby("nome_macrorregiao", observed=False)
        .agg(
            valor_total_por_regiao=("valor_transacao_total_bbagil", "sum"),
            valor_medio_por_regiao=("valor_transacao_total_bbagil", "mean"),
            valor_media_aparada_1pct_por_regiao=(
                "valor_transacao_total_bbagil",
                media_aparada_1pct_superior
            ),
            valor_mediano_por_regiao=("valor_transacao_total_bbagil", "median"),
            quantidade_contemplados_por_regiao=("chave", "nunique")
        )
        .reset_index()
    )

    total_valor = df_resumo["valor_total_por_regiao"].sum()
    total_quantidade = df_resumo["quantidade_contemplados_por_regiao"].sum()

    df_resumo["percentual_valor_por_regiao"] = np.where(
        total_valor > 0,
        df_resumo["valor_total_por_regiao"] / total_valor,
        np.nan
    )

    df_resumo["percentual_quantidade_contemplados_por_regiao"] = np.where(
        total_quantidade > 0,
        df_resumo["quantidade_contemplados_por_regiao"] / total_quantidade,
        np.nan
    )

    df_resumo["visao"] = by_filter

    df_resumo["quantidade_contemplados_por_regiao"] = (
        df_resumo["quantidade_contemplados_por_regiao"]
        .fillna(0)
        .astype("Int64")
    )

    colunas_valor = [
        "valor_total_por_regiao",
        "valor_medio_por_regiao",
        "valor_media_aparada_1pct_por_regiao",
        "valor_mediano_por_regiao"
    ]

    df_resumo[colunas_valor] = (
        df_resumo[colunas_valor]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    colunas_percentual = [
        "percentual_valor_por_regiao",
        "percentual_quantidade_contemplados_por_regiao"
    ]

    df_resumo[colunas_percentual] = (
        df_resumo[colunas_percentual]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    df_resumo = (
        df_resumo
        .sort_values("nome_macrorregiao")
        .reset_index(drop=True)
    )

    return df_resumo


def tabela_resumo_estado_municipio(
    df_aux: pd.DataFrame,
    col_tipo_ente: str = "tipo_ente_bbagil",
    col_valor: str = "valor_transacao_total_bbagil",
    col_chave: str = "chave",
    col_faixa: str = "faixa_vlr_pago_ju_bbagil",
    formatar: bool = True
) -> pd.DataFrame:
    """
    Cria uma tabela-resumo comparando Estados e Municípios.

    Indicadores:
    - Número de contemplados
    - Ticket médio dos pagamentos, usando média aparada de 1%
    - Concentração dos contemplados, por faixa de valor
    - Concentração do recurso executado, por faixa de valor

    Regras:
    - Número de contemplados = nunique da coluna chave
    - Ticket médio = média aparada, removendo os 1% maiores valores
    - Concentração dos contemplados = faixa com maior número de contemplados
    - Concentração do recurso executado = faixa com maior soma de valor
    """

    def media_aparada_1pct_superior(x):
        x = pd.to_numeric(x, errors="coerce").dropna()

        if x.empty:
            return np.nan

        limite_superior = x.quantile(0.99)

        return x[x <= limite_superior].mean()

    df = df_aux.copy()

    df[col_tipo_ente] = (
        df[col_tipo_ente]
        .astype(str)
        .str.upper()
        .str.strip()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df[col_valor] = pd.to_numeric(
        df[col_valor],
        errors="coerce"
    )

    df = df[df[col_tipo_ente].isin(["ESTADO", "MUNICIPIO"])].copy()

    mapa_tipo_ente = {
        "ESTADO": "Estados",
        "MUNICIPIO": "Municípios"
    }

    ordem_colunas = ["Estados", "Municípios"]

    def formatar_numero_br(valor):
        if pd.isna(valor):
            return "-"

        return f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def formatar_moeda_br(valor):
        if pd.isna(valor):
            return "-"

        return (
            f"R$ {valor:,.0f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    resultados = {}

    for tipo_ente_norm, nome_coluna in mapa_tipo_ente.items():
        df_tipo = df[df[col_tipo_ente].eq(tipo_ente_norm)].copy()

        qtd_contemplados = df_tipo[col_chave].nunique()

        ticket_medio_aparado = media_aparada_1pct_superior(
            df_tipo[col_valor]
        )

        df_faixa = (
            df_tipo
            .dropna(subset=[col_faixa])
            .groupby(col_faixa, as_index=False)
            .agg(
                qtd_contemplados=(col_chave, "nunique"),
                valor_total=(col_valor, "sum")
            )
        )

        if df_faixa.empty:
            faixa_maior_qtd = np.nan
            faixa_maior_valor = np.nan
        else:
            faixa_maior_qtd = (
                df_faixa
                .sort_values("qtd_contemplados", ascending=False)
                .iloc[0][col_faixa]
            )

            faixa_maior_valor = (
                df_faixa
                .sort_values("valor_total", ascending=False)
                .iloc[0][col_faixa]
            )

        if formatar:
            resultados[nome_coluna] = {
                "Número de contemplados": formatar_numero_br(qtd_contemplados),
                "Ticket médio dos pagamentos": formatar_moeda_br(ticket_medio_aparado),
                "Concentração dos contemplados, por faixa de valor": faixa_maior_qtd,
                "Concentração do recurso executado, por faixa de valor": faixa_maior_valor
            }
        else:
            resultados[nome_coluna] = {
                "Número de contemplados": qtd_contemplados,
                "Ticket médio dos pagamentos": ticket_medio_aparado,
                "Concentração dos contemplados, por faixa de valor": faixa_maior_qtd,
                "Concentração do recurso executado, por faixa de valor": faixa_maior_valor
            }

    df_resultado = (
        pd.DataFrame(resultados)
        .reset_index()
        .rename(columns={"index": "indicador"})
    )

    df_resultado = df_resultado[
        ["indicador"] + ordem_colunas
    ]

    return df_resultado


def aggregate_execution_by_porte_with_estado_sexo(
    df_cubo: pd.DataFrame,
    proporcao_aparada: float = 0.99
) -> pd.DataFrame:
    """
    Agrega valores, quantidades e percentuais por porte populacional dos municípios,
    acrescentando uma linha agregada para ESTADO.

    A linha de ESTADO usa porte_populacional = -99.

    A função retorna:
    - número de municípios/entes;
    - valor total por porte;
    - quantidade total de contemplados por porte;
    - percentual de valor por porte em relação ao total geral;
    - percentual de quantidade por porte em relação ao total geral;
    - quantidade por Sexo;
    - valor por Sexo;
    - percentual de quantidade por Sexo dentro do porte;
    - percentual de valor por Sexo dentro do porte;
    - valor médio por Sexo;
    - valor médio aparado por Sexo.

    Observações:
    - percentuais são retornados em escala decimal:
      0.55 = 55%;
    - a regra de Sexo válido considera apenas Feminino e Masculino;
    - o valor médio por Sexo é calculado como:
      valor total do sexo / quantidade total do sexo;
    - o valor médio aparado usa o valor médio da linha
      valor_transacao / quantidade e remove o 1% superior dentro de cada
      combinação de porte e Sexo.
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
        "FEMININO": "Feminino",
        "MASCULINO": "Masculino"
    })

    # ------------------------------------------------------------
    # 3. Criar porte de análise
    # Municípios mantêm porte_populacional;
    # Estados recebem porte_populacional = -99
    # ------------------------------------------------------------

    df = df[df["tipo_ente_norm"].isin(["MUNICIPIO", "ESTADO"])].copy()

    df["porte_analise"] = np.where(
        df["tipo_ente_norm"].eq("ESTADO"),
        -99,
        df["porte_populacional"]
    )

    # ------------------------------------------------------------
    # 4. Agregação geral por porte
    # ------------------------------------------------------------

    df_porte = (
        df
        .groupby("porte_analise", dropna=False, as_index=False)
        .agg(
            numero_municipios=("ente", "nunique"),
            valor_total_por_porte=("valor_transacao", "sum"),
            quantidade_contemplados_por_porte=("quantidade", "sum"),
        )
        .rename(columns={"porte_analise": "porte_populacional"})
    )

    # ------------------------------------------------------------
    # 5. Base apenas com Sexo válido
    # ------------------------------------------------------------

    df_sexo = df[
        df["sexo_tratado"].isin(["Feminino", "Masculino"])
    ].copy()

    df_sexo["valor_medio_linha"] = np.where(
        df_sexo["quantidade"].fillna(0).ne(0),
        df_sexo["valor_transacao"] / df_sexo["quantidade"],
        np.nan
    )

    # ------------------------------------------------------------
    # 6. Função auxiliar: média aparada ponderada
    # ------------------------------------------------------------

    def media_aparada_ponderada(
        df_base: pd.DataFrame,
        col_valor: str = "valor_medio_linha",
        col_peso: str = "quantidade",
        q: float = proporcao_aparada
    ) -> float:
        base = df_base[[col_valor, col_peso]].copy()

        base[col_valor] = pd.to_numeric(base[col_valor], errors="coerce")
        base[col_peso] = pd.to_numeric(base[col_peso], errors="coerce")

        base = base.dropna()
        base = base[base[col_peso] > 0]

        if base.empty:
            return np.nan

        limite = base[col_valor].quantile(q)

        base_aparada = base[base[col_valor] <= limite]

        if base_aparada.empty:
            return np.nan

        return np.average(
            base_aparada[col_valor],
            weights=base_aparada[col_peso]
        )

    # ------------------------------------------------------------
    # 7. Agregação por porte e Sexo
    # ------------------------------------------------------------

    df_sexo_agg = (
        df_sexo
        .groupby(["porte_analise", "sexo_tratado"], dropna=False)
        .agg(
            qtd_sexo=("quantidade", "sum"),
            valor_sexo=("valor_transacao", "sum"),
            valor_medio_sexo=("valor_medio_linha", "mean"),
        )
        .reset_index()
    )

    df_media_aparada = (
        df_sexo
        .groupby(["porte_analise", "sexo_tratado"], dropna=False)
        .apply(media_aparada_ponderada)
        .reset_index(name="valor_medio_aparado_sexo")
    )

    df_sexo_agg = df_sexo_agg.merge(
        df_media_aparada,
        on=["porte_analise", "sexo_tratado"],
        how="left"
    )

    # Valor médio correto ponderado:
    # valor total do sexo / quantidade total do sexo
    df_sexo_agg["valor_medio_sexo"] = np.where(
        df_sexo_agg["qtd_sexo"].fillna(0).ne(0),
        df_sexo_agg["valor_sexo"] / df_sexo_agg["qtd_sexo"],
        np.nan
    )

    # ------------------------------------------------------------
    # 8. Totais com Sexo válido por porte
    # ------------------------------------------------------------

    df_total_sexo = (
        df_sexo
        .groupby("porte_analise", dropna=False, as_index=False)
        .agg(
            total_qtd_sexo_valido=("quantidade", "sum"),
            total_valor_sexo_valido=("valor_transacao", "sum")
        )
        .rename(columns={"porte_analise": "porte_populacional"})
    )

    # ------------------------------------------------------------
    # 9. Função auxiliar para pivotar Sexo
    # ------------------------------------------------------------

    def pivotar_sexo(
        df_base: pd.DataFrame,
        coluna_valor: str,
        prefixo: str
    ) -> pd.DataFrame:
        df_pivot = (
            df_base
            .pivot_table(
                index="porte_analise",
                columns="sexo_tratado",
                values=coluna_valor,
                aggfunc="first",
                fill_value=0
            )
            .reindex(columns=["Feminino", "Masculino"])
            .reset_index()
            .rename(columns={"porte_analise": "porte_populacional"})
        )

        df_pivot = df_pivot.rename(
            columns={
                col: f"{prefixo}_{col}"
                for col in df_pivot.columns
                if col != "porte_populacional"
            }
        )

        return df_pivot

    df_qtd_sexo = pivotar_sexo(
        df_base=df_sexo_agg,
        coluna_valor="qtd_sexo",
        prefixo="qtd_sexo"
    )

    df_valor_sexo = pivotar_sexo(
        df_base=df_sexo_agg,
        coluna_valor="valor_sexo",
        prefixo="valor_sexo"
    )

    df_media_sexo = pivotar_sexo(
        df_base=df_sexo_agg,
        coluna_valor="valor_medio_sexo",
        prefixo="valor_medio_sexo"
    )

    df_media_aparada_sexo = pivotar_sexo(
        df_base=df_sexo_agg,
        coluna_valor="valor_medio_aparado_sexo",
        prefixo="valor_medio_aparado_sexo"
    )

    # ------------------------------------------------------------
    # 10. Juntar tudo
    # ------------------------------------------------------------

    df_porte = (
        df_porte
        .merge(df_total_sexo, on="porte_populacional", how="left")
        .merge(df_qtd_sexo, on="porte_populacional", how="left")
        .merge(df_valor_sexo, on="porte_populacional", how="left")
        .merge(df_media_sexo, on="porte_populacional", how="left")
        .merge(df_media_aparada_sexo, on="porte_populacional", how="left")
    )

    # ------------------------------------------------------------
    # 11. Percentuais gerais por porte
    # ------------------------------------------------------------

    valor_total_geral = df_porte["valor_total_por_porte"].sum()
    quantidade_total_geral = df_porte["quantidade_contemplados_por_porte"].sum()

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
    # 12. Percentuais por Sexo dentro do porte
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
        nome_percentual = coluna.replace(
            "qtd_sexo_",
            "percentual_qtd_sexo_"
        )

        df_porte[nome_percentual] = np.where(
            df_porte["total_qtd_sexo_valido"].fillna(0).ne(0),
            df_porte[coluna] / df_porte["total_qtd_sexo_valido"],
            np.nan
        )

    for coluna in colunas_valor_sexo:
        nome_percentual = coluna.replace(
            "valor_sexo_",
            "percentual_valor_sexo_"
        )

        df_porte[nome_percentual] = np.where(
            df_porte["total_valor_sexo_valido"].fillna(0).ne(0),
            df_porte[coluna] / df_porte["total_valor_sexo_valido"],
            np.nan
        )

    # ------------------------------------------------------------
    # 13. Ordenar colunas
    # ------------------------------------------------------------

    colunas_finais = [
        "porte_populacional",
        "numero_municipios",
        "valor_total_por_porte",
        "quantidade_contemplados_por_porte",
        "percentual_valor_por_porte",
        "percentual_quantidade_por_porte",
        "total_qtd_sexo_valido",
        "total_valor_sexo_valido",

        "qtd_sexo_Feminino",
        "qtd_sexo_Masculino",
        "percentual_qtd_sexo_Feminino",
        "percentual_qtd_sexo_Masculino",

        "valor_sexo_Feminino",
        "valor_sexo_Masculino",
        "percentual_valor_sexo_Feminino",
        "percentual_valor_sexo_Masculino",

        "valor_medio_sexo_Feminino",
        "valor_medio_sexo_Masculino",
        "valor_medio_aparado_sexo_Feminino",
        "valor_medio_aparado_sexo_Masculino",
    ]

    for coluna in colunas_finais:
        if coluna not in df_porte.columns:
            df_porte[coluna] = np.nan

    df_porte = df_porte[colunas_finais].copy()

    # ------------------------------------------------------------
    # 14. Converter tipos
    # ------------------------------------------------------------

    colunas_quantidade = [
        "numero_municipios",
        "quantidade_contemplados_por_porte",
        "total_qtd_sexo_valido",
        "qtd_sexo_Feminino",
        "qtd_sexo_Masculino",
    ]

    df_porte[colunas_quantidade] = (
        df_porte[colunas_quantidade]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .astype("Int64")
    )

    colunas_valor = [
        "valor_total_por_porte",
        "total_valor_sexo_valido",
        "valor_sexo_Feminino",
        "valor_sexo_Masculino",
        "valor_medio_sexo_Feminino",
        "valor_medio_sexo_Masculino",
        "valor_medio_aparado_sexo_Feminino",
        "valor_medio_aparado_sexo_Masculino",
    ]

    df_porte[colunas_valor] = (
        df_porte[colunas_valor]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    colunas_percentuais = [
        "percentual_valor_por_porte",
        "percentual_quantidade_por_porte",
        "percentual_qtd_sexo_Feminino",
        "percentual_qtd_sexo_Masculino",
        "percentual_valor_sexo_Feminino",
        "percentual_valor_sexo_Masculino",
    ]

    df_porte[colunas_percentuais] = (
        df_porte[colunas_percentuais]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Float64")
    )

    # ------------------------------------------------------------
    # 15. Ordenar tabela
    # ------------------------------------------------------------

    df_porte = (
        df_porte
        .sort_values("valor_total_por_porte", ascending=False)
        .reset_index(drop=True)
    )

    return df_porte