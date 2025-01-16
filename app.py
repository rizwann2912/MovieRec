import streamlit as st
import pickle
import requests
import gdown
import os

# File paths
simi_file = 'simi.pkl'
movies_file = 'movies.pkl'

# Download the simi.pkl file from Google Drive if not already present
if not os.path.exists(simi_file):
    url = 'https://drive.google.com/uc?id=17rwhbxHtHQUTSi0K05ALh8EKf20iZWmq'  # Corrected URL
    output = simi_file
    gdown.download(url, output, quiet=False)

# Check if movies.pkl exists
if os.path.exists(movies_file):
    print(f"{movies_file} loaded successfully!")
else:
    print(f"{movies_file} is not found.")

# Load the similarity matrix and movies list
simi = pickle.load(open(simi_file, 'rb'))
movies_list = pickle.load(open(movies_file, 'rb'))

# Function to fetch poster URLs using TMDB API
def fetch_poster(movie_title):
    api_key = '9f0ba8aa44abd01293ef1c2065b4736f'
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    try:
        response = requests.get(url)
        data = response.json()

        if data['results']:
            poster_path = data['results'][0]['poster_path']
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/200x300?text=Poster+Not+Found"
    except requests.exceptions.RequestException as e:
        return "https://via.placeholder.com/200x300?text=Error+Fetching+Poster"

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

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://files.oaiusercontent.com/file-KEsjUddqenHi2bHinEUVqv?se=2025-01-15T22%3A03%3A28Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D1950ce40-e7f9-4651-835c-c73bfbb1705d.webp&sig=Cd/VzgA1EDt0wjNCIiOp2fINCZ4dLL9wXSpyXnfYjLs%3D");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app title
st.title('Movie Recommender System')

st.markdown(
    """
    <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
    <strong>Note:</strong> The recommendations are based on similarities in the <em>cast, directors, and overview</em> of the movies.
    </div>
    """,
    unsafe_allow_html=True
)
# Dropdown to select a movie
selected_movie_name = st.selectbox('Select which movie you liked the most', movies_list['title'].values)

# Button to generate recommendations
if st.button('Recommend', type='primary'):
    recommend(selected_movie_name)
