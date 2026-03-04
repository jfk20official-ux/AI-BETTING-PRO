with tab_live:
    lives = fetch({'live': 'all'})
    
    # --- MATCH DE TEST (S'affichera toujours) ---
    st.markdown("""
        <div class="match-card">
            <div style="font-size:0.7em; color:#888; margin-bottom:5px;">🏆 TEST LEAGUE • <span class="live-badge">● 45'</span></div>
            <div class="team-row">
                <div class="team-info"><span>🏠 Equipe Test</span></div>
                <div class="score-live">2</div>
            </div>
            <div class="team-row">
                <div class="team-info"><span>🚀 Equipe IA</span></div>
                <div class="score-live">1</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if not lives:
        st.info("En attente des données réelles de l'API...")
