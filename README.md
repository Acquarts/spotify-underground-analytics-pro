# Spotify Analytics Pro

Sistema profesional de análisis musical que utiliza la API de Spotify para proporcionar insights profundos sobre tendencias de géneros musicales y comparación de artistas, con especialización en géneros underground como BreakBeat.

## Descripción del Proyecto

Spotify Analytics Pro es una plataforma de análisis de datos musicales diseñada para identificar tendencias de mercado, comparar artistas y descubrir géneros emergentes. El sistema está optimizado para detectar automáticamente música underground basándose en métricas como popularidad, energía y presencia en playlists.

### Casos de Uso

- **Análisis de Mercado Musical**: Identificar géneros en crecimiento o declive
- **Comparación de Artistas**: Analizar métricas de múltiples artistas simultáneamente
- **Detección de Underground Gems**: Encontrar géneros y artistas con potencial pero baja visibilidad mainstream
- **Investigación Musical**: Análisis histórico de tendencias con datos almacenados en base de datos
- **A&R y Labels**: Herramienta para descubrir talento emergente

## Características Principales

### Análisis de Géneros Musicales
- Análisis individual de géneros específicos (BreakBeat, Pop, Electronic, etc.)
- Comparación de múltiples géneros simultáneamente
- Detección automática de géneros underground basada en algoritmos
- Métricas avanzadas: popularidad, energía, bailabilidad, valencia, tempo
- Tendencias comparativas mainstream vs underground

### Comparación de Artistas
- Búsqueda y análisis de artistas por nombre
- Comparación de hasta 5 artistas simultáneamente
- Métricas detalladas: popularidad, seguidores, top tracks, géneros
- Análisis de audio features de los tracks más populares
- Detección de "dark horses" (artistas con potencial oculto)
- Comparaciones predefinidas (ej: artistas icónicos de BreakBeat)
- Modo 1v1 para comparaciones directas

### Almacenamiento de Datos
- Base de datos PostgreSQL para análisis histórico
- Snapshots diarios de géneros y artistas
- Seguimiento de evolución temporal de métricas
- Consultas optimizadas con índices

## Stack Tecnológico

### Backend
- **FastAPI** (0.104.1) - Framework web moderno para Python
- **Python** (3.11) - Lenguaje principal
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Spotipy** (2.23.0) - Cliente oficial de Spotify API
- **SQLAlchemy** (2.0.23) - ORM para base de datos
- **Pydantic** (2.5.2) - Validación de datos y settings
- **NumPy** (1.25.2) - Procesamiento numérico
- **Pandas** (2.1.4) - Análisis de datos

### Base de Datos
- **PostgreSQL** (15) - Base de datos relacional principal
- **Redis** (7-alpine) - Sistema de caché (preparado para uso futuro)

### Infraestructura
- **Docker** & **Docker Compose** - Containerización completa
- **Nginx** (configurado para producción)
- Sistema de health checks integrado

### APIs Externas
- **Spotify Web API** - Fuente principal de datos musicales

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  API Endpoints │  │    Services     │  │    Models    │ │
│  │                │  │                 │  │              │ │
│  │  /api/genres   │──│ GenreAnalyzer   │──│  Genre DB    │ │
│  │  /api/artists  │──│ArtistComparator │──│  Artist DB   │ │
│  └────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │      Spotify Web API          │
              │  (Client Credentials Flow)    │
              └───────────────────────────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │   PostgreSQL Database │
                  │   - genre_snapshots   │
                  │   - genre_trends      │
                  │   - artists           │
                  │   - artist_snapshots  │
                  └───────────────────────┘
```

### Estructura de Directorios

```
spotify-analytics/
├── backend/
│   ├── app/
│   │   ├── api/              # Endpoints REST
│   │   │   ├── genres.py     # Análisis de géneros
│   │   │   └── artists.py    # Comparación de artistas
│   │   ├── core/             # Configuración base
│   │   │   └── database.py   # Setup SQLAlchemy
│   │   ├── models/           # Modelos de datos
│   │   │   ├── genre.py      # Tablas de géneros
│   │   │   └── artist.py     # Tablas de artistas
│   │   ├── services/         # Lógica de negocio
│   │   │   ├── genre_analyzer.py
│   │   │   └── artist_comparator.py
│   │   └── main.py           # Aplicación principal
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .env
└── README.md
```

## Instalación y Configuración

### Prerrequisitos

- Docker Desktop instalado y corriendo
- Cuenta de Spotify Developer (gratuita)
- 8GB RAM disponible

### Paso 1: Obtener Credenciales de Spotify

1. Ve a [Spotify for Developers](https://developer.spotify.com/dashboard)
2. Inicia sesión con tu cuenta de Spotify
3. Haz click en "Create App"
4. Completa el formulario:
   - **App name**: "Spotify Analytics"
   - **App description**: "Proyecto de análisis musical"
   - **Redirect URI**: `http://localhost`
