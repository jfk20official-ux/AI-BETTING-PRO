import streamlit as st
from datetime import datetime
import pytz
import numpy as np
from scipy.stats import poisson
from streamlit_autorefresh import st_autorefresh

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(page_title="AI-BETTING PRO", layout="wide")
tz = pytz.timezone("Africa/Bujumbura")

# auto refresh
st_autorefresh(interval=90 * 1000, key="refresh")

# ─────────────────────────────
# STYLE
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
.title {
    text-align:center;
    font-size:28px;
    font-weight:800;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# TITLE
# ─────────────────────────────
st.markdown("<div class='title'>⚽ AI-BETTING PRO</div>", unsafe_allow_html=True)

# ─────────────────────────────
# FAKE MATCHES (SAFE DATA)
# ─────────────────────────────
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
# POISSON MODEL
# ─────────────────────────────
def poisson_model():
    home_lambda = 1.6
    away_lambda = 1.2

    max_g = 6
    h = poisson.pmf(np.arange(max_g), home_lambda)
    a = poisson.pmf(np.arange(max_g), away_lambda)

    matrix = np.outer(h, a)

    p1 = np.sum(np.tril(matrix, -1)) * 100
    px = np.sum(np.diag(matrix)) * 100
    p2 = np.sum(np.triu(matrix, 1)) * 100
    over25 = (1 - np.sum(matrix[:3, :3])) * 100

    return {
        "1": round(p1, 1),
        "X": round(px, 1),
        "2": round(p2, 1),
        "O2.5": round(over25, 1)
    }

# ─────────────────────────────
# LOAD FIXTURES
# ─────────────────────────────
date_str = datetime.now(tz).strftime("%Y-%m-%d")
fixtures = get_fixtures(date_str)

# ─────────────────────────────
# DISPLAY
# ─────────────────────────────
if not fixtures:
    st.warning("Aucun match disponible")
else:
    for m in fixtures:

        mid = m["fixture"]["id"]
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        hg = m["goals"]["home"]
        ag = m["goals"]["away"]

        status = m["fixture"]["status"]["short"]

        st.markdown(f"""
        <div class="match">
            <div>{status}</div>
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
