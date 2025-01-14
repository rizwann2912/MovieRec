import streamlit as st
import pickle
import requests  # To fetch poster URLs from TMDB API

# Load the similarity matrix and movies list
simi = pickle.load(open('simi.pkl', 'rb'))
movies_list = pickle.load(open('movies.pkl', 'rb'))


# Function to fetch poster URLs using TMDB API
def fetch_poster(movie_title):
    api_key = '9f0ba8aa44abd01293ef1c2065b4736f'
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(url)
    data = response.json()

    # Return the poster path if available, else a placeholder image
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        return f"https://image.tmdb.org/t/p/w500{poster_path}"  # Full poster URL
    else:
        return "https://via.placeholder.com/200x300?text=Poster+Not+Found"


# Define the recommendation function
def recommend(movie):
    ind = movies_list[movies_list['title'] == movie].index[0]
    distances = simi[ind]
    movies_list_ = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:30]

    st.write("### Recommendations:")

    # Create a grid with 3 columns
    cols = st.columns(3)  # 3 columns for layout
    for idx, i in enumerate(movies_list_):
        movie_title = movies_list.iloc[i[0]].title
        similarity_percentage = round(i[1] * 100, 2)  # Convert similarity to percentage
        poster_url = fetch_poster(movie_title)  # Fetch poster URL

        # Select the current column (cycled every 3 movies)
        with cols[idx % 3]:
            # Display the movie title, similarity, and poster
            st.image(poster_url, use_container_width=True)
            st.write(f"**{movie_title}**")
            st.write(f"Similarity: {similarity_percentage}%")

# Streamlit app title
st.title('Movie Recommender System')

# Dropdown to select a movie
selected_movie_name = st.selectbox('Select which movie you liked the most', movies_list['title'].values)

# Button to generate recommendations
if st.button('Recommend', type='primary'):
    recommend(selected_movie_name)
