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

def shortcode_a_media_id(shortcode: str) -> int:
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    media_id = 0
    for char in shortcode:
        media_id = (media_id * 64) + alphabet.index(char)
    return media_id

@app.post("/api/obtener-participantes")
def obtener_participantes(data: SorteoRequest):
    try:
        url = data.post_url.strip()
        match = re.search(r'/(?:p|reel|tv)/([^/?#&]+)', url)
        if not match:
            raise HTTPException(status_code=400, detail="Enlace no válido.")
        
        shortcode = match.group(1)
        media_id = str(shortcode_a_media_id(shortcode))

        rapid_url = "https://instagram-api-fast-reliable-data-scraper.p.rapidapi.com/comments"
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "instagram-api-fast-reliable-data-scraper.p.rapidapi.com"
        }

        # Estructura: dict con clave de usuario y valor su foto de perfil
        usuarios_dict = {} 
        min_id = None
        max_paginas = 25  # Limite para evitar bucles infinitos (hasta ~500 comentarios)

        for _ in range(max_paginas):
            params = {"id": media_id}
            if min_id:
                params["min_id"] = min_id

            response = requests.get(rapid_url, headers=headers, params=params, timeout=15)
            if response.status_code != 200:
                break

            data_json = response.json()
            comments_list = data_json.get("comments", []) or []

            if not comments_list:
                break

            for c in comments_list:
                if isinstance(c, dict):
                    user_info = c.get("user", {})
                    username = user_info.get("username") or c.get("owner", {}).get("username")
                    pic_url = user_info.get("profile_pic_url") or c.get("owner", {}).get("profile_pic_url") or ""

                    if username:
                        u_clean = username.lower()
                        if u_clean not in usuarios_dict:
                            usuarios_dict[u_clean] = pic_url

            # Actualizar el cursor para la siguiente página
            min_id = data_json.get("next_min_id") or data_json.get("has_more_headload_comments")
            if not min_id or not data_json.get("has_more_headload_comments", True):
                break

        if not usuarios_dict:
            raise HTTPException(status_code=400, detail="No se encontraron comentarios.")

        # Armar lista estructurada para el frontend
        participantes_lista = [
            {"username": u, "profile_pic": pic} 
            for u, pic in sorted(usuarios_dict.items())
        ]

        return {
            "exito": True,
            "total_unicos": len(participantes_lista),
            "participantes": participantes_lista
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")