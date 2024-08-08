
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import json
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

path_origin = 'result/library/3_format_remove_2024-07-24_18-24-03.json'
path_enlarge = 'result/enlarged_library/self_instruct_4t_similar.json'

with open(path_origin, 'r') as f:
    data_origin = json.load(f)['transformation_library']
with open(path_enlarge, 'r') as f:
    data_enlarge = json.load(f)['transformation_library']

# Download NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize the lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    # Remove non-alphabetic characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z]', ' ', text).lower()
    # Tokenize the text
    words = text.split()
    # Remove stop words and lemmatize
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

# Preprocess the descriptions
processed_descriptions = [preprocess(desc) for desc in data_origin + data_enlarge]

# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the processed descriptions
tfidf_matrix = vectorizer.fit_transform(processed_descriptions)

tsne = TSNE(n_components=2, random_state=42, init='random')
X_tsne = tsne.fit_transform(tfidf_matrix.toarray())

plt.figure(figsize=(10, 6))
plt.scatter(X_tsne[:len(data_origin), 0], X_tsne[:len(data_origin), 1], label='Original')
plt.scatter(X_tsne[len(data_origin):, 0], X_tsne[len(data_origin):, 1], label='Enlarged')
plt.legend()
plt.savefig('tsne_similar_400.png')
plt.show()