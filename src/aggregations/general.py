import pandas as pd


def calcular_ticket_medio_df_aux(
    df_aux: pd.DataFrame,
    coluna_chave: str = "chave",
    coluna_valor: str = "valor_transacao_total_bbagil",
) -> pd.DataFrame:
    """
    Calcula indicadores gerais de valor pago por contemplado.

    A unidade de análise é o contemplado único, identificado pela coluna `chave`.

    Retorna um DataFrame de uma linha com:
    - média simples do valor recebido por contemplado;
    - média aparada, excluindo o 1% dos maiores valores;
    - valor total pago;
    - número total de contemplados únicos.
    """

    df = df_aux[[coluna_chave, coluna_valor]].copy()

    # Garante que cada contemplado apareça uma única vez.
    # Se já estiver único, isso não altera o resultado.
    df_contemplados = (
        df
        .groupby(coluna_chave, as_index=False)[coluna_valor]
        .sum()
    )

    valores = df_contemplados[coluna_valor]

    limite_99 = valores.quantile(0.99)

    media_simples = valores.mean()

    media_aparada_1pct = valores[valores <= limite_99].mean()

    valor_total = valores.sum()

    qtd_contemplados = df_contemplados[coluna_chave].nunique()

    resultado = pd.DataFrame({
        "qtd_contemplados": [qtd_contemplados],
        "valor_total": [valor_total],
        "media": [media_simples],
        "media_aparada_1pct_maiores": [media_aparada_1pct],
        "limite_corte_99pct": [limite_99],
    })

    return resultado



def calcular_percentis_valor_df_aux(
    df_aux: pd.DataFrame,
    coluna_valor: str = "valor_transacao_total_bbagil",
    coluna_chave: str | None = None,
    nome_recorte: str = "GERAL",
) -> pd.DataFrame:
    """
    Calcula estatísticas gerais, percentis e média aparada dos valores pagos.

    Parâmetros
    ----------
    df_aux : pd.DataFrame
        Base de contemplados.

    coluna_valor : str
        Coluna com o valor total recebido pelo contemplado.

    coluna_chave : str | None
        Caso informado, agrega os valores por contemplado único antes do cálculo.
        Exemplo: coluna_chave="chave".

    nome_recorte : str
        Nome que aparecerá na coluna 'tipo_ente' do resultado.

    Retorna
    -------
    pd.DataFrame
        DataFrame de uma linha com estatísticas descritivas dos valores.
    """

    df = df_aux.copy()

    df[coluna_valor] = pd.to_numeric(
        df[coluna_valor],
        errors="coerce"
    )

    if coluna_chave is not None:
        df = (
            df
            .groupby(coluna_chave, as_index=False)[coluna_valor]
            .sum()
        )

    serie_valor = df[coluna_valor].dropna()

    p99 = serie_valor.quantile(0.99)

    media_aparada_1pct = serie_valor[serie_valor <= p99].mean()

    resultado = pd.DataFrame({
        "tipo_ente": [nome_recorte],
        "quantidade_contemplados": [serie_valor.count()],
        "valor_minimo": [serie_valor.min()],
        "p1": [serie_valor.quantile(0.01)],
        "q1": [serie_valor.quantile(0.25)],
        "q2_mediana": [serie_valor.quantile(0.50)],
        "q3": [serie_valor.quantile(0.75)],
        "p99": [p99],
        "valor_maximo": [serie_valor.max()],
        "media": [serie_valor.mean()],
        "media_aparada_1pct": [media_aparada_1pct],
        "desvio_padrao": [serie_valor.std()]
    })

    return resultado