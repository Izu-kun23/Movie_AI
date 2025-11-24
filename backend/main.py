from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import MovieRecommendationModel
from typing import Optional
import uvicorn
import random

# Initialize FastAPI app
app = FastAPI(
    title="Movie Recommendation API",
    description="AI-powered movie recommendation system using TF-IDF and cosine similarity",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
model = None

# Request models
class ChatMessage(BaseModel):
    message: str
    type: Optional[str] = "auto"

# AI responses for more conversational feel
GREETINGS = [
    "Hello! I'm your AI movie recommendation assistant. Tell me a movie you like, and I'll find similar ones for you! 🎬",
    "Hey there! Ready to discover your next favorite movie? Just tell me a film you enjoyed, and I'll work my magic! ✨",
    "Hi! I'm here to help you find amazing movies. Share a movie title you love, and let's explore! 🚀"
]

AI_RESPONSES = {
    "recommendation_intro": [
        "Based on your interest in \"{movie}\", I've found some fantastic recommendations for you!",
        "Great choice! If you enjoyed \"{movie}\", I think you'll love these similar films:",
        "Analyzing \"{movie}\"... Perfect! Here are some movies I think match your taste:"
    ],
    "recommendation_explanation": [
        "I recommend \"{title}\" because it shares similar themes and storytelling style. Similarity: {score:.0%}",
        "\"{title}\" is a great match! It has comparable narrative elements. Match: {score:.0%}",
        "You might enjoy \"{title}\" - it explores similar concepts. Compatibility: {score:.0%}"
    ],
    "error_not_found": [
        "Hmm, I couldn't find \"{movie}\" in my database. Could you try a different movie title?",
        "I don't have \"{movie}\" in my collection yet. Try searching for another film!",
        "Sorry, \"{movie}\" isn't in my database. Please suggest a different movie title."
    ],
    "error_general": [
        "Oops! Something went wrong. Let me try again...",
        "I encountered an issue. Could you rephrase your request?",
        "Hmm, I'm having trouble with that. Let's try something else!"
    ]
}

@app.on_event("startup")
async def startup_event():
    """Initialize the recommendation model on server startup."""
    global model
    try:
        model = MovieRecommendationModel(csv_path='movies.csv')
        model.load_data()
        model.build_model()
        print("Movie recommendation model initialized successfully!")
    except FileNotFoundError as e:
        print(f"Warning: {str(e)}")
        print("Please ensure movies.csv is in the project directory.")
        model = None
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        model = None


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Movie Recommendation API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running" if model is not None else "model not loaded"
    }


