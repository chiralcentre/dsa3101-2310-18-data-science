import numpy as np
import pandas as pd
import re
from gensim.models.doc2vec import TaggedDocument
import nltk
# Add to dockerfile
# RUN [ "python", "-c", "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')" ]
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


def cosine_similarity(v1, v2):
    return np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))


def euclidean_distance(v1, v2):
    return np.linalg.norm(v1-v2)


def embed_text(text, model, tokenizer):
    input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0)
    outputs = model(input_ids)
    last_hidden_states = outputs[0]  # The last hidden-state is the first element of the output tuple
    return last_hidden_states


class Preprocess:
    def __init__(self, data, sw_removal = False, stem = False, lem = False, ds_vocab = False):
        """
        tokenize: Tokenize the corpus
        sw_removal: Removes stopwords
        stem: Performs Stemming (lem must be False, else neither will be performed)
        lem: Performs Lemmatization (stem must be False, else neither will be performed)
        ds_vocb: Filters domain specific vocab.
            i.e. Words that does not help in comparison of uni courses like "student", "course"
            Adding or removing such words should not make the course description feel different
        """

        self.data = data.copy(deep=True)
        self.sw_removal = sw_removal
        self.stem = stem
        self.lem = lem
        self.ds_vocab = ds_vocab

        # Descriptions are short. So the course name may contain important information as well
        self.data['Course_Description'] = self.data['Course_Name'] + " " + self.data['Course_Description']

        # Remove line breaks and punctuations.
        self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: re.sub('\n', ' ',sentence))
        self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: re.sub(r'[^\w\s]', '',sentence))

        # Lowercase everything
        self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: sentence.lower())

        # Tokenization
        self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: word_tokenize(sentence))

        # Remove stopwords
        if self.sw_removal:
            stop_words = set(stopwords.words('english'))
            self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: [word for word in sentence if not word in stop_words])

        # Stemming
        if self.stem:
            if not self.lem:
                ps = PorterStemmer()
                self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: [ps.stem(word) for word in sentence])

        # Lemmatization
        if self.lem:
            if not self.stem:
                lemmatizer = WordNetLemmatizer()
                self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: [lemmatizer.lemmatize(word) for word in sentence])

        # Remove not very meaningful words
        if self.ds_vocab:
            unhelpful_words = {"course", "student", "topic", "concept", "also", "skill", "learn", "include", "knowledge", "aim", "study", "use", "using", "understanding", "different", "various", "cover", "understand", "provide", "able", "eg", "example"}
            self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: [word for word in sentence if not word in unhelpful_words])

        self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: ' '.join(sentence))

    def get_tagged_data(self, ngram_max = 1, tokens_only=False):  # For doc2vec. Return tagged data for training and tokens only for inference
        def process_sentence(sentence):
            output = []
            for i in range(1, ngram_max + 1):  # Apply ngram for n = 1,2,3...
                output += [" ".join(words) for words in ngrams(word_tokenize(sentence), n=i)]
            return output

        if tokens_only:
            return self.data.apply(lambda row:process_sentence(row["Course_Description"]), axis=1)
        return self.data.apply(lambda row:TaggedDocument(words=process_sentence(row["Course_Description"]), tags=[row.name]), axis=1)

    def count_vec(self, ngram_range = (1,1), max_features = None):
        count_vec = CountVectorizer(ngram_range = ngram_range, max_features = max_features)
        return count_vec.fit_transform(self.data["Course_Description"]).toarray()

    def tfidf(self, ngram_range = (1,1), max_features = None):
        tfidf = TfidfVectorizer(ngram_range = ngram_range, max_features = max_features)
        return tfidf.fit_transform(self.data["Course_Description"]).toarray()


class SciBERT_Model:
    def __init__(self, all_courses, all_jobs=None):
        for colname in ["School", "Major", "Course_Code", "Course_Name"]:
            if colname not in all_courses.colnames.values:
                raise Exception(f"Column {colname} is not found in courses data")

        all_courses["id"] = all_courses[["School", "Major", "Course_Code", "Course_Name"]].agg("_".join, axis=1)
        all_courses = all_courses.set_index("id")
        processed_data = Preprocess(all_courses, sw_removal=True, lem=True, ds_vocab=True)
        tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
        model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased')
        all_courses["scibert_vector"] = [embed_text(sentence, model, tokenizer).mean(1).detach().numpy().flatten() for
                                         sentence in processed_data.data["Course_Description"]]


# for i, course in enumerate(all_courses.index):
#     print(course)
#
#     BERT_dis = all_courses.apply(lambda row:[row.name, cosine_similarity(row["scibert_vector"], all_courses.loc[course, "scibert_vector"])], axis=1)
#     BERT_dis = list(BERT_dis)
#     BERT_dis.sort(key = lambda x:x[1], reverse=True)
#     BERT_dis = BERT_dis[1:]  # Remove itself from list of distances (which has cos distance 1)
#     threshold = 0.8
#     print("SciBERT cosine similarity:", list(filter(lambda x: x[1] > threshold, BERT_dis)))
#     print("-----------------------------------------------------------------------------------------------------")
#     if i>20: break