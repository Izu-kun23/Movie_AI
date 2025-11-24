# Backend - Movie Recommendation API

FastAPI backend for movie recommendations using TF-IDF and cosine similarity.

## Local Development

### Start the server locally:

```bash
# Option 1: Use the run script
python run_server.py

# Option 2: Direct uvicorn command
uvicorn main:app --host 0.0.0.0 --port 8000

# Option 3: Run main.py directly
python main.py
```

The server will be available at: `http://127.0.0.1:8000`

## Production Deployment (Render)

### Start Command for Render:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Note:** `$PORT` is automatically set by Render. You don't need to set it locally.

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /recommend?movie=The Matrix&limit=5` - Get recommendations
- `POST /api/chat` - AI chat endpoint
- `GET /movies/search?query=matrix` - Search movies
- `GET /docs` - Interactive API documentation

## Dependencies

See `requirements.txt` for all dependencies.

Main dependencies:
- FastAPI
- Uvicorn
- Pandas
- Scikit-learn

## Files

- `main.py` - FastAPI application
- `model.py` - Recommendation model logic
- `movies.csv` - Movie dataset
- `requirements.txt` - Python dependencies

