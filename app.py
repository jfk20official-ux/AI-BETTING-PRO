st.markdown("""
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#1a3c6d">
    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('sw.js');
            });
        }
    </script>
""", unsafe_allow_html=True)import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration Ultra-Pro
st.set_page_config(page_title="AIBP | THE ORACLE", layout="wide", page_icon="🔮")

# --- DESIGN SUPREME (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background: #000000; color: #ffffff; }
    
    /* Carte Vitrée */
    .card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid #d4af37;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Typographie Or */
    .gold-glow {
        color: #d4af37;
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
        font-family: 'Orbitron', sans-serif;
        text-align: center;
    }
    
    /* Statuts des Matchs */
    .live { color: #ff4b4b; font-weight: bold; animation: blink 1.2s infinite; }
    .ht { color: #00f5d4; font-weight: bold; }
    .ft { color: #888888; font-weight: bold; }
    @keyframes blink { 50% { opacity: 0; } }
    
    /* Footer */
    .footer { font-size: 0.75rem; color: #444; text-align: center; margin-top: 60px; border-top: 1px solid #222; padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION LATERALE ---
with st.sidebar:
    st.markdown("<h2 class='gold-glow'>AIBP GLOBAL</h2>", unsafe_allow_html=True)
    menu = st.radio("SÉLECTION :", ["🌍 LIVES & PRONOS", "📊 CLASSEMENTS", "💎 VIP PREMIUM", "⚙️ ADMIN"])
    st.write("---")
    st.markdown("📧 **SUPPORT OFFICIEL**\njfk20.official@gmail.com")
    if st.button("🔗 PARTAGER L'APP"):
        st.success("Lien prêt à être copié !")

# --- LOGIQUE D'AFFICHAGE ---

if menu == "🌍 LIVES & PRONOS":
    st.markdown("<h1 class='gold-glow'>AIBP : THE ORACLE</h1>", unsafe_allow_html=True)
    
    search = st.text_input("🔍 Scanner une équipe, une ligue ou un statut (Live, FT, Cancelled)...")

    # Base de données simulée Mondiale
    data = [
        {"L": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League", "M": "Arsenal vs Liverpool", "T": "65'", "S": "2-1", "ST": "LIVE", "P": "1", "C": "92%", "R": "1er vs 3ème", "F": "WWWDW"},
        {"L": "🇪🇸 La Liga", "M": "Real Madrid vs Betis", "T": "21:00", "S": "0-0", "ST": "À VENIR", "P": "1", "C": "97%", "R": "2ème vs 7ème", "F": "WWWWW"},
        {"L": "🌍 CAF Champions", "M": "Al Ahly vs TP Mazembe", "T": "HT", "S": "1-0", "ST": "HT", "P": "Over 1.5", "C": "85%", "R": "Phase de Groupes", "F": "WDLWW"},
        {"L": "🇮🇹 Serie A", "M": "Juventus vs Napoli", "T": "FT", "S": "1-1", "ST": "FT", "P": "X", "C": "78%", "R": "4ème vs 6ème", "F": "LDWWW"},
        {"L": "🇩🇪 Bundesliga", "M": "Bayern vs Union Berlin", "T": "-", "S": "-", "ST": "REPORTÉ", "P": "-", "C": "0%", "R": "1er vs 18ème", "F": "-"}
    ]

    for m in data:
        if not search or search.lower() in m['M'].lower() or search.lower() in m['ST'].lower() or search.lower() in m['L'].lower():
            # Style du statut
            st_class = "live" if m['ST'] == "LIVE" else "ht" if m['ST'] == "HT" else "ft"
            
            st.markdown(f"""
            <div class='card'>
                <div style='display:flex; justify-content:space-between; font-size:0.8rem;'>
                    <span style='color:#d4af37;'>{m['L']}</span>
                    <span class='{st_class}'>{m['ST']} {m['T']}</span>
                </div>
                <div style='display:flex; justify-content:space-between; align-items:center; margin:10px 0;'>
                    <span style='font-size:1.2rem; font-weight:bold;'>{m['M']} <span style='color:#d4af37;'>{m['S']}</span></span>
                    <span style='background:rgba(212,175,55,0.2); color:#d4af37; padding:5px 12px; border-radius:8px; font-weight:bold;'>IA: {m['P']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📊 VOIR LES STATISTIQUES ET CLASSEMENT"):
                st.write(f"**Position :** {m['R']}")
                st.write(f"**Forme (5 derniers matchs) :** {m['F']}")
                st.write(f"**Confiance IA :** {m['C']}")
            st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📊 CLASSEMENTS":
    st.markdown("<h1 class='gold-glow'>CLASSEMENTS MONDIAUX</h1>", unsafe_allow_html=True)
    league = st.selectbox("Ligue", ["Premier League", "La Liga", "Serie A", "Ligue 1", "CAF Champions"])
    st.table(pd.DataFrame({'Pos': [1,2,3], 'Club': ['Team A', 'Team B', 'Team C'], 'Pts': [45, 42, 40]}))

elif menu == "💎 VIP PREMIUM":
    st.markdown("<h1 class='gold-glow'>ACCÈS VIP</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card' style='text-align:center;'>🔒 DÉCRYPTAGE REQUIS</div>", unsafe_allow_html=True)
    st.text_input("Clé d'accès", type="password")

elif menu == "⚙️ ADMIN":
    st.markdown("<h1 class='gold-glow'>ADMIN PANEL</h1>", unsafe_allow_html=True)
    if st.text_input("Code Maître", type="password") == "JFK_ADMIN_2024":
        st.metric("UTILISATEURS LIVE", "12,450", "+5%")

# --- FOOTER LEGAL ---
st.markdown("""
    <div class='footer'>
        ALL RIGHTS RESERVED © 2026 AI BETTING PRO - GLOBAL PREDICTION ENGINE<br>
        COPYRIGHT PROTECTED | JFK20 OFFICIAL PARTNER<br>
        Propriété exclusive de AIBP. Toute reproduction est interdite.<br>
        Contact: jfk20.official@gmail.com
    </div>
    """, unsafe_allow_html=True)
