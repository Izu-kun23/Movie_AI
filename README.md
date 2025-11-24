# Movie Recommendation API

An AI-powered movie recommendation backend built with FastAPI, Pandas, and Scikit-learn. This system analyzes movie descriptions using TF-IDF vectorization and cosine similarity to recommend similar movies.

## Overview

This project provides a RESTful API for movie recommendations with an intelligent chat interface. The backend can be connected to any frontend (React, Vue, HTML/JS, etc.).

## Features

- 🤖 AI-powered recommendations using TF-IDF and cosine similarity
- 💬 Conversational AI chat interface
- 🔍 Movie search functionality
- 🚀 FastAPI with automatic interactive documentation
- 📊 Handles large movie datasets efficiently
- 🔄 Case-insensitive and partial title matching

## Project Structure

```
Movie_AI/
├── backend/                 # Python backend code
│   ├── main.py             # FastAPI application
│   ├── model.py            # Recommendation model
│   ├── movies.csv          # Movie dataset
│   ├── csv/                # Source data
│   │   └── tmdb_5000_credits.csv
│   ├── create_movies_from_csv.py    # TMDB API script
│   ├── create_movies_from_imdb.py   # IMDb API script
│   └── add_manual_movies.py         # Manual movie addition
├── frontend/               # Frontend (HTML, Sass, JS)
│   ├── index.html
│   ├── src/
│   │   ├── scss/          # Sass styles
│   │   └── js/            # JavaScript
│   └── dist/              # Compiled files
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Requirements

### Software

- Python 3.9+
- FastAPI
- Uvicorn
- Pandas
- Scikit-learn

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd Movie_AI
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up movie dataset:**
   
   You need a `backend/movies.csv` file with at least:
   - `title`: Movie title
   - `overview`: Movie description/synopsis
   
   **Option 1: Fetch from Credits CSV (Recommended)**
   
   Use the TMDB credits CSV to fetch movies:
   ```bash
   cd backend
   python fetch_movies_from_credits.py YOUR_TMDB_API_KEY
   ```
   
   To test with a smaller dataset first:
   ```bash
   python fetch_movies_from_credits.py YOUR_TMDB_API_KEY 50
   ```
   
   **Option 2: Quick setup (Manual movies)**
   ```bash
   cd backend
   python add_manual_movies.py
   ```
   
   **Option 3: IMDb RapidAPI (Popular Movies):**
   ```bash
   cd backend
   python fetch_movies_from_imdb_api.py
   ```
   
   Or fetch from specific sources:
   ```bash
   python fetch_movies_from_imdb_api.py box_office,popular 20
   ```
   
   **Option 4: Other API scripts:**
   - TMDB API: `python create_movies_from_csv.py YOUR_TMDB_API_KEY`
   - IMDb API: `python create_movies_from_imdb.py`
   
   **Getting a TMDB API Key:**
   1. Sign up: https://www.themoviedb.org/signup
   2. Go to: Settings → API
   3. Request an API key (free for developers)

## Running the Server

### From project root:

```bash
cd backend
uvicorn main:app --reload
```

Or use the run script:

```bash
cd backend
python run_server.py
```

### From backend directory:

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at:
- **API URL:** http://127.0.0.1:8000
- **Interactive Docs:** http://127.0.0.1:8000/docs
- **Alternative Docs:** http://127.0.0.1:8000/redoc

## Running the Frontend

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Build the frontend (if not already built):**
   ```bash
   npm install
   npm run build
   ```

3. **Open in browser:**
   - Open `frontend/index.html` in your browser
   - Or serve with a local server

4. **Watch for changes (development):**
   ```bash
   npm run dev
   ```

## API Endpoints

### 1. Chat with AI (New!)

**Endpoint:** `POST /api/chat`

Natural language movie recommendations:

```json
{
  "message": "I like The Matrix",
  "type": "auto"  // optional: "recommend", "search", "greeting", or "auto"
}
```

**Response:**
```json
{
  "type": "recommendations",
  "message": "Based on your interest in 'The Matrix', I've found some fantastic recommendations!",
  "requested_movie": "The Matrix",
  "recommendations": [
    {
      "title": "Inception",
      "overview": "...",
      "similarity_score": 0.85,
      "explanation": "I recommend 'Inception' because it shares similar themes..."
    }
  ]
}
```

### 2. Get Recommendations

**Endpoint:** `GET /recommend`

```bash
GET /recommend?movie=The Matrix&limit=5
```

### 3. Search Movies

**Endpoint:** `GET /movies/search`

```bash
GET /movies/search?query=matrix&limit=10
```

### 4. Health Check

**Endpoint:** `GET /health`

## How It Works

1. Load movie dataset from CSV
2. Clean and preprocess text data (overviews)
3. Vectorize descriptions using TF-IDF
4. Compute cosine similarity between movies
5. Return most similar movies through AI-powered API

## Example Usage

### Using the AI Chat Interface

Just open `frontend/index.html` and type naturally:
- "I like The Matrix"
- "Recommend movies similar to Inception"
- "Search for Batman"

### Using curl:

```bash
# Chat with AI
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I like The Matrix"}'

# Get recommendations
curl "http://127.0.0.1:8000/recommend?movie=The Matrix&limit=5"
```

## Dataset Management

### Fetch from Credits CSV (Recommended - Uses csv/tmdb_5000_credits.csv):
```bash
cd backend
python fetch_movies_from_credits.py YOUR_TMDB_API_KEY
```

### Add movies manually:
```bash
cd backend
python add_manual_movies.py
```

### Fetch from TMDB API:
```bash
cd backend
python create_movies_from_csv.py YOUR_TMDB_API_KEY
```

### Fetch from IMDb RapidAPI (Top Box Office, Popular, Top Rated):
```bash
cd backend
python fetch_movies_from_imdb_api.py
```

### Fetch from IMDb API (Alternative):
```bash
cd backend
python create_movies_from_imdb.py
```

## Troubleshooting

**Error: "Movie dataset not found"**
- Ensure `backend/movies.csv` exists
- Verify the CSV has `title` and `overview` columns

**Error: "Movie not found"**
- Try using a partial match (e.g., "Matrix" instead of "The Matrix")
- Use the chat interface which handles natural language better

**Frontend can't connect to API:**
- Make sure the backend server is running on http://127.0.0.1:8000
- Check CORS settings in `backend/main.py`

## Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Scikit-Learn Documentation](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

## License

This project is open source and available for educational purposes.
