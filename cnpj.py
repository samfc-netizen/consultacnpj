import streamlit as st
import pandas as pd
import requests
import re
import time
from io import BytesIO
from typing import Dict, Any, Tuple, Optional, List

# =========================================================
# CONFIGURAÇÃO GERAL
# =========================================================
st.set_page_config(
    page_title="CNPJ Intelligence",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

USUARIO_PADRAO = "samuel"
SENHA_PADRAO = "samuel"

# =========================================================
# CSS - VISUAL DE SOFTWARE
# =========================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 28%),
                radial-gradient(circle at top right, rgba(14, 165, 233, 0.10), transparent 24%),
                #f7f9fc;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
            max-width: 1420px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #0b1220;
            border-right: 1px solid rgba(255,255,255,.08);
        }
        [data-testid="stSidebar"] * {
            color: #e5edf7 !important;
        }
        [data-testid="stSidebar"] .stRadio > label {
            display: none;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label {
            background: rgba(255,255,255,.045);
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 12px;
            padding: 9px 12px;
            margin-bottom: 8px;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(59,130,246,.18);
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,.10);
        }

        /* Headings and cards */
        h1, h2, h3, h4 {
            color: #0f172a;
            letter-spacing: -0.02em;
        }
        .app-shell {
            background: rgba(255,255,255,.78);
            border: 1px solid rgba(148, 163, 184, .22);
            border-radius: 22px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.07);
            padding: 22px;
            margin-bottom: 18px;
            backdrop-filter: blur(8px);
        }
        .main-card {
            background: rgba(255,255,255,.86);
            border: 1px solid rgba(226, 232, 240, .95);
            border-radius: 20px;
            padding: 22px;
            box-shadow: 0 14px 35px rgba(15, 23, 42, 0.055);
            margin-bottom: 18px;
        }
        .hero {
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, #08111f 0%, #123b7a 52%, #0ea5e9 100%);
            border-radius: 26px;
            padding: 30px 34px;
            color: white;
            box-shadow: 0 24px 55px rgba(2, 132, 199, 0.22);
            margin-bottom: 20px;
        }
        .hero:after {
            content: '';
            position: absolute;
            width: 280px;
            height: 280px;
            border-radius: 999px;
            background: rgba(255,255,255,.12);
            right: -90px;
            top: -120px;
        }
        .hero h1 {
            color: white;
            font-size: 38px;
            margin-bottom: 8px;
            line-height: 1.05;
        }
        .hero p {
            color: #dbeafe;
            font-size: 16px;
            margin: 0;
            max-width: 850px;
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 11px;
            border-radius: 999px;
            background: rgba(255,255,255,.13);
            border: 1px solid rgba(255,255,255,.20);
            color: #eff6ff;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: .06em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .metric-card {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 17px 18px;
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.055);
        }
        .small-label {
            color: #64748b;
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .075em;
        }
        .big-number {
            color: #0f172a;
            font-size: 29px;
            font-weight: 850;
            margin-top: 5px;
            line-height: 1.1;
        }

        /* Login */
        .login-bg {
            min-height: 78vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px 0;
        }
        .login-card {
            width: 100%;
            max-width: 920px;
            display: grid;
            grid-template-columns: 1.05fr .95fr;
            border-radius: 28px;
            overflow: hidden;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            box-shadow: 0 32px 80px rgba(15, 23, 42, .14);
        }
        .login-brand {
            background: linear-gradient(145deg, #08111f 0%, #133b7c 58%, #0ea5e9 100%);
            padding: 42px;
            color: white;
            position: relative;
            overflow: hidden;
            min-height: 420px;
        }
        .login-brand:before {
            content: '';
            position: absolute;
            right: -70px;
            top: -90px;
            width: 240px;
            height: 240px;
            border-radius: 999px;
            background: rgba(255,255,255,.12);
        }
        .login-brand:after {
            content: '';
            position: absolute;
            left: -80px;
            bottom: -110px;
            width: 260px;
            height: 260px;
            border-radius: 999px;
            background: rgba(255,255,255,.08);
        }
        .login-logo {
            width: 52px;
            height: 52px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,.15);
            border: 1px solid rgba(255,255,255,.20);
            font-size: 25px;
            margin-bottom: 22px;
        }
        .login-brand h1 {
            color: white;
            font-size: 34px;
            line-height: 1.05;
            margin: 0 0 12px 0;
        }
        .login-brand p {
            color: #dbeafe;
            margin: 0;
            font-size: 15px;
            line-height: 1.65;
            max-width: 360px;
        }
        .login-features {
            display: grid;
            gap: 10px;
            margin-top: 30px;
            position: relative;
            z-index: 1;
        }
        .login-feature {
            background: rgba(255,255,255,.10);
            border: 1px solid rgba(255,255,255,.16);
            border-radius: 14px;
            padding: 11px 13px;
            color: #eff6ff;
            font-size: 13px;
            font-weight: 600;
        }
        .login-form-card {
            padding: 42px;
            background: #ffffff;
        }
        .login-form-title {
            font-size: 24px;
            font-weight: 850;
            color: #0f172a;
            margin-bottom: 6px;
        }
        .login-form-subtitle {
            color: #64748b;
            font-size: 14px;
            margin-bottom: 22px;
        }

        /* Inputs/buttons/tables */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div {
            border-radius: 12px !important;
            border-color: #dbe3ef !important;
        }
        .stButton > button, .stDownloadButton > button, button[kind="primary"] {
            border-radius: 12px !important;
            font-weight: 750 !important;
            border: 1px solid rgba(37, 99, 235, .18) !important;
        }
        .stButton > button[kind="primary"], .stFormSubmitButton button {
            background: linear-gradient(135deg, #1d4ed8 0%, #0ea5e9 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 12px 24px rgba(37, 99, 235, .22) !important;
        }
        [data-testid="stDataFrame"] {
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            overflow: hidden;
        }
        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 16px;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
        }

        @media (max-width: 900px) {
            .login-card { grid-template-columns: 1fr; }
            .login-brand { min-height: auto; padding: 30px; }
            .login-form-card { padding: 30px; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# AUTENTICAÇÃO
# =========================================================
def tela_login():
    st.markdown(
        """
        <div class="login-bg">
            <div class="login-card">
                <div class="login-brand">
                    <div class="login-logo">🏢</div>
                    <h1>CNPJ Intelligence</h1>
                    <p>Enriquecimento cadastral, análise por CNAE e segmentação geográfica para transformar listas de CNPJs em inteligência comercial.</p>
                    <div class="login-features">
                        <div class="login-feature">✓ Consulta BrasilAPI + Minha Receita</div>
                        <div class="login-feature">✓ Dashboard por CNAE, UF, município e bairro</div>
                        <div class="login-feature">✓ Exportação em Excel com telefone e e-mail</div>
                    </div>
                </div>
                <div class="login-form-card">
                    <div class="login-form-title">Entrar no sistema</div>
                    <div class="login-form-subtitle">Use suas credenciais para acessar o painel.</div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("form_login", clear_on_submit=False):
        usuario = st.text_input("Login", placeholder="Digite seu login")
        senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        lembrar = st.checkbox("Manter sessão nesta aba", value=True)
        entrar = st.form_submit_button("Acessar painel", use_container_width=True)

    st.markdown(
        """
                    <div style="margin-top:18px;color:#94a3b8;font-size:12px;line-height:1.6;">
                        Ambiente local Streamlit • Acesso restrito
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if entrar:
        if usuario == USUARIO_PADRAO and senha == SENHA_PADRAO:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.rerun()
        else:
            st.error("Login ou senha inválidos.")

def exigir_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        tela_login()
        st.stop()

# =========================================================
# UTILIDADES
# =========================================================
def limpar_cnpj(cnpj) -> str:
    if pd.isna(cnpj):
        return ""
    texto = str(cnpj).strip()
    if re.fullmatch(r"\d+\.0", texto):
        texto = texto[:-2]
    if "e" in texto.lower():
        try:
            texto = str(int(float(texto)))
        except Exception:
            pass
    cnpj_limpo = re.sub(r"\D", "", texto)
    if 1 <= len(cnpj_limpo) < 14:
        cnpj_limpo = cnpj_limpo.zfill(14)
    return cnpj_limpo


def formatar_cnpj(cnpj_limpo: str) -> str:
    if len(cnpj_limpo) != 14:
        return cnpj_limpo
    return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"


def normalizar_nome_coluna(coluna: str) -> str:
    texto = str(coluna).strip().lower()
    texto = re.sub(r"[áàãâä]", "a", texto)
    texto = re.sub(r"[éèêë]", "e", texto)
    texto = re.sub(r"[íìîï]", "i", texto)
    texto = re.sub(r"[óòõôö]", "o", texto)
    texto = re.sub(r"[úùûü]", "u", texto)
    texto = re.sub(r"ç", "c", texto)
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_")


def identificar_coluna_por_nomes(df: pd.DataFrame, termos: List[str]) -> Optional[str]:
    termos_norm = [normalizar_nome_coluna(t) for t in termos]
    for coluna in df.columns:
        nome = normalizar_nome_coluna(coluna)
        if any(t in nome for t in termos_norm):
            return coluna
    return None


def identificar_coluna_cnpj(df: pd.DataFrame) -> Optional[str]:
    por_nome = identificar_coluna_por_nomes(df, ["cnpj"])
    if por_nome:
        return por_nome
    possiveis = []
    for coluna in df.columns:
        validos = 0
        for valor in df[coluna].dropna().head(80):
            if len(limpar_cnpj(valor)) == 14:
                validos += 1
        if validos >= 3:
            possiveis.append(coluna)
    return possiveis[0] if possiveis else None


def montar_endereco(dados: Dict[str, Any]) -> str:
    tipo_logradouro = dados.get("descricao_tipo_de_logradouro", "") or ""
    logradouro = dados.get("logradouro", "") or ""
    numero = dados.get("numero", "") or ""
    complemento = dados.get("complemento", "") or ""
    bairro = dados.get("bairro", "") or ""
    municipio = dados.get("municipio", "") or ""
    uf = dados.get("uf", "") or ""
    cep = dados.get("cep", "") or ""

    linha1 = " ".join(x for x in [tipo_logradouro, logradouro] if x).strip()
    if numero:
        linha1 = f"{linha1}, {numero}" if linha1 else numero
    if complemento:
        linha1 = f"{linha1} - {complemento}" if linha1 else complemento

    linha2 = ""
    if bairro:
        linha2 += bairro
    if municipio or uf:
        cidade_uf = f"{municipio}/{uf}" if municipio and uf else municipio or uf
        linha2 = f"{linha2}, {cidade_uf}" if linha2 else cidade_uf
    if cep:
        linha2 = f"{linha2} - CEP {cep}" if linha2 else f"CEP {cep}"

    return " | ".join([p for p in [linha1, linha2] if p])


def normalizar_socio(socio: Dict[str, Any]) -> str:
    nome = socio.get("nome_socio", "") or socio.get("nome", "") or ""
    qualificacao = socio.get("qualificacao_socio", "") or socio.get("qualificacao", "") or ""
    if nome and qualificacao:
        return f"{nome} - {qualificacao}"
    return nome or qualificacao


def normalizar_resposta(dados: Dict[str, Any], cnpj_limpo: str, fonte: str) -> Dict[str, Any]:
    cnaes_secundarios = dados.get("cnaes_secundarios") or []
    socios = dados.get("qsa") or []
    socios_formatados = [normalizar_socio(s) for s in socios if isinstance(s, dict)]

    return {
        "CNPJ Consultado": cnpj_limpo,
        "CNPJ Formatado": formatar_cnpj(cnpj_limpo),
        "Fonte Consulta": fonte,
        "Razão Social": dados.get("razao_social", "") or "",
        "Nome Fantasia": dados.get("nome_fantasia", "") or "",
        "Situação": dados.get("descricao_situacao_cadastral", "") or "",
        "CNAE Principal": dados.get("cnae_fiscal", "") or "",
        "Descrição CNAE Principal": dados.get("cnae_fiscal_descricao", "") or "",
        "CNAEs Secundários": "; ".join(
            f"{c.get('codigo', '')} - {c.get('descricao', '')}" for c in cnaes_secundarios if isinstance(c, dict)
        ),
        "CEP": dados.get("cep", "") or "",
        "Município": dados.get("municipio", "") or "",
        "UF": dados.get("uf", "") or "",
        "Endereço": montar_endereco(dados),
        "Sócios": "; ".join(socios_formatados),
        "Porte": dados.get("porte", "") or "",
        "Natureza Jurídica": dados.get("natureza_juridica", "") or "",
        "Erro Consulta": "",
    }


def separar_socios_em_colunas(df: pd.DataFrame, coluna_socios: str = "Sócios", max_socios: int = 8) -> pd.DataFrame:
    df = df.copy()
    if coluna_socios not in df.columns:
        return df
    socios_split = df[coluna_socios].fillna("").astype(str).str.split("; ")
    for i in range(max_socios):
        df[f"Sócio {i + 1}"] = socios_split.apply(lambda lista: lista[i] if isinstance(lista, list) and len(lista) > i else "")
    return df


def gerar_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="CNPJs Enriquecidos")
    return output.getvalue()

# =========================================================
# APIs E RETRY
# =========================================================
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "CNPJ-Intelligence-Streamlit/2.0",
    "Accept": "application/json",
})


