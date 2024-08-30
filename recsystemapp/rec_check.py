from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Create your views here.
import csv


def get_result(name):
    df=pd.read_csv("cosmetics.csv")
    df['tags']= df['Brand'] +','+ df['Label']+','+df['Name']+','+df['Ingredients']
    vectorizer = TfidfVectorizer()

    # fit the vectorizer to the documents and transform them into a matrix
    tfidf_matrix = vectorizer.fit_transform(df['tags'])

    # Compute the sigmoid kernel
    sig = sigmoid_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
        # Get the index corresponding to original_title
    idx = indices[name]

        # Get the pairwsie similarity scores 
    sig_scores = list(enumerate(sig[idx]))

        # Sort the movies 
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

        # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:11]

        # Movie indices
    indices = [i[0] for i in sig_scores]

        # Top 10 most similar movies
    result = df.iloc[indices].sort_values(by='Rank',ascending=False)
    return list(result)

get_result()