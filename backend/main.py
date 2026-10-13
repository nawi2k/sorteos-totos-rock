from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import re

app = FastAPI(title="API Sorteos Totos Rock")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clave de RapidAPI
RAPIDAPI_KEY = "ae9598b9c1msh1f0b6e5de81ab67p119a6bjsn2e84c4d02364"

class SorteoRequest(BaseModel):
    post_url: str

@app.post("/api/obtener-participantes")
def obtener_participantes(data: SorteoRequest):
    try:
        url = data.post_url.strip()
        
        # Extraer el shortcode de la publicación
        match = re.search(r'/(?:p|reel|tv)/([^/?#&]+)', url)
        if not match:
            raise HTTPException(
                status_code=400, 
                detail="El enlace no tiene un formato válido de Instagram."
            )
        
        code_or_id = match.group(1)

        rapid_url = "https://instagram-api-fast-reliable-data-scraper.p.rapidapi.com/post_comments"
        
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "instagram-api-fast-reliable-data-scraper.p.rapidapi.com"
        }
        
        params = {"code_or_id_or_url": code_or_id}

        response = requests.get(rapid_url, headers=headers, params=params, timeout=15)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=400, 
                detail="Error al consultar los comentarios. Verificá que la publicación sea pública."
            )

        data_json = response.json()
        comments_list = data_json.get("comments", [])

        usuarios_unicos = set()
        for c in comments_list:
            user_info = c.get("user", {})
            username = user_info.get("username")
            if username:
                usuarios_unicos.add(username.lower())

        if not usuarios_unicos:
            raise HTTPException(
                status_code=400, 
                detail="No se encontraron comentarios en esta publicación."
            )

        return {
            "exito": True,
            "total_unicos": len(usuarios_unicos),
            "participantes": sorted(list(usuarios_unicos))
        }

    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error al procesar la publicación: {str(e)}"
        )