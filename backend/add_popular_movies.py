"""
Add popular movies to existing movies.csv using IMDb API
"""
import pandas as pd
import requests
import time

# Your IMDb API key
API_KEY = "663266ffe2mshb8ea82ebefb8444p1ef691jsn20e470584a5f"
BASE_URL = "https://imdb236.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "imdb236.p.rapidapi.com"
}

# Popular movies to add
POPULAR_MOVIES = [
    "The Matrix",
    "Inception",
    "The Matrix Reloaded",
    "The Matrix Revolutions",
    "Interstellar",
    "Blade Runner",
    "Blade Runner 2049",
    "The Dark Knight",
    "Avatar",
    "Titanic",
    "The Godfather",
    "Pulp Fiction",
    "Fight Club",
    "The Shawshank Redemption",
    "Forrest Gump",
    "The Lord of the Rings: The Fellowship of the Ring",
    "The Lord of the Rings: The Return of the King",
    "Star Wars",
    "Harry Potter and the Philosopher's Stone",
    "Iron Man",
    "Batman Begins",
    "The Terminator",
    "Terminator 2: Judgment Day",
    "Alien",
    "Aliens"
]

def search_movie_on_imdb(movie_title):
    """Search for a specific movie on IMDb"""
    url = f"{BASE_URL}/api/imdb/search"
    params = {
        "q": movie_title,
        "type": "movie",
        "rows": 10
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            # Find exact or close match
            movie_title_lower = movie_title.lower()
            for result in results:
                title = result.get('primaryTitle') or result.get('originalTitle', '')
                if title and movie_title_lower in title.lower():
                    description = result.get('description')
                    if description and len(description.strip()) > 20:
                        return {
                            'title': title,
                            'overview': description
                        }
            
            # If no close match, try first result
            if results:
                first = results[0]
                description = first.get('description')
                if description and len(description.strip()) > 20:
                    return {
                        'title': first.get('primaryTitle') or first.get('originalTitle'),
                        'overview': description
                    }
        
        return None
    except Exception as e:
        print(f"   Error searching '{movie_title}': {str(e)}")
        return None

def add_popular_movies():
    """Add popular movies to existing movies.csv"""
    print("=" * 70)
    print("Adding Popular Movies to Database")
    print("=" * 70)
    
    # Load existing movies
    try:
        existing_df = pd.read_csv('movies.csv')
        existing_titles = set(existing_df['title'].str.lower())
        print(f"\n✅ Loaded existing database with {len(existing_df)} movies")
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=['title', 'overview'])
        existing_titles = set()
        print("\n📝 Creating new movies.csv file")
    
    new_movies = []
    
    print(f"\n🔍 Searching for {len(POPULAR_MOVIES)} popular movies...\n")
    
    for idx, movie_title in enumerate(POPULAR_MOVIES):
        if movie_title.lower() in existing_titles:
            print(f"[{idx+1}/{len(POPULAR_MOVIES)}] '{movie_title}' - Already exists ⏭️")
            continue
        
        print(f"[{idx+1}/{len(POPULAR_MOVIES)}] Searching: '{movie_title}'")
        
        movie_data = search_movie_on_imdb(movie_title)
        
        if movie_data:
            # Check if we already have this exact title
            if movie_data['title'].lower() not in existing_titles:
                new_movies.append(movie_data)
                existing_titles.add(movie_data['title'].lower())
                print(f"   ✅ Found: {movie_data['title']}")
            else:
                print(f"   ⏭️  Already have: {movie_data['title']}")
        else:
            print(f"   ❌ Not found")
        
        time.sleep(0.3)  # Rate limiting
    
    if new_movies:
        # Combine existing and new movies
        new_df = pd.DataFrame(new_movies)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        # Remove duplicates
        combined_df = combined_df.drop_duplicates(subset=['title'], keep='first')
        
        # Save
        combined_df.to_csv('movies.csv', index=False)
        
        print(f"\n✅ SUCCESS!")
        print(f"   Added {len(new_movies)} new movies")
        print(f"   Total movies: {len(combined_df)}")
        print(f"\n   🚀 Restart your server to load the updated dataset!")
        print(f"   Run: uvicorn main:app --reload")
    else:
        print(f"\n⚠️  No new movies were added")
        print(f"   All requested movies may already be in the database")

if __name__ == "__main__":
    add_popular_movies()



