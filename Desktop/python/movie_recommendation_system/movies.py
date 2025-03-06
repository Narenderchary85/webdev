import streamlit as st
import pandas as pd
from movie_recommendation_system.movie import new_df,similarity
import requests

# def fetch_poster(movie_id):
#     response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
#     data=response.json()
#     return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

df=pd.read_csv('credits.csv')
movies_list=new_df['title'].values
st.title("Movie Recommondation")

def recommend(movie):
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    #recommended_movies_posters=[]
    for i in movie_list:
        #movie_id=new_df.iloc[i[0]].movie_id
        recommended_movies.append(new_df.iloc[i[0]].title)
       # recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies#,recommended_movies_posters


selected_movie=st.selectbox('Movie Name',movies_list)
if st.button('Recommond'):
    names=recommend(selected_movie)
    for i in names:
        st.write(i)
    # col1,col2,col3,col4,col5=st.beta_columns(5)
    # with col1:
    #     st.text(names[0])
    #     st.image(posters[0])
    # with col2:
    #     st.text(names[1])
    #     st.image(posters[2])
    # with col3:
    #     st.text(names[3])
    #     st.image(posters[3])
    # with col4:
    #     st.text(names[4])
    #     st.image(posters[4])
    # with col5:
    #     st.text(names[5])
    #     st.image(posters[5])