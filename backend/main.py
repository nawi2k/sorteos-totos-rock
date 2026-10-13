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

RAPIDAPI_KEY = "ae9598b9c1msh1f0b6e5de81ab67p119a6bjsn2e84c4d02364"

class SorteoRequest(BaseModel):
    post_url: str

@app.post("/api/obtener-participantes")
def obtener_participantes(data: SorteoRequest):
    try:
        url = data.post_url.strip()
        
        # Extraer el shortcode limpio borrando todo lo que haya antes y después
        # Ejemplo: https://www.instagram.com/p/DeXqzynCesU/?obrf=... -> DeXqzynCesU
        match = re.search(r'/(?:p|reel|tv)/([^/?#&]+)', url)
        if not match:
            raise HTTPException(
                status_code=400, 
                detail="El enlace ingresado no tiene un formato válido de Instagram."
            )
        
        shortcode = match.group(1)

        rapid_url = "https://instagram-api-fast-reliable-data-scraper.p.rapidapi.com/post_comments"
        
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "instagram-api-fast-reliable-data-scraper.p.rapidapi.com"
        }
        
        params = {"code_or_id_or_url": shortcode}

        response = requests.get(rapid_url, headers=headers, params=params, timeout=20)
        
        if response.status_code != 200:
            # Si RapidAPI devuelve error, mostramos qué respuesta dio exactamente
            msg_error = response.text
            try:
                err_json = response.json()
                msg_error = err_json.get("message") or err_json.get("detail") or response.text
            except:
                pass
            raise HTTPException(
                status_code=400, 
                detail=f"Error en RapidAPI ({response.status_code}): {msg_error}"
            )

        data_json = response.json()
        
        # Obtener lista de comentarios
        comments_list = data_json.get("comments", []) or data_json.get("data", [])

        usuarios_unicos = set()
        for c in comments_list:
            if isinstance(c, dict):
                user_info = c.get("user", {})
                username = user_info.get("username") or c.get("owner", {}).get("username")
                if username:
                    usuarios_unicos.add(username.lower())

        if not usuarios_unicos:
            raise HTTPException(
                status_code=400, 
                detail="No se encontraron comentarios en la publicación."
            )

        return {
            "exito": True,
            "total_unicos": len(usuarios_unicos),
            "participantes": sorted(list(usuarios_unicos))
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error al procesar la publicación: {str(e)}"
        )