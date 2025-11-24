"""
Create movies.csv from IMDb RapidAPI - Improved version
Searches for diverse movies using different strategies
"""
import requests
import pandas as pd
import json
import time
import random

API_KEY = "663266ffe2mshb8ea82ebefb8444p1ef691jsn20e470584a5f"
BASE_URL = "https://imdb236.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "imdb236.p.rapidapi.com"
}

def search_imdb_movies(query, limit=50, cursor=None):
    """Search for movies on IMDb with pagination support"""
    url = f"{BASE_URL}/api/imdb/search"
    params = {
        "q": query,
        "type": "movie",
        "rows": limit
    }
    
    if cursor:
        params["cursor"] = cursor
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            next_cursor = data.get('nextCursorMark')
            return results, next_cursor
        return [], None
    except Exception as e:
        print(f"   Error: {str(e)}")
        return [], None

def extract_movies_from_results(results):
    """Extract title and description from IMDb results"""
    movies = []
    for item in results:
        title = item.get('primaryTitle') or item.get('originalTitle')
        description = item.get('description')
        
        # Only add if we have both title and description (with minimum length)
        if title and description and len(description.strip()) > 30:
            movies.append({
                'title': title,
                'overview': description
            })
    
    return movies

def create_movies_csv(max_movies=500):
    """Create movies.csv by searching IMDb with diverse queries"""
    print("=" * 70)
    print("IMDb RapidAPI - Creating movies.csv (Improved)")
    print("=" * 70)
    
    # More diverse search strategies
    search_strategies = [
        # Genre searches
        {"query": "2023", "limit": 50},
        {"query": "2022", "limit": 50},
        {"query": "2021", "limit": 50},
        {"query": "2020", "limit": 50},
        {"query": "2019", "limit": 50},
        {"query": "2018", "limit": 50},
        # Popular movies by rating
        {"query": "top rated", "limit": 50},
        {"query": "popular", "limit": 50},
        {"query": "best", "limit": 50},
        # Specific popular movies
        {"query": "the matrix", "limit": 50},
        {"query": "inception", "limit": 50},
        {"query": "avatar", "limit": 50},
        {"query": "batman", "limit": 50},
        {"query": "spider", "limit": 50},
        {"query": "marvel", "limit": 50},
        {"query": "star wars", "limit": 50},
        {"query": "harry potter", "limit": 50},
        {"query": "lord rings", "limit": 50},
        {"query": "titanic", "limit": 50},
        {"query": "godfather", "limit": 50},
        {"query": "shawshank", "limit": 50},
        {"query": "pulp fiction", "limit": 50},
        {"query": "fight club", "limit": 50},
        {"query": "interstellar", "limit": 50},
    ]
    
    all_movies = []
    seen_titles = set()
    
    print(f"\n🔍 Searching IMDb with {len(search_strategies)} different queries...")
    print(f"   Target: {max_movies} unique movies\n")
    
    for idx, strategy in enumerate(search_strategies):
        if len(all_movies) >= max_movies:
            break
        
        query = strategy['query']
        limit = strategy.get('limit', 50)
        
        print(f"[{idx+1}/{len(search_strategies)}] Searching: '{query}' (limit: {limit})")
        
        # Search and get first page
        results, cursor = search_imdb_movies(query, limit=limit)
        movies = extract_movies_from_results(results)
        
        # Add unique movies
        new_count = 0
        for movie in movies:
            title = movie['title']
            if title not in seen_titles:
                seen_titles.add(title)
                all_movies.append(movie)
                new_count += 1
        
        print(f"   ✅ Found {len(movies)} movies ({new_count} new) | Total: {len(all_movies)}")
        
        # If we got a cursor and want more results, try next page
        if cursor and len(all_movies) < max_movies:
            print(f"   📄 Fetching next page...")
            results2, _ = search_imdb_movies(query, limit=limit, cursor=cursor)
            movies2 = extract_movies_from_results(results2)
            
            for movie in movies2:
                title = movie['title']
                if title not in seen_titles:
                    seen_titles.add(title)
                    all_movies.append(movie)
                    new_count += 1
            
            print(f"   ✅ Added {new_count} more movies | Total: {len(all_movies)}")
        
        # Rate limiting
        time.sleep(0.5)
    
    if all_movies:
        # Create DataFrame
        movies_df = pd.DataFrame(all_movies)
        movies_df = movies_df.drop_duplicates(subset=['title'])
        movies_df = movies_df[movies_df['overview'].str.strip() != '']
        
        # Shuffle for variety
        movies_df = movies_df.sample(frac=1).reset_index(drop=True)
        
        # Limit to max_movies
        if len(movies_df) > max_movies:
            movies_df = movies_df.head(max_movies)
        
        # Save to CSV
        output_file = "movies.csv"
        movies_df.to_csv(output_file, index=False)
        
        print(f"\n✅ SUCCESS!")
        print(f"   Created: {output_file}")
        print(f"   Total unique movies: {len(movies_df)}")
        print(f"\n   Sample movies:")
        for i, row in movies_df.head(10).iterrows():
            print(f"      - {row['title']}")
        
        print(f"\n   🚀 Your API is ready! Restart the server to load the new dataset.")
        print(f"   Run: uvicorn main:app --reload")
        return True
    else:
        print("\n❌ No movies were extracted")
        return False

if __name__ == "__main__":
    import sys
    
    max_movies = 500
    if len(sys.argv) > 1:
        try:
            max_movies = int(sys.argv[1])
        except:
            pass
    
    create_movies_csv(max_movies=max_movies)

