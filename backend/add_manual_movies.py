"""
Manually add popular movies to movies.csv
Useful when API quota is exceeded or for testing
"""
import pandas as pd

# Popular movies with descriptions
POPULAR_MOVIES = [
    {
        "title": "The Matrix",
        "overview": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
    },
    {
        "title": "The Matrix Reloaded",
        "overview": "Neo and his allies race against time before the machines discover the City of Zion and destroy it. Meanwhile, Neo must decide how he can save Trinity from a dark fate in his dreams."
    },
    {
        "title": "The Matrix Revolutions",
        "overview": "The human city of Zion defends itself against the massive invasion of the machines as Neo fights to end the war at another front while also opposing the rogue Agent Smith."
    },
    {
        "title": "Inception",
        "overview": "A skilled thief is given a chance at redemption by entering the subconscious of a target through dream invasion technology."
    },
    {
        "title": "Interstellar",
        "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
    },
    {
        "title": "Blade Runner",
        "overview": "A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator."
    },
    {
        "title": "Blade Runner 2049",
        "overview": "A young blade runner's discovery of a long-buried secret leads him to track down former blade runner Rick Deckard, who's been missing for thirty years."
    },
    {
        "title": "The Dark Knight",
        "overview": "When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    },
    {
        "title": "The Shawshank Redemption",
        "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    },
    {
        "title": "Pulp Fiction",
        "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
    },
    {
        "title": "Fight Club",
        "overview": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more."
    },
    {
        "title": "The Godfather",
        "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
    },
    {
        "title": "Forrest Gump",
        "overview": "The presidencies of Kennedy and Johnson through the eyes of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart."
    },
    {
        "title": "Avatar",
        "overview": "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home."
    },
    {
        "title": "Star Wars",
        "overview": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle station."
    },
    {
        "title": "The Lord of the Rings: The Fellowship of the Ring",
        "overview": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron."
    },
    {
        "title": "The Lord of the Rings: The Return of the King",
        "overview": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring."
    },
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "overview": "An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, his family and the terrible evil that haunts the magical world."
    },
    {
        "title": "Iron Man",
        "overview": "After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil."
    },
    {
        "title": "Batman Begins",
        "overview": "After training with his mentor, Batman begins his fight to free crime-ridden Gotham City from corruption."
    },
    {
        "title": "The Terminator",
        "overview": "A cyborg assassin is sent back in time to kill Sarah Connor, whose son will one day become a savior against machines in a post-apocalyptic future."
    },
    {
        "title": "Terminator 2: Judgment Day",
        "overview": "A cyborg, identical to the one who failed to kill Sarah Connor, must now protect her ten-year-old son John from a more advanced and powerful cyborg."
    },
    {
        "title": "Alien",
        "overview": "The crew of a commercial spacecraft encounter a deadly lifeform after investigating an unknown transmission."
    },
    {
        "title": "Aliens",
        "overview": "Decades after surviving the Nostromo incident, Ellen Ripley is sent out to re-establish contact with a terraforming colony but finds herself battling the Alien Queen and her offspring."
    },
    {
        "title": "Titanic",
        "overview": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."
    }
]

def add_manual_movies():
    """Add manually curated popular movies to movies.csv"""
    print("=" * 70)
    print("Adding Popular Movies (Manual Entry)")
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
    
    # Filter out movies that already exist
    new_movies = []
    for movie in POPULAR_MOVIES:
        title_lower = movie['title'].lower().strip()
        if title_lower not in existing_titles:
            new_movies.append(movie)
            existing_titles.add(title_lower)
        else:
            print(f"⏭️  '{movie['title']}' already exists")
    
    if new_movies:
        # Combine existing and new movies
        new_df = pd.DataFrame(new_movies)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        # Remove duplicates
        combined_df = combined_df.drop_duplicates(subset=['title'], keep='first')
        
        # Sort by title
        combined_df = combined_df.sort_values('title').reset_index(drop=True)
        
        # Save
        combined_df.to_csv('movies.csv', index=False)
        
        print(f"\n✅ SUCCESS!")
        print(f"   Added {len(new_movies)} new movies")
        print(f"   Total movies in database: {len(combined_df)}")
        print(f"\n   New movies added:")
        for movie in new_movies:
            print(f"      ✅ {movie['title']}")
        
        print(f"\n   🚀 Restart your server to load the updated dataset!")
        print(f"   Run: uvicorn main:app --reload")
    else:
        print(f"\n⚠️  No new movies were added")
        print(f"   All movies may already be in the database")

if __name__ == "__main__":
    add_manual_movies()



