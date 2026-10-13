from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI(title="API Sorteos Totos Rock")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SorteoRequest(BaseModel):
    post_url: str

@app.post("/api/obtener-participantes")
def obtener_participantes(data: SorteoRequest):
    try:
        url = data.post_url.strip()
        
        # Extraer el shortcode (código único de la publicación)
        match = re.search(r'/(?:p|reel|tv)/([^/?#&]+)', url)
        if not match:
            raise HTTPException(
                status_code=400, 
                detail="El enlace no tiene un formato válido de Instagram."
            )
        
        shortcode = match.group(1)

        # Consultar la versión Embed pública de Instagram
        embed_url = f"https://www.instagram.com/p/{shortcode}/embed/captioned/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(embed_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=400, 
                detail="No se pudo acceder a la publicación. Asegurate de que la cuenta sea pública."
            )

        soup = BeautifulSoup(response.text, 'html.parser')
        
        usuarios_unicos = set()

        # Extraer nombres de usuario de las etiquetas de comentarios en el Embed
        for a_tag in soup.find_all('a', class_='CaptionUsername'):
            username = a_tag.get_text(strip=True).lower()
            if username:
                usuarios_unicos.add(username)

        # Búsqueda secundaria por patrón de usuarios de Instagram
        for a_tag in soup.find_all('a'):
            href = a_tag.get('href', '')
            match_user = re.search(r'instagram\.com/([^/?#&]+)', href)
            if match_user:
                user = match_user.group(1).lower()
                if user not in ['p', 'explore', 'reels', 'stories']:
                    usuarios_unicos.add(user)

        if not usuarios_unicos:
            raise HTTPException(
                status_code=400, 
                detail="No se detectaron usuarios o comentarios públicos en esta publicación."
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