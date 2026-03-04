import streamlit as st
import requests
from datetime import datetime
import numpy as np
from scipy.stats import poisson
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BET PRO", layout="wide", initial_sidebar_state="collapsed")
tz = pytz.timezone("Africa/Bujumbura")
date_now = datetime.now(tz).strftime("%Y-%m-%d")

API_KEY_RAPID = "80da65258a3809f6c7ad2c74930ceb90"
FOOTBALL_DATA_KEY = "A6ef05d939bb4da9acae3d8de8c47c8c"

# --- STYLE CSS AVANCÉ (Look Premium Dark) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [data-testid="stapp-root"] { font-family: 'Roboto', sans-serif; background-color: #0e1117; }
    
    .main-card {
        background: linear-gradient(145deg, #1e1e26, #14141b);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        border: 1px solid #2d2d3a;
        transition: 0.3s;
    }
    .main-card:hover { border-color: #00ff88; }
    
    .league-header { color: #888; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; margin-bottom: 8px; }
    .team-line { display: flex; justify-content: space-between; align-items: center; margin: 4px 0; }
    .team-name { font-weight: 500; font-size: 1rem; color: #efefef; }
    .score-live { color: #00ff88; font-weight: bold; font-size: 1.1rem; }
    
    .prob-badge {
        background: #262730;
        color: #00ff88;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: bold;
        border: 1px solid #3e414b;
        margin-right: 4px;
    }
    .prediction-tag { color: #ffca28; font-size: 0.8rem; font-weight: bold; margin-top: 10px; display: block; }
    .status-badge { background: #ff4b4b; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; }
</style>
""", unsafe_allow_html=True)

# --- LOGIQUE IA (Probabilités Poisson) ---
def get_predictions(h_avg=1.6, a_avg=1.2):
    # Simulation simplifiée basée sur des moyennes historiques
    h_probs = [poisson.pmf(i, h_avg) for i in range(5)]
    a_probs = [poisson.pmf(i, a_avg) for i in range(5)]
    m = np.outer(h_probs, a_probs)
    
    home_w = np.sum(np.tril(m, -1))
    draw = np.sum(np.diag(m))
    away_w = np.sum(np.triu(m, 1))
    
    over25 = 1 - (m[0,0]+m[0,1]+m[0,2]+m[1,0]+m[1,1]+m[2,0])
    btts = (1 - h_probs[0]) * (1 - a_probs[0])
    
    return {
        "1X2": [f"{home_w:.0%}", f"{draw:.0%}", f"{away_w:.0%}"],
        "O25": f"{over25:.0%}",
        "BTTS": f"{btts:.0%}",
        "Advice": "1X & Over 1.5" if home_w > 0.45 else "X2 & Under 3.5"
    }

# --- FONCTIONS DATA ---
@st.cache_data(ttl=300)
def fetch_all_football():
    # On tente API-Football d'abord
    url = f"https://v3.football.api-sports.io/fixtures?date={date_now}"
    headers = {"x-rapidapi-key": API_KEY_RAPID, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        r = requests.get(url, headers=headers, timeout=8).json()
        if r.get("response"): return r["response"], "APIF"
    except: pass
    
    # Fallback Football-Data.org
    url2 = "https://api.football-data.org/v4/matches"
    headers2 = {"X-Auth-Token": FOOTBALL_DATA_KEY}
    try:
        r2 = requests.get(url2, headers=headers2, timeout=8).json()
        return r2.get("matches", []), "FDOrg"
    except: return [], "None"

# --- INTERFACE ---
st.title("🛡️ AI-BET PREDICTOR PRO")

tab1, tab2, tab3 = st.tabs(["⚽ FOOTBALL", "🏀 BASKET", "📺 VIDEOS"])

with tab1:
    matches, source = fetch_all_football()
    
    if not matches:
        st.error("⚠️ Quotas API épuisés. Réessayez demain.")
    else:
        for m in matches[:30]:
            # Normalisation des données selon la source
            if source == "APIF":
                h_name, a_name = m['teams']['home']['name'], m['teams']['away']['name']
                h_logo, a_logo = m['teams']['home']['logo'], m['teams']['away']['logo']
                h_score, a_score = m['goals']['home'], m['goals']['away']
                league = m['league']['name']
                status = m['fixture']['status']['short']
                elapsed = m['fixture']['status']['elapsed']
            else:
                h_name, a_name = m['homeTeam']['name'], m['awayTeam']['name']
                h_logo, a_logo = "", ""
                h_score, a_score = m['score']['fullTime']['home'], m['score']['fullTime']['away']
                league = m['competition']['name']
                status = m['status']
                elapsed = ""

            # Calcul des prédictions IA
            preds = get_predictions()

            # Affichage de la carte de match
            with st.container():
                st.markdown(f"""
                <div class="main-card">
                    <div class="league-header">{league} • {status} {f"({elapsed}')" if elapsed else ""}</div>
                    <div class="team-line">
                        <span class="team-name"><img src="{h_logo}" width="20"> {h_name}</span>
                        <span class="score-live">{h_score if h_score is not None else "-"}</span>
                    </div>
                    <div class="team-line">
                        <span class="team-name"><img src="{a_logo}" width="20"> {a_name}</span>
                        <span class="score-live">{a_score if a_score is not None else "-"}</span>
                    </div>
                    <div style="margin-top:12px; display:flex; flex-wrap:wrap; gap:5px;">
                        <span class="prob-badge">1X2: {preds['1X2'][0]} | {preds['1X2'][1]} | {preds['1X2'][2]}</span>
                        <span class="prob-badge">Over 2.5: {preds['O25']}</span>
                        <span class="prob-badge">BTTS: {preds['BTTS']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Détails au clic
                with st.expander("🔍 Analyse & Double Chance"):
                    col_a, col_b = st.columns(2)
                    col_a.metric("Victoire Domicile (1)", preds['1X2'][0])
                    col_b.metric("Double Chance", "1X" if "1X" in preds['Advice'] else "X2")
                    st.write(f"💡 **Conseil Expert :** {preds['Advice']}")
                    st.progress(int(preds['O25'].replace('%','')), text=f"Probabilité Over 2.5 : {preds['O25']}")

# --- BASKET ET VIDEOS (Codes simplifiés pour la démo) ---
with tab2:
    st.info("🏀 Analyse NBA & Euroleague disponible en mode Premium.")

with tab3:
    st.subheader("📺 Résumés Vidéos ScoreBat")
    # (Insérer ici ton code ScoreBat précédent)
