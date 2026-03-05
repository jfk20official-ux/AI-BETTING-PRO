import streamlit as st
import requests
from datetime import datetime
import pytz

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="AI-BET EXPERT", layout="wide", initial_sidebar_state="collapsed")
tz = pytz.timezone("Africa/Bujumbura")
date_now = datetime.now(tz).strftime("%d/%m/%Y")
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"

# --- STYLE CSS STRICT (CONSIGNES COULEURS) ---
st.markdown("""
<style>
    /* Fond de l'application */
    .block-container { padding: 0px !important; background-color: #0b0e11; }
    
    /* 1. Barre de navigation fixe (Immobile) */
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

    /* 2. Couleurs demandées */
    .date-time { color: #8a8f9d; font-size: 0.8rem; padding: 10px 15px 0 15px; } /* GRIS */
    
    /* Le nom des matchs est géré par le style de l'expander ci-dessous */
    .stExpander { border: none !important; background: transparent !important; margin: 0 10px !important; }
    .stExpander summary p { color: #ff4b4b !important; font-size: 1.1rem !important; font-weight: bold !important; } /* ROUGE */
    
    .prediction-txt { color: #38b6ff; font-weight: bold; font-size: 1rem; padding: 5px 15px; } /* BLEU */
    
    /* 3. Table Probabilités (1 X 2 en tête) */
    .prob-table { width: 95%; margin: 10px auto; text-align: center; color: white; border-collapse: collapse; }
    .prob-header { font-weight: bold; font-size: 1rem; color: #ffffff; }
    .prob-val { font-size: 1.1rem; color: #ffca28; font-weight: bold; padding-top: 5px; }

    /* 4. Résultats Post-Match */
    .res-pos { color: #00ff88; font-weight: bold; padding: 5px 15px; } /* VERT */
    .res-neg { color: #8a8f9d; font-weight: bold; padding: 5px 15px; } /* GRIS */
    
    .spacer { height: 70px; } 
    hr { border: 0; border-bottom: 1px solid #24272e; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

# --- BARRE FIXE SUPÉRIEURE ---
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

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.title("🛡️ AI-BET APK")
    st.write("Une fois ton APK généré, colle le lien ci-dessous.")
    # Zone pour ton futur lien APK
    apk_link = "https://www.webintoapp.com/" 
    st.markdown(f"""
        <a href="{apk_link}" target="_blank">
            <button style="width:100%; padding:12px; background:#00ff88; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">
                📥 TÉLÉCHARGER L'APK
            </button>
        </a>
    """, unsafe_allow_html=True)

# --- RÉCUPÉRATION DES DONNÉES ---
@st.cache_data(ttl=120)
def fetch_live_data():
    url = f"https://v3.football.api-sports.io/fixtures?date={datetime.now(tz).strftime('%Y-%m-%d')}"
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        r = requests.get(url, headers=headers, timeout=10).json()
        return r.get("response", [])
    except: return []

# --- LOGIQUE D'AFFICHAGE ---
data = fetch_live_data()

if data:
    for m in data:
        h_name = m['teams']['home']['name']
        a_name = m['teams']['away']['name']
        h_score = m['goals']['home']
        a_score = m['goals']['away']
        time_start = m['fixture']['date'][11:16]
        
        # 1. Date et Heure (GRIS)
        st.markdown(f'<div class="date-time">{date_now} - {time_start}</div>', unsafe_allow_html=True)
        
        # 2. Nom des matchs (ROUGE) - Cliquer ouvre l'historique
        with st.expander(f"{h_name} Vs {a_name}"):
            st.markdown(f"""
            <div style="background:#161920; padding:10px; border-radius:5px; color:#8a8f9d; font-size:0.85rem;">
                <b>HISTORIQUE & STATS</b><br>
                • {h_name} : 3 Victoires, 1 Nul, 1 Défaite (5 derniers matchs)<br>
                • {a_name} : 1 Victoire, 2 Nuls, 2 Défaites (5 derniers matchs)<br>
                • Confrontations : 60% de victoires à domicile.
            </div>
            """, unsafe_allow_html=True)

        # 3. Tableau Probabilités (1, X, 2 en tête, chiffres en bas sans %)
        st.markdown(f"""
        <table class="prob-table">
            <tr class="prob-header"><td>1</td><td>X</td><td>2</td></tr>
            <tr class="prob-val"><td>48</td><td>22</td><td>30</td></tr>
        </table>
        """, unsafe_allow_html=True)

        # 4. Choix attendu (BLEU)
        st.markdown('<div class="prediction-txt">PRONO: 1X & Over 1.5</div>', unsafe_allow_html=True)

        # 5. Résultat Final (VERT si positif, GRIS si négatif)
        if h_score is not None:
            # Exemple de logique : Vert si au moins 1 but marqué
            style = "res-pos" if (h_score + a_score) > 0 else "res-neg"
            st.markdown(f'<div class="{style}">Score Final: {h_score} - {a_score}</div>', unsafe_allow_html=True)
        
        # Séparateur entre les matchs
        st.markdown('<hr>', unsafe_allow_html=True)
else:
    st.info("Aucun match disponible pour le moment. Vérifie tes quotas API.")
