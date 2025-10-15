# 🎵 Spotify Analytics - Frontend con Streamlit

Aplicación web interactiva para análisis de géneros musicales y comparación de artistas usando la API de Spotify.

## 🚀 Características

### 🎯 Análisis de Géneros
- **Análisis Individual**: Analiza géneros específicos con métricas detalladas
- **Comparación Múltiple**: Compara hasta varios géneros simultáneamente
- **Tendencias**: Análisis de géneros mainstream vs underground
- **Visualizaciones**: Gráficos radar, barras y tablas comparativas

### 🥊 Comparación de Artistas
- **Búsqueda y Análisis**: Busca artistas y obtén análisis completos
- **Comparación Múltiple**: Compara hasta 5 artistas simultáneamente
- **BreakBeat Battle**: Compara artistas icónicos del género BreakBeat
- **Batalla 1v1**: Comparación directa entre dos artistas

### 💎 Underground Gems
- Detector automático de géneros underground
- Análisis de potencial de géneros nicho
- Métricas especializadas para música alternativa

## 📋 Requisitos

- Python 3.8+
- Backend FastAPI corriendo (ver instrucciones abajo)
- Credenciales de Spotify API

## 🔧 Instalación

### 1. Clonar el repositorio (si aún no lo has hecho)

```bash
cd spotify-analytics
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (si no existe):

```env
SPOTIFY_CLIENT_ID=tu_client_id
SPOTIFY_CLIENT_SECRET=tu_client_secret
API_BASE_URL=http://localhost:8000
```

### 4. Iniciar el backend (FastAPI)

En una terminal separada:

```bash
cd backend
uvicorn app.main:app --reload
```

El backend estará disponible en `http://localhost:8000`

### 5. Iniciar el frontend (Streamlit)

En otra terminal:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📱 Uso de la Aplicación

### Navegación Principal

La aplicación tiene 5 secciones principales accesibles desde el sidebar:

1. **🏠 Inicio**: Información general y estadísticas rápidas
2. **🎯 Análisis de Géneros**: Análisis individual, comparaciones y tendencias
3. **🥊 Comparación de Artistas**: Búsqueda, análisis y comparaciones
4. **💎 Underground Gems**: Descubre géneros underground
5. **⚔️ Batalla 1v1**: Comparación directa entre artistas

### Análisis de Géneros

#### Análisis Individual
1. Ingresa el nombre de un género (ej: "breakbeat", "electronic", "pop")
2. Haz clic en "Analizar Género"
3. Visualiza métricas como popularidad, energía, bailabilidad
4. Explora el gráfico radar con características del género

#### Comparación Múltiple
1. Ingresa varios géneros separados por coma
2. Compara métricas entre todos los géneros
3. Visualiza rankings de popularidad, energía y bailabilidad
4. Detecta automáticamente géneros underground

#### Análisis de Tendencias
1. Haz clic en "Analizar Tendencias"
2. Compara géneros mainstream vs underground
3. Visualiza diferencias en popularidad y energía

### Comparación de Artistas

#### Búsqueda y Análisis
1. Ingresa el nombre de un artista
2. "Buscar": Información básica
3. "Análisis Completo": Métricas detalladas, top tracks, géneros

#### Comparación Múltiple
1. Ingresa hasta 5 artistas separados por coma
2. Compara popularidad, seguidores y métricas de audio
3. Visualiza ganadores por categoría
4. Lee insights generados automáticamente

#### BreakBeat Battle
1. Haz clic en "Iniciar Battle"
2. Compara The Prodigy, Pendulum y The Chemical Brothers
3. Visualiza gráfico radar comparativo
4. Descubre los ganadores en cada categoría

### Batalla 1v1
1. Ingresa dos artistas en los campos correspondientes
2. Haz clic en "Iniciar Batalla"
3. Comparación lado a lado con métricas clave
4. Visualiza ganadores por categoría

