import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np
from scipy.stats import poisson

# --- CONFIGURATION DES SECRETS (Streamlit Cloud) ---
# Allez dans Settings > Secrets sur Streamlit Cloud et collez :
# API_FOOTBALL_KEY = "votre_cle_ici"
# ADMIN_PASSWORD = "votre_password_ici"

try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
    API_KEY = st.secrets["API_FOOTBALL_KEY"]
except:
    # Valeurs de secours si les secrets ne sont pas encore configurés
    ADMIN_PASSWORD = "Tunga25721204301"
    API_KEY = "80da65258a3809f6c7ad2c74930ceb90"

tz = pytz.timezone("Africa/Bujumbura")

# --- REFRESH AUTO ---
if 'mode' not in st.session_state:
    st.session_state.mode = "Client"

if st.session_state.mode == "Client":
    st_autorefresh(interval=90 * 1000, key="refresh")

st.set_page_config(page_title="AiBettingTips • Livescore", layout="wide")

# --- STYLE CSS (Conservé à 100%) ---
st.markdown("""
<style>
    .stApp { background: #f8f9fa; }
    .match-card { background: white; border-radius: 8px; padding: 12px; margin-bottom: 12px;
                  box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: flex; align-items: center; gap: 12px; }
    .time-col { min-width: 70px; text-align: center; font-weight: bold; }
    .status-live { color: #dc3545; font-weight: 900; }
    .status-fin { color: #6c757d; }
    .teams { flex-grow: 1; }
    .team-row { display: flex; justify-content: space-between; font-size: 1rem; margin: 4px 0; }
    .team-name { font-weight: 600; }
    .score { font-weight: 900; min-width: 30px; text-align: center; }
    .proba-box { background: #e9f5ff; border-radius: 6px; padding: 6px 10px;
                 font-weight: bold; font-size: 0.9rem; text-align: center; min-width: 50px; }
    .proba-1 { background: #d4edda; color: #155724; }
    .proba-x { background: #fff3cd; color: #856404; }
    .proba-2 { background: #f8d7da; color: #721c24; }
    .win-border { border-left: 5px solid #28a745 !important; }
    .loss-border { border-left: 5px solid #dc3545 !important; }
    .wait-border { border-left: 5px solid #ffc107 !important; }
</style>
""", unsafe_allow_html=True)

# --- FONCTION PRÉDICTION POISSON (Conservée) ---
def get_poisson_proba(home, away):
    lambda_home, lambda_away = 1.8, 1.3
    MAX_GOALS = 6
    matrix = np.outer(poisson.pmf(np.arange(MAX_GOALS+1), lambda_home),
                      poisson.pmf(np.arange(MAX_GOALS+1), lambda_away))
    p1 = np.sum(np.tril(matrix, -1)) * 100
    px = np.sum(np.diag(matrix)) * 100
    p2 = np.sum(np.triu(matrix, 1)) * 100
    over25 = (1 - (matrix[0,0] + matrix[0,1] + matrix[1,0] + matrix[1,1] + matrix[0,2] + matrix[2,0])) * 100
    return {"1": round(p1, 1), "X": round(px, 1), "2": round(p2, 1), "Over2.5": round(over25, 1)}

