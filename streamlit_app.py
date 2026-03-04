import streamlit as st
import requests
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import poisson

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="AI ScoreCast Pro", layout="wide", initial_sidebar_state="collapsed")

# --- RÉCUPÉRATION DES SECRETS ---
try:
    API_KEY = st.secrets["API_FOOTBALL_KEY"]
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except:
    API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
    ADMIN_PASSWORD = "Tunga25721204301"

# --- SYSTÈME DE LANGUES ---
languages = {
    "Français": {"live": "EN DIRECT", "prono": "PRONOSTICS", "hist": "HISTORIQUE", "admin": "ADMIN", "install": "INSTALLER L'APP", "btts": "Les deux marquent", "over": "Plus de 2.5", "finished": "FT"},
    "English": {"live": "LIVE", "prono": "PREDICTIONS", "hist": "HISTORY", "admin": "ADMIN", "install": "INSTALL APP", "btts": "Both Teams to Score", "over": "Over 2.5", "finished": "FT"},
    "Español": {"live": "EN VIVO", "prono": "PRONÓSTICOS", "hist": "HISTORIAL", "admin": "ADMIN", "install": "INSTALAR APP", "btts": "Ambos marcan", "over": "Más de 2.5", "finished": "FT"},
    "Português": {"live": "AO VIVO", "prono": "PALPITES", "hist": "HISTÓRICO", "admin": "ADMIN", "install": "INSTALAR APP", "btts": "Ambas marcam", "over": "Mais de 2.5", "finished": "FT"},
    "Deutsch": {"live": "LIVE", "prono": "PROGNOSEN", "hist": "HISTORIE", "admin": "ADMIN", "install": "APP INSTALLIEREN", "btts": "Beide treffen", "over": "Über 2.5", "finished": "FT"},
    "العربية": {"live": "مباشر", "prono": "توقعات", "hist": "الأرشيف", "admin": "مدير", "install": "تثبيت التطبيق", "btts": "كلا الفريقين يسجل", "over": "أكثر من 2.5", "finished": "FT"},
    "中文": {"live": "直播", "prono": "预测", "hist": "历史", "admin": "管理员", "install": "安装应用", "btts": "两队均得分", "over": "超过 2.5", "finished": "FT"},
    "Kiswahili": {"live": "MUBASHARA", "prono": "UTABIRI", "hist": "HISTORIA", "admin": "MSIMAMIZI", "install": "WEKA APP", "btts": "Zote kufunga", "over": "Zaidi ya 2.5", "finished": "FT"}
}

# Choix de la langue dans la sidebar
with st.sidebar:
    st.title("Settings")
    sel_lang = st.selectbox("🌐 Language / Lugha", list(languages.keys()))
    L = languages[sel_lang]

# --- STYLE CSS ---
st.markdown(f"""
    <style>
    .main {{ background-color: #0e1117; }}
    .promo-banner {{ background: linear-gradient(90deg, #1d976c 0%, #93f9b9 100%); color: #000 !important; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 15px; text-decoration: none; display: block; }}
    .match-card {{ background-color: #1a1c23; border: 1px solid #2d2f39; padding: 12px; border-radius: 12px; margin-bottom: 10px; }}
    .team-row {{ display: flex; justify-content: space-between; align-items: center; margin: 5px 0; }}
    .team-info {{ display: flex; align-items: center; gap: 10px; color: white; }}
    .team-logo {{ width: 22px; height: 22px; }}
    .score-live {{ color: #00ff88; font-weight: bold; }}
    .live-badge-static {{ color: white; background-color: #ff4b4b; padding: 2px 6px; border-radius: 4px; font-size: 0.7em; font-weight: bold; }}
    .market-badge {{ background-color: #262932; color: #00ff88; padding: 4px 8px; border-radius: 6px; font-size: 0.75em; font-weight: bold; border: 1px solid #3e414b; margin-right: 5px; margin-top: 8px; display: inline-block; }}
    </style>
""", unsafe_allow_html=True)

