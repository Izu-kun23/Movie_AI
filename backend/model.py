import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


class MovieRecommendationModel:
    """Movie recommendation model using TF-IDF and cosine similarity."""
    
    def __init__(self, csv_path='movies.csv'):
        """
        Initialize the recommendation model.
        
        Args:
            csv_path: Path to the movies CSV file
        """
        self.csv_path = csv_path
        self.df = None
        self.tfidf_matrix = None
        self.vectorizer = None
        self.is_loaded = False
    
    def clean_text(self, text):
        """
        Clean and preprocess text data.
        
        Args:
            text: Text string to clean
            
        Returns:
            Cleaned text string
        """
        if pd.isna(text):
            return ""
        # Convert to lowercase
        text = str(text).lower()
        # Remove special characters and keep only alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def load_data(self):
        """Load and preprocess the movie dataset."""
        try:
            # Load CSV file
            self.df = pd.read_csv(self.csv_path)
            
            # Validate required columns
            required_columns = ['title', 'overview']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Drop rows with missing titles or overviews
            self.df = self.df.dropna(subset=['title', 'overview'])
            
            # Clean the overview text
            self.df['cleaned_overview'] = self.df['overview'].apply(self.clean_text)
            
            # Reset index for easier indexing
            self.df = self.df.reset_index(drop=True)
            
            print(f"Loaded {len(self.df)} movies successfully.")
            self.is_loaded = True
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Movie dataset not found at {self.csv_path}. Please download it from the sources mentioned in README.md")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def build_model(self):
        """Build TF-IDF vectorizer and compute similarity matrix."""
        if not self.is_loaded:
            self.load_data()
        
        # Initialize TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)  # Use unigrams and bigrams
        )
        
        # Fit and transform the cleaned overviews
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['cleaned_overview'])
        
        print("TF-IDF model built successfully.")
    
    def find_movie_index(self, movie_title):
        """
        Find the index of a movie by title (case-insensitive, partial match).
        
        Args:
            movie_title: Title of the movie to find
            
        Returns:
            Index of the movie in the dataframe, or None if not found
        """
        movie_title_lower = str(movie_title).lower().strip()
        
        # Try exact match first
        exact_match = self.df[self.df['title'].str.lower() == movie_title_lower]
        if not exact_match.empty:
            return exact_match.index[0]
        
        # Try partial match
        partial_match = self.df[self.df['title'].str.lower().str.contains(movie_title_lower, na=False)]
        if not partial_match.empty:
            return partial_match.index[0]
        
        return None
    
    def get_recommendations(self, movie_title, limit=5):
        """
        Get movie recommendations based on a given movie title.
        
        Args:
            movie_title: Title of the movie to get recommendations for
            limit: Number of recommendations to return
            
        Returns:
            Dictionary containing the requested movie and list of recommendations
        """
        if not self.is_loaded or self.tfidf_matrix is None:
            self.build_model()
        
        # Find the movie index
        movie_idx = self.find_movie_index(movie_title)
        
        if movie_idx is None:
            return {
                "error": f"Movie '{movie_title}' not found in the database.",
                "requested_movie": movie_title,
                "recommendations": []
            }
        
        # Get the TF-IDF vector for the requested movie
        movie_vector = self.tfidf_matrix[movie_idx]
        
        # Calculate cosine similarity with all movies
        similarity_scores = cosine_similarity(movie_vector, self.tfidf_matrix).flatten()
        
        # Get indices of most similar movies (excluding the movie itself)
        similar_indices = np.argsort(similarity_scores)[::-1][1:limit+1]
        
        # Build recommendations list
        recommendations = []
        for idx in similar_indices:
            movie_data = {
                "title": self.df.iloc[idx]['title'],
                "overview": self.df.iloc[idx]['overview'],
                "similarity_score": float(similarity_scores[idx])
            }
            # Add poster URL if available
            if 'poster' in self.df.columns:
                poster = self.df.iloc[idx].get('poster')
                if pd.notna(poster) and str(poster).strip() and str(poster) != 'nan':
                    movie_data["poster"] = str(poster).strip()
            recommendations.append(movie_data)
        
        return {
            "requested_movie": self.df.iloc[movie_idx]['title'],
            "recommendations": recommendations
        }


# Global model instance (will be initialized in main.py)
model = None

