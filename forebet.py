from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import numpy as np
from scipy.stats import poisson

app = FastAPI(title="Forebet-like Poisson API")

@app.get("/predict")
def predict(
    league: str = Query("E0", description="Code ligue ex: E0 Premier League"),
    home: str = Query(..., description="Équipe domicile"),
    away: str = Query(..., description="Équipe extérieur")
):
    try:
        # Lambda fictives pour test rapide (remplace par ton vrai calcul avec données historiques)
        lambda_home = 1.8  # buts attendus domicile
        lambda_away = 1.3  # buts attendus extérieur

        MAX_GOALS = 6
        matrix = np.outer(poisson.pmf(np.arange(MAX_GOALS+1), lambda_home),
                          poisson.pmf(np.arange(MAX_GOALS+1), lambda_away))

        # Probabilités marchés
        p_home = np.sum(np.tril(matrix, -1)) * 100  # Victoire domicile
        p_draw = np.sum(np.diag(matrix)) * 100      # Nul
        p_away = np.sum(np.triu(matrix, 1)) * 100   # Victoire extérieur
        over_25 = (1 - sum(np.diag(matrix, k).sum() for k in range(-2, 3))) * 100

        return {
            "match": f"{home} vs {away}",
            "probabilities": {
                "1": round(p_home, 1),
                "X": round(p_draw, 1),
                "2": round(p_away, 1)
            },
            "over_2_5": round(over_25, 1)
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
