import streamlit as st
import requests
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURATION PRIVÉE
# ==========================================
API_KEY = "80da65258a3809f6c7ad2c74930ceb90" 
ADMIN_PASSWORD = "Tunga25721204301"
WHATSAPP_LINK = "https://wa.me/TON_NUMERO"
PROMO_CODE_ACTIF = "JFK20" 

# Simulation de base de données interne (Seul l'Admin y accède)
if 'matchs_valides' not in st.session_state:
    st.session_state['matchs_valides'] = [
        {"sport": "⚽ Foot", "equipes": "Real Madrid vs Man City", "predic": "Win 1", "confiance": 97},
        {"sport": "🏀 Basket", "equipes": "Lakers vs Celtics", "predic": "Win 2 (Total +220)", "confiance": 94}
    ]

# ==========================================
# 2. STYLE
# ==========================================
st.set_page_config(page_title="L'Oracle AI", layout="wide")
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Segoe UI'; font-size: 14px; color: #e0e0e0; }
    .gold-glow { color: #D4AF37; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.6); }
    .vip-card { border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; margin-bottom:10px; background: rgba(212, 175, 55, 0.05); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background: rgba(14,17,23,0.9); color: #555; text-align: center; padding: 5px; font-size: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. NAVIGATION
# ==========================================
st.sidebar.markdown("<h1 class='gold-glow'>L'ORACLE AI</h1>", unsafe_allow_html=True)
menu = ["🏠 Accueil", "💎 ESPACE VIP (95%)", "🎁 Promo", "📩 Contact", "🔐 Admin"]
choice = st.sidebar.selectbox("Menu", menu)

# --- ACCUEIL ---
if choice == "🏠 Accueil":
    st.image("https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?q=80&w=500")
    st.markdown("<h2 class='gold-glow'>Système de Prédiction Mondial</h2>", unsafe_allow_html=True)
    st.write("Analyses sportives par intelligence artificielle. Fiabilité garantie.")

# --- ESPACE VIP (CE QUE LE CLIENT VOIT) ---
elif choice == "💎 ESPACE VIP (95%)":
    st.markdown("<h2 class='gold-glow'>💎 Zone Premium</h2>", unsafe_allow_html=True)
    code_vip = st.sidebar.text_input("Clé VIP", type="password")
    
    if code_vip:
        st.success("✅ Accès VIP Activé")
        for m in st.session_state['matchs_valides']:
            st.markdown(f"""
            <div class='vip-card'>
                <h4>{m['sport']} : {m['equipes']}</h4>
                <p>🎯 Pronostic : <b>{m['predic']}</b></p>
                <p style='color:#D4AF37;'>⭐ Fiabilité : <b>Certification 95% +</b></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Veuillez entrer votre clé VIP.")

# --- PROMO ---
elif choice == "🎁 Promo":
    cp = st.text_input("Code Promo", type="password").upper()
    if cp == PROMO_CODE_ACTIF:
        st.info("Accès d'essai limité débloqué.")

# --- ADMIN (CE QUE TOI SEUL VOIS) ---
elif choice == "🔐 Admin":
    psw = st.text_input("Code Maître", type="password")
    if psw == ADMIN_PASSWORD:
        st.success("Bienvenue, Maître de l'Oracle.")
        st.markdown("### 🛠️ Gestion des Pronostics & Précision Réelle")
        
        for i, m in enumerate(st.session_state['matchs_valides']):
            col1, col2, col3 = st.columns([2, 2, 1])
            col1.write(f"**{m['equipes']}**")
            # C'est ici que tu vois le pourcentage réel que les autres ne voient pas
            col2.write(f"📊 Précision réelle : **{m['confiance']}%**")
            if col3.button(f"Supprimer", key=f"del_{i}"):
                st.session_state['matchs_valides'].pop(i)
                st.rerun()
        
        st.divider()
        st.markdown("#### Ajouter un nouveau match certifié")
        with st.form("new_match"):
            s = st.selectbox("Sport", ["⚽ Foot", "🏀 Basket"])
            eq = st.text_input("Match (ex: Lakers vs Celtics)")
            pr = st.text_input("Pronostic (ex: Win 2)")
            conf = st.slider("Ta confiance réelle (%)", 90, 100, 95)
            if st.form_submit_button("Publier au VIP"):
                st.session_state['matchs_valides'].append({"sport": s, "equipes": eq, "predic": pr, "confiance": conf})
                st.success("Match publié avec succès !")
                st.rerun()

# --- FOOTER ---
st.markdown("""<div class="footer">L'Oracle AI v2.7 | © 2026 | All Rights Reserved</div>""", unsafe_allow_html=True)