# --- LOGIQUE PRÉDICTIONS ---
def get_ai_prediction(h_avg, a_avg):
    h_p = [poisson.pmf(i, h_avg if h_avg > 0 else 0.5) for i in range(6)]
    a_p = [poisson.pmf(i, a_avg if a_avg > 0 else 0.5) for i in range(6)]
    m = np.outer(h_p, a_p)
    w, d, l = np.sum(np.tril(m, -1)), np.sum(np.diag(m)), np.sum(np.triu(m, 1))
    ov25 = 1 - (m[0,0]+m[0,1]+m[0,2]+m[1,0]+m[1,1]+m[2,0])
    btts = (1-h_p[0]) * (1-a_p[0])
    return f"{w*100:.0f}%", f"{d*100:.0f}%", f"{l*100:.0f}%", f"{ov25*100:.0f}%", f"{btts*100:.0f}%"

# --- HEADER & PROMO ---
if 'promo_text' not in st.session_state: st.session_state['promo_text'] = "💰 BONUS +200% CODE: TUNGA20"
if 'promo_link' not in st.session_state: st.session_state['promo_link'] = "https://1xbet.com"

st.markdown(f'<a href="{st.session_state["promo_link"]}" class="promo-banner">{st.session_state["promo_text"]}</a>', unsafe_allow_html=True)

# Tabs
tab_live, tab_prono, tab_hist = st.tabs([f"🎮 {L['live']}", f"📈 {L['prono']}", f"📚 {L['hist']}"])

def fetch(params):
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try: return requests.get("https://v3.football.api-sports.io/fixtures", headers=headers, params=params).json().get('response', [])
    except: return []

# --- 1. LIVE ---
with tab_live:
    lives = fetch({'live': 'all'})
    if not lives: st.info("No matches live...")
    for m in lives:
        st.markdown(f"""
        <div class="match-card">
            <div style="font-size:0.7em; color:#888; margin-bottom:5px;">{m['league']['name']} • <span class="live-badge-static">● {m['fixture']['status']['elapsed']}'</span></div>
            <div class="team-row">
                <div class="team-info"><img src="{m['teams']['home']['logo']}" class="team-logo"><span>{m['teams']['home']['name']}</span></div>
                <div class="score-live">{m['goals']['home']}</div>
            </div>
            <div class="team-row">
                <div class="team-info"><img src="{m['teams']['away']['logo']}" class="team-logo"><span>{m['teams']['away']['name']}</span></div>
                <div class="score-live">{m['goals']['away']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 2. PRONOSTICS (1X2, OVER, BTTS) ---
with tab_prono:
    fixtures = fetch({'date': datetime.now().strftime('%Y-%m-%d')})
    for f in fixtures:
        if f['fixture']['status']['short'] in ['NS', 'TBD']:
            w, d, l, ov, bt = get_ai_prediction(1.6, 1.2)
            st.markdown(f"""
            <div class="match-card">
                <div style="font-size:0.7em; color:#888; margin-bottom:8px;">{f['league']['name']} • {f['fixture']['date'][11:16]}</div>
                <div class="team-row"><div class="team-info"><img src="{f['teams']['home']['logo']}" class="team-logo"><span>{f['teams']['home']['name']}</span></div></div>
                <div class="team-row"><div class="team-info"><img src="{f['teams']['away']['logo']}" class="team-logo"><span>{f['teams']['away']['name']}</span></div></div>
                <div class="market-badge">1X2: {w}|{d}|{l}</div>
                <div class="market-badge">Over 2.5: {ov}</div>
                <div class="market-badge">BTTS: {bt}</div>
            </div>
            """, unsafe_allow_html=True)

# --- 3. HISTORIQUE (FT) ---
with tab_hist:
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    past = fetch({'date': yesterday})
    for p in past[:15]:
        st.markdown(f"""
        <div class="match-card" style="opacity:0.8;">
            <div class="team-row">
                <div class="team-info"><span style="font-size:0.85em;">{p['teams']['home']['name']} {p['goals']['home']} - {p['goals']['away']} {p['teams']['away']['name']}</span></div>
                <div style="color:#888; font-size:0.8em; font-weight:bold;">{L['finished']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- INSTALL APP EXPANDER ---
with st.expander(f"📲 {L['install']}"):
    st.write("Android/PC: Menu > Install App")
    st.write("iOS: Share > Add to Home Screen")