def requisitar_json(url: str, tentativas: int, espera_429: float, timeout: int = 25) -> Tuple[Optional[Dict[str, Any]], Optional[int], str]:
    ultima_msg = ""
    ultimo_status = None
    for tentativa in range(1, tentativas + 1):
        try:
            resposta = SESSION.get(url, timeout=timeout)
            ultimo_status = resposta.status_code
            if resposta.status_code == 200:
                try:
                    return resposta.json(), resposta.status_code, ""
                except Exception as e:
                    return None, resposta.status_code, f"Resposta não é JSON válido: {e}"

            if resposta.status_code == 429:
                retry_after = resposta.headers.get("Retry-After")
                try:
                    espera = float(retry_after) if retry_after else espera_429
                except Exception:
                    espera = espera_429
                ultima_msg = f"Erro 429: limite de requisições. Aguardou {espera:.0f}s."
                time.sleep(espera)
                continue

            if 500 <= resposta.status_code <= 599:
                ultima_msg = f"Erro {resposta.status_code}: instabilidade no servidor."
                time.sleep(min(espera_429, 10))
                continue

            texto_erro = resposta.text[:250] if resposta.text else ""
            return None, resposta.status_code, f"Erro {resposta.status_code}: {texto_erro}"
        except requests.exceptions.Timeout:
            ultima_msg = "Timeout na consulta."
            time.sleep(min(espera_429, 10))
        except requests.exceptions.RequestException as e:
            ultima_msg = str(e)
            time.sleep(min(espera_429, 10))
    return None, ultimo_status, ultima_msg or "Falha após tentativas."


