# AI-BET – Livescore & Pronostics Foot

Application Streamlit avec livescore (API-Football), pronos admin et probabilités AI (via backend FastAPI optionnel).

## Installation locale

1. `git clone <ton-repo>`
2. `cd ai-bet-football`
3. `python -m venv .venv`
4. `source .venv/bin/activate`  (Linux/Mac) ou `.venv\Scripts\activate` (Windows)
5. `pip install -r requirements.txt`
6. Crée `.streamlit/secrets.toml` :

```toml
[general]
ADMIN_PASSWORD = "ton_mot_de_passe_secret"

[api]
API_FOOTBALL_KEY = "ta_cle_rapidapi_ici"
FASTAPI_URL = "http://127.0.0.1:8000/predict"   # ou ton URL déployée
