import csv
import string


def load_movies(filename):
    movies = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            if row['overview']:  
                movies.append({
                    'title': row['title'],
                    'overview': row['overview'].lower()
                })
    return movies


def tokenize(text):
    
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text.translate(translator)
   
    return set(clean_text.lower().split())


def compute_similarity(words1, words2):
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    if not union:
        return 0
    return len(intersection) / len(union)


def recommend_movie(title, movies, top_n=3):
    input_movie = None
    
    for movie in movies:
        if movie['title'].lower() == title.lower():
            input_movie = movie
            break

    if not input_movie:
        return f"Movie '{title}' not found."

    
    input_words = tokenize(input_movie['overview'])

    scores = []
    for movie in movies:
        if movie['title'] == input_movie['title']:
            continue
       
        words = tokenize(movie['overview'])
        
        similarity = compute_similarity(input_words, words)
        scores.append((movie['title'], similarity))

    scores.sort(key=lambda x: x[1], reverse=True)

    
    return [title for title, _ in scores[:top_n]]


movies = load_movies(r'C:\Users\paul\Downloads\archive (5)\tmdb_5000_movies.csv')  
query = input("Enter the Query:")
recommendations = recommend_movie(query, movies)

print(f"\nMovies similar to '{query}':")
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")
