import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity


movies=pd.read_csv('movies.csv')
credits=pd.read_csv('credits.csv')

movies=movies.merge(credits,on='title')

#PREPROCESSING DATA
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]

#droping null values 
movies.dropna(inplace=True)

#converting the string in to list 
def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)

#exracting the first 3 cast 
def convert3(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L

movies['cast']=movies['cast'].apply(convert3)

#exracting the directors from the crew
def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
            break
    return L

movies['crew']=movies['crew'].apply(fetch_director)

#overview
movies['overview']=movies['overview'].apply(lambda x:x.split())

#spaces between the names are removes
movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])

#merging the columns
movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

new_df=movies[['movie_id','title','tags']]
new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: x.lower())


#VECTORIZATION

#[actions,action,acting] =[act,act,act]
ps=PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    
    return " ".join(y)

new_df.loc[:, 'tags'] = new_df['tags'].apply(stem)

cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()
cv.get_feature_names_out()

#cosine similarity distance
similarity=cosine_similarity(vectors)

#Main function
def recommend(movie):
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    for i in movie_list:
            print(new_df.iloc[i[0]].title)

recommend('Spider-Man 2')
