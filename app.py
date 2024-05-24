import streamlit as st
import pickle
import pandas as pd
import requests
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

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
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        try:
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movies.append(movies.iloc[i[0]].title)
        except:
            pass
    return recommended_movies, recommended_movie_posters


page_bg_img = """
        <style>
        [data-testid="stAppViewContainer"]{
            background-image: url("https://user-images.githubusercontent.com/33485020/108069438-5ee79d80-7089-11eb-8264-08fdda7e0d11.jpg");
            background-size: cover;
        }
        #movie-recommendation-system{
        color:red;
        background-color:rgba(0,0,0,0.7);
        }
       /*[data-testid="stMarkdownContainer"]{
       background-color:rgba(0,0,0,0.7);
       }*/
        </style>
        """
st.title('Movie Recommendation System')
movie_watched = st.selectbox(
    'What movie have you watched?',
    (movies['title'].values)
)

if st.button('Recommend', type='primary'):
    names, posters = recommend(movie_watched)
    col1, col2, col3, col4, col5 = st.columns(5)
    try:
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])
    except:
        pass

st.markdown(page_bg_img, unsafe_allow_html=True)


