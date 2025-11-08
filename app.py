import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Spotify Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL base de la API (configurable)
# Try Streamlit secrets first, then environment variables, then default
try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "https://spotify-underground-analytics-pro-production.up.railway.app"))
except:
    API_BASE_URL = os.getenv("API_BASE_URL", "https://spotify-underground-analytics-pro-production.up.railway.app")

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1DB954;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #282828;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1DB954;
    }
    .winner-badge {
        background-color: #1DB954;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Función para hacer peticiones a la API
def api_request(endpoint: str, params: Dict = None) -> Dict:
    """Realiza peticiones a la API"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        st.write(f"🔗 Requesting: {url}")  # Debug
        response = requests.get(url, params=params, timeout=30)
        st.write(f"📊 Status Code: {response.status_code}")  # Debug
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error conectando con la API: {str(e)}")
        st.error(f"🔗 URL intentada: {url}")
        st.error(f"📋 Tipo de error: {type(e).__name__}")
        return None

# Header principal
st.markdown('<h1 class="main-header">🎵 Spotify Analytics</h1>', unsafe_allow_html=True)
st.markdown("---")

# Debug: Mostrar URL de la API
with st.expander("🔧 Debug Info"):
    st.write(f"**API Base URL:** {API_BASE_URL}")
    try:
        st.write(f"**Secrets available:** {list(st.secrets.keys())}")
    except:
        st.write(f"**Secrets available:** No secrets configured")

# Sidebar con navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio(
    "Selecciona una sección:",
    ["🏠 Inicio", "🎯 Análisis de Géneros", "🥊 Comparación de Artistas", "💎 Underground Gems", "⚔️ Batalla 1v1"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Configuración")
api_url_input = st.sidebar.text_input("URL de la API", value=API_BASE_URL)
if api_url_input != API_BASE_URL:
    API_BASE_URL = api_url_input

# Verificar estado de la API
with st.sidebar:
    if st.button("🔍 Verificar API"):
        health = api_request("/health")
        if health:
            st.success("✅ API conectada")
            st.json(health)
        else:
            st.error("❌ API no disponible")

# ============================================================================
# PÁGINA DE INICIO
# ============================================================================
if page == "🏠 Inicio":
    st.title("Bienvenido a Spotify Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Análisis de Géneros")
        st.write("""
        - Analiza géneros musicales específicos
        - Obtén métricas de audio (energía, bailabilidad, etc.)
        - Compara múltiples géneros
        - Encuentra géneros underground
        """)

    with col2:
        st.markdown("### 🥊 Comparación de Artistas")
        st.write("""
        - Busca artistas por nombre
        - Análisis completo de artistas
        - Compara hasta 5 artistas simultáneamente
        - Batallas 1v1 entre artistas
        """)

    st.markdown("---")
    st.markdown("### 📊 Estadísticas Rápidas")

    # Obtener información de la API
    root_info = api_request("/")
    if root_info:
        st.success(f"✅ API Version: {root_info.get('version', 'N/A')}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("🎵 Análisis de Géneros Disponible")
        with col2:
            st.info("🎤 Comparación de Artistas Disponible")
        with col3:
            st.info("💎 Detección Underground Disponible")

# ============================================================================
# PÁGINA DE ANÁLISIS DE GÉNEROS
# ============================================================================
elif page == "🎯 Análisis de Géneros":
    st.title("🎯 Análisis de Géneros Musicales")

    tab1, tab2, tab3 = st.tabs(["Análisis Individual", "Comparación Múltiple", "Tendencias"])

    # TAB 1: Análisis Individual
    with tab1:
        st.subheader("Analiza un género específico")

        genre_input = st.text_input(
            "Nombre del género",
            placeholder="Ej: breakbeat, electronic, pop, rock...",
            key="single_genre"
        )

        if st.button("🔍 Analizar Género", key="analyze_single"):
            if genre_input:
                with st.spinner(f"Analizando {genre_input}..."):
                    result = api_request(f"/api/genres/analyze/{genre_input}")

                    if result and result.get("status") == "success":
                        data = result.get("data", {})

                        # Métricas principales
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric("Popularidad Promedio", f"{data.get('avg_popularity', 0):.1f}")
                        with col2:
                            st.metric("Energía", f"{data.get('avg_energy', 0):.2f}")
                        with col3:
                            st.metric("Bailabilidad", f"{data.get('avg_danceability', 0):.2f}")
                        with col4:
                            st.metric("Tracks Analizados", data.get('total_tracks', 0))

                        # Gráfico radar de características
                        if all(k in data for k in ['avg_energy', 'avg_danceability', 'avg_valence', 'avg_acousticness']):
                            st.markdown("### 📊 Características del Género")

                            fig = go.Figure()

                            categories = ['Energía', 'Bailabilidad', 'Valencia', 'Acústica', 'Instrumental']
                            values = [
                                data.get('avg_energy', 0),
                                data.get('avg_danceability', 0),
                                data.get('avg_valence', 0),
                                data.get('avg_acousticness', 0),
                                data.get('avg_instrumentalness', 0)
                            ]

                            fig.add_trace(go.Scatterpolar(
                                r=values,
                                theta=categories,
                                fill='toself',
                                name=genre_input.title()
                            ))

                            fig.update_layout(
                                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                                showlegend=True,
                                height=500
                            )

                            st.plotly_chart(fig, use_container_width=True)

                        # Información adicional
                        with st.expander("📋 Ver datos completos"):
                            # Métricas principales
                            st.markdown("#### 📊 Métricas del Género")

                            metrics_df = pd.DataFrame([
                                {"Métrica": "Género", "Valor": data.get('genre', 'N/A').title()},
                                {"Métrica": "Tracks Analizados", "Valor": data.get('tracks_analyzed', 0)},
                                {"Métrica": "Presencia en Playlists", "Valor": data.get('playlist_presence', 0)},
                                {"Métrica": "Popularidad Promedio", "Valor": f"{data.get('avg_popularity', 0):.2f}"},
                                {"Métrica": "Energía", "Valor": f"{data.get('avg_energy', 0):.3f}"},
                                {"Métrica": "Bailabilidad", "Valor": f"{data.get('avg_danceability', 0):.3f}"},
                                {"Métrica": "Valencia", "Valor": f"{data.get('avg_valence', 0):.3f}"},
                                {"Métrica": "Tempo (BPM)", "Valor": f"{data.get('avg_tempo', 0):.1f}"},
                                {"Métrica": "Acústica", "Valor": f"{data.get('avg_acousticness', 0):.3f}"},
                                {"Métrica": "Instrumental", "Valor": f"{data.get('avg_instrumentalness', 0):.3f}"}
                            ])
                            st.dataframe(metrics_df, hide_index=True, use_container_width=True)

                            # Estado del modo
                            if data.get('development_mode'):
                                st.markdown("#### ⚙️ Estado del Análisis")
                                status_df = pd.DataFrame([
                                    {"Campo": "Modo", "Estado": "Development Mode"},
                                    {"Campo": "Audio Features", "Estado": "Estimadas" if data.get('estimated') else "No disponibles"}
                                ])
                                st.dataframe(status_df, hide_index=True, use_container_width=True)

                                if data.get('note'):
                                    st.info(data.get('note'))

                            # Top tracks
                            if data.get('top_tracks'):
                                st.markdown("#### 🎵 Top Tracks")
                                tracks_df = pd.DataFrame(data.get('top_tracks', []))
                                if not tracks_df.empty:
                                    tracks_df = tracks_df.rename(columns={
                                        'name': 'Track',
                                        'artist': 'Artista',
                                        'popularity': 'Popularidad'
                                    })
                                    st.dataframe(tracks_df, hide_index=True, use_container_width=True)
            else:
                st.warning("Por favor ingresa un nombre de género")

    # TAB 2: Comparación Múltiple
    with tab2:
        st.subheader("Compara múltiples géneros")

        genres_input = st.text_input(
            "Géneros a comparar (separados por coma)",
            placeholder="Ej: breakbeat, electronic, pop, rock",
            value="breakbeat,electronic,pop,rock",
            key="multiple_genres"
        )

        if st.button("🔍 Comparar Géneros", key="compare_multiple"):
            if genres_input:
                with st.spinner("Comparando géneros..."):
                    result = api_request("/api/genres/analyze/multiple", params={"genres": genres_input})

                    if result and result.get("status") == "success":
                        data = result.get("data", {})
                        genres_data = data.get("genres", {})

                        # Crear DataFrame para comparación
                        comparison_list = []
                        for genre_name, genre_info in genres_data.items():
                            if "error" not in genre_info:
                                comparison_list.append({
                                    "Género": genre_name.title(),
                                    "Popularidad": genre_info.get("avg_popularity", 0),
                                    "Energía": genre_info.get("avg_energy", 0),
                                    "Bailabilidad": genre_info.get("avg_danceability", 0),
                                    "Tracks": genre_info.get("total_tracks", 0)
                                })

                        if comparison_list:
                            df = pd.DataFrame(comparison_list)

                            # Gráficos de comparación
                            col1, col2 = st.columns(2)

                            with col1:
                                fig1 = px.bar(
                                    df,
                                    x="Género",
                                    y="Popularidad",
                                    title="Popularidad por Género",
                                    color="Popularidad",
                                    color_continuous_scale="Viridis"
                                )
                                st.plotly_chart(fig1, use_container_width=True)

                            with col2:
                                fig2 = px.bar(
                                    df,
                                    x="Género",
                                    y="Energía",
                                    title="Energía por Género",
                                    color="Energía",
                                    color_continuous_scale="Plasma"
                                )
                                st.plotly_chart(fig2, use_container_width=True)

                            # Tabla de comparación
                            st.markdown("### 📊 Tabla Comparativa")
                            st.dataframe(df.set_index("Género"), use_container_width=True)

                            # Rankings
                            if "comparison" in data and "rankings" in data["comparison"]:
                                st.markdown("### 🏆 Rankings")
                                rankings = data["comparison"]["rankings"]

                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.markdown("**🔥 Más Popular**")
                                    for i, genre in enumerate(rankings.get("by_popularity", [])[:3], 1):
                                        st.write(f"{i}. {genre.title()}")

                                with col2:
                                    st.markdown("**⚡ Más Energético**")
                                    for i, genre in enumerate(rankings.get("by_energy", [])[:3], 1):
                                        st.write(f"{i}. {genre.title()}")

                                with col3:
                                    st.markdown("**💃 Más Bailable**")
                                    for i, genre in enumerate(rankings.get("by_danceability", [])[:3], 1):
                                        st.write(f"{i}. {genre.title()}")

                            # Underground gems
                            if "comparison" in data and "underground_gems" in data["comparison"]:
                                underground = data["comparison"]["underground_gems"]
                                if underground:
                                    st.markdown("### 💎 Underground Gems Encontrados")
                                    for gem in underground:
                                        st.success(f"✨ **{gem.title()}** - Género underground detectado")
            else:
                st.warning("Por favor ingresa al menos un género")

    # TAB 3: Análisis de Tendencias
    with tab3:
        st.subheader("📈 Análisis de Tendencias: Mainstream vs Underground")

        if st.button("🔍 Analizar Tendencias", key="analyze_trends"):
            with st.spinner("Analizando tendencias..."):
                result = api_request("/api/genres/trending")

                if result and result.get("status") == "success":
                    data = result.get("data", {})
                    insights = data.get("insights", {})

                    # Métricas comparativas
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 🎤 Mainstream")
                        st.metric(
                            "Popularidad Promedio",
                            f"{insights.get('mainstream_avg_popularity', 0):.1f}"
                        )

                    with col2:
                        st.markdown("### 💎 Underground")
                        st.metric(
                            "Popularidad Promedio",
                            f"{insights.get('underground_avg_popularity', 0):.1f}"
                        )

                    # Comparación de energía
                    if "energy_comparison" in insights:
                        energy_comp = insights["energy_comparison"]
                        st.markdown("### ⚡ Comparación de Energía")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Mainstream", f"{energy_comp.get('mainstream_avg_energy', 0):.2f}")
                        with col2:
                            st.metric("Underground", f"{energy_comp.get('underground_avg_energy', 0):.2f}")
                        with col3:
                            winner = energy_comp.get('energy_winner', 'N/A')
                            st.metric("Ganador", winner.title())

                    # Datos completos
                    with st.expander("📋 Ver análisis completo"):
                        st.markdown("#### 🎤 Géneros Mainstream Analizados")
                        mainstream_analysis = data.get("mainstream_analysis", {})
                        mainstream_genres = mainstream_analysis.get("genres", {})

                        if mainstream_genres:
                            mainstream_list = []
                            for genre_name, genre_data in mainstream_genres.items():
                                if "error" not in genre_data:
                                    mainstream_list.append({
                                        "Género": genre_name.title(),
                                        "Popularidad": f"{genre_data.get('avg_popularity', 0):.1f}",
                                        "Energía": f"{genre_data.get('avg_energy', 0):.2f}",
                                        "Bailabilidad": f"{genre_data.get('avg_danceability', 0):.2f}",
                                        "Tracks": genre_data.get('tracks_analyzed', 0)
                                    })

                            if mainstream_list:
                                st.dataframe(pd.DataFrame(mainstream_list), hide_index=True, use_container_width=True)

                        st.markdown("#### 💎 Géneros Underground Analizados")
                        underground_analysis = data.get("underground_analysis", {})
                        underground_genres = underground_analysis.get("genres", {})

                        if underground_genres:
                            underground_list = []
                            for genre_name, genre_data in underground_genres.items():
                                if "error" not in genre_data:
                                    underground_list.append({
                                        "Género": genre_name.title(),
                                        "Popularidad": f"{genre_data.get('avg_popularity', 0):.1f}",
                                        "Energía": f"{genre_data.get('avg_energy', 0):.2f}",
                                        "Bailabilidad": f"{genre_data.get('avg_danceability', 0):.2f}",
                                        "Tracks": genre_data.get('tracks_analyzed', 0)
                                    })

                            if underground_list:
                                st.dataframe(pd.DataFrame(underground_list), hide_index=True, use_container_width=True)

# ============================================================================
# PÁGINA DE COMPARACIÓN DE ARTISTAS
# ============================================================================
elif page == "🥊 Comparación de Artistas":
    st.title("🥊 Comparación de Artistas")

    tab1, tab2, tab3 = st.tabs(["Búsqueda y Análisis", "Comparación Múltiple", "BreakBeat Battle"])

    # TAB 1: Búsqueda y Análisis
    with tab1:
        st.subheader("🔍 Buscar y Analizar Artista")

        artist_name = st.text_input(
            "Nombre del artista",
            placeholder="Ej: Pendulum, The Prodigy, Daft Punk...",
            key="search_artist"
        )

        col1, col2 = st.columns(2)

        with col1:
            search_btn = st.button("🔍 Buscar", key="btn_search")

        with col2:
            analyze_btn = st.button("📊 Análisis Completo", key="btn_analyze")

        if search_btn and artist_name:
            with st.spinner(f"Buscando {artist_name}..."):
                result = api_request("/api/artists/search", params={"name": artist_name})

                if result and result.get("status") == "success":
                    data = result.get("data", {})

                    st.success(f"✅ Artista encontrado: **{data.get('name')}**")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Popularidad", data.get("popularity", 0))
                    with col2:
                        st.metric("Seguidores", f"{data.get('followers', 0):,}")
                    with col3:
                        genres = data.get("genres", [])
                        st.write(f"**Géneros:** {', '.join(genres[:3])}")

        if analyze_btn and artist_name:
            with st.spinner(f"Analizando {artist_name}..."):
                result = api_request(f"/api/artists/analyze/{artist_name}")

                if result and result.get("status") == "success":
                    data = result.get("data", {})

                    st.markdown(f"## 🎤 {data.get('name')}")

                    # Métricas principales
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Popularidad", data.get("popularity", 0))
                    with col2:
                        st.metric("Seguidores", f"{data.get('followers', 0):,}")
                    with col3:
                        top_tracks = data.get("top_tracks", [])
                        st.metric("Top Tracks", len(top_tracks))
                    with col4:
                        genres = data.get("genres", [])
                        st.metric("Géneros", len(genres))

                    # Géneros
                    if genres:
                        st.markdown("### 🎵 Géneros")
                        st.write(", ".join([g.title() for g in genres]))

                    # Top Tracks
                    if top_tracks:
                        st.markdown("### 🎵 Top Tracks")

                        tracks_data = []
                        for track in top_tracks[:10]:
                            tracks_data.append({
                                "Track": track.get("name", "N/A"),
                                "Popularidad": track.get("popularity", 0),
                                "Duración (min)": round(track.get("duration_ms", 0) / 60000, 2)
                            })

                        if tracks_data:
                            df = pd.DataFrame(tracks_data)
                            st.dataframe(df, use_container_width=True)

                    # Métricas de audio promedio
                    if "avg_audio_features" in data:
                        st.markdown("### 📊 Características de Audio Promedio")
                        features = data["avg_audio_features"]

                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric("Energía", f"{features.get('energy', 0):.2f}")
                        with col2:
                            st.metric("Bailabilidad", f"{features.get('danceability', 0):.2f}")
                        with col3:
                            st.metric("Valencia", f"{features.get('valence', 0):.2f}")
                        with col4:
                            st.metric("Tempo", f"{features.get('tempo', 0):.0f} BPM")

    # TAB 2: Comparación Múltiple
    with tab2:
        st.subheader("🥊 Compara Múltiples Artistas")

        artists_input = st.text_input(
            "Artistas a comparar (separados por coma, máx 5)",
            placeholder="Ej: Pendulum, The Prodigy, The Chemical Brothers",
            key="compare_artists"
        )

        if st.button("🔍 Comparar", key="btn_compare_multi"):
            if artists_input:
                with st.spinner("Comparando artistas..."):
                    result = api_request("/api/artists/compare", params={"artists": artists_input})

                    if result and result.get("status") == "success":
                        data = result.get("data", {})
                        detailed_data = data.get("detailed_data", {})
                        comparison = data.get("comparison", {})

                        # Crear DataFrame para comparación
                        comparison_list = []
                        for artist_name, artist_info in detailed_data.items():
                            comparison_list.append({
                                "Artista": artist_name,
                                "Popularidad": artist_info.get("popularity", 0),
                                "Seguidores": artist_info.get("followers", 0),
                                "Top Tracks": len(artist_info.get("top_tracks", []))
                            })

                        if comparison_list:
                            df = pd.DataFrame(comparison_list)

                            # Gráficos de comparación
                            col1, col2 = st.columns(2)

                            with col1:
                                fig1 = px.bar(
                                    df,
                                    x="Artista",
                                    y="Popularidad",
                                    title="Popularidad por Artista",
                                    color="Popularidad",
                                    color_continuous_scale="Viridis"
                                )
                                st.plotly_chart(fig1, use_container_width=True)

                            with col2:
                                fig2 = px.bar(
                                    df,
                                    x="Artista",
                                    y="Seguidores",
                                    title="Seguidores por Artista",
                                    color="Seguidores",
                                    color_continuous_scale="Plasma"
                                )
                                st.plotly_chart(fig2, use_container_width=True)

                            # Tabla comparativa
                            st.markdown("### 📊 Tabla Comparativa")
                            st.dataframe(df.set_index("Artista"), use_container_width=True)

                            # Ganadores
                            if "winners" in comparison:
                                st.markdown("### 🏆 Ganadores")
                                winners = comparison["winners"]

                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.success(f"**Popularidad:** {winners.get('popularity', 'N/A')}")
                                with col2:
                                    st.success(f"**Seguidores:** {winners.get('followers', 'N/A')}")
                                with col3:
                                    st.success(f"**Energía:** {winners.get('energy', 'N/A')}")

                            # Insights
                            if "insights" in comparison:
                                st.markdown("### 💡 Insights")
                                for insight in comparison["insights"]:
                                    st.info(insight)
            else:
                st.warning("Por favor ingresa al menos 2 artistas")

    # TAB 3: BreakBeat Battle
    with tab3:
        st.subheader("🎵 BreakBeat Battle")
        st.write("Compara los artistas más icónicos del BreakBeat")

        if st.button("⚡ Iniciar Battle", key="btn_breakbeat"):
            with st.spinner("Preparando la batalla..."):
                result = api_request("/api/artists/compare/breakbeat")

                if result and result.get("status") == "success":
                    data = result.get("data", {})
                    detailed_data = data.get("detailed_data", {})
                    comparison = data.get("comparison", {})

                    st.success("✅ Batalla iniciada: The Prodigy vs Pendulum vs The Chemical Brothers")

                    # Crear DataFrame para comparación
                    comparison_list = []
                    for artist_name, artist_info in detailed_data.items():
                        comparison_list.append({
                            "Artista": artist_name,
                            "Popularidad": artist_info.get("popularity", 0),
                            "Seguidores": artist_info.get("followers", 0),
                            "Energía Promedio": artist_info.get("avg_audio_features", {}).get("energy", 0)
                        })

                    if comparison_list:
                        df = pd.DataFrame(comparison_list)

                        # Gráfico de radar comparativo
                        st.markdown("### 📊 Comparación Visual")

                        fig = go.Figure()

                        for artist_name, artist_info in detailed_data.items():
                            features = artist_info.get("avg_audio_features", {})

                            fig.add_trace(go.Scatterpolar(
                                r=[
                                    artist_info.get("popularity", 0) / 100,
                                    features.get("energy", 0),
                                    features.get("danceability", 0),
                                    features.get("valence", 0),
                                    features.get("acousticness", 0)
                                ],
                                theta=['Popularidad', 'Energía', 'Bailabilidad', 'Valencia', 'Acústica'],
                                fill='toself',
                                name=artist_name
                            ))

                        fig.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                            showlegend=True,
                            height=600
                        )

                        st.plotly_chart(fig, use_container_width=True)

                        # Tabla comparativa
                        st.markdown("### 📊 Estadísticas")
                        st.dataframe(df.set_index("Artista"), use_container_width=True)

                        # Ganadores
                        if "winners" in comparison:
                            st.markdown("### 🏆 Ganadores")
                            winners = comparison["winners"]

                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.success(f"**🔥 Popularidad**\n\n{winners.get('popularity', 'N/A')}")
                            with col2:
                                st.success(f"**👥 Seguidores**\n\n{winners.get('followers', 'N/A')}")
                            with col3:
                                st.success(f"**⚡ Energía**\n\n{winners.get('energy', 'N/A')}")

# ============================================================================
# PÁGINA DE UNDERGROUND GEMS
# ============================================================================
elif page == "💎 Underground Gems":
    st.title("💎 Underground Gems Finder")
    st.write("Descubre géneros underground con alto potencial")

    if st.button("🔍 Buscar Underground Gems", key="find_gems"):
        with st.spinner("Buscando géneros underground..."):
            result = api_request("/api/genres/underground")

            if result and result.get("status") == "success":
                data = result.get("data", {})
                underground_genres = data.get("underground_genres", [])

                st.success(f"✅ Se encontraron {len(underground_genres)} géneros underground")

                if underground_genres:
                    for genre in underground_genres:
                        with st.expander(f"💎 {genre.get('name', 'N/A').title()}", expanded=True):
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.metric("Popularidad", f"{genre.get('avg_popularity', 0):.1f}")
                            with col2:
                                st.metric("Energía", f"{genre.get('avg_energy', 0):.2f}")
                            with col3:
                                st.metric("Bailabilidad", f"{genre.get('avg_danceability', 0):.2f}")

                            st.write(f"**Reason:** {genre.get('reason', 'N/A')}")
                else:
                    st.info("No se encontraron géneros underground en esta búsqueda")

                # Métricas generales
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Total Analizados", data.get("total_analyzed", 0))
                with col2:
                    st.metric("Gems Encontrados", data.get("gems_found", 0))

# ============================================================================
# PÁGINA DE BATALLA 1v1
# ============================================================================
elif page == "⚔️ Batalla 1v1":
    st.title("⚔️ Batalla 1 vs 1")
    st.write("Comparación directa entre dos artistas")

    col1, col2 = st.columns(2)

    with col1:
        artist1 = st.text_input(
            "Artista 1",
            placeholder="Ej: Pendulum",
            key="artist1_vs"
        )

    with col2:
        artist2 = st.text_input(
            "Artista 2",
            placeholder="Ej: The Prodigy",
            key="artist2_vs"
        )

    if st.button("⚔️ Iniciar Batalla", key="btn_vs"):
        if artist1 and artist2:
            with st.spinner(f"Preparando batalla: {artist1} vs {artist2}..."):
                result = api_request("/api/artists/vs", params={"artist1": artist1, "artist2": artist2})

                if result and result.get("status") == "success":
                    data = result.get("data", {})

                    st.markdown(f"## {data.get('matchup', 'N/A')}")
                    st.markdown("---")

                    # Comparación lado a lado
                    col1, col2 = st.columns(2)

                    artist1_data = data.get(artist1, {})
                    artist2_data = data.get(artist2, {})

                    with col1:
                        st.markdown(f"### 🎤 {artist1}")
                        st.metric("Popularidad", artist1_data.get("popularity", 0))
                        st.metric("Seguidores", f"{artist1_data.get('followers', 0):,}")

                        top_track = artist1_data.get("top_track", {})
                        if top_track:
                            st.write(f"**Top Track:** {top_track.get('name', 'N/A')}")

                        genres = artist1_data.get("genres", [])
                        if genres:
                            st.write(f"**Géneros:** {', '.join(genres)}")

                    with col2:
                        st.markdown(f"### 🎤 {artist2}")
                        st.metric("Popularidad", artist2_data.get("popularity", 0))
                        st.metric("Seguidores", f"{artist2_data.get('followers', 0):,}")

                        top_track = artist2_data.get("top_track", {})
                        if top_track:
                            st.write(f"**Top Track:** {top_track.get('name', 'N/A')}")

                        genres = artist2_data.get("genres", [])
                        if genres:
                            st.write(f"**Géneros:** {', '.join(genres)}")

                    # Ganadores
                    st.markdown("---")
                    st.markdown("### 🏆 Ganadores por Categoría")

                    winners = data.get("winners", {})

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.success(f"**🔥 Popularidad**\n\n{winners.get('popularity', 'N/A')}")
                    with col2:
                        st.success(f"**👥 Seguidores**\n\n{winners.get('followers', 'N/A')}")
                    with col3:
                        st.success(f"**⚡ Energía**\n\n{winners.get('energy', 'N/A')}")

                    # Insights
                    if "insights" in data:
                        st.markdown("### 💡 Insights")
                        for insight in data["insights"]:
                            st.info(insight)
        else:
            st.warning("Por favor ingresa los nombres de ambos artistas")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>🎵 Spotify Analytics - Powered by Streamlit & FastAPI</p>
    </div>
    """,
    unsafe_allow_html=True
)