5. Guarda la app
6. Copia el **Client ID** y **Client Secret**

### Paso 2: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Credenciales de Spotify
SPOTIFY_CLIENT_ID=tu_client_id_aqui
SPOTIFY_CLIENT_SECRET=tu_client_secret_aqui

# Base de datos
DATABASE_URL=postgresql://spotify_user:spotify_pass@postgres:5432/spotify_analytics

# Redis
REDIS_URL=redis://redis:6379

# Seguridad
SECRET_KEY=tu-clave-secreta-aleatoria

# Configuración
LOG_LEVEL=INFO
```

### Paso 3: Iniciar la Aplicación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd spotify-analytics

# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend
```

### Paso 4: Verificar Instalación

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Root**: http://localhost:8000

## Uso de la API

### Documentación Interactiva

La API incluye documentación automática con Swagger UI en:
```
http://localhost:8000/docs
```

### Endpoints Principales

#### Análisis de Géneros

**Analizar un género específico:**
```bash
GET /api/genres/analyze/{genre}

# Ejemplo:
curl http://localhost:8000/api/genres/analyze/breakbeat
```

**Comparar múltiples géneros:**
```bash
GET /api/genres/analyze/multiple?genres=breakbeat,electronic,pop

# Respuesta incluye rankings y comparaciones
```

**Encontrar géneros underground:**
```bash
GET /api/genres/underground

# Detecta automáticamente géneros con baja popularidad pero alta energía
```

**Comparar dos géneros:**
```bash
GET /api/genres/compare?genre1=breakbeat&genre2=pop
```

#### Comparación de Artistas

**Buscar un artista:**
```bash
GET /api/artists/search?name=Pendulum

# Retorna información básica del artista
```

**Analizar un artista en detalle:**
```bash
GET /api/artists/analyze/Pendulum

# Incluye top tracks, géneros, métricas de audio
```

**Comparar múltiples artistas:**
```bash
GET /api/artists/compare?artists=Pendulum,The Prodigy,The Chemical Brothers

# Compara hasta 5 artistas simultáneamente
# Incluye rankings, ganadores e insights automáticos
```

**Comparación 1 vs 1:**
```bash
GET /api/artists/vs?artist1=Pendulum&artist2=The Prodigy

# Formato simplificado para comparación directa
```

**Comparar artistas de BreakBeat:**
```bash
GET /api/artists/compare/breakbeat

# Compara artistas icónicos: The Prodigy, Pendulum, The Chemical Brothers
```

### Ejemplos de Respuestas

#### Análisis de Género
```json
{
  "status": "success",
  "data": {
    "genre": "breakbeat",
    "tracks_analyzed": 20,
    "playlist_presence": 8,
    "avg_popularity": 32.1,
    "avg_energy": 0.78,
    "avg_tempo": 145.5,
    "top_tracks": [
      {
        "name": "Out of Space",
        "artist": "The Prodigy",
        "popularity": 68
      }
    ]
  }
}
```

#### Comparación de Artistas
```json
{
  "status": "success",
  "data": {
    "artists_compared": ["Pendulum", "The Prodigy"],
    "comparison": {
      "winners": {
        "popularity": {"artist": "The Prodigy", "value": 72},
        "followers": {"artist": "The Prodigy", "value": 2500000}
      },
      "insights": [
        "The Prodigy lidera en popularidad con 72 puntos",
        "Pendulum es más energético con 0.85 de energía"
      ]
    }
  }
}
```

## Modelo de Datos

### Tablas Principales

**genre_snapshots**
- Snapshots diarios de métricas por género
- Campos: avg_popularity, avg_energy, avg_danceability, avg_tempo, etc.

**artists**
- Información básica de artistas
- Campos: id, name, popularity, followers, genres

**artist_snapshots**
- Evolución histórica de métricas de artistas
- Campos: popularity, followers, avg_energy, consistency_score

## Limitaciones Conocidas

### Modo Development de Spotify

El proyecto está configurado para funcionar con Spotify en modo Development, que tiene las siguientes limitaciones:

- **Rate Limiting**: 25 peticiones por segundo máximo
- **Datos Limitados**: Máximo 20-50 tracks por análisis
- **Audio Features**: Puede fallar con error 403 en algunos casos
- **Delays**: Se incluyen delays de 0.3-1 segundo entre peticiones

