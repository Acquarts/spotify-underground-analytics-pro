from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..services.artist_comparator import ArtistComparator

router = APIRouter(prefix="/api/artists", tags=["Artist Comparison"])

@router.get("/search")
async def search_artist(
    name: str = Query(..., description="Nombre del artista a buscar"),
    db: Session = Depends(get_db)
):
    """
    🔍 Busca un artista por nombre
    
    - **name**: Nombre del artista
    - **returns**: Información básica del artista encontrado
    """
    try:
        comparator = ArtistComparator(db)
        result = comparator.search_artist(name)
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Artista '{name}' no encontrado"
            )
        
        return {
            "status": "success",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error buscando artista: {str(e)}"
        )

@router.get("/analyze/{artist_name}")
async def analyze_artist(
    artist_name: str,
    db: Session = Depends(get_db)
):
    """
    🎤 Analiza un artista específico en detalle
    
    - **artist_name**: Nombre del artista
    - **returns**: Análisis completo con métricas, top tracks, géneros
    """
    try:
        comparator = ArtistComparator(db)
        result = comparator.get_artist_complete_data(artist_name)
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Artista '{artist_name}' no encontrado"
            )
        
        return {
            "status": "success",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analizando artista: {str(e)}"
        )

@router.get("/compare")
async def compare_artists(
    artists: str = Query(..., description="Nombres de artistas separados por coma"),
    db: Session = Depends(get_db)
):
    """
    🥊 Compara múltiples artistas
    
    - **artists**: Lista de artistas separados por coma (ej: "Pendulum,The Prodigy")
    - **returns**: Comparación detallada con rankings, ganadores e insights
    
    Máximo 5 artistas por comparación.
    """
    try:
        # Parsear artistas
        artist_list = [a.strip() for a in artists.split(",")]
        
        if len(artist_list) < 2:
            raise HTTPException(
                status_code=400,
                detail="Se necesitan al menos 2 artistas para comparar"
            )
        
        if len(artist_list) > 5:
            raise HTTPException(
                status_code=400,
                detail="Máximo 5 artistas por comparación"
            )
        
        comparator = ArtistComparator(db)
        result = comparator.compare_artists(artist_list)
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        return {
            "status": "success",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error comparando artistas: {str(e)}"
        )

@router.get("/compare/breakbeat")
async def compare_breakbeat_artists(
    db: Session = Depends(get_db)
):
    """
    🎵 Compara artistas icónicos de BreakBeat
    
    Compara artistas clásicos del género BreakBeat:
    - The Prodigy
    - Pendulum
    - The Chemical Brothers
    """
    try:
        breakbeat_artists = [
            "The Prodigy",
            "Pendulum", 
            "The Chemical Brothers"
        ]
        
        comparator = ArtistComparator(db)
        result = comparator.compare_artists(breakbeat_artists)
        
        if "error" in result:
            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )
        
        return {
            "status": "success",
            "data": result,
            "genre": "breakbeat",
            "description": "Comparación de artistas icónicos del BreakBeat"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error comparando artistas de BreakBeat: {str(e)}"
        )

@router.get("/vs")
async def artist_versus(
    artist1: str = Query(..., description="Primer artista"),
    artist2: str = Query(..., description="Segundo artista"),
    db: Session = Depends(get_db)
):
    """
    ⚔️ Comparación directa 1 vs 1
    
    - **artist1**: Primer artista
    - **artist2**: Segundo artista
    - **returns**: Comparación head-to-head detallada
    """
    try:
        comparator = ArtistComparator(db)
        result = comparator.compare_artists([artist1, artist2])
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        # Simplificar para formato 1v1
        data1 = result['detailed_data'].get(artist1, {})
        data2 = result['detailed_data'].get(artist2, {})
        
        versus_result = {
            "matchup": f"{artist1} vs {artist2}",
            artist1: {
                "popularity": data1.get('popularity', 0),
                "followers": data1.get('followers', 0),
                "top_track": data1.get('top_tracks', [{}])[0] if data1.get('top_tracks') else {},
                "genres": data1.get('genres', [])[:3]
            },
            artist2: {
                "popularity": data2.get('popularity', 0),
                "followers": data2.get('followers', 0),
                "top_track": data2.get('top_tracks', [{}])[0] if data2.get('top_tracks') else {},
                "genres": data2.get('genres', [])[:3]
            },
            "winners": result['comparison'].get('winners', {}),
            "insights": result['comparison'].get('insights', [])
        }
        
        return {
            "status": "success",
            "data": versus_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en comparación 1v1: {str(e)}"
        )

@router.get("/underground/comparison")
async def compare_underground_vs_mainstream(
    db: Session = Depends(get_db)
):
    """
    💎 Underground vs Mainstream
    
    Compara artistas underground de BreakBeat vs artistas mainstream de Pop
    """
    try:
        underground = ["Pendulum", "Chase & Status"]
        mainstream = ["Taylor Swift", "Ed Sheeran"]
        
        comparator = ArtistComparator(db)
        
        # Comparar grupos
        underground_result = comparator.compare_artists(underground)
        mainstream_result = comparator.compare_artists(mainstream)
        
        return {
            "status": "success",
            "data": {
                "underground": {
                    "artists": underground,
                    "analysis": underground_result
                },
                "mainstream": {
                    "artists": mainstream,
                    "analysis": mainstream_result
                },
                "insight": "Comparación entre artistas underground de BreakBeat y artistas mainstream de Pop"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en comparación underground vs mainstream: {str(e)}"
        )