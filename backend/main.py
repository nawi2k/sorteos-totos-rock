from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import instaloader
import re

app = FastAPI(title="API Sorteos Totos Rock")

# Permitir solicitudes CORS desde cualquier origen (Vercel, Localhost, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar Instaloader con un User-Agent personalizado para evitar bloqueos
L = instaloader.Instaloader()
L.context._session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

class SorteoRequest(BaseModel):
    post_url: str

@app.post("/api/obtener-participantes")
def obtener_participantes(data: SorteoRequest):
    try:
        url = data.post_url.strip()
        
        # Expresión regular para extraer solo el código único del post/reel (ej: DeXqzynCesU)
        # Ignora cualquier parámetro como ?obrf=... o &igsh=...
        match = re.search(r'/(?:p|reel|tv)/([^/?#&]+)', url)
        
        if not match:
            raise HTTPException(
                status_code=400, 
                detail="El enlace ingresado no tiene un formato válido de publicación o reel de Instagram."
            )
        
        shortcode = match.group(1)

        # Descargar la publicación mediante el shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Usamos un Set en Python para garantizar 1 solo intento por usuario (elimina duplicados)
        usuarios_unicos = set()
        
        for comment in post.get_comments():
            if comment.owner and comment.owner.username:
                usuarios_unicos.add(comment.owner.username.lower())

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