def consultar_brasilapi(cnpj_limpo: str, tentativas: int, espera_429: float):
    return requisitar_json(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", tentativas, espera_429)


def consultar_minha_receita(cnpj_limpo: str, tentativas: int, espera_429: float):
    return requisitar_json(f"https://minhareceita.org/{cnpj_limpo}", tentativas, espera_429)


def resposta_vazia(cnpj_limpo: str, erro: str = "") -> Dict[str, Any]:
    base = normalizar_resposta({}, cnpj_limpo, "")
    base["Erro Consulta"] = erro
    return base


def consultar_cnpj(cnpj, tentativas: int, espera_429: float, usar_fallback: bool = True) -> Dict[str, Any]:
    cnpj_limpo = limpar_cnpj(cnpj)
    if len(cnpj_limpo) != 14:
        return resposta_vazia(cnpj_limpo, "CNPJ inválido")

    erros = []
    dados, status, erro = consultar_brasilapi(cnpj_limpo, tentativas, espera_429)
    if dados:
        return normalizar_resposta(dados, cnpj_limpo, "BrasilAPI")
    erros.append(f"BrasilAPI: {erro or 'sem resposta'}")

    if usar_fallback:
        dados, status, erro = consultar_minha_receita(cnpj_limpo, tentativas, espera_429)
        if dados:
            return normalizar_resposta(dados, cnpj_limpo, "Minha Receita")
        erros.append(f"Minha Receita: {erro or 'sem resposta'}")

    return resposta_vazia(cnpj_limpo, " | ".join(erros))



def coluna_existente(df: pd.DataFrame, candidatos: List[str]) -> Optional[str]:
    for cand in candidatos:
        if cand in df.columns:
            return cand
    norm_map = {normalizar_nome_coluna(c): c for c in df.columns}
    for cand in candidatos:
        nc = normalizar_nome_coluna(cand)
        if nc in norm_map:
            return norm_map[nc]
    return None


def extrair_bairro_cidade_satelite(endereco: str) -> str:
    """Extrai o trecho depois do primeiro | e antes da vírgula.

    Exemplos:
    - ... | SANTA MARIA, BRASILIA/DF - CEP ... -> SANTA MARIA
    - ... | CREMACAO, BELEM/PA - CEP ... -> CREMACAO
    """
    if pd.isna(endereco):
        return ""
    texto = str(endereco).strip()
    if "|" not in texto:
        return ""
    depois = texto.split("|", 1)[1].strip()
    if not depois:
        return ""
    bairro = depois.split(",", 1)[0].strip()
    bairro = re.sub(r"\s+", " ", bairro)
    return bairro


def preparar_dashboard(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().fillna("")

    col_end = coluna_existente(df, ["Endereço", "Endereco"])
    col_mun = coluna_existente(df, ["Município", "Municipio", "Cidade"])
    col_uf = coluna_existente(df, ["UF"])
    col_cnpj = coluna_existente(df, ["CNPJ Formatado", "CNPJ Consultado", "CNPJ"])
    col_tel = coluna_existente(df, ["Telefone Upload", "TELEFONE", "Telefone", "Fone", "Celular", "Whatsapp"])
    col_email = coluna_existente(df, ["E-mail Upload", "E-MAIL", "Email", "E_mail", "Mail"])

    if col_end:
        df["Cidade Satélite / Bairro"] = df[col_end].apply(extrair_bairro_cidade_satelite)
    else:
        df["Cidade Satélite / Bairro"] = ""

    if col_mun:
        df["Município Dashboard"] = df[col_mun].astype(str).str.strip().str.upper()
    else:
        df["Município Dashboard"] = ""

    if col_uf:
        df["UF Dashboard"] = df[col_uf].astype(str).str.strip().str.upper()
    else:
        df["UF Dashboard"] = ""

    if col_cnpj:
        df["CNPJ Dashboard"] = df[col_cnpj].astype(str)
    else:
        df["CNPJ Dashboard"] = ""

    if col_tel:
        df["Telefone Dashboard"] = df[col_tel].astype(str)
    else:
        df["Telefone Dashboard"] = ""

    if col_email:
        df["E-mail Dashboard"] = df[col_email].astype(str)
    else:
        df["E-mail Dashboard"] = ""

    # Quando o Município estiver vazio, tenta extrair do endereço: "..., BRASILIA/DF - CEP ..."
    if col_end:
        mask_mun_vazio = df["Município Dashboard"].eq("")
        extraido = df[col_end].astype(str).str.extract(r",\s*([^,/|]+)\s*/\s*([A-Z]{2})\s*-\s*CEP", expand=True)
        if not extraido.empty:
            df.loc[mask_mun_vazio, "Município Dashboard"] = extraido.loc[mask_mun_vazio, 0].fillna("").str.strip().str.upper()
            mask_uf_vazio = df["UF Dashboard"].eq("")
            df.loc[mask_uf_vazio, "UF Dashboard"] = extraido.loc[mask_uf_vazio, 1].fillna("").str.strip().str.upper()

    return df


def contar_cnpjs(df: pd.DataFrame, grupo: List[str]) -> pd.DataFrame:
    base = df.copy()
    if "CNPJ Dashboard" in base.columns and base["CNPJ Dashboard"].astype(str).str.strip().ne("").any():
        cont = base.groupby(grupo, dropna=False)["CNPJ Dashboard"].nunique().reset_index(name="Quantidade de CNPJs")
    else:
        cont = base.groupby(grupo, dropna=False).size().reset_index(name="Quantidade de CNPJs")
    return cont.sort_values("Quantidade de CNPJs", ascending=False).reset_index(drop=True)


def tabela_cnae_dashboard(df: pd.DataFrame) -> pd.DataFrame:
    col_cod = coluna_existente(df, ["CNAE Principal"])
    col_desc = coluna_existente(df, ["Descrição CNAE Principal", "Descricao CNAE Principal"])
    df2 = df.copy()
    df2["CNAE Código"] = df2[col_cod].astype(str).str.strip() if col_cod else "Não informado"
    df2["CNAE Descrição"] = df2[col_desc].astype(str).str.strip() if col_desc else "Não informado"
    df2.loc[df2["CNAE Código"].eq(""), "CNAE Código"] = "Não informado"
    df2.loc[df2["CNAE Descrição"].eq(""), "CNAE Descrição"] = "Não informado"
    return contar_cnpjs(df2, ["CNAE Código", "CNAE Descrição"])


def exibir_drill_cnae(df: pd.DataFrame, cnae_codigo: str, cnae_desc: str):
    col_cod = coluna_existente(df, ["CNAE Principal"])
    col_desc = coluna_existente(df, ["Descrição CNAE Principal", "Descricao CNAE Principal"])
    filtro = pd.Series([True] * len(df), index=df.index)
    if col_cod:
        filtro &= df[col_cod].astype(str).str.strip().replace("", "Não informado").eq(cnae_codigo)
    if col_desc:
        filtro &= df[col_desc].astype(str).str.strip().replace("", "Não informado").eq(cnae_desc)
    detalhe = df.loc[filtro].copy()
    cols = [
        "CNPJ Dashboard", "Razão Social", "Telefone Dashboard", "E-mail Dashboard",
        "Município Dashboard", "UF Dashboard", "Cidade Satélite / Bairro", "Endereço"
    ]
    cols = [c for c in cols if c in detalhe.columns]
    detalhe = detalhe[cols].rename(columns={
        "CNPJ Dashboard": "CNPJ",
        "Telefone Dashboard": "Telefone",
        "E-mail Dashboard": "E-mail",
        "Município Dashboard": "Município",
        "UF Dashboard": "UF",
    })
    st.markdown(f"##### Drill-down do CNAE: {cnae_codigo} - {cnae_desc}")
    st.dataframe(detalhe, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Baixar drill do CNAE",
        data=gerar_excel(detalhe),
        file_name=f"drill_cnae_{re.sub(r'[^0-9A-Za-z]+', '_', cnae_codigo)}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )


def exibir_drill_uf(df: pd.DataFrame, uf: str):
    detalhe = df[df["UF Dashboard"].eq(uf)].copy()
    resumo_municipios = contar_cnpjs(detalhe, ["Município Dashboard", "Cidade Satélite / Bairro"])
    resumo_municipios = resumo_municipios.rename(columns={
        "Município Dashboard": "Município",
        "Cidade Satélite / Bairro": "Cidade Satélite / Bairro",
    })
    st.markdown(f"##### Municípios e bairros/cidades satélites em {uf}")
    st.dataframe(resumo_municipios, use_container_width=True, hide_index=True)

    cols = [
        "CNPJ Dashboard", "Razão Social", "Telefone Dashboard", "E-mail Dashboard",
        "Município Dashboard", "UF Dashboard", "Cidade Satélite / Bairro", "Endereço"
    ]
    cols = [c for c in cols if c in detalhe.columns]
    detalhe = detalhe[cols].rename(columns={
        "CNPJ Dashboard": "CNPJ",
        "Telefone Dashboard": "Telefone",
        "E-mail Dashboard": "E-mail",
        "Município Dashboard": "Município",
        "UF Dashboard": "UF",
    })
    st.markdown(f"##### Endereços detalhados em {uf}")
    st.dataframe(detalhe, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Baixar drill da UF",
        data=gerar_excel(detalhe),
        file_name=f"drill_uf_{uf}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

# =========================================================
# COMPONENTES VISUAIS
# =========================================================
def hero():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">Software comercial • CNPJ Intelligence</div>
            <h1>Enriquecimento e análise de CNPJs</h1>
            <p>Consulta, enriquecimento cadastral e análise visual de clientes por CNAE, situação, porte, UF, município e cidade satélite/bairro.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card_metric(label: str, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="small-label">{label}</div>
            <div class="big-number">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_kpis(df: pd.DataFrame):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card_metric("Registros", f"{len(df):,}".replace(",", "."))
    with col2:
        cnpjs = df["CNPJ Consultado"].nunique() if "CNPJ Consultado" in df.columns else 0
        card_metric("CNPJs únicos", f"{cnpjs:,}".replace(",", "."))
    with col3:
        erros = df["Erro Consulta"].fillna("").astype(str).ne("").sum() if "Erro Consulta" in df.columns else 0
        card_metric("Erros", f"{erros:,}".replace(",", "."))
    with col4:
        fontes = df["Fonte Consulta"].replace("", pd.NA).dropna().nunique() if "Fonte Consulta" in df.columns else 0
        card_metric("Fontes usadas", fontes)


def grafico_barras(df: pd.DataFrame, coluna: str, titulo: str, top: int = 15):
    if coluna not in df.columns:
        st.info(f"Coluna '{coluna}' não encontrada.")
        return
    base = df[coluna].fillna("Não informado").replace("", "Não informado").value_counts().head(top).reset_index()
    base.columns = [coluna, "Quantidade"]
    st.bar_chart(base.set_index(coluna), use_container_width=True)

# =========================================================
# APP
# =========================================================
exigir_login()

with st.sidebar:
    st.markdown("""
    <div style="padding:10px 4px 18px 4px;">
        <div style="font-size:22px;font-weight:850;letter-spacing:-.03em;">🏢 CNPJ Intelligence</div>
        <div style="font-size:12px;color:#94a3b8!important;margin-top:4px;">Painel de inteligência cadastral</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Usuário logado: {st.session_state.get('usuario', '')}")
    pagina = st.radio("Menu", ["Consulta e Enriquecimento", "Dashboard", "Configurações"], label_visibility="collapsed")
    st.divider()
    if st.button("Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()

if pagina == "Consulta e Enriquecimento":
    hero()
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Upload da planilha")
    st.write("A planilha esperada deve ter as colunas **CNPJ**, **TELEFONE** e **E-MAIL**. O sistema identifica automaticamente essas colunas e preserva telefone/e-mail no Excel final.")

    col_cfg1, col_cfg2, col_cfg3, col_cfg4 = st.columns(4)
    with col_cfg1:
        tempo_entre_consultas = st.number_input("Tempo entre CNPJs (s)", min_value=0.0, max_value=60.0, value=2.0, step=0.5)
    with col_cfg2:
        espera_429 = st.number_input("Espera no 429 (s)", min_value=10.0, max_value=300.0, value=60.0, step=10.0)
    with col_cfg3:
        tentativas = st.number_input("Tentativas por API", min_value=1, max_value=10, value=3, step=1)
    with col_cfg4:
        usar_fallback = st.checkbox("Fallback Minha Receita", value=True)

    ignorar_duplicados = st.checkbox("Usar cache para CNPJs repetidos", value=True)
    arquivo = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])
    st.markdown('</div>', unsafe_allow_html=True)

    if arquivo:
        df = pd.read_excel(arquivo, dtype=str).fillna("")

        coluna_cnpj_auto = identificar_coluna_cnpj(df)
        coluna_tel_auto = identificar_coluna_por_nomes(df, ["telefone", "fone", "celular", "whatsapp"])
        coluna_email_auto = identificar_coluna_por_nomes(df, ["email", "e_mail", "e-mail", "mail"])

        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("Conferência das colunas")
        col1, col2, col3 = st.columns(3)
        with col1:
            coluna_cnpj = st.selectbox("Coluna CNPJ", df.columns, index=list(df.columns).index(coluna_cnpj_auto) if coluna_cnpj_auto in df.columns else 0)
        with col2:
            coluna_telefone = st.selectbox("Coluna TELEFONE", ["Não usar"] + list(df.columns), index=(list(df.columns).index(coluna_tel_auto) + 1) if coluna_tel_auto in df.columns else 0)
        with col3:
            coluna_email = st.selectbox("Coluna E-MAIL", ["Não usar"] + list(df.columns), index=(list(df.columns).index(coluna_email_auto) + 1) if coluna_email_auto in df.columns else 0)

        df["CNPJ Normalizado Upload"] = df[coluna_cnpj].map(limpar_cnpj)
        qtd_linhas = len(df)
        qtd_validos = df["CNPJ Normalizado Upload"].str.len().eq(14).sum()
        qtd_unicos = df.loc[df["CNPJ Normalizado Upload"].str.len().eq(14), "CNPJ Normalizado Upload"].nunique()
        c1, c2, c3 = st.columns(3)
        with c1: card_metric("Linhas", f"{qtd_linhas:,}".replace(",", "."))
        with c2: card_metric("CNPJs válidos", f"{qtd_validos:,}".replace(",", "."))
        with c3: card_metric("CNPJs únicos", f"{qtd_unicos:,}".replace(",", "."))
        st.dataframe(df.head(30), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🚀 Iniciar consulta", type="primary", use_container_width=True):
            resultados = []
            cache = {}
            total = len(df)
            barra = st.progress(0)
            status = st.empty()
            resumo = st.empty()

            qtd_brasilapi = 0
            qtd_minha = 0
            qtd_cache = 0
            qtd_erro = 0

            for i, linha in df.iterrows():
                cnpj_original = linha[coluna_cnpj]
                cnpj_limpo = limpar_cnpj(cnpj_original)
                status.info(f"Consultando {i + 1} de {total}: {formatar_cnpj(cnpj_limpo)}")

                if ignorar_duplicados and cnpj_limpo in cache:
                    resultado = cache[cnpj_limpo].copy()
                    resultado["Fonte Consulta"] = f"{resultado.get('Fonte Consulta', '')} (cache)".strip()
                    qtd_cache += 1
                else:
                    resultado = consultar_cnpj(cnpj_original, int(tentativas), float(espera_429), usar_fallback)
                    if ignorar_duplicados and cnpj_limpo:
                        cache[cnpj_limpo] = resultado.copy()

                # Preserva telefone e e-mail do upload no resultado final.
                resultado["Telefone Upload"] = linha[coluna_telefone] if coluna_telefone != "Não usar" else ""
                resultado["E-mail Upload"] = linha[coluna_email] if coluna_email != "Não usar" else ""

                fonte = resultado.get("Fonte Consulta", "")
                erro = resultado.get("Erro Consulta", "")
                if "BrasilAPI" in fonte and "cache" not in fonte:
                    qtd_brasilapi += 1
                elif "Minha Receita" in fonte and "cache" not in fonte:
                    qtd_minha += 1
                elif erro:
                    qtd_erro += 1

                resultados.append(resultado)
                barra.progress((i + 1) / total)
                resumo.write(f"BrasilAPI: {qtd_brasilapi} | Minha Receita: {qtd_minha} | Cache: {qtd_cache} | Erros: {qtd_erro}")
                if tempo_entre_consultas > 0:
                    time.sleep(float(tempo_entre_consultas))

            df_api = pd.DataFrame(resultados)
            df_final = pd.concat([df.reset_index(drop=True), df_api.reset_index(drop=True)], axis=1)
            df_final = separar_socios_em_colunas(df_final, "Sócios", max_socios=8)
            st.session_state["df_resultado"] = df_final

            st.success("Consulta finalizada.")
            mostrar_kpis(df_final)
            st.dataframe(df_final, use_container_width=True)
            st.download_button(
                "⬇️ Baixar Excel enriquecido",
                data=gerar_excel(df_final),
                file_name="cnpjs_enriquecidos_software.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

elif pagina == "Dashboard":
    hero()
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Dashboard visual")
    st.write("Use o resultado da consulta atual ou envie uma planilha já enriquecida para análise. O dashboard agora possui drill-down por CNAE e por UF.")
    arquivo_dash = st.file_uploader("Enviar planilha enriquecida para dashboard", type=["xlsx"], key="dash_upload")

    if arquivo_dash:
        df_dash = pd.read_excel(arquivo_dash, dtype=str).fillna("")
        st.session_state["df_resultado"] = df_dash
    elif "df_resultado" in st.session_state:
        df_dash = st.session_state["df_resultado"].copy()
    else:
        df_dash = pd.DataFrame()

    if df_dash.empty:
        st.info("Faça uma consulta ou envie uma planilha enriquecida para abrir o dashboard.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        df_dash = separar_socios_em_colunas(df_dash, "Sócios", max_socios=8)
        df_dash = preparar_dashboard(df_dash)
        st.session_state["df_resultado"] = df_dash

        mostrar_kpis(df_dash)
        st.divider()

        colf1, colf2, colf3 = st.columns(3)
        with colf1:
            ufs = sorted([x for x in df_dash["UF Dashboard"].dropna().unique() if str(x).strip()])
            filtro_uf = st.multiselect("Filtrar UF", ufs)
        with colf2:
            municipios = sorted([x for x in df_dash["Município Dashboard"].dropna().unique() if str(x).strip()])
            filtro_mun = st.multiselect("Filtrar Município", municipios)
        with colf3:
            bairros = sorted([x for x in df_dash["Cidade Satélite / Bairro"].dropna().unique() if str(x).strip()])
            filtro_bairro = st.multiselect("Filtrar cidade satélite/bairro", bairros)

        df_filtrado = df_dash.copy()
        if filtro_uf:
            df_filtrado = df_filtrado[df_filtrado["UF Dashboard"].isin(filtro_uf)]
        if filtro_mun:
            df_filtrado = df_filtrado[df_filtrado["Município Dashboard"].isin(filtro_mun)]
        if filtro_bairro:
            df_filtrado = df_filtrado[df_filtrado["Cidade Satélite / Bairro"].isin(filtro_bairro)]

        st.caption(f"Base filtrada: {len(df_filtrado):,} registros".replace(",", "."))

        aba1, aba2, aba3, aba4 = st.tabs([
            "📌 CNAEs com drill",
            "🗺️ UF / Município com drill",
            "🏙️ Cidade satélite / Bairro",
            "📄 Base detalhada",
        ])

        with aba1:
            st.markdown("### Ranking por CNAE")
            tabela_cnae = tabela_cnae_dashboard(df_filtrado)
            st.dataframe(tabela_cnae, use_container_width=True, hide_index=True)

            if not tabela_cnae.empty:
                opcoes_cnae = [
                    f"{row['CNAE Código']} - {row['CNAE Descrição']} ({row['Quantidade de CNPJs']} CNPJs)"
                    for _, row in tabela_cnae.iterrows()
                ]
                selecionado = st.selectbox("Clique/selecione um CNAE para abrir o drill", opcoes_cnae)
                idx = opcoes_cnae.index(selecionado)
                row = tabela_cnae.iloc[idx]
                exibir_drill_cnae(df_filtrado, str(row["CNAE Código"]), str(row["CNAE Descrição"]))

            st.download_button(
                "⬇️ Baixar ranking de CNAEs",
                data=gerar_excel(tabela_cnae),
                file_name="ranking_cnaes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with aba2:
            st.markdown("### Ranking por UF")
            tabela_uf = contar_cnpjs(df_filtrado, ["UF Dashboard"]).rename(columns={"UF Dashboard": "UF"})
            st.dataframe(tabela_uf, use_container_width=True, hide_index=True)

            if not tabela_uf.empty:
                opcoes_uf = [f"{row['UF']} ({row['Quantidade de CNPJs']} CNPJs)" for _, row in tabela_uf.iterrows()]
                selecionado_uf = st.selectbox("Clique/selecione uma UF para abrir municípios e endereços", opcoes_uf)
                uf = selecionado_uf.split(" ", 1)[0]
                exibir_drill_uf(df_filtrado, uf)

            st.download_button(
                "⬇️ Baixar ranking de UF",
                data=gerar_excel(tabela_uf),
                file_name="ranking_uf.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with aba3:
            st.markdown("### Segmentação por município e cidade satélite/bairro")
            st.write("O campo **Cidade Satélite / Bairro** é extraído do trecho depois do `|` no endereço. Em Brasília, isso ajuda a separar regiões como Santa Maria, Gama, Ceilândia etc.; em outras cidades, normalmente representa o bairro.")
            tabela_bairro = contar_cnpjs(df_filtrado, ["UF Dashboard", "Município Dashboard", "Cidade Satélite / Bairro"]).rename(columns={
                "UF Dashboard": "UF",
                "Município Dashboard": "Município",
            })
            st.dataframe(tabela_bairro, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Baixar segmentação por bairro/cidade satélite",
                data=gerar_excel(tabela_bairro),
                file_name="segmentacao_bairro_cidade_satelite.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with aba4:
            st.markdown("### Base detalhada tratada")
            cols_preferidas = [
                "CNPJ Dashboard", "Razão Social", "Telefone Dashboard", "E-mail Dashboard",
                "CNAE Principal", "Descrição CNAE Principal", "Município Dashboard", "UF Dashboard",
                "Cidade Satélite / Bairro", "Endereço", "Situação", "Porte", "Natureza Jurídica", "Sócios"
            ]
            cols = [c for c in cols_preferidas if c in df_filtrado.columns]
            restante = [c for c in df_filtrado.columns if c not in cols]
            base_exibicao = df_filtrado[cols + restante]
            st.dataframe(base_exibicao, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Baixar base do dashboard",
                data=gerar_excel(base_exibicao),
                file_name="dashboard_cnpj_base_tratada.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

else:
    hero()
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Configurações do sistema")
    st.write("Login padrão configurado no código:")
    st.code("Login: samuel\nSenha: samuel")
    st.warning("Para uso real em produção, troque esse login fixo por autenticação com banco de dados ou variáveis de ambiente.")
    st.markdown("""
    **Planilha esperada para upload:**

    - CNPJ
    - TELEFONE
    - E-MAIL

    O sistema preserva o telefone e o e-mail na exportação final como **Telefone Upload** e **E-mail Upload**.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
