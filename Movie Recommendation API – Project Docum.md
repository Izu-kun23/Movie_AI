Movie Recommendation API – Project Documentation
Overview
This project is an AI-powered movie recommendation backend built with FastAPI, Pandas, Scikit-learn,
and Python.
It analyzes movie descriptions using TF-IDF and cosine similarity to recommend similar movies.
The backend can be connected to any frontend (React, Vue, HTML/JS).
Requirements
Software:
- Python 3.9+
- FastAPI
- Uvicorn
- Pandas
- Scikit-learn
Install dependencies:
pip install fastapi uvicorn pandas scikit-learn
Dataset Requirements
A movies.csv file with at least:
- title
- overview
Where to Get Movie Data
- Kaggle TMDB Dataset: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
- IMDb Datasets: https://developer.imdb.com/non-commercial-datasets/
- TMDB API: https://developer.themoviedb.org/
Getting a TMDB API Key (Optional)
1. Sign up: https://www.themoviedb.org/signup
2. Go to Settings → API
3. Request Developer API Key (v3)
Usage of TMDB API:
https://api.themoviedb.org/3/movie/550?api_key=YOUR_API_KEY
Project Structure
movie-recommender/
■■■ main.py
■■■ model.py
■■■ movies.csv
■■■ requirements.txt
■■■ README.md
How the Recommendation System Works
1. Load movie dataset
2. Clean text data
3. Vectorize descriptions (TF-IDF)
4. Compute cosine similarity
5. Return most similar movies through API
Running the Server
uvicorn main:app --reload
API URL: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs
Example Request:
GET /recommend?movie=The Matrix&limit;=5
Example Response:
{
}
"requested_movie": "The Matrix",
"recommendations": [...]
Possible Improvements
- User accounts
- Like/dislike system
- Search endpoint
- ML upgrade to deep learning
- Database integration
- Auto-updating movie list via TMDB API
Useful Links
FastAPI: https://fastapi.tiangolo.com/
Scikit-Learn: https://scikit-learn.org/
Pandas: https://pandas.pydata.org/