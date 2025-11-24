"""
Fetch movies from IMDb RapidAPI using various endpoints:
- Top Box Office
- Most Popular Movies
- Top Rated English Movies
- Top 250 TV Shows

This script fetches movie data and adds it to movies.csv
"""
import pandas as pd
import requests
import time
import os
from typing import Optional, Dict, List

# IMDb RapidAPI Configuration
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "4693d1a451mshbcee3887e70e47bp12b701jsn82f577692fd1")
RAPIDAPI_BASE_URL = "https://imdb236.p.rapidapi.com/api/imdb"
RAPIDAPI_HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "imdb236.p.rapidapi.com"
}

def fetch_movie_details(imdb_id: str) -> Optional[Dict]:
    """
    Fetch detailed movie information from IMDb using movie ID.
    
    Args:
        imdb_id: IMDb ID (e.g., "tt0816692")
        
    Returns:
        Dictionary with movie data or None if not found
    """
    try:
        # Fetch movie details (you may need to adjust the endpoint based on API)
        url = f"{RAPIDAPI_BASE_URL}/{imdb_id}"
        response = requests.get(url, headers=RAPIDAPI_HEADERS, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    except Exception as e:
        print(f"   ⚠️  Error fetching details for {imdb_id}: {str(e)}")
        return None

def fetch_movie_poster(imdb_id: str) -> Optional[str]:
    """
    Fetch movie poster URL from IMDb API.
    
    Args:
        imdb_id: IMDb ID (e.g., "tt0816692")
        
    Returns:
        Poster URL string or None if not found
    """
    try:
        url = f"{RAPIDAPI_BASE_URL}/{imdb_id}/poster"
        response = requests.get(url, headers=RAPIDAPI_HEADERS, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Handle different response structures
            poster_url = (
                data.get("poster") or
                data.get("Poster") or
                data.get("image") or
                data.get("Image") or
                data.get("url") or
                data.get("Url")
            )
            return poster_url if poster_url and poster_url != "N/A" else None
        return None
    except Exception as e:
        return None

def fetch_movie_description(imdb_id: str) -> Optional[str]:
    """
    Try to fetch movie description/plot from IMDb.
    Note: Adjust this based on the actual API response structure.
    """
    try:
        url = f"{RAPIDAPI_BASE_URL}/{imdb_id}"
        response = requests.get(url, headers=RAPIDAPI_HEADERS, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Try different possible keys for description
            description = (
                data.get("description") or 
                data.get("plot") or 
                data.get("overview") or 
                data.get("summary") or
                data.get("plotSummary", {}).get("text", "")
            )
            return description if description else None
        return None
    except:
        return None

def fetch_top_box_office() -> List[Dict]:
    """Fetch top box office movies."""
    url = f"{RAPIDAPI_BASE_URL}/top-box-office"
    try:
        response = requests.get(url, headers=RAPIDAPI_HEADERS, timeout=10)
        if response.status_code == 429:
            print(f"   ⚠️  Rate limit/quota exceeded. Please upgrade your RapidAPI plan.")
            return []
        elif response.status_code != 200:
            print(f"   ⚠️  API returned status {response.status_code}")
            return []
        
        data = response.json()
        
        # Handle quota exceeded message
        if isinstance(data, dict) and 'message' in data and 'quota' in data.get('message', '').lower():
            print(f"   ⚠️  API quota exceeded: {data.get('message', '')}")
            return []
        
        # Handle different response structures
        if isinstance(data, dict):
            return data.get("data", []) or data.get("results", []) or []
        elif isinstance(data, list):
            return data
        return []
    except Exception as e:
        print(f"   ⚠️  Error fetching top box office: {str(e)}")
        return []

def fetch_most_popular_movies() -> List[Dict]:
    """Fetch most popular movies."""
    url = f"{RAPIDAPI_BASE_URL}/most-popular-movies"
    try:
        response = requests.get(url, headers=RAPIDAPI_HEADERS, timeout=10)
        if response.status_code == 429:
            print(f"   ⚠️  Rate limit/quota exceeded. Please upgrade your RapidAPI plan.")
            return []
        elif response.status_code != 200:
            print(f"   ⚠️  API returned status {response.status_code}")
            return []
        
        data = response.json()
        
        if isinstance(data, dict) and 'message' in data and 'quota' in data.get('message', '').lower():
            print(f"   ⚠️  API quota exceeded: {data.get('message', '')}")
            return []
        
        if isinstance(data, dict):
            return data.get("data", []) or data.get("results", []) or []
        elif isinstance(data, list):
            return data
        return []
    except Exception as e:
        print(f"   ⚠️  Error fetching most popular: {str(e)}")
        return []

def fetch_top_rated_english() -> List[Dict]:
    """Fetch top rated English movies."""
    url = f"{RAPIDAPI_BASE_URL}/top-rated-english-movies"
    try:
        response = requests.get(url, headers=RAPIDAPI_HEADERS, timeout=10)
        if response.status_code == 429:
            print(f"   ⚠️  Rate limit/quota exceeded. Please upgrade your RapidAPI plan.")
            return []
        elif response.status_code != 200:
            print(f"   ⚠️  API returned status {response.status_code}")
            return []
        
        data = response.json()
        
        if isinstance(data, dict) and 'message' in data and 'quota' in data.get('message', '').lower():
            print(f"   ⚠️  API quota exceeded: {data.get('message', '')}")
            return []
        
        if isinstance(data, dict):
            return data.get("data", []) or data.get("results", []) or []
        elif isinstance(data, list):
            return data
        return []
    except Exception as e:
        print(f"   ⚠️  Error fetching top rated: {str(e)}")
        return []

def extract_movie_info(movie_item: Dict, source: str = "") -> Optional[Dict]:
    """
    Extract title, description, and poster from movie item.
    Handles different API response structures.
    """
    try:
        # Try different possible keys for title
        title = (
            movie_item.get("title") or
            movie_item.get("Title") or
            movie_item.get("name") or
            movie_item.get("Name") or
            movie_item.get("originalTitle") or
            movie_item.get("fullTitle")
        )
        
        if not title:
            return None
        
        # Get IMDb ID
        imdb_id = (
            movie_item.get("id") or
            movie_item.get("Id") or
            movie_item.get("imdbId") or
            movie_item.get("imdbID") or
            movie_item.get("imdb_id") or
            movie_item.get("imdb") or
            ""  # Extract from fullTitle if present
        )
        
        # Try to extract IMDb ID from fullTitle format like "Movie Title (2023) (tt1234567)"
        if not imdb_id and isinstance(movie_item.get("fullTitle"), str):
            import re
            match = re.search(r'tt\d{7,8}', movie_item.get("fullTitle", ""))
            if match:
                imdb_id = match.group(0)
        
        # Try different possible keys for description
        description = (
            movie_item.get("description") or
            movie_item.get("Description") or
            movie_item.get("plot") or
            movie_item.get("Plot") or
            movie_item.get("overview") or
            movie_item.get("Overview") or
            movie_item.get("summary") or
            movie_item.get("Summary") or
            movie_item.get("plotSummary", {}).get("text", "") if isinstance(movie_item.get("plotSummary"), dict) else ""
        )
        
        # Try different possible keys for poster
        poster_url = (
            movie_item.get("poster") or
            movie_item.get("Poster") or
            movie_item.get("image") or
            movie_item.get("Image") or
            movie_item.get("posterUrl") or
            movie_item.get("thumbnail") or
            None
        )
        
        # If no description or poster, try to fetch from IMDb API using IMDb ID
        if imdb_id:
            if not description or len(description.strip()) < 10:
                description = fetch_movie_description(imdb_id)
                time.sleep(0.25)  # Rate limiting
            
            if not poster_url or poster_url == "N/A":
                poster_url = fetch_movie_poster(imdb_id)
                time.sleep(0.25)  # Rate limiting
        
        # If still no description, create a placeholder
        if not description or len(description.strip()) < 10:
            description = f"A popular {source.lower()} movie: {title}"
        
        result = {
            "title": title.strip(),
            "overview": description.strip()
        }
        
        # Add poster if available
        if poster_url and poster_url != "N/A":
            result["poster"] = poster_url.strip()
        
        return result
        
    except Exception as e:
        print(f"   ⚠️  Error extracting movie info: {str(e)}")
        return None

def fetch_movies_from_imdb_api(
    output_file: str = "movies.csv",
    sources: Optional[List[str]] = None,
    limit_per_source: Optional[int] = None
):
    """
    Fetch movies from IMDb RapidAPI and add to movies.csv.
    
    Args:
        output_file: Path to output CSV file
        sources: List of sources to fetch from ['box_office', 'popular', 'top_rated']
        limit_per_source: Limit number of movies per source
    """
    print("=" * 70)
    print("Fetch Movies from IMDb RapidAPI")
    print("=" * 70)
    
    if sources is None:
        sources = ['box_office', 'popular', 'top_rated']
    
    # Load existing movies
    existing_titles = set()
    if os.path.exists(output_file):
        try:
            existing_df = pd.read_csv(output_file)
            existing_titles = set(existing_df['title'].str.lower().str.strip())
            print(f"\n✅ Loaded existing database with {len(existing_df)} movies")
        except:
            print(f"\n⚠️  Could not load existing {output_file}, will create new file")
    
    all_movies = []
    
    # Fetch from different sources
    source_functions = {
        'box_office': ('Top Box Office', fetch_top_box_office),
        'popular': ('Most Popular Movies', fetch_most_popular_movies),
        'top_rated': ('Top Rated English Movies', fetch_top_rated_english)
    }
    
    for source in sources:
        if source not in source_functions:
            print(f"\n⚠️  Unknown source: {source}, skipping...")
            continue
        
        source_name, fetch_func = source_functions[source]
        print(f"\n📡 Fetching {source_name}...")
        
        try:
            movies_data = fetch_func()
            
            if not movies_data:
                print(f"   ❌ No data returned from {source_name}")
                continue
            
            print(f"   ✅ Received {len(movies_data)} items")
            
            # Limit if specified
            if limit_per_source:
                movies_data = movies_data[:limit_per_source]
                print(f"   ⚠️  Limited to first {limit_per_source} items")
            
            # Extract movie info
            print(f"   🔄 Processing {len(movies_data)} movies...")
            processed = 0
            skipped = 0
            
            for item in movies_data:
                movie_info = extract_movie_info(item, source_name)
                
                if not movie_info:
                    skipped += 1
                    continue
                
                # Check if already exists
                title_lower = movie_info['title'].lower().strip()
                if title_lower in existing_titles:
                    skipped += 1
                    continue
                
                all_movies.append(movie_info)
                existing_titles.add(title_lower)
                processed += 1
                
                # Progress indicator
                if processed % 10 == 0:
                    print(f"      [{processed}/{len(movies_data)}] Processed...")
                
                # Rate limiting
                time.sleep(0.25)
            
            print(f"   ✅ Added {processed} new movies, skipped {skipped} (duplicates/missing info)")
            
        except Exception as e:
            print(f"   ❌ Error processing {source_name}: {str(e)}")
            continue
    
    # Save to CSV
    if all_movies:
        new_df = pd.DataFrame(all_movies)
        
        # Ensure poster column exists (fill missing with empty string)
        if 'poster' not in new_df.columns:
            new_df['poster'] = ''
        
        # Merge with existing if exists
        if os.path.exists(output_file):
            try:
                existing_df = pd.read_csv(output_file)
                # Ensure poster column exists in existing
                if 'poster' not in existing_df.columns:
                    existing_df['poster'] = ''
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                combined_df = combined_df.drop_duplicates(subset=['title'], keep='first')
                final_df = combined_df
            except:
                final_df = new_df
        else:
            final_df = new_df
        
        # Reorder columns: title, overview, poster
        column_order = ['title', 'overview']
        if 'poster' in final_df.columns:
            column_order.append('poster')
        final_df = final_df[[col for col in column_order if col in final_df.columns]]
        
        final_df.to_csv(output_file, index=False)
        
        print(f"\n" + "=" * 70)
        print(f"✅ SUCCESS!")
        print(f"=" * 70)
        print(f"   Created/Updated: {output_file}")
        print(f"   Total movies: {len(final_df)}")
        print(f"   New movies added: {len(all_movies)}")
        print(f"\n   🚀 Restart your server to load the updated dataset!")
        print(f"   Run: cd backend && uvicorn main:app --reload")
        print("=" * 70)
        return True
    else:
        print(f"\n⚠️  No new movies were added.")
        return False

if __name__ == "__main__":
    import sys
    
    sources = None
    limit = None
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        sources_arg = sys.argv[1]
        sources = [s.strip() for s in sources_arg.split(',') if s.strip()]
    
    if len(sys.argv) > 2:
        try:
            limit = int(sys.argv[2])
        except ValueError:
            print("⚠️  Invalid limit value, processing all movies")
    
    fetch_movies_from_imdb_api(sources=sources, limit_per_source=limit)

