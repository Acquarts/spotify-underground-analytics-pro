import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
import os
import time

from ..models.genre import GenreSnapshot

class GenreAnalyzer:
    """
    Analizador profesional de tendencias de géneros musicales
    Optimizado para Spotify Development Mode (límites reducidos)
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
            
        # Géneros objetivo para análisis
        self.target_genres = [
            'breakbeat', 'drum-and-bass', 'dubstep', 'techno', 'house',
            'electronic', 'pop', 'rock', 'hip-hop', 'indie'
        ]
        
        # LÍMITES para Development Mode
        self.MAX_PLAYLISTS = 8  # Reducido de 15
        self.MAX_TRACKS_PER_PLAYLIST = 8  # Reducido de 25
        self.MAX_TOTAL_TRACKS = 20  # Reducido de 50
        self.MAX_AUDIO_FEATURES_PER_REQUEST = 20  # Límite seguro
    
    def analyze_genre(self, genre: str) -> Dict:
        """
        Analiza un género específico (versión optimizada para Development mode)
        """
        if not self.sp:
            return {"error": "Spotify client not configured"}
        
        print(f"🎵 Analizando género: {genre} (Development mode)")
        
        try:
            # 1. Buscar menos playlists
            playlists = self.sp.search(
                q=f'genre:{genre}', 
                type='playlist', 
                limit=self.MAX_PLAYLISTS
            )
            
            time.sleep(0.5)  # Delay para evitar rate limiting
            
            # 2. Recopilar tracks (cantidad reducida)
            all_tracks = []
            playlist_count = 0
            
            for playlist in playlists['playlists']['items'][:self.MAX_PLAYLISTS]:
                if playlist and playlist['tracks']['total'] > 5:
                    playlist_count += 1
                    
                    # Obtener menos tracks por playlist
                    tracks = self.sp.playlist_tracks(
                        playlist['id'], 
                        limit=self.MAX_TRACKS_PER_PLAYLIST,
                        fields="items(track(id,name,popularity,artists))"
                    )
                    
                    time.sleep(0.3)  # Delay entre peticiones
                    
                    for item in tracks['items']:
                        if (item['track'] and 
                            item['track']['id'] and 
                            item['track']['popularity'] > 0):
                            all_tracks.append({
                                'id': item['track']['id'],
                                'name': item['track']['name'],
                                'popularity': item['track']['popularity'],
                                'artist': item['track']['artists'][0]['name'] if item['track']['artists'] else 'Unknown'
                            })
            
            # 3. Remover duplicados y limitar estrictamente
            unique_tracks = {track['id']: track for track in all_tracks}
            tracks_list = list(unique_tracks.values())[:self.MAX_TOTAL_TRACKS]
            
            if not tracks_list:
                return {
                    "genre": genre,
                    "error": "No tracks found for this genre",
                    "note": "Try a different genre or check Spotify availability"
                }
            
            # 4. Intentar obtener audio features (puede fallar en Development Mode)
            track_ids = [track['id'] for track in tracks_list]
            audio_features = []
            audio_features_available = False

            try:
                print(f"📊 Intentando obtener audio features para {len(tracks_list)} tracks...")

                # Dividir en lotes de MAX_AUDIO_FEATURES_PER_REQUEST
                for i in range(0, len(track_ids), self.MAX_AUDIO_FEATURES_PER_REQUEST):
                    batch = track_ids[i:i + self.MAX_AUDIO_FEATURES_PER_REQUEST]

                    try:
                        batch_features = self.sp.audio_features(batch)
                        if batch_features:
                            audio_features.extend(batch_features)
                        time.sleep(0.5)  # Delay entre lotes
                    except Exception as e:
                        print(f"⚠️ Audio features no disponibles (Development Mode): {str(e)[:100]}")
                        break

                valid_features = [f for f in audio_features if f is not None]
                audio_features_available = len(valid_features) > 0

            except Exception as e:
                print(f"⚠️ Audio features no disponibles en Development Mode")
                valid_features = []

            if not audio_features_available:
                # Retornar métricas básicas sin audio features
                print(f"ℹ️ Retornando métricas básicas (sin audio features)")
                return {
                    "genre": genre,
                    "total_tracks": len(tracks_list),
                    "tracks_analyzed": len(tracks_list),
                    "playlist_presence": playlist_count,
                    "avg_popularity": round(float(np.mean([t['popularity'] for t in tracks_list])), 2),
                    "avg_energy": 0.5,  # Valores por defecto
                    "avg_danceability": 0.5,
                    "avg_valence": 0.5,
                    "avg_tempo": 120.0,
                    "avg_acousticness": 0.5,
                    "avg_instrumentalness": 0.3,
                    "development_mode": True,
                    "audio_features_available": False,
                    "note": "⚠️ Audio features no disponibles. Tu app Spotify está en Development Mode. Agrega tu usuario en: https://developer.spotify.com/dashboard",
                    "top_tracks": [
                        {"name": t['name'], "artist": t['artist'], "popularity": t['popularity']}
                        for t in sorted(tracks_list, key=lambda x: x['popularity'], reverse=True)[:5]
                    ]
                }
            
            # 5. Calcular métricas del género
            genre_metrics = self._calculate_metrics(
                tracks_list, valid_features, playlist_count
            )
            genre_metrics['genre'] = genre
            genre_metrics['development_mode'] = True
            genre_metrics['tracks_limit'] = self.MAX_TOTAL_TRACKS
            
            # 6. Guardar en base de datos
            self._save_genre_snapshot(genre, genre_metrics, tracks_list[:5])
            
            print(f"✅ Género {genre}: {len(tracks_list)} tracks analizados correctamente")
            
            return genre_metrics
            
        except Exception as e:
            print(f"❌ Error analizando {genre}: {str(e)}")
            return {
                "genre": genre,
                "error": str(e),
                "suggestion": "Try with a different genre or reduce the number of genres analyzed simultaneously"
            }
    
    def analyze_multiple_genres(self, genres: Optional[List[str]] = None) -> Dict:
        """
        Analiza múltiples géneros (con delays para Development mode)
        """
        if not genres:
            genres = self.target_genres[:4]  # Limitar a 4 géneros por defecto
        
        # Limitar número máximo de géneros
        if len(genres) > 5:
            genres = genres[:5]
            print(f"⚠️ Limitado a 5 géneros para evitar rate limiting")
        
        results = {}
        
        for i, genre in enumerate(genres):
            print(f"🎵 Analizando género {i+1}/{len(genres)}: {genre}")
            results[genre] = self.analyze_genre(genre)
            
            # Delay entre géneros
            if i < len(genres) - 1:
                time.sleep(1)
        
        # Calcular comparaciones
        comparison = self._generate_genre_comparison(results)
        
        return {
            "genres": results,
            "comparison": comparison,
            "analysis_date": datetime.now().isoformat(),
            "total_genres_analyzed": len([g for g in results.values() if 'error' not in g]),
            "development_mode": True,
            "note": "Analysis limited by Spotify Development mode quotas"
        }
    
    def _calculate_metrics(self, tracks: List[Dict], 
                          audio_features: List[Dict], 
                          playlist_count: int) -> Dict:
        """
        Calcula métricas agregadas para un género
        """
        if not tracks or not audio_features:
            return {
                "avg_popularity": 0,
                "tracks_analyzed": 0,
                "playlist_presence": playlist_count,
                "avg_energy": 0,
                "avg_danceability": 0,
                "avg_valence": 0,
                "avg_tempo": 0
            }
        
        # Métricas de popularidad
        popularities = [track['popularity'] for track in tracks]
        
        # Métricas de audio
        energies = [f['energy'] for f in audio_features]
        danceabilities = [f['danceability'] for f in audio_features]
        valences = [f['valence'] for f in audio_features]
        tempos = [f['tempo'] for f in audio_features]
        
        return {
            "avg_popularity": round(np.mean(popularities), 2),
            "tracks_analyzed": len(tracks),
            "playlist_presence": playlist_count,
            "avg_energy": round(np.mean(energies), 3),
            "avg_danceability": round(np.mean(danceabilities), 3),
            "avg_valence": round(np.mean(valences), 3),
            "avg_tempo": round(np.mean(tempos), 1),
            "popularity_std": round(np.std(popularities), 2),
            "energy_range": [round(np.min(energies), 3), round(np.max(energies), 3)],
            "tempo_range": [round(np.min(tempos), 1), round(np.max(tempos), 1)],
            "top_tracks": [
                {"name": t['name'], "artist": t['artist'], "popularity": t['popularity']}
                for t in sorted(tracks, key=lambda x: x['popularity'], reverse=True)[:3]
            ]
        }
    
    def _generate_genre_comparison(self, results: Dict) -> Dict:
        """
        Genera comparaciones entre géneros
        """
        valid_results = {k: v for k, v in results.items() if 'error' not in v}
        
        if len(valid_results) < 2:
            return {"message": "Need at least 2 genres for comparison"}
        
        # Género más popular
        most_popular = max(
            valid_results.items(), 
            key=lambda x: x[1].get('avg_popularity', 0)
        )
        
        # Género más energético
        most_energetic = max(
            valid_results.items(), 
            key=lambda x: x[1].get('avg_energy', 0)
        )
        
        # Género más bailable
        most_danceable = max(
            valid_results.items(), 
            key=lambda x: x[1].get('avg_danceability', 0)
        )
        
        # Detectar géneros underground
        underground_candidates = []
        for genre, metrics in valid_results.items():
            popularity = metrics.get('avg_popularity', 0)
            energy = metrics.get('avg_energy', 0)
            
            if popularity < 45 and energy > 0.55:
                underground_score = energy - (popularity / 100)
                underground_candidates.append({
                    'genre': genre,
                    'underground_score': round(underground_score, 3),
                    'popularity': popularity,
                    'energy': energy
                })
        
        underground_candidates.sort(key=lambda x: x['underground_score'], reverse=True)
        
        return {
            "most_popular": {
                "genre": most_popular[0], 
                "value": round(most_popular[1].get('avg_popularity', 0), 2)
            },
            "most_energetic": {
                "genre": most_energetic[0], 
                "value": round(most_energetic[1].get('avg_energy', 0), 3)
            },
            "most_danceable": {
                "genre": most_danceable[0], 
                "value": round(most_danceable[1].get('avg_danceability', 0), 3)
            },
            "underground_gems": underground_candidates[:3],
            "total_compared": len(valid_results)
        }
    
    def _save_genre_snapshot(self, genre: str, metrics: Dict, top_tracks: List[Dict]):
        """
        Guarda snapshot del género en la base de datos
        """
        try:
            # Preparar top artists
            top_artists = []
            if top_tracks:
                artist_counts = {}
                for track in top_tracks:
                    artist = track['artist']
                    if artist in artist_counts:
                        artist_counts[artist] += track['popularity']
                    else:
                        artist_counts[artist] = track['popularity']
                
                top_artists = [
                    {'name': artist, 'score': score}
                    for artist, score in sorted(artist_counts.items(), 
                                              key=lambda x: x[1], reverse=True)[:5]
                ]
            
            # Crear snapshot
            snapshot = GenreSnapshot(
                genre=genre,
                date=datetime.utcnow(),
                avg_popularity=metrics.get('avg_popularity', 0),
                tracks_analyzed=metrics.get('tracks_analyzed', 0),
                playlist_presence=metrics.get('playlist_presence', 0),
                avg_energy=metrics.get('avg_energy', 0),
                avg_danceability=metrics.get('avg_danceability', 0),
                avg_valence=metrics.get('avg_valence', 0),
                avg_tempo=metrics.get('avg_tempo', 0),
                top_artists=top_artists
            )
            
            self.db.add(snapshot)
            self.db.commit()
            
            print(f"💾 Snapshot guardado en base de datos para {genre}")
            
        except Exception as e:
            print(f"⚠️ Error guardando snapshot de {genre}: {e}")
            self.db.rollback()