import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_autorefresh import st_autorefresh

# ────────────────────────────────────────────────
# CONFIGURATION (tout sensible vient de secrets)
# ────────────────────────────────────────────────
st.set_page_config(page_title="AI-BET • Livescore + Pronos", layout="wide")

# Récupération sécurisée des secrets
API_KEY = st.secrets["api"].get("API_FOOTBALL_KEY", "")
FASTAPI_URL = st.secrets["api"].get("FASTAPI_URL", "")
ADMIN_PWD = st.secrets["general"].get("ADMIN_PASSWORD", "")

# Vérification rapide (optionnel : affiche un warning si manquant)
if not API_KEY:
    st.warning("Clé API-Football manquante dans secrets.toml → pas de matchs chargés")
if not ADMIN_PWD:
    st.warning("Mot de passe admin manquant dans secrets.toml → mode admin désactivé")
if not FASTAPI_URL:
    st.info("Backend FastAPI non configuré → pas de probabilités AI affichées")

# Timezone Burundi
tz = pytz.timezone("Africa/Bujumbura")

# Refresh modéré (90s) seulement en mode client
if 'mode' not in st.session_state:
    st.session_state.mode = "Client"
if st.session_state.mode == "Client":
    st_autorefresh(interval=90 * 1000, key="data_refresh")

# Style (inchangé, juste rappel)
st.markdown("""
<style>
    .stApp { background: #f8f9fa; }
    .match-card { background: white; border-radius: 8px; padding: 12px; margin-bottom: 12px;
                  box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: flex; align-items: center; gap: 12px; }
    .time-col { min-width: 70px; text-align: center; font-weight: bold; }
    .time { font-size: 1.1rem; }
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
    .win-border { border-left: 5px solid #28a745; }
    .loss-border { border-left: 5px solid #dc3545; }
    .wait-border { border-left: 5px solid #ffc107; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────
with st.sidebar:
    st.header("AI-BET")
    toggle_admin = st.toggle("Mode Admin")

    if toggle_admin:
        pwd_input = st.text_input("Mot de passe Admin", type="password")
        if pwd_input == ADMIN_PWD:
            st.session_state.mode = "Admin"
            st.success("Mode Admin activé")
        else:
            st.session_state.mode = "Client"
            if pwd_input:
                st.error("Mot de passe incorrect")
    else:
        st.session_state.mode = "Client"

    show_tomorrow = st.checkbox("Afficher matchs de demain", value=False)

# ────────────────────────────────────────────────
# FONCTIONS (inchangées sauf utilisation de secrets)
# ────────────────────────────────────────────────
@st.cache_data(ttl=60, show_spinner="Chargement...")
def fetch_fixtures(date_str):
    if not API_KEY:
        return []
    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}
    try:
        resp = requests.get(url, headers=headers, timeout=8).json()
        return resp.get("response", []) if not resp.get("errors") else []
    except:
        return []

def get_proba_from_backend(home, away, league_code="E0"):
    if not FASTAPI_URL:
        return None
    try:
        r = requests.get(FASTAPI_URL, params={"league": league_code, "home": home, "away": away}, timeout=6)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# ────────────────────────────────────────────────
# AFFICHAGE (le reste est identique à la version précédente)
# ────────────────────────────────────────────────
if st.session_state.mode == "Admin":
    st.subheader("Panel Admin - Ajouter Prono")
    col1, col2, col3 = st.columns([3,2,1])
    with col1: match_id = st.text_input("ID du match (fixture.id)")
    with col2: prono = st.selectbox("Prono AI", ["1", "X", "2"])
    if st.button("Enregistrer Prono"):
        if match_id:
            if 'pronos' not in st.session_state: st.session_state.pronos = {}
            st.session_state.pronos[match_id] = {"p": prono}
            st.success(f"Prono {prono} pour {match_id}")
        else:
            st.warning("ID match requis")
else:
    st.markdown("<h3 style='text-align:center; color:#1A73E8;'>AI-LIVESCORE & PRONOS</h3>", unsafe_allow_html=True)

    target_date = datetime.now(tz).date()
    if show_tomorrow: target_date += timedelta(days=1)
    date_str = target_date.strftime("%Y-%m-%d")

    fixtures = fetch_fixtures(date_str)

    if not fixtures:
        st.info(f"Aucun match ou problème API pour {date_str}")
    else:
        live = [m for m in fixtures if m['fixture']['status']['short'] in ['1H','HT','2H']]
        coming = [m for m in fixtures if m['fixture']['status']['short'] == 'NS']
        finished = [m for m in fixtures if m['fixture']['status']['short'] == 'FT']

        for group, title in [(live, "⚽ En direct"), (coming, "À venir"), (finished, "Terminés")]:
            if group:
                st.subheader(title)
                for m in sorted(group, key=lambda x: x['fixture']['date']):
                    fid = str(m['fixture']['id'])
                    home = m['teams']['home']['name']
                    away = m['teams']['away']['name']
                    score_h = m['goals']['home'] if m['goals']['home'] is not None else "-"
                    score_a = m['goals']['away'] if m['goals']['away'] is not None else "-"
                    status = m['fixture']['status']['short']
                    elapsed = m['fixture']['status']['elapsed'] or ""

                    dt = datetime.fromisoformat(m['fixture']['date'].replace("Z", "+00:00")).astimezone(tz)
                    time_str = dt.strftime("%H:%M")
                    date_short = dt.strftime("%d/%m")

                    prono = ""
                    border_class = "wait-border"
                    if fid in st.session_state.get('pronos', {}):
                        p = st.session_state.pronos[fid]['p']
                        prono = f"<div class='proba-box'>{p}</div>"
                        if status == "FT":
                            res = "1" if score_h > score_a else ("2" if score_a > score_h else "X")
                            border_class = "win-border" if p == res else "loss-border"

                    proba_html = ""
                    if status == "NS" and not prono:
                        proba = get_proba_from_backend(home, away)
                        if proba:
                            p1, px, p2 = proba['1X2']['1'], proba['1X2']['X'], proba['1X2']['2']
                            over, btts = proba['Over2.5'], proba['BTTS']
                            proba_html = f"""
                            <div style="display:flex; gap:6px; margin-top:6px;">
                                <div class='proba-box proba-1'>{p1}%</div>
                                <div class='proba-box proba-x'>{px}%</div>
                                <div class='proba-box proba-2'>{p2}%</div>
                                <div class='proba-box'>O2.5 {over}%</div>
                                <div class='proba-box'>BTTS {btts}%</div>
                            </div>
                            """

                    status_disp = f"{elapsed}'" if elapsed else status
                    status_class = "status-live" if status in ['1H','HT','2H'] else "status-fin"

                    st.markdown(f"""
                    <div class="match-card {border_class}">
                        <div class="time-col">
                            <div class="time">{time_str}</div>
                            <div style="font-size:0.8rem; color:#666;">{date_short}</div>
                        </div>
                        <div style="min-width:40px; text-align:center; font-weight:bold;" class="{status_class}">
                            {status_disp}
                        </div>
                        <div class="teams">
                            <div class="team-row"><span class="team-name">{home}</span><span class="score">{score_h}</span></div>
                            <div class="team-row"><span class="team-name">{away}</span><span class="score">{score_a}</span></div>
                            {proba_html}
                        </div>
                        {prono}
                    </div>
                    """, unsafe_allow_html=True)
