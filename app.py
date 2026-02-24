import streamlit as st
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURATION LEGERE ---
st.set_page_config(page_title="aiprobet", layout="centered")
st_autorefresh(interval=30 * 1000, key="aipro_refresh")

# --- PARAMÈTRES ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
PWD_ADMIN = "Tunga25721204301"

if 'pronos' not in st.session_state: st.session_state.pronos = {}
if 'mode' not in st.session_state: st.session_state.mode = "Client"

# --- STYLE COMPACT & CADRES INVISIBLES ---
st.markdown("""
    <style>
    .stApp { background-color: #F4F7F9; }
    /* Titre Ligue */
    .league-header { 
        background: #FFF; padding: 4px 10px; margin: 10px 0 2px 0;
        font-size: 11px; font-weight: bold; color: #555;
        border-bottom: 1px solid #EEE; display: flex; align-items: center;
    }
    /* Cadre Match quasi invisible */
    .m-card {
        background: white; padding: 6px 10px; margin-bottom: 1px;
        display: flex; align-items: center; font-family: sans-serif;
    }
    .m-time { color: #888; font-size: 9px; width: 45px; text-align: center; }
    .m-status { width: 30px; text-align: center; font-size: 9px; font-weight: bold; }
    .live { color: #FF0000; }
    .teams-area { flex-grow: 1; margin-left: 10px; border-left: 1px solid #F9F9F9; padding-left: 10px; }
    .team { color: #1A73E8; font-weight: 700; font-size: 13px; display: flex; justify-content: space-between; }
    .score { color: #000; font-weight: 900; }
    .ai-box {
        background: #FFD700; color: #000; font-weight: 900;
        padding: 2px 6px; border-radius: 3px; font-size: 12px;
        min-width: 25px; text-align: center; margin-left: 10px;
    }
    .win { border-right: 4px solid #28A745; }
    .loss { border-right: 4px solid #DC3545; }
    .wait { border-right: 4px solid #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# --- RECUPERATION DATA (GROUPÉE PAR LIGUE) ---
@st.cache_data(ttl=20)
def get_grouped_data():
    t = datetime.now().strftime("%Y-%m-%d")
    u = f"https://v3.football.api-sports.io/fixtures?date={t}"
    h = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        r = requests.get(u, headers=h, timeout=5).json().get('response', [])
        # Tri : Finis -> Live -> Venir
        r = sorted(r, key=lambda x: (0 if x['fixture']['status']['short']=='FT' else (1 if x['fixture']['status']['short'] in ['1H','2H','HT'] else 2)))
        
        grouped = {}
        for m in r:
            l_name = f"{m['league']['country']} - {m['league']['name']}"
            if l_name not in grouped: grouped[l_name] = []
            grouped[l_name].append(m)
        return grouped
    except: return {}

# --- DOUBLE FACE ---
with st.sidebar:
    st.write("### aiprobet")
    if st.toggle("ADMIN MODE"):
        if st.text_input("Pass", type="password") == PWD_ADMIN: st.session_state.mode = "Admin"
    else: st.session_state.mode = "Client"

# --- INTERFACE ---
if st.session_state.mode == "Admin":
    st.subheader("⚙️ Panel aiprobet")
    m_id = st.text_input("ID Match")
    m_p = st.selectbox("Prono IA", ["1", "X", "2"])
    if st.button("Valider"):
        st.session_state.pronos[m_id] = {"p": m_p}
        st.success("Pronostic injecté !")
else:
    st.markdown("<h4 style='text-align:center;color:#1A73E8;margin-bottom:0;'>aiprobet</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-size:9px;color:gray;margin-top:0;'>AI PRONOSTICS BET</p>", unsafe_allow_html=True)
    
    # Mode Scroll : On affiche tout dans une seule page
    grouped_data = get_grouped_data()
    
    for league, matches in grouped_data.items():
        # En-tête du championnat avec un petit drapeau symbolique (Emoji)
        st.markdown(f'<div class="league-header">🏆 {league.upper()}</div>', unsafe_allow_html=True)
        
        for m in matches:
            mid = str(m['fixture']['id'])
            h, a = m['teams']['home']['name'], m['teams']['away']['name']
            hs = m['goals']['home'] if m['goals']['home'] is not None else "0"
            as_ = m['goals']['away'] if m['goals']['away'] is not None else "0"
            st_s = m['fixture']['status']['short']
            
            # Heure
            dt = datetime.fromisoformat(m['fixture']['date'].replace('Z', '+00:00'))
            t_s = dt.strftime("%H:%M")
            
            # Status
            disp = f"{m['fixture']['status']['elapsed']}'" if st_s in ['1H','2H'] else st_s
            cl = "live" if st_s in ['1H','2H','HT'] else ""
            
            # IA & Validation
            ai_h, b_c = "", "wait"
            if mid in st.session_state.pronos:
                p = st.session_state.pronos[mid]['p']
                if st_s == "FT":
                    res = "1" if m['goals']['home'] > m['goals']['away'] else ("2" if m['goals']['away'] > m['goals']['home'] else "X")
                    b_c = "win" if p == res else "loss"
                ai_h = f"<div class='ai-box'>{p}</div>"

            st.markdown(f"""
            <div class="m-card {b_c}">
                <div class="m-time">{t_s}</div>
                <div class="m-status {cl}">{disp}</div>
                <div class="teams-area">
                    <div class="team"><span>{h[:15]}</span><span class="score">{hs}</span></div>
                    <div class="team"><span>{a[:15]}</span><span class="score">{as_}</span></div>
                </div>
                {ai_h}
            </div>
            """, unsafe_allow_html=True)
