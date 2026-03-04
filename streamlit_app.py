import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
import numpy as np
from scipy.stats import poisson
import os

# ====================== CONFIGURATION DES CLÉS ======================
# Liste de clés pour éviter les pannes de quota
API_KEYS = [
    os.getenv("API_FOOTBALL_KEY", "80da65258a3809f6c7ad2c74930ceb90"),
    "MET_ICI_TA_DEUXIEME_CLE", # Ajoute tes autres clés ici
    "MET_ICI_TA_TROISIEME_CLE"
]

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Tunga25721204301")
tz = pytz.timezone("Africa/Bujumbura")

# ====================== FONCTION FETCH AVEC BASCULEMENT ======================
@st.cache_data(ttl=60)
def fetch_fixtures_multi_key(date_str):
    """Essaie chaque clé une par une si la précédente échoue."""
    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"
    
    for key in API_KEYS:
        if not key or key.startswith("MET_ICI"): 
            continue
            
        headers = {"x-rapidapi-key": key, "x-rapidapi-host": "v3.football.api-sports.io"}
        try:
            response = requests.get(url, headers=headers, timeout=8)
            data = response.json()
            
            # Si pas d'erreurs de quota ou de clé
            if not data.get("errors"):
                return data.get("response", [])
            else:
                # Si erreur de quota (Rate limit), on passe à la clé suivante
                continue 
        except:
            continue # En cas de timeout ou crash, on essaie la clé suivante
            
    return [] # Si aucune clé ne fonctionne

# ====================== LOGIQUE DE PRÉDICTION ======================
def get_poisson_proba(home, away):
    # On garde tes moyennes de base
    l_h, l_a = 1.8, 1.3
    MAX_GOALS = 6
    matrix = np.outer(poisson.pmf(np.arange(MAX_GOALS+1), l_h),
                      poisson.pmf(np.arange(MAX_GOALS+1), l_a))

    p1 = np.sum(np.tril(matrix, -1)) * 100
    px = np.sum(np.diag(matrix)) * 100
    p2 = np.sum(np.triu(matrix, 1)) * 100
    over25 = (1 - sum(np.diag(matrix, k).sum() for k in range(-2, 3))) * 100
    btts = (1 - matrix[0,0] - sum(matrix[i,0] for i in range(1, MAX_GOALS+1)) - sum(matrix[0,j] for j in range(1, MAX_GOALS+1))) * 100

    return {
        "1X2": {"1": round(p1, 1), "X": round(px, 1), "2": round(p2, 1)},
        "Over2.5": round(over25, 1), "BTTS": round(btts, 1)
    }

# ====================== INTERFACE STREAMLIT ======================
st.set_page_config(page_title="AI-BET PRO", layout="wide")

# (Je simplifie ici pour la lisibilité, garde tes dictionnaires de langues)
tabs = st.tabs(["Livescore", "Predictions", "Statistics"])

with tabs[0]:
    target = datetime.now(tz).date()
    date_str = target.strftime("%Y-%m-%d")
    
    # Appel de la nouvelle fonction multi-clés
    fixtures = fetch_fixtures_multi_key(date_str)

    if not fixtures:
        st.warning("⚠️ Toutes les API sont actuellement saturées. Réessayez plus tard.")
    else:
        # Tri des matchs par statut
        live_matches = [m for m in fixtures if m['fixture']['status']['short'] in ['1H','HT','2H']]
        upcoming = [m for m in fixtures if m['fixture']['status']['short'] == 'NS']
        
        if live_matches:
            st.subheader("🔴 En Direct")
            for m in live_matches:
                st.write(f"{m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}")
        
        if upcoming:
            st.subheader("📅 À venir")
            for m in upcoming[:10]:
                st.write(f"{m['teams']['home']['name']} vs {m['teams']['away']['name']}")

with tabs[1]:
    st.subheader("Prédictions IA")
    if fixtures:
        for m in [m for m in fixtures if m['fixture']['status']['short'] == 'NS'][:10]:
            p = get_poisson_proba(m['teams']['home']['name'], m['teams']['away']['name'])
            st.info(f"**{m['teams']['home']['name']} vs {m['teams']['away']['name']}**\n\n1X2: {p['1X2']['1']}% | {p['1X2']['X']}% | {p['1X2']['2']}%")
