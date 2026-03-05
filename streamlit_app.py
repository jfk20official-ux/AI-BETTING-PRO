import streamlit as st
import requests
from datetime import datetime
import pytz

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BET EXPERT", layout="wide", initial_sidebar_state="collapsed")
tz = pytz.timezone("Africa/Bujumbura")
date_now = datetime.now(tz).strftime("%d/%m/%Y")
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"

# --- STYLE CSS STRICT (Couleurs et Barre Fixe) ---
st.markdown("""
<style>
    .block-container { padding: 0px !important; background-color: #0b0e11; }
    
    /* 1. Barre de navigation fixe */
    .sticky-nav {
        position: fixed; top: 0; width: 100%; z-index: 1000;
        background: #161920; display: flex; overflow-x: auto;
        padding: 12px; gap: 10px; border-bottom: 2px solid #2d3442;
    }
    .nav-btn {
        background: #212630; color: #ffffff; padding: 7px 18px;
        border-radius: 5px; font-weight: bold; font-size: 0.85rem;
        border: 1px solid #3e4451; white-space: nowrap;
    }

    /* 2. Conteneur de Match */
    .match-card { padding: 20px 15px; border-bottom: 1px solid #24272e; margin-top: 5px; }
    
    /* 3. Couleurs demandées */
    .date-time { color: #8a8f9d; font-size: 0.8rem; font-weight: 400; } /* GRIS */
    .team-names { color: #ff4b4b; font-size: 1.1rem; font-weight: bold; cursor: pointer; } /* ROUGE */
    .prediction-txt { color: #38b6ff; font-weight: bold; font-size: 1rem; margin-top: 10px; } /* BLEU */
    
    /* 4. Table Probabilités */
    .prob-table { width: 100%; margin-top: 10px; text-align: center; color: white; border-collapse: collapse; }
    .prob-header { font-weight: bold; font-size: 0.9rem; padding-bottom: 5px; }
    .prob-val { font-size: 1rem; color: #ffca28; font-weight: bold; }

    /* 5. Résultats Post-Match */
    .res-pos { color: #00ff88; font-weight: bold; } /* VERT */
    .res-neg { color: #8a8f9d; font-weight: bold; } /* GRIS */
    
    .spacer { height: 70px; } /* Pour ne pas cacher le premier match sous la barre */
</style>
""", unsafe_allow_html=True)

# --- 1. BARRE FIXE ---
st.markdown("""
<div class="sticky-nav">
    <div class="nav-btn">1X2</div>
    <div class="nav-btn">BTTS</div>
    <div class="nav-btn">Over 2.5</div>
    <div class="nav-btn">VIP</div>
    <div class="nav-btn">JFK20</div>
</div>
<div class="spacer"></div>
""", unsafe_allow_html=True)

# --- FONCTION DATA ---
@st.cache_data(ttl=120)
def fetch_matches():
    url = f"https://v3.football.api-sports.io/fixtures?date={datetime.now(tz).strftime('%Y-%m-%d')}"
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        return requests.get(url, headers=headers, timeout=10).json().get("response", [])
    except: return []

# --- AFFICHAGE ---
data = fetch_matches()

if data:
    for m in data:
        h_name = m['teams']['home']['name']
        a_name = m['teams']['away']['name']
        h_score = m['goals']['home']
        a_score = m['goals']['away']
        time_start = m['fixture']['date'][11:16]
        
        # Simulation de la logique de couleur de résultat
        # Si le score est présent, on définit si c'est positif (vert) ou négatif (gris)
        res_style = "res-pos" if h_score is not None and (h_score + a_score) > 0 else "res-neg"
        
        with st.container():
            # Date et Heure (Gris)
            st.markdown(f'<div class="date-time">{date_now} - {time_start}</div>', unsafe_allow_html=True)
            
            # Nom des matches (Rouge) dans un expander pour l'historique
            with st.expander(f"{h_name} Vs {a_name}", expanded=False):
                st.markdown(f"""
                <div style="background:#0e1117; padding:10px; border-radius:5px; font-size:0.8rem; color:#8a8f9d;">
                    <b>Historique {h_name}:</b> V-N-D-V-V <br>
                    <b>Historique {a_name}:</b> D-V-N-D-N <br>
                    <b>Confrontations directes:</b> 2 Victoires {h_name}, 1 Nul.
                </div>
                """, unsafe_allow_html=True)
            
            # Table Probabilités (Titres en haut, chiffres en bas)
            st.markdown(f"""
            <table class="prob-table">
                <tr class="prob-header"><td>1</td><td>X</td><td>2</td></tr>
                <tr class="prob-val"><td>45</td><td>25</td><td>30</td></tr>
            </table>
            """, unsafe_allow_html=True)
            
            # Choix attendu (Bleu)
            st.markdown('<div class="prediction-txt">PRONO: 1X & Over 1.5</div>', unsafe_allow_html=True)
            
            # Résultat Final (Vert ou Gris)
            if h_score is not None:
                st.markdown(f'<div class="{res_style}">Score Final: {h_score} - {a_score}</div>', unsafe_allow_html=True)
            
            st.markdown('<div style="margin-bottom:20px; border-bottom:1px solid #24272e;"></div>', unsafe_allow_html=True)
else:
    st.info("Chargement des événements...")