@app.get("/recommend")
async def recommend(
    movie: str = Query(..., description="Title of the movie to get recommendations for"),
    limit: int = Query(5, ge=1, le=20, description="Number of recommendations to return (1-20)")
):
    """
    Get movie recommendations based on a movie title.
    
    Args:
        movie: Title of the movie (case-insensitive, supports partial matches)
        limit: Number of recommendations to return (default: 5, max: 20)
    
    Returns:
        Dictionary containing the requested movie and recommendations
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Recommendation model is not loaded. Please ensure movies.csv exists."
        )
    
    try:
        result = model.get_recommendations(movie, limit=limit)
        
        # Check if movie was found
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/api/chat")
async def chat_endpoint(chat_message: ChatMessage):
    """
    AI chat endpoint for conversational movie recommendations.
    
    Expected format:
    {
        "message": "I like The Matrix",
        "type": "recommend" or "search" or "greeting" (optional, auto-detected if not provided)
    }
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Recommendation model is not loaded."
        )
    
    user_message = chat_message.message.strip().lower()
    msg_type = chat_message.type or "auto"
    
    try:
        # Auto-detect intent if not specified
        if msg_type == "auto":
            if any(word in user_message for word in ["hello", "hi", "hey", "greetings"]):
                msg_type = "greeting"
            elif any(word in user_message for word in ["recommend", "suggest", "similar", "like", "enjoyed"]):
                msg_type = "recommend"
            elif any(word in user_message for word in ["search", "find", "look for"]):
                msg_type = "search"
            else:
                msg_type = "recommend"  # Default to recommendation
        
        # Handle greeting
        if msg_type == "greeting":
            return {
                "type": "greeting",
                "message": random.choice(GREETINGS),
                "timestamp": None
            }
        
        # Extract movie title from message
        # Try to find movie titles in the message
        movie_title = None
        
        # Common patterns
        patterns = [
            "like (.+?)(?:,|$|!|.)",
            "recommend (.+?)(?:,|$|!|.)",
            "suggest (.+?)(?:,|$|!|.)",
            "similar to (.+?)(?:,|$|!|.)",
            "enjoyed (.+?)(?:,|$|!|.)",
            "watch (.+?)(?:,|$|!|.)",
            "search for (.+?)(?:,|$|!|.)",
            "find (.+?)(?:,|$|!|.)",
        ]
        
        import re
        for pattern in patterns:
            match = re.search(pattern, user_message, re.IGNORECASE)
            if match:
                movie_title = match.group(1).strip()
                break
        
        # If no pattern matched, try the whole message
        if not movie_title:
            # Remove common words
            words_to_remove = ["recommend", "suggest", "similar", "like", "movies", "movie", "film", "films"]
            words = user_message.split()
            movie_title = " ".join([w for w in words if w.lower() not in words_to_remove])
        
        if not movie_title or len(movie_title) < 2:
            return {
                "type": "error",
                "message": "I'd love to help! Could you tell me a movie title you'd like recommendations for?",
                "timestamp": None
            }
        
        # Handle search
        if msg_type == "search":
            query_lower = movie_title.lower()
            matches = model.df[
                model.df['title'].str.lower().str.contains(query_lower, na=False)
            ].head(10)
            
            if matches.empty:
                return {
                    "type": "search_results",
                    "message": f"I couldn't find any movies matching '{movie_title}'. Try a different search!",
                    "movies": [],
                    "timestamp": None
                }
            
            results = []
            for idx, row in matches.iterrows():
                movie_data = {
                    "title": row['title'],
                    "overview": row['overview']
                }
                # Add poster URL if available
                if 'poster' in matches.columns and pd.notna(row.get('poster')) and str(row.get('poster')).strip() and str(row.get('poster')) != 'nan':
                    movie_data["poster"] = str(row['poster']).strip()
                results.append(movie_data)
            
            return {
                "type": "search_results",
                "message": f"I found {len(results)} movies matching '{movie_title}':",
                "movies": results,
                "timestamp": None
            }
        
        # Handle recommendation
        result = model.get_recommendations(movie_title, limit=5)
        
        if "error" in result:
            error_msg = random.choice(AI_RESPONSES["error_not_found"]).format(movie=movie_title)
            return {
                "type": "error",
                "message": error_msg,
                "timestamp": None
            }
        
        # Create AI response
        intro = random.choice(AI_RESPONSES["recommendation_intro"]).format(movie=result["requested_movie"])
        
        # Add explanations for each recommendation
        recommendations_with_explanations = []
        for rec in result["recommendations"]:
            explanation = random.choice(AI_RESPONSES["recommendation_explanation"]).format(
                title=rec["title"],
                score=rec["similarity_score"]
            )
            recommendations_with_explanations.append({
                **rec,
                "explanation": explanation
            })
        
        return {
            "type": "recommendations",
            "message": intro,
            "requested_movie": result["requested_movie"],
            "recommendations": recommendations_with_explanations,
            "timestamp": None
        }
        
    except Exception as e:
        error_msg = random.choice(AI_RESPONSES["error_general"])
        return {
            "type": "error",
            "message": error_msg,
            "error": str(e),
            "timestamp": None
        }


@app.get("/movies/search")
async def search_movies(
    query: str = Query(..., description="Search query for movie titles"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results to return")
):
    """
    Search for movies by title.
    
    Args:
        query: Search query (case-insensitive, partial match)
        limit: Maximum number of results to return
    
    Returns:
        List of matching movies
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Recommendation model is not loaded. Please ensure movies.csv exists."
        )
    
    try:
        query_lower = query.lower().strip()
        matches = model.df[
            model.df['title'].str.lower().str.contains(query_lower, na=False)
        ].head(limit)
        
        results = []
        for idx, row in matches.iterrows():
            results.append({
                "title": row['title'],
                "overview": row['overview']
            })
        
        return {
            "query": query,
            "count": len(results),
            "movies": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
