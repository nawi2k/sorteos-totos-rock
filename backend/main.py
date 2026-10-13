from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import instaloader

app = FastAPI(title="API Sorteos Totos Rock")

# Permitir solicitudes desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

L = instaloader.Instaloader()

class SorteoRequest(BaseModel):
    post_url: str

@app.post("/api/obtener-participantes")
def obtener_participantes(data: SorteoRequest):
    try:
        # Extraer shortcode del enlace de Instagram
        # Ejemplo: https://www.instagram.com/p/C123456/ -> C123456
        url = data.post_url.strip().rstrip('/')
        shortcode = url.split('/')[-1] if '/p/' in url else url.split('/')[-2]

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Guardar en un Set para garantizar 1 solo intento por usuario
        usuarios_unicos = set()
        
        for comment in post.get_comments():
            usuarios_unicos.add(comment.owner.username)

        return {
            "exito": True,
            "total_unicos": len(usuarios_unicos),
            "participantes": list(usuarios_unicos)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la publicación: {str(e)}")