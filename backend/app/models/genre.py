from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class GenreSnapshot(Base):
    """
    Almacena snapshots diarios de métricas de géneros musicales
    """
    __tablename__ = "genre_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    genre = Column(String(50), nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Métricas principales
    avg_popularity = Column(Float, default=0.0)
    tracks_analyzed = Column(Integer, default=0)
    playlist_presence = Column(Integer, default=0)
    
    # Audio features promedio
    avg_energy = Column(Float, default=0.0)
    avg_danceability = Column(Float, default=0.0)
    avg_valence = Column(Float, default=0.0)
    avg_tempo = Column(Float, default=0.0)
    
    # Datos adicionales en JSON
    top_artists = Column(JSON)  # Lista de top artistas del género
    
    def __repr__(self):
        return f"<GenreSnapshot {self.genre} - {self.date.strftime('%Y-%m-%d')}>"

class GenreTrend(Base):
    """
    Tendencias calculadas de géneros musicales
    """
    __tablename__ = "genre_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    genre = Column(String(50), nullable=False, index=True)
    analysis_date = Column(DateTime, default=datetime.utcnow)
    period_days = Column(Integer, default=30)
    
    # Métricas de tendencia
    growth_rate = Column(Float, default=0.0)
    momentum = Column(Float, default=0.0)
    volatility = Column(Float, default=0.0)
    trend_direction = Column(String(20))  # 'rising', 'falling', 'stable'
    
    # Market share relativo
    market_share = Column(Float, default=0.0)
    
    def __repr__(self):
        return f"<GenreTrend {self.genre} - {self.trend_direction}>"