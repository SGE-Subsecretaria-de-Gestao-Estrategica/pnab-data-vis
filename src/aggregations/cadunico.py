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

    df_cpf_cadunico = df_cpf.loc[
        df_cpf["pessoaCad_cadunico"].eq(1.0)
    ].copy()

    total_contemplados_cpf = df_cpf["quantidade"].sum()

    qtd_contemplados_cadunico = df_cpf_cadunico["quantidade"].sum()

    valor_recebido_cadunico = df_cpf_cadunico["valor_transacao"].sum()

    perc_contemplados_cadunico = (
        qtd_contemplados_cadunico / total_contemplados_cpf 
        if total_contemplados_cpf > 0
        else 0
    )

    df_resultado = pd.DataFrame(
        {
            "perc_contemplados_cadunico": [perc_contemplados_cadunico],
            "qtd_contemplados_cadunico": [qtd_contemplados_cadunico],
            "qtd_documentos_unicos_cadunico": [qtd_documentos_unicos_cadunico],
            "valor_recebido_cadunico": [valor_recebido_cadunico],
        }
    )

    return df_resultado