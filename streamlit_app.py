import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np
from scipy.stats import poisson
import sqlite3
import os

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(page_title="AI-BETTING PRO", layout="wide")

tz = pytz.timezone("Africa/Bujumbura")
def get_fixtures(date_str):
    return [
        {
            "fixture": {
                "id": "1",
                "date": "2026-06-06T18:00:00Z",
                "status": {"short": "NS"}
            },
            "teams": {
                "home": {"name": "FC Alpha"},
                "away": {"name": "FC Beta"}
            },
            "goals": {"home": None, "away": None}
        },
        {
            "fixture": {
                "id": "2",
                "date": "2026-06-06T20:00:00Z",
                "status": {"short": "NS"}
            },
            "teams": {
                "home": {"name": "Real Test"},
                "away": {"name": "AI United"}
            },
            "goals": {"home": None, "away": None}
        }
    ]

# ─────────────────────────────
# CACHE SESSION (anti quota)
# ─────────────────────────────
if "cache" not in st.session_state:
    st.session_state.cache = {}

# ─────────────────────────────
# AUTO REFRESH SAFE
# ─────────────────────────────
st_autorefresh(interval=90 * 1000, key="refresh")

# ─────────────────────────────
# SQLITE SIMPLE (dans même fichier)
# ─────────────────────────────
def init_db():
    conn = sqlite3.connect("ai-bet.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        id TEXT PRIMARY KEY,
        home TEXT,
        away TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_match(mid, home, away, date):
    conn = sqlite3.connect("ai-bet.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO matches VALUES (?, ?, ?, ?)
    """, (mid, home, away, date))

    conn.commit()
    conn.close()

init_db()

# ─────────────────────────────
# STYLE (inchangé simple)
# ─────────────────────────────
st.markdown("""
<style>
.match {
    background: white;
    padding: 12px;
    margin: 10px 0;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}
.team { font-weight: 600; }
.score { font-weight: 800; }
.box {
    padding: 4px 8px;
    background: #e9f5ff;
    border-radius: 6px;
    font-size: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# POISSON MODEL (base)
# ─────────────────────────────
def poisson_model():
    home_lambda = 1.6
    away_lambda = 1.2

    max_g = 6

    h = poisson.pmf(np.arange(max_g), home_lambda)
    a = poisson.pmf(np.arange(max_g), away_lambda)

    m = np.outer(h, a)

    p1 = np.sum(np.tril(m, -1)) * 100
    px = np.sum(np.diag(m)) * 100
    p2 = np.sum(np.triu(m, 1)) * 100
    over25 = (1 - np.sum(m[:3, :3])) * 100

    return {
        "1": round(p1, 1),
        "X": round(px, 1),
        "2": round(p2, 1),
        "O2.5": round(over25, 1)
    }

# ─────────────────────────────
# API SAFE + CACHE + ANTI QUOTA
# ─────────────────────────────
@st.cache_data(ttl=300)
def get_fixtures(date_str):

    if date_str in st.session_state.cache:
        return st.session_state.cache[date_str]

    if not API_KEY:
        return []

    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        fixtures = data.get("response", [])

        st.session_state.cache[date_str] = fixtures

        return fixtures

    except:
        return []

# ─────────────────────────────
# UI
# ─────────────────────────────
st.title("⚽ AI-BETTING PRO")

show_tomorrow = st.sidebar.checkbox("Demain")

date = datetime.now(tz).date()
if show_tomorrow:
    date += timedelta(days=1)

date_str = date.strftime("%Y-%m-%d")

# ─────────────────────────────
# DATA LOAD
# ─────────────────────────────
fixtures = get_fixtures(date_str)

if not fixtures:
    st.warning("Aucun match ou API indisponible")
else:

    for m in fixtures[:20]:

        mid = str(m["fixture"]["id"])

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        hg = m["goals"]["home"]
        ag = m["goals"]["away"]

        status = m["fixture"]["status"]["short"]

        dt = datetime.fromisoformat(
            m["fixture"]["date"].replace("Z", "+00:00")
        ).astimezone(tz)

        time = dt.strftime("%H:%M")

        # SAVE INTO DB (silencieux)
        save_match(mid, home, away, m["fixture"]["date"])

        st.markdown(f"""
        <div class="match">
            <div>{time} | {status}</div>
            <div class="team">{home} vs {away}</div>
            <div class="score">{hg} - {ag}</div>
        </div>
        """, unsafe_allow_html=True)

        if status == "NS":
            p = poisson_model()

            st.markdown(f"""
            <div style="display:flex; gap:6px;">
                <div class="box">1 {p['1']}%</div>
                <div class="box">X {p['X']}%</div>
                <div class="box">2 {p['2']}%</div>
                <div class="box">O2.5 {p['O2.5']}%</div>
            </div>
            """, unsafe_allow_html=True)
