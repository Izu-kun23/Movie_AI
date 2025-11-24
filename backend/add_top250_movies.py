"""
Add IMDb Top 250 movies to existing movies.csv
This uses the IMDb Top 250 endpoint which includes popular movies like The Matrix
"""
import pandas as pd
import requests
import time

# Your IMDb API key
API_KEY = "4693d1a451mshbcee3887e70e47bp12b701jsn82f577692fd1"
BASE_URL = "https://imdb236.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "imdb236.p.rapidapi.com"
}

def get_top250_movies():
    """Fetch IMDb Top 250 movies"""
    url = f"{BASE_URL}/api/imdb/top250-movies"
    
    print("📡 Fetching IMDb Top 250 movies...")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Successfully fetched data")
            return data
        elif response.status_code == 401:
            print("❌ ERROR: Invalid API key!")
            return None
        elif response.status_code == 403:
            print("❌ ERROR: Access denied - check your subscription")
            return None
        else:
            print(f"❌ ERROR: Status code {response.status_code}")
            print(response.text[:200])
            return None
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None

def extract_movies_from_top250(data):
    """Extract movie data from Top 250 response"""
    movies = []
    
    # Try different possible response structures
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get('results', []) or data.get('data', []) or data.get('movies', []) or []
    else:
        print(f"⚠️  Unexpected data structure: {type(data)}")
        return movies
    
    print(f"   Found {len(items)} items in response")
    
    for item in items:
        # Try to get title and description
        title = item.get('primaryTitle') or item.get('originalTitle') or item.get('title') or item.get('name')
        description = item.get('description') or item.get('plot') or item.get('synopsis') or item.get('overview')
        
        if title and description and len(description.strip()) > 20:
            movies.append({
                'title': title,
                'overview': description
            })
    
    return movies

def add_top250_movies(limit=250):
    """Add Top 250 movies to existing movies.csv"""
    print("=" * 70)
    print("Adding IMDb Top 250 Movies to Database")
    print("=" * 70)
    
    # Load existing movies
    try:
        existing_df = pd.read_csv('movies.csv')
        existing_titles = set(existing_df['title'].str.lower().str.strip())
        print(f"\n✅ Loaded existing database with {len(existing_df)} movies")
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=['title', 'overview'])
        existing_titles = set()
        print("\n📝 Creating new movies.csv file")
    
    # Fetch Top 250
    data = get_top250_movies()
    
    if not data:
        print("\n❌ Could not fetch Top 250 movies")
        return
    
    # Extract movies
    print("\n📦 Processing movie data...")
    all_movies = extract_movies_from_top250(data)
    
    if not all_movies:
        print("\n⚠️  No movies extracted from response")
        print("   Response structure:")
        print(str(data)[:500])
        return
    
    print(f"   Extracted {len(all_movies)} movies with titles and descriptions")
    
    # Filter out duplicates
    new_movies = []
    for movie in all_movies:
        title_lower = movie['title'].lower().strip()
        if title_lower not in existing_titles:
            new_movies.append(movie)
            existing_titles.add(title_lower)
    
    if new_movies:
        # Limit if specified
        if limit and len(new_movies) > limit:
            new_movies = new_movies[:limit]
        
        # Combine existing and new movies
        new_df = pd.DataFrame(new_movies)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        # Remove duplicates (in case of any)
        combined_df = combined_df.drop_duplicates(subset=['title'], keep='first')
        
        # Sort by title for better organization
        combined_df = combined_df.sort_values('title').reset_index(drop=True)
        
        # Save
        combined_df.to_csv('movies.csv', index=False)
        
        print(f"\n✅ SUCCESS!")
        print(f"   Added {len(new_movies)} new movies")
        print(f"   Total movies in database: {len(combined_df)}")
        print(f"\n   Sample new movies:")
        for i, row in new_df.head(10).iterrows():
            print(f"      - {row['title']}")
        
        print(f"\n   🚀 Restart your server to load the updated dataset!")
        print(f"   Run: uvicorn main:app --reload")
    else:
        print(f"\n⚠️  No new movies were added")
        print(f"   All movies from Top 250 may already be in the database")

if __name__ == "__main__":
    import sys
    
    limit = 250
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except:
            pass
    
    add_top250_movies(limit=limit)

