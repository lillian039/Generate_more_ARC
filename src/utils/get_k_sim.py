import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class KSIM:
    def __init__(self, descriptions):
        self.descriptions = descriptions
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
        processed_descriptions = [preprocess(desc) for desc in descriptions]

        # Initialize the TF-IDF vectorizer
        vectorizer = TfidfVectorizer()

        # Fit and transform the processed descriptions
        tfidf_matrix = vectorizer.fit_transform(processed_descriptions)

        # Compute the cosine similarity matrix
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def _get_top_k_similar(self, similarity_matrix, k):
            print(sorted(similarity_matrix[k])[-k-1:-1])
            top_k_indices = np.argsort(similarity_matrix, axis=1)[:, -k-1:-1][:, ::-1]
            return top_k_indices

    def _get_top_large(self, similarity_matrix, min_value):
            # print(sorted(similarity_matrix))
            indices = [i for i, value in enumerate(similarity_matrix) if value > min_value]
            return indices


    def get_k_sim(self, str_task_description, k_sim):
        # Compute the top k similar descriptions
        top_sim = self._get_top_k_similar(self.similarity_matrix, k_sim)
        if str_task_description not in self.descriptions:
             print(str_task_description)
             return None
        cur_task_index = self.descriptions.index(str_task_description)
        return top_sim[cur_task_index]

    def get_lager_sim(self, str_task_description, min_value):
        if str_task_description not in self.descriptions:
             print(str_task_description)
             return None
        cur_task_index = self.descriptions.index(str_task_description)
        top_sim = self._get_top_large(self.similarity_matrix[cur_task_index], min_value)
        return top_sim

    def get_content_from_index(self, index, transformation_rule):
        concept = []
        for i in index:
             concept += transformation_rule[i]
        return concept
    
    def get_object_from_index(self, index):
        objects = []
        for i in index:
              objects.append(self.descriptions[i])
        return objects