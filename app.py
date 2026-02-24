import streamlit as st
import requests
import random
import string
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURATION ---
st.set_page_config(page_title="AI-BETTING-PRO", layout="centered")
st_autorefresh(interval=30 * 1000, key="v11_refresh")

# --- PARAMÈTRES ---
API_KEY = "80da65258a3809f6c7ad2c74930ceb90"
PWD_ADMIN = "Tunga25721204301"

if 'pronos' not in st.session_state: st.session_state.pronos = {}
if 'view_mode' not in st.session_state: st.session_state.view_mode = "Client"

# --- DESIGN SYSTEM (STYLE PRO) ---
st.markdown("""
    <style>
    .stApp { background-color: #F9FAFB; }
    .match-card { 
        background: white; padding: 15px; border-radius: 12px; margin-bottom: 10px;
        border: 1px solid #E5E7EB; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
    }
    .team-name { font-weight: 600; font-size: 16px; color: #111827; }
    .score-badge { 
        background: #F3F4F6; color: #D4AF37; font-weight: 800; 
        padding: 4px 10px; border-radius: 6px; font-size: 18px;
    }
    .date-footer { 
        margin-top: 10px; padding-top: 8px; border-top: 1px solid #F3F4F6;
        color: #6B7280; font-size: 12px; display: flex; justify-content: space-between;
    }
    .circle { 
        display: inline-block; width: 28px; height: 28px; line-height: 24px; 
        border-radius: 50%; text-align: center; font-weight: bold; font-size: 14px;
        border: 2px solid;
    }
    .win { border-color: #10B981; color: #10B981; background: #ECFDF5; }
    .loss { border-color: #EF4444; color: #EF4444; background: #FEF2F2; }
    .pending { border-color: #D4AF37; color: #D4AF37; background: #FFFBEB; }
    
    /* Bouton Admin */
    .admin-switch { background: #1F2937; color: white; padding: 10px; border-radius: 8px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE API ---
@st.cache_data(ttl=60)
def fetch_matches():
    # Utilise la date actuelle du système
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    try:
        res = requests.get(url, headers=headers, timeout=5).json().get('response', [])
        return res
    except: return []

# --- BARRE LATÉRALE (LE DOUBLE FACE) ---
st.sidebar.markdown("### 🛡️ CENTRE DE CONTRÔLE")
is_admin_active = st.sidebar.toggle("Mode Maître (Admin)")

if is_admin_active:
    access_code = st.sidebar.text_input("Code Secret", type="password")
    if access_code == PWD_ADMIN:
        st.session_state.view_mode = st.sidebar.segmented_control(
            "CHOISIR LA FACE", ["Admin", "Client"], default="Admin"
        )
    else:
        if access_code: st.sidebar.error("Code incorrect")
        st.session_state.view_mode = "Client"
else:
    st.session_state.view_mode = "Client"

# --- 1. FACE ADMIN (BACK-OFFICE) ---
if st.session_state.view_mode == "Admin":
    st.markdown("<h2 style='color:#1F2937;'>🛠️ Gestion des Pronostics</h2>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.write("Entrez l'ID du match pour lier votre analyse.")
        m_id = st.text_input("ID du Match (ex: 1034221)")
        m_pick = st.selectbox("Votre Prédiction", ["1", "X", "2"])
        if st.button("🚀 PUBLIER MAINTENANT"):
            if m_id:
                st.session_state.pronos[m_id] = {"pick": m_pick}
                st.success(f"Prono '{m_pick}' activé pour le match {m_id}")
            else:
                st.warning("Veuillez entrer un ID de match.")

# --- 2. FACE CLIENT (VITRINE) ---
else:
    st.markdown("<h1 style='text-align:center; color:#111;'>AI-BETTING-PRO</h1>", unsafe_allow_html=True)
    
    data = fetch_matches()
    if not data:
        st.info("Récupération des matchs du jour en cours...")
    
    for m in data[:35]: # Optimisation quota
        mid = str(m['fixture']['id'])
        status = m['fixture']['status']['short']
        h_name, a_name = m['teams']['home']['name'], m['teams']['away']['name']
        h_score = m['goals']['home'] if m['goals']['home'] is not None else "-"
        a_score = m['goals']['away'] if m['goals']['away'] is not None else "-"
        
        # Formatage Date Complète (Jour Mois Année)
        raw_dt = datetime.fromisoformat(m['fixture']['date'].replace('Z', '+00:00'))
        date_full = raw_dt.strftime("%d %B %Y") # ex: 24 Février 2026
        heure_exacte = raw_dt.strftime("%H:%M")

        # Gestion du Prono & Cercle de validation
        prono_display = ""
        if mid in st.session_state.pronos:
            p_val = st.session_state.pronos[mid]['pick']
            c_class = "pending"
            if status == "FT":
                res = "1" if m['goals']['home'] > m['goals']['away'] else ("2" if m['goals']['away'] > m['goals']['home'] else "X")
                c_class = "win" if p_val == res else "loss"
            prono_display = f"<div class='circle {c_class}'>{p_val}</div>"

        # HTML de la Carte
        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="flex-grow:1;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span class="team-name">{h_name}</span>
                        <span class="score-badge">{h_score}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <span class="team-name">{a_name}</span>
                        <span class="score-badge">{a_score}</span>
                    </div>
                </div>
                <div style="margin-left:20px;">{prono_display}</div>
            </div>
            <div class="date-footer">
                <span>📅 {date_full}</span>
                <span>⏰ <b>{heure_exacte}</b> | {status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
