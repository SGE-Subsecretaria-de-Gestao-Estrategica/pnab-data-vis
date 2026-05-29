"""
Updates the "Link do SVG" column in the De-para CSV with GitHub URLs for each chart SVG.
Run: python3 update-csv-links.py
"""

import csv
from pathlib import Path

CSV_IN = Path("/Users/victorgois/Downloads/De-para gráficos e visualizacoes, titulos e fontes de dados - Página1.csv")
CSV_OUT = CSV_IN  # overwrite in place
BASE_URL = "https://github.com/SGE-Subsecretaria-de-Gestao-Estrategica/pnab-data-vis/blob/main/svgs/"

def url(section: int, filename: str) -> str:
    return f"{BASE_URL}section_{section}/{filename}"

# Maps data row index (0-based, after header) → SVG URL.
# Rows without a matching SVG are omitted (link stays blank).
# Keys are 0-based data row indices (row 0 = first data row after the header).
# CSV line N  =  data index N-2  (subtract 1 for header, 1 for 1-based CSV lines)
MAPPING = {
    # ── Section 1 ────────────────────────────────────────────────────────────
    # 0: "Valores Distribuidos - Visao geral" — no single SVG
    1:  url(1, "executedValueByUf--Valor-executado-por-UF.svg"),
    # 2: "Tabela com valores dos entes municipais e estaduais" — no SVG (table)
    3:  url(1, "valuePerCaptaByState--Valor-per-capita-por-UF-bandeiras.svg"),
    4:  url(1, "valuesByPopulationSize--Treemap-Distribuição-de-Valores-por-Porte.svg"),
    5:  url(1, "capitalInterior--Stacked-capital-vs-interior-valor-e-quantidade.svg"),
    6:  url(1, "capitalInterior--BigNumber-valor-total-para-zona-rural.svg"),
    7:  url(1, "executedValueByZone--Proporção-UrbanoRural-por-UF-Municípios.svg"),
    8:  url(1, "capitalInterior--BigNumber-pagamentos-para-o-interior.svg"),
    9:  url(1, "capitalInterior--BigNumber-valor-total-para-o-interior.svg"),
    10: url(1, "specialTerritoryBigNumbers--BigNumber-agentes-em-territórios-especiais.svg"),
    11: url(1, "proportionalByState--Silhueta-proporcional-Valor-executado-por-região.svg"),
    12: url(1, "executedValueByRegion--Percentual-da-População.svg"),
    13: url(1, "proportionalByState--Silhueta-proporcional-Valor-executado-por-estado.svg"),
    14: url(1, "rankingByState--Ranking-Valor-executado-por-estado.svg"),
    15: url(1, "populationVsInvestment--Bubble-População-vs-Investimento-por-estado.svg"),
    16: url(1, "equityRankSlope--Slope-Posição-por-valor-vs-posição-por-população.svg"),
    17: url(1, "valuePerCaptaByState--Valor-per-capita-por-UF-abreviação.svg"),
    18: url(1, "grantStatsBoxPlot--BoxPlot-Distribuição-da-mediana-de-repasse-por-região.svg"),
    19: url(1, "executedValueByRegion--Valor-Executado-por-Região.svg"),
    20: url(1, "executedValueByUfDiverging--blueTeal.svg"),
    21: url(1, "executedValueByState--Valor-Executado-por-Estado.svg"),
    22: url(1, "municipalityValueHeatmap--Heatmap-Estados-por-faixa-de-valor-pago.svg"),
    23: url(1, "executedValueByZone--Proporção-UrbanoRural-por-UF-Municípios.svg"),
    24: url(1, "valuesByPopulationSize--Treemap-Distribuição-de-Valores-por-Porte.svg"),
    25: url(1, "valuesByPopulationSize--Bubble-Municípios-vs-Valor-Total-tamanho-beneficiários.svg"),
    26: url(1, "valuesByPopulationSize--Diverging-Bars-Proporção-Urbano-vs-Rural-por-Porte.svg"),
    27: url(1, "valuesByPopulationSize--Stacked-Bars-Equidade-Valor-Investido-vs-Beneficiários.svg"),
    28: url(1, "specialTerritoryBigNumbers--BigNumber-agentes-em-territórios-especiais.svg"),
    29: url(1, "specialTerritory--DivergingBarChart-Lacuna-de-equidade-blueTeal.svg"),
    30: url(1, "specialTerritory--HorizontalStackedBarChart-Estado-vs-Município-tealorange.svg"),

    # ── Section 2 ────────────────────────────────────────────────────────────
    31: url(2, "valueRangeDistribution--Distribuição-nacional-de-beneficiários-por-faixa-de-valor.svg"),
    32: url(2, "valueConcentrationByRange--do-valor-total-por-faixa-de-pagamento.svg"),
    33: url(2, "culturalAgentsByRegion--Agentes-culturais-contemplados-por-região-do-total.svg"),
    34: url(2, "valueRangeByUf--Faixa-de-valor-pago-por-UF-pct-dentro-de-cada-estado.svg"),
    35: url(2, "valueRangeByUf--Faixa-de-valor-pago-por-UF-pct-dentro-de-cada-estado.svg"),
    36: url(2, "valueRangeByPorte--Faixa-de-valor-por-porte-de-município.svg"),
    37: url(2, "valueRangeByPorte--Faixa-de-valor-por-porte-de-município.svg"),
    38: url(2, "specialTerritoryByType--HorizontalBarChart-valor-por-tipo-de-território-especial-teal.svg"),
    39: url(2, "personTypeBigNumbers--CPF-do-valor-total.svg"),
    40: url(2, "personTypeBigNumbers--CNPJ-do-valor-total.svg"),
    41: url(2, "esferaBigNumbers--BigNumber-CPF-nos-estados.svg"),
    42: url(2, "esferaBigNumbers--BigNumber-CNPJ-nos-estados.svg"),
    43: url(2, "esferaBigNumbers--BigNumber-CNPJ-nos-municípios.svg"),
    44: url(2, "esferaBigNumbers--BigNumber-CPF-nos-municípios.svg"),
    45: url(2, "personTypeDiverging--Divergente-do-valor-por-esfera-CPF-vs-CNPJ.svg"),
    46: url(2, "personTypeDiverging--Stacked-Beneficiários-vs-Valor-o-flip-CPFCNPJ.svg"),
    47: url(2, "valueRangeDistribution--Distribuição-nacional-de-beneficiários-por-faixa-de-valor.svg"),
    48: url(2, "valueRangeByPersonType--Faixas-de-valor-CPF-vs-CNPJ-dentro-de-cada-tipo.svg"),
    49: url(2, "personTypeProportional--Área-proporcional-Valor-médio-por-beneficiário-CPF-vs-CNPJ.svg"),
    50: url(2, "personTypeBoxPlot--BoxPlot-Distribuição-de-valores-por-tipo-de-beneficiário-CPF-vs-CNPJ.svg"),

    # ── Section 3 ────────────────────────────────────────────────────────────
    # 51, 52: infographic — no SVG
    53: url(3, "pfPjSplit--Donut-Pessoa-Física-vs-Pessoa-Jurídica.svg"),
    54: url(3, "pfPjSplit--Donut-Pessoa-Física-vs-Pessoa-Jurídica.svg"),
    55: url(3, "sexDistribution--BigNumber-masculino.svg"),
    56: url(3, "sexDistribution--BigNumber-feminino.svg"),
    57: url(3, "sexDistribution--Pictograma-1-ícone-1-em-cada-15-agentes.svg"),
    58: url(3, "sexDonut--Donut-distribuição-por-quantidade-de-agentes.svg"),
    # 59-65: no matching SVGs
    66: url(3, "ageGroupPyramid--Pirâmide-etária-por-sexo.svg"),
    67: url(3, "ageGroupByRegion--Agentes-culturais-por-faixa-etária-e-região.svg"),
    # 68, 69: no matching SVGs
    70: url(3, "cboActivities--Top-20-atividades-econômicas-CBORAIS.svg"),

    # ── Section 4 ────────────────────────────────────────────────────────────
    71: url(4, "vinculoFormalTotals--com-vínculo-formal.svg"),
    72: url(4, "vinculoFormalTotals--sem-vínculo-formal.svg"),
    73: url(4, "vinculoFormalTotals--Área-proporcional-Valor-pago-por-grupo.svg"),
    74: url(4, "vinculoFormalBySexo--Divergente-Sem-vs-com-vínculo-formal-por-sexo.svg"),
    75: url(4, "vinculoFormalByAge--Barras-empilhadas-Sem-vs-com-vínculo-por-faixa-etária.svg"),
    76: url(4, "vinculoFormalByEscolaridade--Barras-Beneficiários-com-vínculo-formal-por-escolaridade.svg"),
    77: url(4, "vinculoFormalByRegion--Barras-empilhadas-Sem-vs-com-vínculo-por-região.svg"),
    78: url(4, "vinculoFormalByRegion--Silhueta-Beneficiários-com-vínculo-formal-por-região.svg"),
    79: url(4, "vinculoFormalByRaca--Barras-Beneficiários-com-vínculo-formal-por-raçacor.svg"),
    80: url(4, "vinculoFormalByRaca--Treemap-Proporção-por-raçacor.svg"),
    81: url(4, "vinculoFormalRacaSexo--Heatmap-Raca-cor-por-sexo-azul.svg"),
    82: url(4, "vinculoFormalByUf--Silhueta-Beneficiários-com-vínculo-formal-por-UF.svg"),
    83: url(4, "vinculoFormalByUf--Ranking-com-vínculo-formal-por-UF.svg"),

    # ── Section 5 ────────────────────────────────────────────────────────────
    84: url(5, "cadunicoBigNumbers--BigNumber-contemplados-no-CadÚnico.svg"),
    85: url(5, "cadunicoBigNumbers--BigNumber-quantidade-de-contemplados-no-CadÚnico.svg"),
    86: url(5, "cadunicoBigNumbers--BigNumber-valor-repassado-ao-grupo-CadÚnico.svg"),
    87: url(5, "cadunicoBigNumbers--BigNumber-documentos-únicos.svg"),
    88: url(5, "cadunicoBigNumbers--BigNumber-valor-repassado-ao-grupo-CadÚnico.svg"),
    89: url(5, "cadunicoBigNumbers--BigNumber-dos-recursos-totais-destinados-ao-CadÚnico.svg"),
    90: url(5, "cadunicoBigNumbers--BigNumber-feminino-no-CadÚnico.svg"),
    91: url(5, "cadunicoBigNumbers--BigNumber-faixa-25-54-anos-no-CadÚnico.svg"),
    92: url(5, "cadunicoFaixaSexo--HorizontalStackedBarChart-faixa-etaria-por-sexo-bluePurple.svg"),
    93: url(5, "cadunicoRenda--DonutChart-faixa-de-renda-per-capita.svg"),
    94: url(5, "cadunicoRenda--DonutChart-situação-de-renda.svg"),
    95: url(5, "cadunicoBigNumbers--BigNumber-urbano-no-CadÚnico.svg"),
    96: url(5, "cadunicoBigNumbers--BigNumber-pequeno-porte-no-CadÚnico.svg"),
    97: url(5, "cadunicoTreemaps--Treemap-situação-de-domicílio-Urbana-Rural.svg"),
    98: url(5, "cadunicoTreemaps--Treemap-porte-municipal.svg"),
    99: url(5, "cadunicoByUf--HorizontalBarChart-CadÚnico-por-UF-blue.svg"),
    100: url(5, "cadunicoByValue--HorizontalBarChart-distribuição-por-faixa-de-valor-blue.svg"),
    101: url(5, "cadunicoBigNumbers--BigNumber-Bolsa-Família.svg"),
    102: url(5, "cadunicoBigNumbers--BigNumber-valor-Bolsa-Família.svg"),
    103: url(5, "cadunicoBigNumbers--BigNumber-BPC.svg"),
    104: url(5, "cadunicoBigNumbers--BigNumber-valor-BPC.svg"),
}

def main():
    text = CSV_IN.read_text(encoding="utf-8-sig")
    reader = csv.DictReader(text.splitlines())
    fieldnames = reader.fieldnames

    rows = list(reader)
    filled = 0

    # Clear all existing links before re-applying the mapping
    for row in rows:
        row["Link do SVG"] = ""

    for i, row in enumerate(rows):
        link = MAPPING.get(i)
        if link:
            row["Link do SVG"] = link
            filled += 1

    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {filled} rows → {CSV_OUT}")

if __name__ == "__main__":
    main()