### Underground Gems
1. Haz clic en "Buscar Underground Gems"
2. Descubre géneros underground automáticamente
3. Visualiza métricas de cada género encontrado
4. Lee las razones por las que se consideran underground

## 🎨 Características de la Interfaz

- **Diseño responsivo**: Se adapta a diferentes tamaños de pantalla
- **Tema Spotify**: Colores inspirados en la marca Spotify (#1DB954)
- **Gráficos interactivos**: Usando Plotly para visualizaciones dinámicas
- **Tabs organizados**: Navegación intuitiva por pestañas
- **Métricas destacadas**: Cards con información clave
- **Spinner de carga**: Feedback visual durante peticiones a la API

## 🛠️ Configuración Avanzada

### Cambiar URL de la API

Puedes cambiar la URL del backend desde el sidebar de la aplicación en "Configuración".

### Verificar Estado de la API

Usa el botón "🔍 Verificar API" en el sidebar para comprobar:
- Estado de conexión con la base de datos
- Estado de conexión con Spotify API
- Features disponibles

## 🐛 Troubleshooting

### El frontend no se conecta al backend
- Verifica que el backend esté corriendo en `http://localhost:8000`
- Revisa la URL configurada en el sidebar
- Comprueba que no haya errores en la consola del backend

### No se encuentran artistas o géneros
- Verifica que las credenciales de Spotify API estén configuradas
- Revisa el estado de la API con el botón "Verificar API"
- Comprueba que la base de datos esté conectada

### Errores de visualización
- Asegúrate de tener instaladas todas las dependencias (`pip install -r requirements.txt`)
- Limpia la caché de Streamlit: `Ctrl + R` o `Cmd + R`

## 📊 Métricas Disponibles

### Géneros
- **Popularidad**: Nivel de popularidad promedio (0-100)
- **Energía**: Intensidad y actividad percibida (0-1)
- **Bailabilidad**: Qué tan adecuado es para bailar (0-1)
- **Valencia**: Positividad musical (0-1)
- **Acústica**: Presencia de instrumentos acústicos (0-1)
- **Instrumental**: Cantidad de contenido instrumental (0-1)

### Artistas
- **Popularidad**: Popularidad del artista (0-100)
- **Seguidores**: Número total de seguidores
- **Top Tracks**: Mejores canciones del artista
- **Géneros**: Géneros asociados al artista
- **Características de Audio**: Métricas promedio de sus canciones

## 🔗 Endpoints de la API Utilizados

- `GET /`: Información de la API
- `GET /health`: Estado del sistema
- `GET /api/genres/analyze/{genre}`: Análisis de género
- `GET /api/genres/analyze/multiple`: Comparación de géneros
- `GET /api/genres/underground`: Géneros underground
- `GET /api/genres/compare`: Comparar dos géneros
- `GET /api/genres/trending`: Análisis de tendencias
- `GET /api/artists/search`: Buscar artista
- `GET /api/artists/analyze/{artist_name}`: Análisis de artista
- `GET /api/artists/compare`: Comparar artistas
- `GET /api/artists/vs`: Batalla 1v1
- `GET /api/artists/compare/breakbeat`: BreakBeat battle

## 🚀 Deployment

### Usando Docker Compose

Si usas Docker Compose (incluye backend y frontend):

```bash
docker-compose up
```

### Deploy en Streamlit Cloud

1. Sube tu código a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. Configura las variables de entorno
5. Deploy

## 📝 Notas

- El backend debe estar corriendo antes de usar el frontend
- Las credenciales de Spotify API son necesarias para el funcionamiento completo
- La base de datos PostgreSQL debe estar configurada y accesible
- Para mejores resultados, usa nombres de artistas y géneros en inglés

## 👨‍💻 Desarrollado con

- **Streamlit**: Framework de frontend
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Manipulación de datos
- **Requests**: Comunicación con la API
- **FastAPI**: Backend API
- **Spotipy**: Cliente de Spotify API

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🎵 ¡Disfruta explorando la música!

Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio.
