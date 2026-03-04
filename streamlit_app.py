import streamlit as st
import requests
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import poisson

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="AI ScoreCast Pro", layout="wide", initial_sidebar_state="collapsed")

# --- 2. IDENTIFIANTS ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
BASE_URL = "https://v3.football.api-sports.io/fixtures"

# --- 3. STYLE CSS (Look Application Pro) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .match-card { background-color: #1a1c23; border: 1px solid #2d2f39; padding: 12px; border-radius: 12px; margin-bottom: 10px; }
    .team-row { display: flex; justify-content: space-between; align-items: center; margin: 5px 0; }
    .team-info { display: flex; align-items: center; gap: 10px; color: white; }
    .team-logo { width: 22px; height: 22px; }
    .score-live { color: #00ff88; font-weight: bold; font-size: 1.2em; }
    .live-badge { color: white; background-color: #ff4b4b; padding: 2px 6px; border-radius: 4px; font-size: 0.7em; font-weight: bold; }
    .market-badge { background-color: #262932; color: #00ff88; padding: 4px 8px; border-radius: 6px; font-size: 0.75em; font-weight: bold; border: 1px solid #3e414b; margin-top: 8px; display: inline-block; }
    header, footer, #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. FONCTIONS TECHNIQUES ---
def fetch(params):
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        return response.json().get('response', [])
    except:
        return []

def get_ai_prediction():
    # Algorithme de Poisson (Simulé avec moyennes standards)
    h_avg, a_avg = 1.6, 1.2
    h_p = [poisson.pmf(i, h_avg) for i in range(6)]
    a_p = [poisson.pmf(i, a_avg) for i in range(6)]
    m = np.outer(h_p, a_p)
    w, d, l = np.sum(np.tril(m, -1)), np.sum(np.diag(m)), np.sum(np.triu(m, 1))
    ov25 = 1 - (m[0,0]+m[0,1]+m[0,2]+m[1,0]+m[1,1]+m[2,0])
    bt = (1-h_p[0]) * (1-a_p[0])
    return f"{w*100:.0f}%", f"{d*100:.0f}%", f"{l*100:.0f}%", f"{ov25*100:.0f}%", f"{bt*100:.0f}%"

# --- 5. INTERFACE PRINCIPALE ---
st.title("⚽ AI ScoreCast Pro")

tab_live, tab_prono = st.tabs(["🔴 LIVE", "📈 PRONOSTICS"])

# --- SECTION LIVE ---
with tab_live:
    lives = fetch({'live': 'all'})
    if lives:
        for m in lives:
            st.markdown(f"""
            <div class="match-card">
                <div style="font-size:0.7em; color:#888; margin-bottom:5px;">{m['league']['name']} • <span class="live-badge">● {m['fixture']['status']['elapsed']}'</span></div>
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
    else:
        st.info("Aucun match en direct. Consultez les pronostics ci-dessous.")
        # Optionnel : On peut afficher un message encourageant à aller voir l'onglet Pronos

# --- SECTION PRONOSTICS ---
with tab_prono:
    fixtures = fetch({'date': datetime.now().strftime('%Y-%m-%d')})
    # On filtre pour ne garder que les matchs qui n'ont pas encore commencé
    upcoming = [f for f in fixtures if f['fixture']['status']['short'] in ['NS', 'TBD']]
    
    if not upcoming:
        st.write("Pas de nouveaux matchs prévus pour aujourd'hui.")
    else:
        for f in upcoming[:20]: # Affiche les 20 prochains
            w, d, l, ov, bt = get_ai_prediction()
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
