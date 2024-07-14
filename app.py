import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{movie_id}?api_key=9f0ba8aa44abd01293ef1c2065b4736f&language=en-US'.format(
        movie_id=movie_id)
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w185/" + data['poster_path']


def recommend(movie):
    # Ensure correct indexing
    ind = movies[movies['title'] == movie].index[0]
    distances = simi[ind]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


# Load the movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Align the movies dataframe and the similarity matrix
simi = pickle.load(open('simi.pkl', 'rb'))

# Ensure that the similarity matrix is a DataFrame and aligns with the movie indices
simi_df = pd.DataFrame(simi, index=movies.index, columns=movies.index)

# Streamlit app
st.title('MovieRec')

selected_movie_name = st.selectbox('What is your favorite movie?', movies['title'].values)

if st.button('Recommend'):
    name, posters = recommend(selected_movie_name)

    st.write('Here are some movies you might like:')
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(posters[0])

    with col2:
        st.text(name[1])
        st.image(posters[1])

    with col3:
        st.text(name[2])
        st.image(posters[2])

    with col4:
        st.text(name[3])
        st.image(posters[3])

    with col5:
        st.text(name[4])
        st.image(posters[4])