# --- API FETCH (Version Stable) ---
@st.cache_data(ttl=60)
def fetch_fixtures(date_str):
    if not API_KEY:
        st.error("Clé API manquante dans les Secrets")
        return []
    
    # URL pour API-SPORTS (RapidAPI)
    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"
    headers = {
        "x-rapidapi-key": API_KEY, 
        "x-rapidapi-host": "v3.football.api-sports.io"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", [])
        else:
            st.error(f"Erreur API {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return []

# --- SIDEBAR (Conservé) ---
with st.sidebar:
    st.header("AI-BET")
    toggle = st.toggle("Mode Admin")
    if toggle:
        pwd = st.text_input("Mot de passe", type="password")
        if pwd == ADMIN_PASSWORD:
            st.session_state.mode = "Admin"
            st.success("Admin OK")
        else:
            st.session_state.mode = "Client"
    else:
        st.session_state.mode = "Client"
    show_tomorrow = st.checkbox("Voir demain", value=False)

# --- INTERFACE PRINCIPALE ---
if st.session_state.mode == "Admin":
    st.subheader("Panel Admin - Prono manuel")
    mid = st.text_input("ID Match (ex: 123456)")
    p = st.selectbox("Prono", ["1", "X", "2"])
    if st.button("Enregistrer le prono"):
        if mid:
            if 'pronos' not in st.session_state: st.session_state.pronos = {}
            st.session_state.pronos[mid] = {"p": p}
            st.success(f"Prono enregistré pour {mid}")
else:
    st.markdown("<h3 style='text-align:center; color:#1A73E8;'>AiBettingTips LIVESCORE</h3>", unsafe_allow_html=True)

    target = datetime.now(tz).date()
    if show_tomorrow: target += timedelta(days=1)
    date_str = target.strftime("%Y-%m-%d")

    fixtures = fetch_fixtures(date_str)

    if not fixtures:
        st.info(f"Aucun match disponible pour le {date_str}. Vérifiez votre clé API ou les matchs du jour.")
    else:
        # Tri des matchs
        live = [m for m in fixtures if m['fixture']['status']['short'] in ['1H','HT','2H']]
        upcoming = [m for m in fixtures if m['fixture']['status']['short'] == 'NS']
        finished = [m for m in fixtures if m['fixture']['status']['short'] == 'FT']

        for group, title in [(live, "🔴 En direct"), (upcoming, "📅 À venir"), (finished, "🏁 Terminés")]:
            if group:
                st.subheader(title)
                for m in sorted(group, key=lambda x: x['fixture']['date']):
                    fid = str(m['fixture']['id'])
                    h, a = m['teams']['home']['name'], m['teams']['away']['name']
                    sh = m['goals']['home'] if m['goals']['home'] is not None else "-"
                    sa = m['goals']['away'] if m['goals']['away'] is not None else "-"
                    stt = m['fixture']['status']['short']
                    el = m['fixture']['status']['elapsed'] or ""

                    # Gestion de l'heure
                    try:
                        dt = datetime.fromisoformat(m['fixture']['date'].replace("Z", "+00:00")).astimezone(tz)
                        heure = dt.strftime("%H:%M")
                    except:
                        heure = "--:--"

                    # Logique de bordure
                    bord = "wait-border"
                    prono_display = ""
                    if fid in st.session_state.get('pronos', {}):
                        pr = st.session_state.pronos[fid]['p']
                        prono_display = f"<div class='proba-box' style='border:1px solid #1A73E8'>Prono: {pr}</div>"
                        if stt == "FT":
                            try:
                                res = "1" if int(sh) > int(sa) else ("2" if int(sa) > int(sh) else "X")
                                bord = "win-border" if pr == res else "loss-border"
                            except: pass

                    # Probabilités auto
                    proba_html = ""
                    if stt == "NS" and not prono_display:
                        probs = get_poisson_proba(h, a)
                        proba_html = f"""
                        <div style="display:flex; gap:6px; margin-top:6px;">
                            <div class='proba-box proba-1'>1: {probs['1']}%</div>
                            <div class='proba-box proba-x'>X: {probs['X']}%</div>
                            <div class='proba-box proba-2'>2: {probs['2']}%</div>
                        </div>
                        """

                    stat_disp = f"{el}'" if stt in ['1H','2H'] else stt
                    stat_cls = "status-live" if stt in ['1H','HT','2H'] else "status-fin"

                    st.markdown(f"""
                    <div class="match-card {bord}">
                        <div class="time-col">
                            <div style="font-size:1.1rem;">{heure}</div>
                        </div>
                        <div style="min-width:50px; text-align:center;" class="{stat_cls}">
                            {stat_disp}
                        </div>
                        <div class="teams">
                            <div class="team-row"><span>{h}</span><b>{sh}</b></div>
                            <div class="team-row"><span>{a}</span><b>{sa}</b></div>
                            {proba_html}
                        </div>
                        {prono_display}
                    </div>
                    """, unsafe_allow_html=True)
