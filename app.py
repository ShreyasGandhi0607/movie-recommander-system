from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=3667c3fcfda14f207445d8c6d1303b64&language=en-US'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


if __name__ == '__main__':
    movies = pickle.load(open('notebook/movies.pkl', 'rb'))
    similarity = pickle.load(open('notebook/similiraty.pkl', 'rb'))
    movie_list = movies['title'].values
    app.run(debug=True)
