
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import json
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from PIL import Image

path = 'data/LARC/larc_confident/'
files = os.listdir(path)
files = sorted(files)

descriptions = []
name_list = []
for file in files:
    cur_path = path + file
    with open(cur_path, 'r') as f:
        task = json.load(f)
    task_description = task['descriptions']
    name_list.append(task['name'])
    for i, description in enumerate(task_description):
        descriptions.append(description['see_description'] + ' ' + description['grid_description'] + ' ' + description['do_description'])


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

tsne = TSNE(n_components=2, random_state=42, init='random')
X_tsne = tsne.fit_transform(tfidf_matrix.toarray())
print(X_tsne)

def place_image(X_tsne):
    min_X  = min(min(row) for row in X_tsne)
    max_X = max(max(row) for row in X_tsne)
    scale = 20000
    X_scale = [[int((x - min_X) / (max_X - min_X) * scale) for x in row] for row in X_tsne]
    # image_path = 'img/train/cat_img_all/'
    image_path = 'img/syn_img_test/'
    result = Image.new('RGB', (scale + 300, scale + 300), color='white')
    for i, name in enumerate(name_list):
        name = name.split('.')[0]
        # img = Image.open(image_path + name + '_all_cat.png')
        img = Image.open(image_path + name + '_test_0_syn.png')
        width, height = img.size
        img = img.resize((200 * width // height, 200), Image.Resampling.BILINEAR)
        result.paste(img, (X_scale[i][0], X_scale[i][1]))
    result.save('img/tsne6.png')

place_image(X_tsne)
# plt.figure(figsize=(10, 6))
# scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
# plt.title("t-SNE visualization of the LARC confident dataset")
# plt.xlabel("t-SNE component 1")
# plt.ylabel("t-SNE component 2")
# plt.show()