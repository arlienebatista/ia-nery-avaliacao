"""Gravacao das respostas dos juizes.

Destino primario: uma planilha do Google Sheets, configurada via secrets do
Streamlit. Se a credencial nao estiver configurada (ou falhar), o app grava
em resultados/respostas.csv, no proprio diretorio da aplicacao.

O armazenamento e append-only: cada questao salva gera uma linha nova. Ao
retomar uma avaliacao, vale a ultima linha de cada par (codigo_juiz, id_pergunta).
"""

import csv
import os
from datetime import datetime

import streamlit as st

COLUNAS = [
    "timestamp",
    "codigo_juiz",
    "id_pergunta",
    "perfil",
    "acuracia",
    "clareza",
    "seguranca",
    "justificativa",
    "comentario",
    "comentario_geral",
]

ID_COMENTARIO_GERAL = "_GERAL_"

DIR_APP = os.path.dirname(os.path.abspath(__file__))
CSV_LOCAL = os.path.join(DIR_APP, "resultados", "respostas.csv")

ESCOPO_GOOGLE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def registro_vazio():
    return {c: "" for c in COLUNAS}


# ---------------------------------------------------------------- Google Sheets


def _config_sheets():
    """Le os secrets. Retorna None se nao houver configuracao."""
    try:
        if "gcp_service_account" not in st.secrets or "planilha" not in st.secrets:
            return None
        conta = dict(st.secrets["gcp_service_account"])
        planilha = dict(st.secrets["planilha"])
    except Exception:
        return None
    if not conta or not planilha.get("url"):
        return None
    return conta, planilha


@st.cache_resource(show_spinner=False)
def _aba_sheets():
    """Abre (ou cria) a aba de respostas. Retorna None se nao der para usar."""
    config = _config_sheets()
    if config is None:
        return None
    conta, planilha = config
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        credencial = Credentials.from_service_account_info(conta, scopes=ESCOPO_GOOGLE)
        cliente = gspread.authorize(credencial)
        arquivo = cliente.open_by_url(planilha["url"])
        nome_aba = planilha.get("aba", "respostas")
        try:
            aba = arquivo.worksheet(nome_aba)
        except Exception:
            aba = arquivo.add_worksheet(title=nome_aba, rows=1000, cols=len(COLUNAS))
        if not aba.row_values(1):
            aba.append_row(COLUNAS, value_input_option="RAW")
        return aba
    except Exception as erro:  # credencial invalida, sem permissao, sem rede
        st.session_state["_erro_sheets"] = str(erro)
        return None


# ------------------------------------------------------------------- CSV local


def _garante_csv():
    os.makedirs(os.path.dirname(CSV_LOCAL), exist_ok=True)
    if not os.path.exists(CSV_LOCAL):
        with open(CSV_LOCAL, "w", newline="", encoding="utf-8-sig") as f:
            csv.writer(f).writerow(COLUNAS)


# ---------------------------------------------------------------------- API


def descricao_destino():
    """Texto curto sobre onde as respostas estao sendo gravadas."""
    if _aba_sheets() is not None:
        return "Google Sheets"
    return "arquivo local (resultados/respostas.csv)"


def salvar(registro):
    """Grava um registro. Retorna (ok, mensagem_de_erro)."""
    linha = registro_vazio()
    linha.update({k: v for k, v in registro.items() if k in COLUNAS})
    linha["timestamp"] = agora()

    aba = _aba_sheets()
    if aba is not None:
        try:
            aba.append_row([str(linha[c]) for c in COLUNAS], value_input_option="RAW")
            return True, ""
        except Exception as erro:
            return False, "Falha ao gravar no Google Sheets: {}".format(erro)

    try:
        _garante_csv()
        with open(CSV_LOCAL, "a", newline="", encoding="utf-8-sig") as f:
            csv.writer(f).writerow([linha[c] for c in COLUNAS])
        return True, ""
    except Exception as erro:
        return False, "Falha ao gravar o arquivo local: {}".format(erro)


def _todas_linhas():
    aba = _aba_sheets()
    if aba is not None:
        try:
            return aba.get_all_records()
        except Exception:
            return []
    if not os.path.exists(CSV_LOCAL):
        return []
    with open(CSV_LOCAL, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def carregar_do_juiz(codigo_juiz):
    """Ultima resposta de cada questao ja gravada por esse codigo de juiz."""
    codigo = (codigo_juiz or "").strip().casefold()
    if not codigo:
        return {}
    respostas = {}
    for linha in _todas_linhas():
        if str(linha.get("codigo_juiz", "")).strip().casefold() != codigo:
            continue
        respostas[str(linha.get("id_pergunta", ""))] = {
            "acuracia": str(linha.get("acuracia", "")),
            "clareza": str(linha.get("clareza", "")),
            "seguranca": str(linha.get("seguranca", "")),
            "justificativa": str(linha.get("justificativa", "")),
            "comentario": str(linha.get("comentario", "")),
            "comentario_geral": str(linha.get("comentario_geral", "")),
        }
    return respostas
