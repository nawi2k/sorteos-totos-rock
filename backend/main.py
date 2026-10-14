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

        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "instagram-api-fast-reliable-data-scraper.p.rapidapi.com"
        }

        usuarios_dict = {}
        
        # Probamos primero el endpoint de comentarios extendidos pasándole el link completo y el shortcode
        urls_a_probar = [
            ("https://instagram-api-fast-reliable-data-scraper.p.rapidapi.com/comments", {"id": media_id, "count": "500"}),
            ("https://instagram-api-fast-reliable-data-scraper.p.rapidapi.com/comments", {"code_or_id_or_url": f"https://www.instagram.com/p/{shortcode}/"}),
        ]

        for rapid_url, params in urls_a_probar:
            response = requests.get(rapid_url, headers=headers, params=params, timeout=20)
            if response.status_code == 200:
                data_json = response.json()
                
                # Extraer comentarios
                comments_list = data_json.get("comments") or data_json.get("data") or data_json.get("items") or []
                if isinstance(comments_list, list) and len(comments_list) > 0:
                    for c in comments_list:
                        if isinstance(c, dict):
                            user_info = c.get("user") or c.get("owner") or {}
                            username = user_info.get("username")
                            pic_url = user_info.get("profile_pic_url") or ""

                            if username:
                                u_clean = username.lower().strip()
                                if u_clean not in usuarios_dict:
                                    usuarios_dict[u_clean] = pic_url
                    
                    # Si ya logramos extraer más de los 12-13 iniciales, cortamos la búsqueda
                    if len(usuarios_dict) > 15:
                        break

        if not usuarios_dict:
            raise HTTPException(status_code=400, detail="No se pudieron obtener los comentarios de la publicación.")

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