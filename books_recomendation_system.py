# -*- coding: utf-8 -*-
"""Books_recomendation_system.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nDNgZdS4cl802b4KLM1Gsyxs41mc6jx7
"""

import numpy as np
import pandas as pd

movies=pd.read_csv('/content/tmdb_5000_movies.csv')
credits = pd.read_csv('/content/tmdb_5000_credits.csv')

movies.head(1)  #displaying first dataset of this csv file

credits.head()

movies=movies.merge(credits,on='title')
movies=movies[['genres','id','keywords','title','overview','cast','crew']]
movies.head()

#formatting genres,keywords,castand crew
#preprocessing
movies.isnull().sum() #getting all null values

movies.dropna(inplace=True)#droping all rows where there is null value
movies.duplicated().sum()
movies.iloc[0].genres #this format is in dictionary

def convert(obj):
  L=[]
  for i in ast.literal_eval(obj): # here the obj passed in this helper fuction is in list of string format but we want it in the format of just list
    L.append(i["name"]);
  return L

import ast
movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)

def convert3(obj):
  L=[]
  counter=0
  for i in ast.literal_eval(obj): # here the obj passed in this helper fuction is in list of string format but we want it in the format of just list
    if counter !=3:
      L.append(i["name"]);
      L.append(i["character"])
      counter+=1
    else:
      break
  return L

movies['cast']=movies['cast'].apply(convert3)
movies.head()

def fetch_director(obj):
  L=[]
  for i in ast.literal_eval(obj): # here the obj passed in this helper fuction is in list of string format but we want it in the format of just list
    if i["job"] =="Director":
      L.append(i["name"]);
      break;
  return L

movies['crew']=movies['crew'].apply(fetch_director)
movies.head()

#converting string overview to list
movies['overview']=movies['overview'].apply(lambda x:x.split())
movies.head()

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']
new_df=movies[['id','genres','title','tags']]
new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())

new_df['genres']=new_df['genres'].apply(lambda x:" ".join(x))
new_df['genres']=new_df['genres'].apply(lambda x:x.lower())

new_df.head()

'''here our preprocessing ends and actual code for finding the similar features of movies starts
vectorization tecnique is used here vo calculating the frequency of most commonly
occouring words and removing of stop words like is, on, the, will be removed'''
# vactorization is a Natural language Processing technique
#Vectorization techniques
#1. Bag of Words
#2. TF-IDF
#3. Word2Vec
'''Vectorization is jargon for a classic approach of converting input data from its raw format (i.e. text ) into
vectors of real numbers which is the format that ML models support.In Machine Learning, vectorization is a step in
feature extraction. The idea is to get some distinct features out of the text for the model to train on,
by converting text to numerical vectors.'''
# Bag of words
'''Most simple of all the techniques out there. It involves three operations:'''
# Tokenization:First, the input text is tokenized. A sentence is represented as a list of its constituent words, and it’s done for all the input sentences.
# Vocabulary creation:Of all the obtained tokenized words, only unique words are selected to create the vocabulary and then sorted by alphabetical order.
# Vector creation: Finally, a sparse matrix is created for the input, out of the frequency of vocabulary words. In this sparse matrix, each row is a
#                  sentence vector whose length (the columns of the matrix) is equal to the size of the vocabulary.

# this library is used for stamming which means that it will reove similar words used in different context like love,lovving, loved,lovelly
import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
    y=[]
    for i in text.split():
      y.append(ps.stem(i))

    return " ".join(y)

new_df['tags']=new_df['tags'].apply(stem)

from sklearn.feature_extraction.text import CountVectorizer
cv= CountVectorizer(max_features=5000,stop_words='english')
vector=cv.fit_transform(new_df['tags']).toarray()
cv.get_feature_names_out()

#here we will use cosine similarity rather than using eucledian distance as tags are being measured in vector quantity

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vector)
def recommend(movie):
  movie_index=new_df[new_df['title']==movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]

  for i in movies_list:
    print(new_df.iloc[i[0]].title)

def recommend1(genre):
  movie_index=new_df[new_df['genres']==genre].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]

  for i in movies_list:
    print(new_df.iloc[i[0]].title)

def switch_case(num):
  if num==1:
    name=input('Enter movie name: ')
    print()
    recommend(name)

  elif num==2 :
    genre=input('Enter Genre of movie type you want: ')
    print()
    recommend1(genre)

  else:
     print('Invalid type')

print('Welcome to the world of The silver screen')
print("Do you wanna watch movie ??? Let's  go.")
print()
while(True):
  print('what type of movie are you interested in?')
  print("1. Movie name ")
  print("2. Genre")
  print()
  num=int(input("Enter any one number"))
  print()
  switch_case(num)
  print()
  n=int(input('Do you want to continue? If yes enter 1: '))
  if n!=1:
    False
    break