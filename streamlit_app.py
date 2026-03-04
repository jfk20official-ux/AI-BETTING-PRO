import streamlit as st
import requests
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import numpy as np
from scipy.stats import poisson

# --- CONFIGURATION PAGE (Style Mobile First) ---
st.set_page_config(page_title="AI ScoreCast Pro", layout="wide", initial_sidebar_state="collapsed")

# --- RÉCUPÉRATION DES SECRETS ---
try:
    API_KEY = st.secrets["API_FOOTBALL_KEY"]
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except:
    API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
    ADMIN_PASSWORD = "Tunga25721204301"

# --- STYLE CSS (Inspiré de PredictX / ScoreCast) ---
st.markdown("""
    <style>
    /* Couleurs de fond et texte */
    .main { background-color: #0e1117; }
    div[data-testid="stVerticalBlock"] { gap: 0rem; }
    
    /* Bannière Code Promo style ScoreCast */
    .promo-banner {
        background: linear-gradient(90deg, #1d976c 0%, #93f9b9 100%);
        color: #000 !important;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 15px;
        text-decoration: none;
        display: block;
        font-size: 0.9em;
    }

    /* Cartes de Match Style Sombre */
    .match-card {
        background-color: #1a1c23;
        border: 1px solid #2d2f39;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    
    .team-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 5px 0;
    }
    
    .team-info { display: flex; align-items: center; gap: 10px; }
    .team-logo { width: 25px; height: 25px; }
    .team-name { font-size: 0.95em; font-weight: 500; color: #ffffff; }
    .score { font-weight: bold; color: #00ff88; font-size: 1.1em; }

    /* Badges Marchés */
    .market-container { display: flex; gap: 5px; margin-top: 10px; overflow-x: auto; }
    .market-badge {
        background-color: #262932;
        color: #00ff88;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.75em;
        font-weight: bold;
        border: 1px solid #3e414b;
        white-space: nowrap;
    }

    /* Badge Live Clignotant */
    .live-dot {
        color: #ff4b4b;
        font-weight: bold;
        animation: blink 1s infinite;
        font-size: 0.8em;
    }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
    
    /* Tabs personnalisés */
    .stTabs [data-baseweb="tab-list"] { background-color: #0e1117; }
    .stTabs [data-baseweb="tab"] { color: #888; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #00ff88; }
    </style>
""", unsafe_allow_html=True)

# --- ÉDITION ADMIN (PROMO) ---
if 'promo_txt' not in st.session_state: st.session_state['promo_txt'] = "💰 BONUS +200% avec le code : TUNGA20"
if 'promo_url' not in st.session_state: st.session_state['promo_url'] = "https://1xbet.com"

# --- LOGIQUE PRÉDICTIONS ---
def get_ai_prediction(h_avg, a_avg):
    h_p = [poisson.pmf(i, h_avg if h_avg > 0 else 0.5) for i in range(6)]
    a_p = [poisson.pmf(i, a_avg if a_avg > 0 else 0.5) for i in range(6)]
    m = np.outer(h_p, a_p)
    w, d, l = np.sum(np.tril(m, -1)), np.sum(np.diag(m)), np.sum(np.triu(m, 1))
    ov25 = 1 - (m[0,0]+m[0,1]+m[0,2]+m[1,0]+m[1,1]+m[2,0])
    btts = (1-h_p[0]) * (1-a_p[0])
    return f"{w*100:.0f}%", f"{d*100:.0f}%", f"{l*100:.0f}%", f"{ov25*100:.0f}%", f"{btts*100:.0f}%"

# --- SIDEBAR ADMIN ---
with st.sidebar:
    st.title("Admin Panel")
    if st.checkbox("🔑 Login"):
        if st.text_input("Pass", type="password") == ADMIN_PASSWORD:
            st.session_state['promo_txt'] = st.text_input("Texte Promo", st.session_state['promo_txt'])
            st.session_state['promo_url'] = st.text_input("Lien", st.session_state['promo_url'])

# --- HEADER APP ---
st.markdown(f'<a href="{st.session_state["promo_url"]}" class="promo-banner">{st.session_state["promo_txt"]}</a>', unsafe_allow_html=True)

tab_live, tab_prono, tab_yesterday = st.tabs(["🎮 LIVE", "📈 PRONOS", "📚 HISTORIQUE"])

def fetch(p):
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try: return requests.get("https://v3.football.api-sports.io/fixtures", headers=headers, params=p).json().get('response', [])
    except: return []

# --- 1. ONGLET LIVE ---
with tab_live:
    st_autorefresh(interval=60000, key="refresh")
    lives = fetch({'live': 'all'})
    if not lives: st.info("Attente de matchs en direct...")
    for m in lives:
        st.markdown(f"""
        <div class="match-card">
            <div style="font-size:0.7em; color:#888;">{m['league']['name']} • <span class="live-dot">● {m['fixture']['status']['elapsed']}'</span></div>
            <div class="team-row">
                <div class="team-info"><img src="{m['teams']['home']['logo']}" class="team-logo"><span class="team-name">{m['teams']['home']['name']}</span></div>
                <div class="score">{m['goals']['home']}</div>
            </div>
            <div class="team-row">
                <div class="team-info"><img src="{m['teams']['away']['logo']}" class="team-logo"><span class="team-name">{m['teams']['away']['name']}</span></div>
                <div class="score">{m['goals']['away']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- 2. ONGLET PRONOS (1X2, Over, BTTS) ---
with tab_prono:
    fixtures = fetch({'date': datetime.now().strftime('%Y-%m-%d')})
    for f in fixtures:
        if f['fixture']['status']['short'] in ['NS', 'TBD']:
            w, d, l, ov, bt = get_ai_prediction(1.6, 1.3) # Simulé
            st.markdown(f"""
            <div class="match-card">
                <div style="font-size:0.7em; color:#888; margin-bottom:8px;">{f['league']['name']} • {f['fixture']['date'][11:16]}</div>
                <div class="team-row"><div class="team-info"><img src="{f['teams']['home']['logo']}" class="team-logo"><span class="team-name">{f['teams']['home']['name']}</span></div></div>
                <div class="team-row"><div class="team-info"><img src="{f['teams']['away']['logo']}" class="team-logo"><span class="team-name">{f['teams']['away']['name']}</span></div></div>
                <div class="market-container">
                    <div class="market-badge">1X2: {w}|{d}|{l}</div>
                    <div class="market-badge">+2.5: {ov}</div>
                    <div class="market-badge">BTTS: {bt}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- 3. HISTORIQUE ---
with tab_yesterday:
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    past = fetch({'date': yesterday})
    for p in past[:20]: # Limité aux 20 premiers
        st.markdown(f"""
        <div class="match-card" style="opacity:0.8;">
            <div class="team-row">
                <span class="team-name" style="font-size:0.8em;">{p['teams']['home']['name']} {p['goals']['home']} - {p['goals']['away']} {p['teams']['away']['name']}</span>
                <span style="color:#00ff88; font-size:0.8em;">FINI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
