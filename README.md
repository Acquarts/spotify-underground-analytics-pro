# 🎵 Spotify Analytics - Streamlit Frontend

Interactive web application for music genre analysis and artist comparison using the Spotify API.

## 🚀 Features

### 🎯 Genre Analysis
- **Individual Analysis**: Analyze specific genres with detailed metrics
- **Multiple Comparison**: Compare up to several genres simultaneously
- **Trends**: Analysis of mainstream vs underground genres
- **Visualizations**: Radar charts, bar graphs, and comparative tables

### 🥊 Artist Comparison
- **Search and Analysis**: Search artists and get complete analysis
- **Multiple Comparison**: Compare up to 5 artists simultaneously
- **BreakBeat Battle**: Compare iconic BreakBeat genre artists
- **1v1 Battle**: Direct comparison between two artists

### 💎 Underground Gems
- Automatic underground genre detector
- Niche genre potential analysis
- Specialized metrics for alternative music

## 📋 Requirements

- Python 3.8+
- FastAPI backend running (see instructions below)
- Spotify API credentials

## 🔧 Installation

### 1. Clone the repository (if you haven't already)

```bash
cd spotify-analytics
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root (if it doesn't exist):

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
API_BASE_URL=http://localhost:8000
```

### 4. Start the backend (FastAPI)

In a separate terminal:

```bash
cd backend
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

### 5. Start the frontend (Streamlit)

In another terminal:

```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

## 📱 Using the Application

### Main Navigation

The application has 5 main sections accessible from the sidebar:

1. **🏠 Home**: General information and quick statistics
2. **🎯 Genre Analysis**: Individual analysis, comparisons, and trends
3. **🥊 Artist Comparison**: Search, analysis, and comparisons
4. **💎 Underground Gems**: Discover underground genres
5. **⚔️ 1v1 Battle**: Direct comparison between artists

### Genre Analysis

#### Individual Analysis
1. Enter the name of a genre (e.g., "breakbeat", "electronic", "pop")
2. Click "Analyze Genre"
3. View metrics such as popularity, energy, danceability
4. Explore the radar chart with genre characteristics

#### Multiple Comparison
1. Enter several genres separated by comma
2. Compare metrics among all genres
3. Visualize rankings of popularity, energy, and danceability
4. Automatically detect underground genres

#### Trend Analysis
1. Click "Analyze Trends"
2. Compare mainstream vs underground genres
3. Visualize differences in popularity and energy

### Artist Comparison

#### Search and Analysis
1. Enter an artist's name
2. "Search": Basic information
3. "Complete Analysis": Detailed metrics, top tracks, genres

#### Multiple Comparison
1. Enter up to 5 artists separated by comma
2. Compare popularity, followers, and audio metrics
3. Visualize winners by category
4. Read automatically generated insights

#### BreakBeat Battle
1. Click "Start Battle"
2. Compare The Prodigy, Pendulum, and The Chemical Brothers
3. Visualize comparative radar chart
4. Discover winners in each category

### 1v1 Battle
1. Enter two artists in the corresponding fields
2. Click "Start Battle"
3. Side-by-side comparison with key metrics
4. Visualize winners by category

### Underground Gems
1. Click "Search Underground Gems"
2. Discover underground genres automatically
3. Visualize metrics for each found genre
4. Read the reasons why they're considered underground

## 🎨 Interface Features

- **Responsive design**: Adapts to different screen sizes
- **Spotify theme**: Colors inspired by Spotify brand (#1DB954)
- **Interactive charts**: Using Plotly for dynamic visualizations
- **Organized tabs**: Intuitive tab navigation
- **Featured metrics**: Cards with key information
- **Loading spinner**: Visual feedback during API requests

## 🛠️ Advanced Configuration

### Change API URL

You can change the backend URL from the sidebar in "Configuration".

### Verify API Status

Use the "🔍 Verify API" button in the sidebar to check:
- Database connection status
- Spotify API connection status
- Available features

## 🐛 Troubleshooting

### Frontend doesn't connect to backend
- Verify that the backend is running at `http://localhost:8000`
- Check the URL configured in the sidebar
- Check that there are no errors in the backend console

### Can't find artists or genres
- Verify that Spotify API credentials are configured
- Check API status with the "Verify API" button
- Check that the database is connected

### Visualization errors
- Make sure all dependencies are installed (`pip install -r requirements.txt`)
- Clear Streamlit cache: `Ctrl + R` or `Cmd + R`

## 📊 Available Metrics

### Genres
- **Popularity**: Average popularity level (0-100)
- **Energy**: Perceived intensity and activity (0-1)
- **Danceability**: How suitable for dancing (0-1)
- **Valence**: Musical positivity (0-1)
- **Acousticness**: Presence of acoustic instruments (0-1)
- **Instrumentalness**: Amount of instrumental content (0-1)

### Artists
- **Popularity**: Artist popularity (0-100)
- **Followers**: Total number of followers
- **Top Tracks**: Artist's best songs
- **Genres**: Genres associated with the artist
- **Audio Features**: Average metrics from their songs

## 🔗 API Endpoints Used

- `GET /`: API information
- `GET /health`: System status
- `GET /api/genres/analyze/{genre}`: Genre analysis
- `GET /api/genres/analyze/multiple`: Genre comparison
- `GET /api/genres/underground`: Underground genres
- `GET /api/genres/compare`: Compare two genres
- `GET /api/genres/trending`: Trend analysis
- `GET /api/artists/search`: Search artist
- `GET /api/artists/analyze/{artist_name}`: Artist analysis
- `GET /api/artists/compare`: Compare artists
- `GET /api/artists/vs`: 1v1 battle
- `GET /api/artists/compare/breakbeat`: BreakBeat battle

## 🚀 Deployment

### Using Docker Compose

If using Docker Compose (includes backend and frontend):

```bash
docker-compose up
```

### Deploy on Streamlit Cloud

1. Upload your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Configure environment variables
5. Deploy

## 📝 Notes

- The backend must be running before using the frontend
- Spotify API credentials are necessary for full functionality
- PostgreSQL database must be configured and accessible
- For best results, use artist and genre names in English

## 👨‍💻 Built With

- **Streamlit**: Frontend framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **Requests**: API communication
- **FastAPI**: Backend API
- **Spotipy**: Spotify API client

## 📄 License

This project is open source and available under the MIT License.

## 🎵 Enjoy exploring music!

If you have questions or suggestions, feel free to open an issue in the repository.
