import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np
from scipy.stats import poisson
import os

# ====================== CONFIGURATION ======================
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Tunga25721204301")
API_KEY = os.getenv("API_FOOTBALL_KEY", "80da65258a3809f6c7ad2c74930ceb90")

tz = pytz.timezone("Africa/Bujumbura")

if 'mode' not in st.session_state:
    st.session_state.mode = "Client"
if st.session_state.mode == "Client":
    st_autorefresh(interval=90 * 1000, key="refresh")

st.set_page_config(page_title="AI-BET • Livescore & Pronos", layout="wide")

# Style
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

# Sidebar
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
            if pwd: st.error("Mot de passe incorrect")
    else:
        st.session_state.mode = "Client"

    show_tomorrow = st.checkbox("Demain", value=False)

# Poisson
def get_poisson_proba(home, away):
    lambda_home = 1.8
    lambda_away = 1.3

    MAX_GOALS = 6
    matrix = np.outer(poisson.pmf(np.arange(MAX_GOALS+1), lambda_home),
                      poisson.pmf(np.arange(MAX_GOALS+1), lambda_away))

    p1 = np.sum(np.tril(matrix, -1)) * 100
    px = np.sum(np.diag(matrix)) * 100
    p2 = np.sum(np.triu(matrix, 1)) * 100
    over25 = (1 - sum(np.diag(matrix, k).sum() for k in range(-2, 3))) * 100

    return {
        "1": round(p1, 1),
        "X": round(px, 1),
        "2": round(p2, 1),
        "Over2.5": round(over25, 1)
    }

# ====================== FETCH MATCHS - 3 SOURCES GRATUITES ======================
@st.cache_data(ttl=60, show_spinner="Chargement des matchs...")
def fetch_fixtures(date_str):
    # 1. TheSportsDB (priorité 1 - très large couverture)
    try:
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={date_str}"
        r = requests.get(url, timeout=10).json()
        events = r.get("events", [])
        fixtures = []
        for e in events:
            fixtures.append({
                "fixture": {
                    "id": e.get("idEvent"),
                    "date": e.get("dateEvent") + "T" + e.get("strTime", "00:00:00"),
                    "status": {"short": "NS" if e.get("strStatus") == "Not Started" else "FT"}
                },
                "teams": {
                    "home": {"name": e.get("strHomeTeam")},
                    "away": {"name": e.get("strAwayTeam")}
                },
                "goals": {"home": e.get("intHomeScore"), "away": e.get("intAwayScore")}
            })
        if fixtures:
            return fixtures
    except:
        pass

    # 2. Football-Data.org (priorité 2)
    try:
        url = f"https://api.football-data.org/v4/matches?date={date_str}"
        headers = {"X-Auth-Token": "votre_clé_football_data"}  # gratuit après inscription
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            return r.json().get("matches", [])
    except:
        pass

    # 3. API-Football (priorité 3 - ta clé actuelle)
    try:
        url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}
        r = requests.get(url, headers=headers, timeout=8).json()
        if not r.get("errors"):
            return r.get("response", [])
    except:
        pass

    st.warning("Aucune source de données disponible aujourd'hui.")
    return []

# ====================== AFFICHAGE ======================
if st.session_state.mode == "Admin":
    st.subheader("Panel Admin - Prono")
    mid = st.text_input("ID Match")
    p = st.selectbox("Prono", ["1", "X", "2"])
    if st.button("Enregistrer"):
        if mid:
            if 'pronos' not in st.session_state: st.session_state.pronos = {}
            st.session_state.pronos[mid] = {"p": p}
            st.success("Prono enregistré")
else:
    st.markdown("<h3 style='text-align:center; color:#1A73E8;'>AI-BET LIVESCORE & PRONOS</h3>", unsafe_allow_html=True)

    target = datetime.now(tz).date()
    if show_tomorrow: target += timedelta(days=1)
    date_str = target.strftime("%Y-%m-%d")

    fixtures = fetch_fixtures(date_str)

    if not fixtures:
        st.info(f"Aucun match trouvé pour le {date_str}")
    else:
        for group, title in [
            ([m for m in fixtures if m.get('fixture', {}).get('status', {}).get('short') in ['1H','HT','2H']], "En direct"),
            ([m for m in fixtures if m.get('fixture', {}).get('status', {}).get('short') == 'NS'], "À venir"),
            ([m for m in fixtures if m.get('fixture', {}).get('status', {}).get('short') == 'FT'], "Terminés")
        ]:
            if group:
                st.subheader(title)
                for m in sorted(group, key=lambda x: x.get('fixture', {}).get('date', '')):
                    fid = str(m.get('fixture', {}).get('id', ''))
                    h = m.get('teams', {}).get('home', {}).get('name', 'Unknown')
                    a = m.get('teams', {}).get('away', {}).get('name', 'Unknown')
                    sh = m.get('goals', {}).get('home', '-')
                    sa = m.get('goals', {}).get('away', '-')
                    stt = m.get('fixture', {}).get('status', {}).get('short', 'NS')
                    el = m.get('fixture', {}).get('status', {}).get('elapsed', '')

                    dt = datetime.fromisoformat(str(m.get('fixture', {}).get('date', '2026-01-01T00:00:00')).replace("Z", "+00:00")).astimezone(tz)
                    heure = dt.strftime("%H:%M")
                    jour = dt.strftime("%d/%m")

                    bord = "wait-border"
                    prono_html = ""
                    if fid in st.session_state.get('pronos', {}):
                        pr = st.session_state.pronos[fid]['p']
                        prono_html = f"<div class='proba-box'>{pr}</div>"
                        if stt == "FT":
                            res = "1" if sh > sa else ("2" if sa > sh else "X")
                            bord = "win-border" if pr == res else "loss-border"

                    proba_html = ""
                    if stt == "NS" and not prono_html:
                        proba = get_poisson_proba(h, a)
                        p1 = proba["1"]
                        px = proba["X"]
                        p2 = proba["2"]
                        o25 = proba["Over2.5"]
                        proba_html = f"""
                        <div style="display:flex; gap:6px; margin-top:6px;">
                            <div class='proba-box proba-1'>{p1}%</div>
                            <div class='proba-box proba-x'>{px}%</div>
                            <div class='proba-box proba-2'>{p2}%</div>
                            <div class='proba-box'>O2.5 {o25}%</div>
                        </div>
                        """

                    stat_disp = f"{el}'" if el else stt
                    stat_cls = "status-live" if stt in ['1H','HT','2H'] else "status-fin"

                    st.markdown(f"""
                    <div class="match-card {bord}">
                        <div class="time-col">
                            <div class="time">{heure}</div>
                            <div style="font-size:0.8rem; color:#666;">{jour}</div>
                        </div>
                        <div style="min-width:40px; text-align:center; font-weight:bold;" class="{stat_cls}">
                            {stat_disp}
                        </div>
                        <div class="teams">
                            <div class="team-row"><span class="team-name">{h}</span><span class="score">{sh}</span></div>
                            <div class="team-row"><span class="team-name">{a}</span><span class="score">{sa}</span></div>
                            {proba_html}
                        </div>
                        {prono_html}
                    </div>
                    """, unsafe_allow_html=True)
