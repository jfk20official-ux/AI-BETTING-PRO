@st.cache_data(ttl=60, show_spinner="Chargement des matchs...")
def fetch_fixtures(date_str):
    if not API_KEY:
        st.error("Clé API manquante")
        return []
    
    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "v3.football.api-sports.io"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("errors"):
            st.error(f"Erreur API : {data['errors']}")
            return []
        return data.get("response", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur connexion API : {e}")
        return []
    except Exception as e:
        st.error(f"Erreur inattendue : {e}")
        return []
