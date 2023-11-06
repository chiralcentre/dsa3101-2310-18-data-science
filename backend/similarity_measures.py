import numpy as np
import pandas as pd
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import torch
from transformers import BertTokenizer, BertModel
# Add to dockerfile
# RUN [ "python", "-c", "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')" ]
# RUN ["git", "lfs", "install"]
# RUN ["git", "clone", "https://huggingface.co/bert-base-uncased"]


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def euclidean_distance(v1, v2):
    return np.linalg.norm(v1 - v2)


def embed_text(text, model, tokenizer):
    # Truncate off the front for job description. Info near the end is more relevant. Courses doesn't need truncation.
    text = " ".join(word_tokenize(text)[-512:])
    input_ids = torch.tensor([tokenizer.encode(text, truncation=True)])
    outputs = model(input_ids)
    hidden_states = outputs[2]
    token_vecs = hidden_states[-2][0]
    return torch.mean(token_vecs, dim=0)


class Preprocess:
    def __init__(self, data, sw_removal=False, stem=False, lem=False, ds_vocab=False):
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
        self.data['Course_Description'] = self.data['Course_Description'].apply(
            lambda sentence: re.sub('\n', ' ', sentence))
        self.data['Course_Description'] = self.data['Course_Description'].apply(
            lambda sentence: re.sub(r'[^\w\s]', '', sentence))

        # Lowercase everything
        self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: sentence.lower())

        # Tokenization
        self.data['Course_Description'] = self.data['Course_Description'].apply(
            lambda sentence: word_tokenize(sentence))

        # Remove stopwords
        if self.sw_removal:
            stop_words = set(stopwords.words('english'))
            self.data['Course_Description'] = self.data['Course_Description'].apply(
                lambda sentence: [word for word in sentence if not word in stop_words])

        # Stemming
        if self.stem:
            if not self.lem:
                ps = PorterStemmer()
                self.data['Course_Description'] = self.data['Course_Description'].apply(
                    lambda sentence: [ps.stem(word) for word in sentence])

        # Lemmatization
        if self.lem:
            if not self.stem:
                lemmatizer = WordNetLemmatizer()
                self.data['Course_Description'] = self.data['Course_Description'].apply(
                    lambda sentence: [lemmatizer.lemmatize(word) for word in sentence])

        # Remove not very meaningful words
        if self.ds_vocab:
            unhelpful_words = {"course", "student", "topic", "concept", "also", "skill", "learn", "include",
                               "knowledge", "aim", "study", "use", "using", "understanding", "different", "various",
                               "cover", "understand", "provide", "able", "eg", "example"}
            self.data['Course_Description'] = self.data['Course_Description'].apply(
                lambda sentence: [word for word in sentence if not word in unhelpful_words])

        self.data['Course_Description'] = self.data['Course_Description'].apply(lambda sentence: ' '.join(sentence))


class BERT_Model:
    def __init__(self, all_courses, all_jobs=None):
        """
        Inputs:
            all_courses: A pandas dataframe containing at least 4 columns named "School", "Major", "Course_Code", "Course_Name"
            (Optional) all_jobs: A pandas dataframe containing at least 3 columns named "job_title", "job_desc", "job_type"
        """
        for colname in ["School", "Major", "Course_Code", "Course_Name"]:
            if colname not in all_courses.columns.values:
                raise Exception(f"Column {colname} is not found in courses data")

        all_courses["id"] = all_courses[["School", "Major", "Course_Code", "Course_Name"]].agg("_".join, axis=1)
        all_courses = all_courses.set_index("id")
        processed_data = Preprocess(all_courses, sw_removal=True, lem=True, ds_vocab=True)
        # tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')  # Download from internet
        # model = AutoModel.from_pretrained('bert-base-uncased')
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)  # Read local model
        model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
        all_courses["bert_vector"] = [embed_text(sentence, model, tokenizer).detach().numpy() for
                                      sentence in processed_data.data["Course_Description"]]
        self.all_courses = all_courses

    def get_similar_courses(self, school, major, course_code, course_name, limit=-1, threshold=0):
        """
        Input the details of the target course. Output a dictionary of similar courses (in decreasing similarity)
        May limit output count and minimum cosine similarity threshold
        """
        id = "_".join([school, major, course_code, course_name])
        BERT_dis = self.all_courses.apply(
            lambda row: [row.name, cosine_similarity(row["bert_vector"], self.all_courses.loc[id, "bert_vector"])], axis=1)
        BERT_dis = list(BERT_dis)
        BERT_dis = list(filter(lambda x: x[1] >= threshold, BERT_dis))  # Apply minimum similarity threshold
        BERT_dis.sort(key=lambda x: x[1], reverse=True)
        if limit >= 0:
            return dict(BERT_dis[:limit])  # Apply output limit
        return dict(BERT_dis)


if __name__ == '__main__':  # Code for testing
    mdl = BERT_Model(pd.read_csv('Scraping/data/module_details_labelled.csv'))
    print(mdl.get_similar_courses("NUS", "CHS", "DSA1101", "Introduction to Data Science"))
    print(mdl.get_similar_courses("NUS", "CHS", "DSA1101", "Introduction to Data Science", limit=2))
    print(mdl.get_similar_courses("NUS", "CHS", "DSA1101", "Introduction to Data Science", threshold=0.9))
    # for i, course in enumerate(mdl.all_courses.index):
    #     print(course)
    #
    #     BERT_dis = mdl.all_courses.apply(
    #         lambda row: [row.name, cosine_similarity(row["bert_vector"], mdl.all_courses.loc[course, "bert_vector"])],
    #         axis=1)
    #     BERT_dis = list(BERT_dis)
    #     BERT_dis.sort(key=lambda x: x[1], reverse=True)
    #     BERT_dis = BERT_dis[1:]  # Remove itself from list of distances (which has cos distance 1)
    #     threshold = 0.9
    #     print("BERT cosine similarity:", list(filter(lambda x: x[1] > threshold, BERT_dis)))
    #     print("-----------------------------------------------------------------------------------------------------")
    #     if i > 20: break
