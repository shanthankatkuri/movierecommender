import streamlit as st
import streamlit.components.v1 as components
import pickle
import pandas as pd
import re
import requests
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def convert_to_url_friendly(text):
    # Convert to lowercase
    text = text.lower()
    # Replace spaces with hyphens
    text = text.replace(' ', '-')
    # Remove any characters that are not letters, numbers, or hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=e9da140da37eaa85f480a34d0effa4b8')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    title = movies['title'].apply(lambda x : x.lower())
    movie_index = movies[title == movie.lower()].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    recommended_movies_ids = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        try:
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_ids.append(movie_id)
        except:
            pass
    return recommended_movies, recommended_movie_posters, recommended_movies_ids


page_bg_img = """
        <style>
        [data-testid="stAppViewContainer"]{
            background-image: url("https://user-images.githubusercontent.com/33485020/108069438-5ee79d80-7089-11eb-8264-08fdda7e0d11.jpg");
            background-size: cover;
        }
        [data-testid="stImage"]{
            border: 5px solid red;
            border-radius: 15px;
        }
        #movie-recommendation-system{
        color:red;
        background-color:rgba(0,0,0,0.7);
        }
        </style>
        """

st.title('Movie Recommendation System')
movie_watched = st.selectbox(
    'What movie have you watched?',
    (movies['title'].values)
)

if st.button('Recommend', type='primary'):
    names, posters, ids = recommend(movie_watched)
    for index, (name, poster,id) in enumerate(zip(names, posters, ids)):
        title_url = convert_to_url_friendly(name)
        target_link = f"https://www.themoviedb.org/movie/{id}-{title_url}"
        # print(title_url)
        # print(target_link)
        try:
            st.header(name)
            # st.image(poster)
            st.markdown(f'<a href="{target_link}" target="_blank"><img src="{poster}" alt="Clickable Image" style="border:5px solid red; border-radius:15px; width:300px;"></a>', unsafe_allow_html=True)
        except:
            pass

st.markdown(page_bg_img, unsafe_allow_html=True)


