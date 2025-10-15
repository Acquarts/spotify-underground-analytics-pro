from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Importar configuración de base de datos
from .core.database import get_db, create_tables, engine
from .models.genre import Base as GenreBase
from .models.artist import Base as ArtistBase

# Importar routers de API
from .api import genres, artists

# Cargar variables de entorno
load_dotenv()

# Crear app FastAPI
app = FastAPI(
    title="Spotify Analytics API",
    description="API profesional para análisis musical con Spotify - Especializada en géneros underground y comparación de artistas",
    version="1.0.0",
    docs_url="/docs"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers de API
app.include_router(genres.router)
app.include_router(artists.router)

# Cliente Spotify
spotify_client = None

def get_spotify_client():
    """Inicializar cliente de Spotify"""
    global spotify_client
    
    if spotify_client is None:
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            return None
            
        try:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            spotify_client = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager
            )
        except Exception as e:
            print(f"Error inicializando Spotify: {e}")
            return None
    
    return spotify_client

# Evento de startup - crear tablas
@app.on_event("startup")
async def startup_event():
    """Crear tablas al iniciar la aplicación"""
    try:
        # Crear todas las tablas de géneros y artistas
        GenreBase.metadata.create_all(bind=engine)
        ArtistBase.metadata.create_all(bind=engine)
        print("✅ Tablas de base de datos creadas correctamente")
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "🎵 Spotify Analytics API",
        "version": "1.0.0", 
        "docs": "/docs",
        "features": [
            "🎯 Análisis de géneros musicales",
            "💎 Detección de géneros underground", 
            "🥊 Comparación de artistas",
            "📈 Análisis de tendencias",
            "🎵 Especializado en BreakBeat y géneros nicho",
            "⚔️ Comparaciones 1v1 entre artistas"
        ],
        "genre_endpoints": [
            "/api/genres/analyze/{genre}",
            "/api/genres/underground",
            "/api/genres/compare",
            "/api/genres/trending"
        ],
        "artist_endpoints": [
            "/api/artists/search?name={artist}",
            "/api/artists/analyze/{artist_name}",
            "/api/artists/compare?artists={artist1,artist2}",
            "/api/artists/vs?artist1={}&artist2={}",
            "/api/artists/compare/breakbeat"
        ]
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Verificar salud del sistema"""
    
    # Probar conexión con base de datos
    try:
        db.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception as e:
        database_status = f"error: {str(e)}"
    
    # Probar conexión con Spotify
    spotify = get_spotify_client()
    spotify_status = "disconnected"
    
    if spotify:
        try:
            result = spotify.search(q="test", type="artist", limit=1)
            spotify_status = "connected"
        except Exception as e:
            spotify_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": database_status,
        "spotify_api": spotify_status,
        "credentials_configured": bool(os.getenv("SPOTIFY_CLIENT_ID") and os.getenv("SPOTIFY_CLIENT_SECRET")),
        "features_available": {
            "genre_analysis": database_status == "connected" and spotify_status == "connected",
            "artist_comparison": database_status == "connected" and spotify_status == "connected"
        }
    }

@app.get("/test/search/{artist_name}")
async def test_search_artist(artist_name: str):
    """Probar búsqueda de artista"""
    
    spotify = get_spotify_client()
    if not spotify:
        return {"error": "Spotify client not configured"}
    
    try:
        results = spotify.search(q=artist_name, type='artist', limit=3)
        artists = []
        
        for artist in results['artists']['items']:
            artists.append({
                "name": artist['name'],
                "popularity": artist['popularity'],
                "followers": artist['followers']['total'],
                "genres": artist['genres'][:3]
            })
        
        return {
            "query": artist_name,
            "results": artists,
            "total_found": len(artists)
        }
        
    except Exception as e:
        return {"error": f"Error searching: {str(e)}"}

@app.get("/database/test")
async def test_database(db: Session = Depends(get_db)):
    """Probar conexión con base de datos"""
    try:
        # Probar query simple
        result = db.execute(text("SELECT current_database(), current_user, version()"))
        row = result.fetchone()
        
        return {
            "status": "success",
            "database": row[0] if row else "unknown",
            "user": row[1] if row else "unknown", 
            "version": row[2] if row else "unknown"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)