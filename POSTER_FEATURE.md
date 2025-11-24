# Movie Poster Feature

The application now supports displaying movie posters in recommendations and search results!

## What's New

### ✅ Backend Updates

1. **Fetch Script** (`fetch_movies_from_imdb_api.py`):
   - Added `fetch_movie_poster()` function to get poster URLs from IMDb API
   - Updated `extract_movie_info()` to fetch and store poster URLs
   - Posters are saved to CSV in the `poster` column

2. **Model** (`model.py`):
   - Updated `get_recommendations()` to include poster URLs in results
   - Handles missing poster data gracefully

3. **API** (`main.py`):
   - Search results now include poster URLs
   - Recommendations include poster URLs

### ✅ Frontend Updates

1. **JavaScript** (`main.js`):
   - `displayRecommendations()` now shows movie posters
   - `displaySearchResults()` now shows movie posters
   - Handles missing posters gracefully (hides poster element on error)

2. **CSS** (`main.scss`):
   - Added `.movie-card-chat__poster` styles for recommendation cards
   - Added `.search-result-item__poster` styles for search results
   - Responsive design with proper image sizing and flexbox layout

## CSV Structure

The `movies.csv` file now supports an optional `poster` column:

```csv
title,overview,poster
The Matrix,"A computer hacker learns...",https://example.com/poster.jpg
Inception,"A thief who steals...",https://example.com/poster2.jpg
```

If a movie doesn't have a poster, the column can be empty or omitted.

## How to Fetch Movies with Posters

### Using IMDb RapidAPI

```bash
cd backend
python fetch_movies_from_imdb_api.py
```

This script will:
1. Fetch movies from Top Box Office, Most Popular, and Top Rated
2. Get poster URLs from IMDb API using movie IDs
3. Save everything to `movies.csv` with poster URLs included

### Poster URLs

The script fetches posters from:
- IMDb RapidAPI endpoint: `/api/imdb/{imdb_id}/poster`
- Posters are stored as full URLs in the CSV

## Display

### Recommendation Cards

Posters appear on the left side of recommendation cards:
- Size: 150x225px (desktop), 100x150px (mobile)
- Rounded corners
- Proper aspect ratio maintained

### Search Results

Posters appear as thumbnails in search results:
- Size: 80x120px
- Compact design for list view

## Error Handling

- If a poster URL fails to load, the image is hidden automatically
- Movies without posters still display correctly (just no image)
- The layout adapts gracefully whether posters are present or not

## Future Enhancements

Possible improvements:
- Fallback poster images (placeholder images)
- Lazy loading for better performance
- Poster caching
- Higher resolution options

