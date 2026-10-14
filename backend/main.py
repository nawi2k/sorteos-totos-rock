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
            raise HTTPException(status_code=400, detail="Enlace de Instagram no válido.")
        
        shortcode = match.group(1)
        media_id = str(shortcode_a_media_id(shortcode))

        rapid_url = "https://instagram-api-fast-reliable-data-scraper.p.rapidapi.com/comments"
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "instagram-api-fast-reliable-data-scraper.p.rapidapi.com"
        }

        usuarios_dict = {}
        cursor = None
        
        # Bucle para recorrer todas las páginas de comentarios
        for _ in range(50):  # Hasta 2500 comentarios
            params = {"id": media_id, "code_or_id_or_url": shortcode}
            if cursor:
                params["min_id"] = cursor
                params["pagination_token"] = cursor

            response = requests.get(rapid_url, headers=headers, params=params, timeout=15)
            if response.status_code != 200:
                break

            data_json = response.json()
            
            # Extraer lista de comentarios buscando en todas las claves posibles
            comments_list = (
                data_json.get("comments") or 
                data_json.get("data") or 
                data_json.get("items") or []
            )

            if not isinstance(comments_list, list) or len(comments_list) == 0:
                break

            nuevos_agregados = 0
            for c in comments_list:
                if isinstance(c, dict):
                    user_info = c.get("user") or c.get("owner") or {}
                    username = user_info.get("username")
                    pic_url = user_info.get("profile_pic_url") or ""

                    if username:
                        u_clean = username.lower().strip()
                        if u_clean not in usuarios_dict:
                            usuarios_dict[u_clean] = pic_url
                            nuevos_agregados += 1

            # Obtener el puntero para avanzar a la siguiente página
            next_cursor = (
                data_json.get("next_min_id") or 
                data_json.get("pagination_token") or 
                data_json.get("min_id") or
                data_json.get("next_cursor")
            )

            # Si no hay más cursor o no se sumaron comentarios nuevos, frenar
            if not next_cursor or next_cursor == cursor or nuevos_agregados == 0:
                break
            
            cursor = next_cursor

        if not usuarios_dict:
            raise HTTPException(status_code=400, detail="No se encontraron comentarios en la publicación.")

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
        raise HTTPException(status_code=400, detail=f"Error al procesar la publicación: {str(e)}")