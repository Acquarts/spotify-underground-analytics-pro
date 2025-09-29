import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
import os
import time

from ..models.artist import Artist, ArtistSnapshot

class ArtistComparator:
    """
    Comparador profesional de artistas
    Optimizado para Spotify Development Mode
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Inicializar cliente Spotify
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        if client_id and client_secret:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            self.sp = spotipy.Spotify(
                client_credentials_manager=client_credentials_manager
            )
        else:
            self.sp = None
        
        # Límites para Development Mode
        self.MAX_TOP_TRACKS = 5  # Reducido
        self.MAX_ARTISTS_COMPARE = 5  # Máximo artistas por comparación
    
    def search_artist(self, artist_name: str) -> Optional[Dict]:
        """
        Busca un artista por nombre
        """
        if not self.sp:
            return None
        
        try:
            results = self.sp.search(q=artist_name, type='artist', limit=1)
            
            if results['artists']['items']:
                artist = results['artists']['items'][0]
                return {
                    'id': artist['id'],
                    'name': artist['name'],
                    'popularity': artist['popularity'],
                    'followers': artist['followers']['total'],
                    'genres': artist['genres'],
                    'image': artist['images'][0]['url'] if artist['images'] else None
                }
            
            return None
            
        except Exception as e:
            print(f"Error buscando artista {artist_name}: {str(e)}")
            return None
    
    def get_artist_complete_data(self, artist_name: str) -> Optional[Dict]:
        """
        Obtiene datos completos de un artista
        """
        if not self.sp:
            return None
        
        print(f"🎤 Analizando artista: {artist_name}")
        
        try:
            # Buscar artista
            artist_data = self.search_artist(artist_name)
            if not artist_data:
                return None
            
            artist_id = artist_data['id']
            
            time.sleep(0.3)
            
            # Obtener top tracks (reducido a 5)
            top_tracks = self.sp.artist_top_tracks(artist_id)
            
            if not top_tracks['tracks']:
                return artist_data
            
            # Limitar a MAX_TOP_TRACKS
            tracks = top_tracks['tracks'][:self.MAX_TOP_TRACKS]
            track_ids = [track['id'] for track in tracks]
            
            time.sleep(0.3)
            
            # Obtener audio features
            audio_features = []
            try:
                features = self.sp.audio_features(track_ids)
                audio_features = [f for f in features if f is not None]
            except Exception as e:
                print(f"⚠️ No se pudieron obtener audio features: {str(e)}")
            
            # Calcular métricas
            popularities = [track['popularity'] for track in tracks]
            
            artist_data['avg_track_popularity'] = np.mean(popularities)
            artist_data['top_track_popularity'] = max(popularities)
            artist_data['tracks_analyzed'] = len(tracks)
            
            if audio_features:
                artist_data['avg_energy'] = np.mean([f['energy'] for f in audio_features])
                artist_data['avg_danceability'] = np.mean([f['danceability'] for f in audio_features])
                artist_data['avg_valence'] = np.mean([f['valence'] for f in audio_features])
                artist_data['avg_tempo'] = np.mean([f['tempo'] for f in audio_features])
                
                # Calcular consistency (qué tan consistente es el artista)
                pop_std = np.std(popularities)
                pop_mean = np.mean(popularities)
                consistency = 1 - (pop_std / pop_mean) if pop_mean > 0 else 0
                artist_data['consistency_score'] = max(0, min(1, consistency))
            else:
                artist_data['note'] = "Audio features not available"
            
            # Información de álbumes
            time.sleep(0.3)
            albums = self.sp.artist_albums(artist_id, album_type='album', limit=10)
            artist_data['total_albums'] = albums['total']
            
            # Top 3 tracks
            artist_data['top_tracks'] = [
                {
                    'name': track['name'],
                    'popularity': track['popularity'],
                    'album': track['album']['name']
                }
                for track in tracks[:3]
            ]
            
            # Guardar en base de datos
            self._save_or_update_artist(artist_data)
            
            print(f"✅ Artista {artist_name} analizado correctamente")
            
            return artist_data
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de {artist_name}: {str(e)}")
            return None
    
    def compare_artists(self, artist_names: List[str]) -> Dict:
        """
        Compara múltiples artistas
        """
        if len(artist_names) < 2:
            return {"error": "Se necesitan al menos 2 artistas para comparar"}
        
        if len(artist_names) > self.MAX_ARTISTS_COMPARE:
            return {"error": f"Máximo {self.MAX_ARTISTS_COMPARE} artistas por comparación"}
        
        print(f"🥊 Comparando {len(artist_names)} artistas...")
        
        artists_data = {}
        
        for i, artist_name in enumerate(artist_names):
            print(f"📊 Artista {i+1}/{len(artist_names)}: {artist_name}")
            
            artist_data = self.get_artist_complete_data(artist_name)
            
            if artist_data:
                artists_data[artist_name] = artist_data
            
            # Delay entre artistas
            if i < len(artist_names) - 1:
                time.sleep(1)
        
        if len(artists_data) < 2:
            return {"error": "No se pudieron obtener datos de suficientes artistas"}
        
        # Realizar comparación
        comparison = self._perform_comparison(artists_data)
        
        return {
            "artists_compared": list(artists_data.keys()),
            "total_artists": len(artists_data),
            "detailed_data": artists_data,
            "comparison": comparison,
            "analysis_date": datetime.now().isoformat()
        }
    
    def _perform_comparison(self, artists_data: Dict) -> Dict:
        """
        Realiza el análisis comparativo
        """
        comparison = {
            "rankings": {},
            "winners": {},
            "insights": []
        }
        
        # Métricas a comparar
        metrics = [
            ('popularity', 'Popularidad'),
            ('followers', 'Seguidores'),
            ('avg_track_popularity', 'Popularidad de Tracks'),
            ('avg_energy', 'Energía'),
            ('avg_danceability', 'Bailabilidad')
        ]
        
        for metric_key, metric_name in metrics:
            # Extraer valores
            metric_values = {}
            for artist_name, data in artists_data.items():
                value = data.get(metric_key, 0)
                if value is not None:
                    metric_values[artist_name] = value
            
            if not metric_values:
                continue
            
            # Ranking
            ranked = sorted(metric_values.items(), key=lambda x: x[1], reverse=True)
            
            comparison['rankings'][metric_key] = [
                {
                    'rank': i + 1,
                    'artist': artist,
                    'value': round(value, 2) if isinstance(value, float) else value
                }
                for i, (artist, value) in enumerate(ranked)
            ]
            
            # Ganador de esta métrica
            comparison['winners'][metric_key] = {
                'artist': ranked[0][0],
                'value': round(ranked[0][1], 2) if isinstance(ranked[0][1], float) else ranked[0][1]
            }
        
        # Generar insights
        comparison['insights'] = self._generate_insights(artists_data, comparison)
        
        return comparison
    
    def _generate_insights(self, artists_data: Dict, comparison: Dict) -> List[str]:
        """
        Genera insights inteligentes de la comparación
        """
        insights = []
        
        # Artista más popular
        if 'popularity' in comparison['winners']:
            winner = comparison['winners']['popularity']
            insights.append(
                f"🏆 {winner['artist']} lidera en popularidad con {winner['value']} puntos"
            )
        
        # Artista con más seguidores
        if 'followers' in comparison['winners']:
            winner = comparison['winners']['followers']
            insights.append(
                f"👥 {winner['artist']} tiene la mayor base de fans con {self._format_number(winner['value'])} seguidores"
            )
        
        # Artista más energético
        if 'avg_energy' in comparison['winners']:
            winner = comparison['winners']['avg_energy']
            if winner['value'] > 0.7:
                insights.append(
                    f"⚡ {winner['artist']} es el más energético con {winner['value']:.2f} de energía"
                )
        
        # Detectar "dark horses" (bajo popularity pero buena música)
        for artist_name, data in artists_data.items():
            popularity = data.get('popularity', 0)
            energy = data.get('avg_energy', 0)
            consistency = data.get('consistency_score', 0)
            
            if popularity < 50 and energy > 0.6 and consistency > 0.7:
                insights.append(
                    f"💎 {artist_name} es una joya oculta: baja popularidad pero alta calidad musical"
                )
        
        # Artista más consistente
        consistent_artists = [
            (name, data.get('consistency_score', 0))
            for name, data in artists_data.items()
            if 'consistency_score' in data
        ]
        
        if consistent_artists:
            most_consistent = max(consistent_artists, key=lambda x: x[1])
            if most_consistent[1] > 0.7:
                insights.append(
                    f"🎯 {most_consistent[0]} es el más consistente con un score de {most_consistent[1]:.2f}"
                )
        
        return insights
    
    def _save_or_update_artist(self, artist_data: Dict):
        """
        Guarda o actualiza artista en la base de datos
        """
        try:
            # Buscar si existe
            existing = self.db.query(Artist).filter(
                Artist.id == artist_data['id']
            ).first()
            
            if existing:
                # Actualizar
                existing.popularity = artist_data['popularity']
                existing.followers = artist_data['followers']
                existing.updated_at = datetime.utcnow()
            else:
                # Crear nuevo
                new_artist = Artist(
                    id=artist_data['id'],
                    name=artist_data['name'],
                    popularity=artist_data['popularity'],
                    followers=artist_data['followers'],
                    genres=artist_data['genres']
                )
                self.db.add(new_artist)
            
            # Crear snapshot
            snapshot = ArtistSnapshot(
                artist_id=artist_data['id'],
                date=datetime.utcnow(),
                popularity=artist_data['popularity'],
                followers=artist_data['followers'],
                avg_energy=artist_data.get('avg_energy', 0),
                avg_danceability=artist_data.get('avg_danceability', 0),
                avg_valence=artist_data.get('avg_valence', 0),
                avg_tempo=artist_data.get('avg_tempo', 0),
                consistency_score=artist_data.get('consistency_score', 0),
                avg_track_popularity=artist_data.get('avg_track_popularity', 0)
            )
            
            self.db.add(snapshot)
            self.db.commit()
            
            print(f"💾 Datos guardados en BD para {artist_data['name']}")
            
        except Exception as e:
            print(f"⚠️ Error guardando artista: {e}")
            self.db.rollback()
    
    def _format_number(self, num: int) -> str:
        """Formatea números grandes"""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        if num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)