Para producción con más datos, se recomienda solicitar "Extended Quota Mode" en el dashboard de Spotify Developer.

### Optimizaciones Implementadas

- Reducción de tracks analizados (20 vs 50)
- Delays entre peticiones para evitar rate limiting
- Peticiones en lotes pequeños
- Manejo de errores robusto con fallbacks

## Comandos Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f backend

# Parar servicios
docker-compose down

# Reconstruir después de cambios en código
docker-compose up --build

# Acceder a la base de datos
docker-compose exec postgres psql -U spotify_user -d spotify_analytics

# Ver estado de containers
docker ps

# Limpiar todo (incluyendo volúmenes)
docker-compose down -v
```

## Mejoras Futuras

- [ ] Solicitar Extended Quota Mode de Spotify
- [ ] Añadir sistema de caché con Redis para reducir llamadas a Spotify
- [ ] Implementar sistema de usuarios y autenticación
- [ ] Crear dashboard frontend con visualizaciones
- [ ] Añadir análisis predictivo con machine learning
- [ ] Exportar reportes en PDF/Excel
- [ ] Integración con otras plataformas (Apple Music, YouTube Music)
- [ ] Sistema de alertas para nuevos lanzamientos de artistas seguidos

## Tecnologías Aprendidas

Este proyecto demuestra competencias en:

- **API Development**: Diseño e implementación de REST APIs profesionales
- **Data Engineering**: Pipeline de extracción, transformación y carga de datos
- **Base de Datos**: Modelado relacional y optimización de queries
- **Containerización**: Docker y orquestación de servicios
- **Integración de APIs**: Consumo de APIs externas con manejo de rate limiting
- **Análisis de Datos**: Procesamiento y agregación de métricas musicales
- **Arquitectura de Software**: Estructura modular y separación de responsabilidades

## Licencia

MIT License - Ver archivo LICENSE para más detalles

## Autor

Proyecto desarrollado como demostración de habilidades en data science y desarrollo backend.

## Agradecimientos

- Spotify por proporcionar una API robusta y bien documentada
- FastAPI por el excelente framework web
- La comunidad open source por las herramientas utilizadas

---

**Nota**: Este proyecto está optimizado para Spotify Development Mode. Para uso en producción con mayor volumen de datos, se recomienda solicitar Extended Quota Mode en el Spotify Developer Dashboard.# Spotify Analytics Pro

Sistema profesional de análisis musical que utiliza la API de Spotify para proporcionar insights profundos sobre tendencias de géneros musicales y comparación de artistas, con especialización en géneros underground como BreakBeat.

## Descripción del Proyecto

Spotify Analytics Pro es una plataforma de análisis de datos musicales diseñada para identificar tendencias de mercado, comparar artistas y descubrir géneros emergentes. El sistema está optimizado para detectar automáticamente música underground basándose en métricas como popularidad, energía y presencia en playlists.

### Casos de Uso

- **Análisis de Mercado Musical**: Identificar géneros en crecimiento o declive
- **Comparación de Artistas**: Analizar métricas de múltiples artistas simultáneamente
- **Detección de Underground Gems**: Encontrar géneros y artistas con potencial pero baja visibilidad mainstream
- **Investigación Musical**: Análisis histórico de tendencias con datos almacenados en base de datos
- **A&R y Labels**: Herramienta para descubrir talento emergente

## Características Principales

### Análisis de Géneros Musicales
- Análisis individual de géneros específicos (BreakBeat, Pop, Electronic, etc.)
- Comparación de múltiples géneros simultáneamente
- Detección automática de géneros underground basada en algoritmos
- Métricas avanzadas: popularidad, energía, bailabilidad, valencia, tempo
- Tendencias comparativas mainstream vs underground

### Comparación de Artistas
- Búsqueda y análisis de artistas por nombre
- Comparación de hasta 5 artistas simultáneamente
- Métricas detalladas: popularidad, seguidores, top tracks, géneros
- Análisis de audio features de los tracks más populares
- Detección de "dark horses" (artistas con potencial oculto)
- Comparaciones predefinidas (ej: artistas icónicos de BreakBeat)
- Modo 1v1 para comparaciones directas

### Almacenamiento de Datos
- Base de datos PostgreSQL para análisis histórico
- Snapshots diarios de géneros y artistas
- Seguimiento de evolución temporal de métricas
- Consultas optimizadas con índices

## Stack Tecnológico

### Backend
- **FastAPI** (0.104.1) - Framework web moderno para Python
- **Python** (3.11) - Lenguaje principal
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Spotipy** (2.23.0) - Cliente oficial de Spotify API
- **SQLAlchemy** (2.0.23) - ORM para base de datos
- **Pydantic** (2.5.2) - Validación de datos y settings
- **NumPy** (1.25.2) - Procesamiento numérico
- **Pandas** (2.1.4) - Análisis de datos

### Base de Datos
- **PostgreSQL** (15) - Base de datos relacional principal
- **Redis** (7-alpine) - Sistema de caché (preparado para uso futuro)

### Infraestructura
- **Docker** & **Docker Compose** - Containerización completa
- **Nginx** (configurado para producción)
- Sistema de health checks integrado

### APIs Externas
- **Spotify Web API** - Fuente principal de datos musicales

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  API Endpoints │  │    Services     │  │    Models    │ │
│  │                │  │                 │  │              │ │
│  │  /api/genres   │──│ GenreAnalyzer   │──│  Genre DB    │ │
│  │  /api/artists  │──│ArtistComparator │──│  Artist DB   │ │
│  └────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │      Spotify Web API          │
              │  (Client Credentials Flow)    │
              └───────────────────────────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │   PostgreSQL Database │
                  │   - genre_snapshots   │
                  │   - genre_trends      │
                  │   - artists           │
                  │   - artist_snapshots  │
                  └───────────────────────┘
```

