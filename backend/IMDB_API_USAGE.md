# IMDb RapidAPI Integration

This script uses the IMDb RapidAPI to fetch popular movies from multiple sources.

## Available Endpoints

The script uses these IMDb RapidAPI endpoints:

1. **Top Box Office**: `/api/imdb/top-box-office`
2. **Most Popular Movies**: `/api/imdb/most-popular-movies`
3. **Top Rated English Movies**: `/api/imdb/top-rated-english-movies`
4. **Top 250 TV Shows**: `/api/imdb/top250-tv` (not used yet, but available)

## Additional Features Available

The API also provides:
- **Movie Posters**: `/api/imdb/{imdb_id}/poster`
- **Movie Cast**: `/api/imdb/{imdb_id}/cast`

## Usage

### Basic Usage (All Sources)

```bash
cd backend
python fetch_movies_from_imdb_api.py
```

This will fetch from all sources: top box office, most popular, and top rated.

### Specific Sources

```bash
# Only top box office
python fetch_movies_from_imdb_api.py box_office

# Multiple sources
python fetch_movies_from_imdb_api.py box_office,popular

# With limit per source
python fetch_movies_from_imdb_api.py box_office,popular 20
```

### Available Sources

- `box_office` - Top box office movies
- `popular` - Most popular movies
- `top_rated` - Top rated English movies

## API Key Configuration

The script uses the RapidAPI key from:
1. Environment variable `RAPIDAPI_KEY`
2. Default hardcoded key (replace with your own)

**To use your own key:**

```bash
export RAPIDAPI_KEY=your_key_here
python fetch_movies_from_imdb_api.py
```

Or edit the script and replace the default key in `RAPIDAPI_KEY` variable.

## Rate Limiting

The script includes:
- 0.25 second delay between requests
- Error handling for quota exceeded (429 status)
- Graceful handling of API errors

**Note**: If you exceed your monthly quota, you'll see an error message. You may need to upgrade your RapidAPI plan.

## API Response Structure

The script handles different response structures:
- Dictionary with `data` or `results` key
- Direct list of movies
- Various field names (title/Title, description/Description/plot, etc.)

## Troubleshooting

**Error: "You have exceeded the MONTHLY quota"**
- Your RapidAPI plan has reached its limit
- Upgrade your plan or wait for the quota to reset
- The script will continue with other sources if one fails

**Error: "No data returned"**
- API may be temporarily unavailable
- Check your internet connection
- Verify your API key is correct

**Movies not being added:**
- Check if movies already exist (duplicates are skipped)
- Ensure movies have valid titles and descriptions
- Check the console output for specific errors

