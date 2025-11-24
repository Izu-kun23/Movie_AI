# Project Structure

## Final Organization

```
Movie_AI/
│
├── backend/                    # All Python backend code
│   ├── __init__.py
│   ├── main.py                # FastAPI application & AI chat endpoint
│   ├── model.py               # Recommendation model (TF-IDF)
│   ├── movies.csv             # Movie database
│   ├── run_server.py          # Server startup script
│   │
│   ├── csv/                   # Source data
│   │   └── tmdb_5000_credits.csv
│   │
│   └── Scripts/               # Utility scripts
│       ├── create_movies_from_csv.py   # Fetch from TMDB API
│       ├── create_movies_from_imdb.py  # Fetch from IMDb API
│       ├── add_manual_movies.py        # Add popular movies manually
│       ├── add_top250_movies.py        # Fetch IMDb Top 250
│       └── add_popular_movies.py       # Add popular movies
│
├── frontend/                  # All frontend code
│   ├── index.html            # Main HTML (AI chat interface)
│   ├── package.json          # npm dependencies
│   │
│   ├── src/                  # Source files
│   │   ├── scss/            # Sass stylesheets
│   │   │   ├── _variables.scss
│   │   │   ├── _mixins.scss
│   │   │   └── main.scss
│   │   └── js/              # JavaScript
│   │       └── main.js
│   │
│   └── dist/                # Compiled files
│       ├── css/
│       │   └── main.css
│       └── js/
│           └── main.js
│
├── venv/                     # Python virtual environment
├── requirements.txt          # Python dependencies
├── README.md                # Main documentation
└── QUICK_START.md           # Quick start guide
```

## Running the Project

### Backend (from backend/ directory)
```bash
cd backend
uvicorn main:app --reload
```

### Frontend
Open `frontend/index.html` in your browser

## Paths

All paths in the codebase are relative to their directories:
- Backend scripts expect `movies.csv` in `backend/`
- Frontend expects API at `http://127.0.0.1:8000`
- All relative paths work when run from correct directory