### Estructura de Directorios

```
spotify-analytics/
├── backend/
│   ├── app/
│   │   ├── api/              # Endpoints REST
│   │   │   ├── genres.py     # Análisis de géneros
│   │   │   └── artists.py    # Comparación de artistas
│   │   ├── core/             # Configuración base
│   │   │   └── database.py   # Setup SQLAlchemy
│   │   ├── models/           # Modelos de datos
│   │   │   ├── genre.py      # Tablas de géneros
│   │   │   └── artist.py     # Tablas de artistas
│   │   ├── services/         # Lógica de negocio
│   │   │   ├── genre_analyzer.py
│   │   │   └── artist_comparator.py
│   │   └── main.py           # Aplicación principal
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .env
└── README.md
```

## Instalación y Configuración

### Prerrequisitos

- Docker Desktop instalado y corriendo
- Cuenta de Spotify Developer (gratuita)
- 8GB RAM disponible

### Paso 1: Obtener Credenciales de Spotify

1. Ve a [Spotify for Developers](https://developer.spotify.com/dashboard)
2. Inicia sesión con tu cuenta de Spotify
3. Haz click en "Create App"
4. Completa el formulario:
   - **App name**: "Spotify Analytics"
   - **App description**: "Proyecto de análisis musical"
   - **Redirect URI**: `http://localhost`
5. Guarda la app
6. Copia el **Client ID** y **Client Secret**

### Paso 2: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Credenciales de Spotify
SPOTIFY_CLIENT_ID=tu_client_id_aqui
SPOTIFY_CLIENT_SECRET=tu_client_secret_aqui

# Base de datos
DATABASE_URL=postgresql://spotify_user:spotify_pass@postgres:5432/spotify_analytics

# Redis
REDIS_URL=redis://redis:6379

# Seguridad
SECRET_KEY=tu-clave-secreta-aleatoria

# Configuración
LOG_LEVEL=INFO
```

### Paso 3: Iniciar la Aplicación

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd spotify-analytics

# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend
```

### Paso 4: Verificar Instalación

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Root**: http://localhost:8000

## Uso de la API

### Documentación Interactiva

La API incluye documentación automática con Swagger UI en:
```
http://localhost:8000/docs
```

### Endpoints Principales

#### Análisis de Géneros

**Analizar un género específico:**
```bash
GET /api/genres/analyze/{genre}

# Ejemplo:
curl http://localhost:8000/api/genres/analyze/breakbeat
```

**Comparar múltiples géneros:**
```bash
GET /api/genres/analyze/multiple?genres=breakbeat,electronic,pop

# Respuesta incluye rankings y comparaciones
```

**Encontrar géneros underground:**
```bash
GET /api/genres/underground

# Detecta automáticamente géneros con baja popularidad pero alta energía
```

**Comparar dos géneros:**
```bash
GET /api/genres/compare?genre1=breakbeat&genre2=pop
```

#### Comparación de Artistas

**Buscar un artista:**
```bash
GET /api/artists/search?name=Pendulum

# Retorna información básica del artista
```

**Analizar un artista en detalle:**
```bash
GET /api/artists/analyze/Pendulum

# Incluye top tracks, géneros, métricas de audio
```

**Comparar múltiples artistas:**
```bash
GET /api/artists/compare?artists=Pendulum,The Prodigy,The Chemical Brothers

# Compara hasta 5 artistas simultáneamente
# Incluye rankings, ganadores e insights automáticos
```

**Comparación 1 vs 1:**
```bash
GET /api/artists/vs?artist1=Pendulum&artist2=The Prodigy

# Formato simplificado para comparación directa
```

**Comparar artistas de BreakBeat:**
```bash
GET /api/artists/compare/breakbeat

# Compara artistas icónicos: The Prodigy, Pendulum, The Chemical Brothers
```

### Ejemplos de Respuestas

#### Análisis de Género
```json
{
  "status": "success",
  "data": {
    "genre": "breakbeat",
    "tracks_analyzed": 20,
    "playlist_presence": 8,
    "avg_popularity": 32.1,
    "avg_energy": 0.78,
    "avg_tempo": 145.5,
    "top_tracks": [
      {
        "name": "Out of Space",
        "artist": "The Prodigy",
        "popularity": 68
      }
    ]
  }
}
```

#### Comparación de Artistas
```json
{
  "status": "success",
  "data": {
    "artists_compared": ["Pendulum", "The Prodigy"],
    "comparison": {
      "winners": {
        "popularity": {"artist": "The Prodigy", "value": 72},
        "followers": {"artist": "The Prodigy", "value": 2500000}
      },
      "insights": [
        "The Prodigy lidera en popularidad con 72 puntos",
        "Pendulum es más energético con 0.85 de energía"
      ]
    }
  }
}
```

## Modelo de Datos

### Tablas Principales

**genre_snapshots**
- Snapshots diarios de métricas por género
- Campos: avg_popularity, avg_energy, avg_danceability, avg_tempo, etc.

**artists**
- Información básica de artistas
- Campos: id, name, popularity, followers, genres

**artist_snapshots**
- Evolución histórica de métricas de artistas
- Campos: popularity, followers, avg_energy, consistency_score

## Limitaciones Conocidas

### Modo Development de Spotify

El proyecto está configurado para funcionar con Spotify en modo Development, que tiene las siguientes limitaciones:

- **Rate Limiting**: 25 peticiones por segundo máximo
- **Datos Limitados**: Máximo 20-50 tracks por análisis
- **Audio Features**: Puede fallar con error 403 en algunos casos
- **Delays**: Se incluyen delays de 0.3-1 segundo entre peticiones

Para producción con más datos, se recomienda solicitar "Extended Quota Mode" en el dashboard de Spotify Developer.

### Optimizaciones Implementadas

- Reducción de tracks analizados (20 vs 50)
- Delays entre peticiones para evitar rate limiting
- Peticiones en lotes pequeños
- Manejo de errores robusto con fallbacks

## Comandos Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f backend

# Parar servicios
docker-compose down

# Reconstruir después de cambios en código
docker-compose up --build

# Acceder a la base de datos
docker-compose exec postgres psql -U spotify_user -d spotify_analytics

# Ver estado de containers
docker ps

# Limpiar todo (incluyendo volúmenes)
docker-compose down -v
```

## Mejoras Futuras

- [ ] Solicitar Extended Quota Mode de Spotify
- [ ] Añadir sistema de caché con Redis para reducir llamadas a Spotify
- [ ] Implementar sistema de usuarios y autenticación
- [ ] Crear dashboard frontend con visualizaciones
- [ ] Añadir análisis predictivo con machine learning
- [ ] Exportar reportes en PDF/Excel
- [ ] Integración con otras plataformas (Apple Music, YouTube Music)
- [ ] Sistema de alertas para nuevos lanzamientos de artistas seguidos

## Tecnologías Aprendidas

Este proyecto demuestra competencias en:

- **API Development**: Diseño e implementación de REST APIs profesionales
- **Data Engineering**: Pipeline de extracción, transformación y carga de datos
- **Base de Datos**: Modelado relacional y optimización de queries
- **Containerización**: Docker y orquestación de servicios
- **Integración de APIs**: Consumo de APIs externas con manejo de rate limiting
- **Análisis de Datos**: Procesamiento y agregación de métricas musicales
- **Arquitectura de Software**: Estructura modular y separación de responsabilidades

## Licencia

MIT License - Ver archivo LICENSE para más detalles

## Autor

Proyecto desarrollado como demostración de habilidades en data science y desarrollo backend.

## Agradecimientos

- Spotify por proporcionar una API robusta y bien documentada
- FastAPI por el excelente framework web
- La comunidad open source por las herramientas utilizadas

---

**Nota**: Este proyecto está optimizado para Spotify Development Mode. Para uso en producción con mayor volumen de datos, se recomienda solicitar Extended Quota Mode en el Spotify Developer Dashboard.
