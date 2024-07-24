import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pydpp.dpp import DPP
import random

# random_seed = 123
# np.random.seed(random_seed)
# random.seed(random_seed)

# Prepare your dataset
# descriptions = [
#     "The cat is on the mat.",
#     "A dog is in the yard.",
#     "Birds are flying in the sky.",
#     "The sun is shining brightly.",
#     "There are clouds in the sky."
# ]

def get_dpp(descriptions, random_seed, size=100):
    np.random.seed(random_seed)
    random.seed(random_seed)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(descriptions).toarray()

    dpp = DPP(X)
    dpp.compute_kernel(kernel_type='cos-sim')
    samples = dpp.sample_k(size)
    # print(samples)
    return_description = [descriptions[i] for i in samples]
    random.shuffle(return_description)
    return return_description