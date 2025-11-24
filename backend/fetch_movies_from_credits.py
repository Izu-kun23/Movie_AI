"""
Fetch movies from TMDB API using movie IDs from csv/tmdb_5000_credits.csv
This script reads the credits CSV and fetches overviews for all movies
"""
import pandas as pd
import requests
import time
import os
from typing import Optional

# TMDB API Configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "YOUR_TMDB_API_KEY_HERE")
TMDB_BASE_URL = "https://api.themoviedb.org/3/movie"

def fetch_movie_from_tmdb(movie_id: int, api_key: str) -> Optional[dict]:
    """
    Fetch movie data from TMDB API using movie ID.
    
    Args:
        movie_id: TMDB movie ID
        api_key: TMDB API key
        
    Returns:
        Dictionary with movie data or None if not found
    """
    url = f"{TMDB_BASE_URL}/{movie_id}"
    params = {"api_key": api_key}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 401:
            return {"error": "Invalid API key"}
        elif response.status_code == 404:
            return None  # Movie not found
        elif response.status_code != 200:
            return {"error": f"API error {response.status_code}"}
        
        data = response.json()
        
        # Get overview
        overview = data.get("overview", "")
        if not overview or len(overview.strip()) < 10:
            return None
        
        # Get title (prefer original title)
        title = data.get("title") or data.get("original_title", "")
        if not title:
            return None
        
        return {
            "title": title,
            "overview": overview,
            "release_date": data.get("release_date", ""),
            "popularity": data.get("popularity", 0),
            "vote_average": data.get("vote_average", 0)
        }
        
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except Exception as e:
        return {"error": str(e)}

def fetch_movies_from_credits_csv(
    credits_file: str = "csv/tmdb_5000_credits.csv",
    output_file: str = "movies.csv",
    api_key: Optional[str] = None,
    limit: Optional[int] = None
):
    """
    Create movies.csv from credits CSV by fetching overviews from TMDB API.
    """
    print("=" * 70)
    print("Fetch Movies from Credits CSV using TMDB API")
    print("=" * 70)
    
    # Check if credits file exists
    if not os.path.exists(credits_file):
        print(f"❌ Error: {credits_file} not found!")
        print(f"   Looking for: {os.path.abspath(credits_file)}")
        return False
    
    # Load credits file
    print(f"\n📂 Loading credits file: {credits_file}")
    try:
        credits_df = pd.read_csv(credits_file)
        print(f"   ✅ Found {len(credits_df)} movies in credits file")
    except Exception as e:
        print(f"   ❌ Error loading CSV: {str(e)}")
        return False
    
    # Validate columns
    if 'movie_id' not in credits_df.columns or 'title' not in credits_df.columns:
        print(f"   ❌ Error: Missing required columns")
        print(f"   Required: movie_id, title")
        print(f"   Found: {list(credits_df.columns)}")
        return False
    
    # Get API key
    if not api_key:
        api_key = TMDB_API_KEY
    
    if not api_key or api_key == "YOUR_TMDB_API_KEY_HERE":
        print("\n" + "=" * 70)
        print("⚠️  TMDB API KEY REQUIRED")
        print("=" * 70)
        print("\nTo fetch movie overviews, you need a free TMDB API key:")
        print("1. Sign up: https://www.themoviedb.org/signup")
        print("2. Go to: Settings → API")
        print("3. Request an API key (free for developers)")
        print("\nThen run this script with your API key:")
        print(f"   python fetch_movies_from_credits.py YOUR_TMDB_API_KEY")
        print("\nOr set as environment variable:")
        print("   export TMDB_API_KEY=your_key_here")
        print("=" * 70)
        return False
    
    # Test API key
    print(f"\n🔑 Testing TMDB API key...")
    test_response = requests.get(f"{TMDB_BASE_URL}/550", params={"api_key": api_key}, timeout=10)
    if test_response.status_code == 401:
        print("❌ ERROR: Invalid API key!")
        print("   Please check your TMDB API key and try again.")
        return False
    elif test_response.status_code != 200:
        print(f"⚠️  Warning: Test request returned status {test_response.status_code}")
    else:
        print("✅ API key is valid!")
    
    # Limit if specified (for testing)
    if limit:
        credits_df = credits_df.head(limit)
        print(f"\n⚠️  Processing only first {limit} movies (for testing)")
    else:
        print(f"\n🔄 Fetching overviews for all {len(credits_df)} movies...")
    
    movies_data = []
    successful = 0
    failed = 0
    errors = []
    
    total = len(credits_df)
    start_time = time.time()
    
    print(f"   This will take approximately {int(total * 0.25 / 60) + 1} minutes")
    print(f"   Please be patient...\n")
    
    for idx, row in credits_df.iterrows():
        movie_id = row['movie_id']
        title_from_csv = row['title']
        
        # Progress indicator every 10 movies
        if (idx + 1) % 10 == 0:
            elapsed = time.time() - start_time
            rate = (idx + 1) / elapsed if elapsed > 0 else 0
            remaining = (total - idx - 1) / rate if rate > 0 else 0
            print(f"[{idx + 1}/{total}] Progress: {successful} ✅ | {failed} ❌ | "
                  f"ETA: {int(remaining/60)}m {int(remaining%60)}s")
        
        # Fetch movie data
        movie_data = fetch_movie_from_tmdb(movie_id, api_key)
        
        if movie_data:
            if "error" in movie_data:
                # Show first few errors
                if failed < 3:
                    error_msg = movie_data['error']
                    print(f"   ⚠️  Movie {movie_id} ({title_from_csv}): {error_msg}")
                failed += 1
                errors.append(f"Movie {movie_id}: {movie_data['error']}")
            else:
                movies_data.append({
                    'title': movie_data['title'],
                    'overview': movie_data['overview']
                })
                successful += 1
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
        
        # Check if output file exists
        if os.path.exists(output_file):
            # Merge with existing movies
            try:
                existing_df = pd.read_csv(output_file)
                existing_titles = set(existing_df['title'].str.lower())
                new_movies = movies_df[~movies_df['title'].str.lower().isin(existing_titles)]
                
                if len(new_movies) > 0:
                    combined_df = pd.concat([existing_df, new_movies], ignore_index=True)
                    combined_df = combined_df.drop_duplicates(subset=['title'])
                    movies_df = combined_df
                    print(f"\n   📊 Merged with existing {len(existing_df)} movies")
                    print(f"   ➕ Added {len(new_movies)} new movies")
            except:
                pass  # If can't merge, just overwrite
        
        movies_df.to_csv(output_file, index=False)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n" + "=" * 70)
        print(f"✅ SUCCESS!")
        print(f"=" * 70)
        print(f"   Created/Updated: {output_file}")
        print(f"   Total movies: {len(movies_df)}")
        print(f"   Successful fetches: {successful}")
        print(f"   Failed: {failed}")
        print(f"   Time taken: {int(elapsed_time/60)}m {int(elapsed_time%60)}s")
        print(f"\n   🚀 Restart your server to load the updated dataset!")
        print(f"   Run: cd backend && uvicorn main:app --reload")
        print("=" * 70)
        return True
    else:
        print(f"\n❌ No movies were fetched successfully.")
        if errors:
            print(f"   Errors encountered:")
            for error in errors[:5]:
                print(f"      - {error}")
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
    
    fetch_movies_from_credits_csv(api_key=api_key, limit=limit)

