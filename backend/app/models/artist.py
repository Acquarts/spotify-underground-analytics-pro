from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Artist(Base):
    """
    Información básica de artistas para comparación
    """
    __tablename__ = "artists"
    
    id = Column(String(50), primary_key=True, index=True)  # Spotify ID
    name = Column(String(200), nullable=False, index=True)
    popularity = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    genres = Column(JSON)  # Array de géneros
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Artist {self.name}>"

class ArtistSnapshot(Base):
    """
    Snapshots históricos de métricas de artistas
    """
    __tablename__ = "artist_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(String(50), nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Métricas básicas
    popularity = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    
    # Audio features promedio (del top tracks)
    avg_energy = Column(Float, default=0.0)
    avg_danceability = Column(Float, default=0.0)
    avg_valence = Column(Float, default=0.0)
    avg_tempo = Column(Float, default=0.0)
    
    # Métricas calculadas
    consistency_score = Column(Float, default=0.0)
    avg_track_popularity = Column(Float, default=0.0)
    
    def __repr__(self):
        return f"<ArtistSnapshot {self.artist_id} - {self.date.strftime('%Y-%m-%d')}>"