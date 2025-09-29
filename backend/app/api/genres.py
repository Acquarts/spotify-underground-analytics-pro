from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..services.genre_analyzer import GenreAnalyzer

router = APIRouter(prefix="/api/genres", tags=["Genre Analysis"])

@router.get("/analyze/{genre}")
async def analyze_single_genre(
    genre: str,
    db: Session = Depends(get_db)
):
    """
    🎵 Analiza un género musical específico
    
    - **genre**: Nombre del género (breakbeat, electronic, pop, etc.)
    - **returns**: Análisis completo con métricas de audio y popularidad
    """
    try:
        analyzer = GenreAnalyzer(db)
        result = analyzer.analyze_genre(genre.lower())
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing genre {genre}: {str(e)}"
        )

@router.get("/analyze/multiple")
async def analyze_multiple_genres(
    genres: Optional[str] = "breakbeat,electronic,pop,rock",
    db: Session = Depends(get_db)
):
    """
    🎯 Analiza múltiples géneros y los compara
    
    - **genres**: Lista de géneros separados por coma
    - **returns**: Análisis comparativo con rankings y underground gems
    """
    try:
        analyzer = GenreAnalyzer(db)
        
        # Parsear géneros
        genre_list = [g.strip().lower() for g in genres.split(",")]
        
        result = analyzer.analyze_multiple_genres(genre_list)
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing multiple genres: {str(e)}"
        )

@router.get("/underground")
async def find_underground_genres(
    db: Session = Depends(get_db)
):
    """
    💎 Encuentra géneros underground automáticamente
    
    Analiza géneros enfocándose en encontrar "gems" underground:
    - Baja popularidad mainstream  
    - Alta energía musical
    - Potencial de crecimiento
    """
    try:
        analyzer = GenreAnalyzer(db)
        
        # Géneros candidatos a ser underground
        underground_candidates = [
            'breakbeat', 'drum-and-bass', 'dubstep', 'hardstyle',
            'psytrance', 'darkwave', 'industrial', 'witch-house'
        ]
        
        result = analyzer.analyze_multiple_genres(underground_candidates)
        
        # Filtrar solo los underground gems
        underground_gems = result.get('comparison', {}).get('underground_gems', [])
        
        return {
            "status": "success",
            "data": {
                "underground_genres": underground_gems,
                "analysis_summary": result.get('comparison', {}),
                "total_analyzed": len(underground_candidates),
                "gems_found": len(underground_gems)
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error finding underground genres: {str(e)}"
        )

@router.get("/compare")
async def compare_genres(
    genre1: str = "breakbeat",
    genre2: str = "electronic",
    db: Session = Depends(get_db)
):
    """
    🥊 Compara dos géneros directamente
    
    - **genre1**: Primer género a comparar
    - **genre2**: Segundo género a comparar  
    - **returns**: Comparación detallada lado a lado
    """
    try:
        analyzer = GenreAnalyzer(db)
        
        # Analizar ambos géneros
        result1 = analyzer.analyze_genre(genre1.lower())
        result2 = analyzer.analyze_genre(genre2.lower())
        
        # Crear comparación directa
        comparison = {
            "genres_compared": [genre1, genre2],
            "winner_popularity": genre1 if result1.get('avg_popularity', 0) > result2.get('avg_popularity', 0) else genre2,
            "winner_energy": genre1 if result1.get('avg_energy', 0) > result2.get('avg_energy', 0) else genre2,
            "winner_danceability": genre1 if result1.get('avg_danceability', 0) > result2.get('avg_danceability', 0) else genre2,
            "detailed_comparison": {
                genre1: result1,
                genre2: result2
            }
        }
        
        return {
            "status": "success", 
            "data": comparison
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing genres: {str(e)}"
        )

@router.get("/trending")
async def get_trending_analysis(
    db: Session = Depends(get_db)
):
    """
    📈 Análisis de géneros trending vs underground
    
    Compara géneros mainstream vs underground para encontrar tendencias
    """
    try:
        analyzer = GenreAnalyzer(db)
        
        # Géneros mainstream
        mainstream = ['pop', 'rock', 'hip-hop', 'country']
        
        # Géneros underground  
        underground = ['breakbeat', 'drum-and-bass', 'psytrance', 'darkwave']
        
        # Analizar ambos grupos
        mainstream_result = analyzer.analyze_multiple_genres(mainstream)
        underground_result = analyzer.analyze_multiple_genres(underground)
        
        return {
            "status": "success",
            "data": {
                "mainstream_analysis": mainstream_result,
                "underground_analysis": underground_result,
                "insights": {
                    "mainstream_avg_popularity": _calculate_avg_popularity(mainstream_result),
                    "underground_avg_popularity": _calculate_avg_popularity(underground_result),
                    "energy_comparison": _compare_energy_levels(mainstream_result, underground_result)
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in trending analysis: {str(e)}"
        )

# Funciones auxiliares
def _calculate_avg_popularity(analysis_result):
    """Calcula popularidad promedio de un análisis"""
    genres = analysis_result.get('genres', {})
    valid_genres = [g for g in genres.values() if 'error' not in g]
    
    if not valid_genres:
        return 0
    
    popularities = [g.get('avg_popularity', 0) for g in valid_genres]
    return sum(popularities) / len(popularities)

def _compare_energy_levels(mainstream_result, underground_result):
    """Compara niveles de energía entre mainstream y underground"""
    mainstream_energy = _calculate_avg_energy(mainstream_result)
    underground_energy = _calculate_avg_energy(underground_result)
    
    return {
        "mainstream_avg_energy": mainstream_energy,
        "underground_avg_energy": underground_energy,
        "energy_winner": "underground" if underground_energy > mainstream_energy else "mainstream",
        "energy_difference": abs(underground_energy - mainstream_energy)
    }

def _calculate_avg_energy(analysis_result):
    """Calcula energía promedio de un análisis"""
    genres = analysis_result.get('genres', {})
    valid_genres = [g for g in genres.values() if 'error' not in g]
    
    if not valid_genres:
        return 0
    
    energies = [g.get('avg_energy', 0) for g in valid_genres]
    return sum(energies) / len(energies)