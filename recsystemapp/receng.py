from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import joblib

df=pd.read_csv("cosmetics.csv")
df['tags']= df['Brand'] +','+ df['Label']+','+df['Name']+','+df['Ingredients']

def give_rec(title):
    vectorizer = TfidfVectorizer()

# fit the vectorizer to the documents and transform them into a matrix
    tfidf_matrix = vectorizer.fit_transform(df['tags'])

# Compute the sigmoid kernel
    sig = sigmoid_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['Name']).drop_duplicates()
    # Get the index corresponding to original_title
    idx = indices[title]

    # Get the pairwsie similarity scores 
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies 
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:11]

    # Movie indices
    indices = [i[0] for i in sig_scores]

    # Top 10 most similar movies
    return df.iloc[indices].sort_values(by='Rank',ascending=False)


vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['tags'])
sig = sigmoid_kernel(tfidf_matrix, tfidf_matrix)
joblib.dump(sig,'sigkernal.joblib')
joblib.dump(vectorizer,'vectorizer.joblib')