import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURATION LEGERE ---
st.set_page_config(page_title="AI-BET", layout="centered")
st_autorefresh(interval=30 * 1000, key="eco_refresh")

# --- PARAMÈTRES ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
PWD_ADMIN = "Tunga25721204301"

if 'pronos' not in st.session_state: st.session_state.pronos = {}
if 'mode' not in st.session_state: st.session_state.mode = "Client"

# --- STYLE COMPATIBLE ANCIENS ANDROID ---
st.markdown("""
    <style>
    .stApp { background-color: #EBF0F5; }
    .m-card {
        background: white; padding: 6px 10px; margin-bottom: 2px;
        display: flex; align-items: center; border-radius: 2px;
        font-family: sans-serif; border-bottom: 1px solid #DDD;
    }
    .m-date { color: #444; font-size: 9px; width: 60px; font-weight: bold; }
    .m-status { width: 35px; text-align: center; font-size: 10px; font-weight: bold; }
    .live { color: #FF0000; }
    .fin { color: #555; }
    .teams-area { flex-grow: 1; margin-left: 8px; border-left: 1px solid #EEE; padding-left: 8px; }
    .team { color: #1A73E8; font-weight: 800; font-size: 13px; display: flex; justify-content: space-between; }
    .score { color: #000; font-weight: 900; }
    .ai-box {
        background: #FFD700; color: #000; font-weight: 900;
        padding: 1px 5px; border-radius: 3px; font-size: 12px;
        min-width: 25px; text-align: center; margin-left: 10px;
    }
    .win { border-right: 5px solid #28A745; }
    .loss { border-right: 5px solid #DC3545; }
    .wait { border-right: 5px solid #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# --- RECUPERATION DATA ---
@st.cache_data(ttl=20)
def get_data():
    t = datetime.now().strftime("%Y-%m-%d")
    u = f"https://v3.football.api-sports.io/fixtures?date={t}"
    h = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        r = requests.get(u, headers=h, timeout=5).json().get('response', [])
        return sorted(r, key=lambda x: (0 if x['fixture']['status']['short']=='FT' else (1 if x['fixture']['status']['short'] in ['1H','2H','HT'] else 2)))
    except: return []

# --- DOUBLE FACE ---
with st.sidebar:
    if st.toggle("ADMIN"):
        if st.text_input("Pass", type="password") == PWD_ADMIN: st.session_state.mode = "Admin"
    else: st.session_state.mode = "Client"

# --- INTERFACE ---
if st.session_state.mode == "Admin":
    st.subheader("⚙️ Panel")
    m_id = st.text_input("ID Match")
    m_p = st.selectbox("Prono", ["1", "X", "2"])
    if st.button("OK"):
        st.session_state.pronos[m_id] = {"p": m_p}
        st.success("Posté")
else:
    st.markdown("<h4 style='text-align:center;color:#1A73E8;'>AI-LIVESCORE</h4>", unsafe_allow_html=True)
    data = get_data()
    for m in data:
        mid = str(m['fixture']['id'])
        h, a = m['teams']['home']['name'], m['teams']['away']['name']
        hs = m['goals']['home'] if m['goals']['home'] is not None else "0"
        as_ = m['goals']['away'] if m['goals']['away'] is not None else "0"
        st_s = m['fixture']['status']['short']
        
        # Date Heure
        dt = datetime.fromisoformat(m['fixture']['date'].replace('Z', '+00:00'))
        d_s, t_s = dt.strftime("%d/%m"), dt.strftime("%H:%M")
        
        # Style Status
        disp = f"{m['fixture']['status']['elapsed']}'" if st_s in ['1H','2H'] else st_s
        cl = "live" if st_s in ['1H','2H','HT'] else "fin"
        
        # IA & Bordure
        ai_h, b_c = "", "wait"
        if mid in st.session_state.pronos:
            p = st.session_state.pronos[mid]['p']
            if st_s == "FT":
                res = "1" if m['goals']['home'] > m['goals']['away'] else ("2" if m['goals']['away'] > m['goals']['home'] else "X")
                b_c = "win" if p == res else "loss"
            ai_h = f"<div class='ai-box'>{p}</div>"

        st.markdown(f"""
        <div class="m-card {b_c}">
            <div class="m-date">{d_s}<br>{t_s}</div>
            <div class="m-status {cl}">{disp}</div>
            <div class="teams-area">
                <div class="team"><span>{h[:12]}</span><span class="score">{hs}</span></div>
                <div class="team"><span>{a[:12]}</span><span class="score">{as_}</span></div>
            </div>
            {ai_h}
        </div>
        """, unsafe_allow_html=True)
