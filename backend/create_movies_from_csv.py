"""
Script to create movies.csv from csv/tmdb_5000_credits.csv
This will use the TMDB API to fetch overviews for all movies.
"""
import pandas as pd
import requests
import time
import json
import os
from typing import Optional

# TMDB API Configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "YOUR_API_KEY_HERE")
TMDB_BASE_URL = "https://api.themoviedb.org/3/movie"

def fetch_movie_overview(movie_id: int, api_key: str) -> Optional[dict]:
    """
    Fetch movie overview from TMDB API.
    
    Args:
        movie_id: TMDB movie ID
        api_key: TMDB API key
        
    Returns:
        Dictionary with overview and other info, or None if not found
    """
    url = f"{TMDB_BASE_URL}/{movie_id}"
    params = {"api_key": api_key}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        # Check for API errors
        if response.status_code == 401:
            return {"error": "Invalid API key"}
        elif response.status_code == 404:
            return None  # Movie not found
        elif response.status_code != 200:
            error_data = response.json() if response.content else {}
            return {"error": f"API error {response.status_code}: {error_data.get('status_message', 'Unknown error')}"}
        
        response.raise_for_status()
        data = response.json()
        
        # Check if overview exists and is not empty
        overview = data.get("overview", "")
        if not overview:
            return None
            
        return {
            "overview": overview,
            "title": data.get("title", ""),
            "release_date": data.get("release_date", "")
        }
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def create_movies_csv(credits_file: str = "csv/tmdb_5000_credits.csv", 
                     output_file: str = "movies.csv",
                     api_key: Optional[str] = None,
                     limit: Optional[int] = None):
    """
    Create movies.csv from credits file by fetching overviews from TMDB API.
    """
    # Check if credits file exists
    if not os.path.exists(credits_file):
        print(f"❌ Error: {credits_file} not found!")
        print(f"   Looking for file at: {os.path.abspath(credits_file)}")
        return False
    
    # Load credits file
    print(f"📂 Loading credits file: {credits_file}")
    credits_df = pd.read_csv(credits_file)
    print(f"   Found {len(credits_df)} movies in credits file")
    
    # Get API key
    if not api_key:
        api_key = TMDB_API_KEY
    
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("\n" + "="*70)
        print("⚠️  TMDB API KEY REQUIRED")
        print("="*70)
        print("\nTo fetch movie overviews, you need a free TMDB API key:")
        print("1. Sign up: https://www.themoviedb.org/signup")
        print("2. Go to: Settings → API")
        print("3. Request an API key (free for developers)")
        print("\nThen run this script with your ACTUAL API key:")
        print("   python create_movies_from_csv.py YOUR_ACTUAL_API_KEY_HERE")
        print("\n⚠️  IMPORTANT: Replace 'YOUR_ACTUAL_API_KEY_HERE' with your real API key!")
        print("\nOr set it as environment variable:")
        print("   export TMDB_API_KEY=your_actual_key_here")
        print("   python create_movies_from_csv.py")
        print("\n" + "="*70)
        print("ALTERNATIVE: Download tmdb_5000_movies.csv from Kaggle")
        print("URL: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata")
        print("Then place it in the project root as 'movies.csv'")
        print("="*70)
        return False
    
    # Test API key with a simple request
    print(f"\n🔑 Testing API key...")
    test_response = requests.get(f"{TMDB_BASE_URL}/550", params={"api_key": api_key}, timeout=10)
    if test_response.status_code == 401:
        print("❌ ERROR: Invalid API key!")
        print("   Status Code: 401 Unauthorized")
        print("   Please check your API key and try again.")
        print("\n   Make sure you:")
        print("   1. Signed up at https://www.themoviedb.org/signup")
        print("   2. Requested an API key from Settings → API")
        print("   3. Copied the correct API key (it should be a long string)")
        return False
    elif test_response.status_code != 200:
        print(f"❌ ERROR: API request failed with status {test_response.status_code}")
        try:
            error_data = test_response.json()
            print(f"   Error: {error_data.get('status_message', 'Unknown error')}")
        except:
            print(f"   Response: {test_response.text[:200]}")
        return False
    else:
        print("✅ API key is valid!")
    
    # Limit movies if specified (for testing)
    if limit:
        credits_df = credits_df.head(limit)
        print(f"\n⚠️  Processing only first {limit} movies (for testing)")
    
    movies_data = []
    total = len(credits_df)
    successful = 0
    failed = 0
    
    print(f"\n🔄 Fetching overviews for {total} movies from TMDB API...")
    print("   This will take approximately {} minutes".format(int(total * 0.25 / 60) + 1))
    print("   Please be patient...\n")
    
    start_time = time.time()
    
    for idx, row in credits_df.iterrows():
        movie_id = row['movie_id']
        title = row['title']
        
        # Progress indicator
        if (idx + 1) % 10 == 0:
            elapsed = time.time() - start_time
            rate = (idx + 1) / elapsed if elapsed > 0 else 0
            remaining = (total - idx - 1) / rate if rate > 0 else 0
            print(f"[{idx + 1}/{total}] Progress: {successful} success, {failed} failed | "
                  f"ETA: {int(remaining/60)}m {int(remaining%60)}s")
        
        movie_data = fetch_movie_overview(movie_id, api_key)
        
        if movie_data:
            if "error" in movie_data:
                # Show first few errors to help debug
                if failed < 3:
                    print(f"   ⚠️  Movie {movie_id} ({title}): {movie_data['error']}")
                failed += 1
            elif movie_data.get("overview"):
                movies_data.append({
                    'title': movie_data.get("title") or title,
                    'overview': movie_data["overview"]
                })
                successful += 1
            else:
                failed += 1
        else:
            failed += 1
        
        # Rate limiting - TMDB allows 40 requests per 10 seconds
        # Using 0.25 seconds = ~4 requests per second = safe
        time.sleep(0.25)
    
    # Create DataFrame and save
    if movies_data:
        movies_df = pd.DataFrame(movies_data)
        movies_df = movies_df.drop_duplicates(subset=['title'])
        movies_df = movies_df[movies_df['overview'].str.strip() != '']
        
        movies_df.to_csv(output_file, index=False)
        
        elapsed_time = time.time() - start_time
        print(f"\n" + "="*70)
        print(f"✅ SUCCESS!")
        print(f"="*70)
        print(f"   Created: {output_file}")
        print(f"   Total movies: {len(movies_df)}")
        print(f"   Successful: {successful}")
        print(f"   Failed: {failed}")
        print(f"   Time taken: {int(elapsed_time/60)}m {int(elapsed_time%60)}s")
        print(f"\n   Your API is ready! Restart the server to load the new dataset.")
        print("="*70)
        return True
    else:
        print(f"\n❌ No movies were fetched successfully.")
        print(f"   Please check your API key and try again.")
        return False

if __name__ == "__main__":
    import sys
    
    api_key = None
    limit = None
    
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            limit = int(sys.argv[2])
        except ValueError:
            print("⚠️  Invalid limit value, processing all movies")
    
    create_movies_csv(api_key=api_key, limit=limit)

