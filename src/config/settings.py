from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[2] # PASTA RAÍZ DO PROJETO

DATA_PATH = ROOT / "data"

DATA_PATH_SECTION1 = DATA_PATH / "section_1"
DATA_PATH_SECTION2 = DATA_PATH / "section_2"
DATA_PATH_SECTION3 = DATA_PATH / "section_3"
DATA_PATH_SECTION4 = DATA_PATH / "section_4"
DATA_PATH_SECTION5 = DATA_PATH / "section_5"
DATA_PATH_SECTION6 = DATA_PATH / "section_6"
DATA_PATH_SECTION7 = DATA_PATH / "section_7"

CUBO_PATH = DATA_PATH / "input_data" / "dados_cubo_final_v0__2026-05-20_13-03.xlsx"


CATEGORIES_SPECIAL_TERRITORIES = [
    "Não especial",
    "Favela e Comunidade Urbana",
    "Setor com baixo patamar domiciliar",
    "Agrupamento quilombola",
    "Agrupamento indígena",
    "Quartel e base militar",
    "Não informado",
    "Agrovila do PA",
    "Unidade prisional",
    "Convento / hospital / ILPI / IACA",
    "Alojamento / acampamento",
]