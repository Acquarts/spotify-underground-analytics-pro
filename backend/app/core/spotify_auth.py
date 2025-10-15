"""
Sistema de autenticación OAuth para Spotify
Permite autenticación de usuario para acceder a audio features en Development Mode
"""
import os
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import spotipy

def get_spotify_client_with_oauth():
    """
    Cliente Spotify con OAuth (requiere autenticación de usuario)
    Usar para features avanzados como audio-features en Development Mode
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8000/callback")

    if not client_id or not client_secret:
        return None

    try:
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-library-read user-top-read",
            cache_path=".spotify_cache",
            open_browser=True
        )

        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        print(f"Error en OAuth: {e}")
        return None


def get_spotify_client_credentials():
    """
    Cliente Spotify con Client Credentials (sin autenticación de usuario)
    Funciona para búsquedas básicas
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        return None

    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        print(f"Error en Client Credentials: {e}")
        return None


def get_spotify_client(prefer_oauth=False):
    """
    Obtiene el mejor cliente disponible

    Args:
        prefer_oauth: Si es True, intenta OAuth primero

    Returns:
        Cliente de Spotify o None
    """
    if prefer_oauth:
        # Intentar OAuth primero
        client = get_spotify_client_with_oauth()
        if client:
            print("✅ Usando Spotify con OAuth (acceso completo)")
            return client

        # Fallback a Client Credentials
        print("⚠️ OAuth no disponible, usando Client Credentials")
        return get_spotify_client_credentials()
    else:
        # Client Credentials por defecto
        return get_spotify_client_credentials()
