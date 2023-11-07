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
    # Second last layer contains the tokens' encoded vector. Only 1 batch so index [0].
    token_vecs = hidden_states[-2][0]
    # Average over all token vectors to get paragraph vector
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
                lambda sentence: [word for word in sentence if word not in stop_words])

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


class Preprocess_jobs:
    def __init__(self, data):
        self.data = data.copy(deep=True)

        # Remove line breaks and punctuations.
        self.data['job_desc'] = self.data['job_desc'].apply(lambda sentence: re.sub('\n', ' ',sentence))
        self.data['job_desc'] = self.data['job_desc'].apply(lambda sentence: re.sub(r'[^\w\s]', '',sentence))

        # Lowercase everything
        self.data['job_desc'] = self.data['job_desc'].apply(lambda sentence: sentence.lower())

        # Tokenization
        self.data['job_desc'] = self.data['job_desc'].apply(lambda sentence: word_tokenize(sentence))

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        self.data['job_desc'] = self.data['job_desc'].apply(lambda sentence: [word for word in sentence if word not in stop_words])

        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        self.data['job_desc'] = self.data['job_desc'].apply(lambda sentence: [lemmatizer.lemmatize(word) for word in sentence])

        self.data['job_desc'] = self.data['job_desc'].apply(lambda sentence: ' '.join(sentence))


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
        # self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')  # Download from Internet
        # self.model = AutoModel.from_pretrained('bert-base-uncased')
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)  # Read local model
        self.model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)
        all_courses["bert_vector"] = [embed_text(sentence, self.model, self.tokenizer).detach().numpy() for
                                      sentence in processed_data.data["Course_Description"]]
        self.all_courses = all_courses

        if all_jobs is not None:
            processed_job_data = Preprocess_jobs(all_jobs)
            all_jobs["bert_vector"] = [embed_text(sentence, self.model, self.tokenizer).detach().numpy() for
                                       sentence in processed_job_data.data["job_desc"]]
            self.all_jobs = all_jobs

    def get_similar_courses(self, school, major, course_code, course_name, limit=-1, threshold=0.0, course_types=()):
        """
        Input the details of the target course. Output a dictionary of similar courses (in decreasing similarity)
            Dictionary format {course_id : similarity score}.
            course_id is school, major, course_code, course_name joined by underscore.
        May limit output count and minimum cosine similarity threshold.
        May choose output course type from a subset of ["Core", "Elective", "GE"].
        """
        id = "_".join([school, major, course_code, course_name])
        if course_types != "All":
            selected_courses = self.all_courses[self.all_courses["Category"].isin(course_types)]
        else:
            selected_courses = self.all_courses
        BERT_dis = selected_courses.apply(
            lambda row: [row.name, cosine_similarity(row["bert_vector"], self.all_courses.loc[id, "bert_vector"])], axis=1)
        BERT_dis = list(BERT_dis)
        BERT_dis = list(filter(lambda x: x[1] >= threshold, BERT_dis))  # Apply minimum similarity threshold
        BERT_dis.sort(key=lambda x: x[1], reverse=True)
        if limit >= 0:
            return dict(BERT_dis[:limit])  # Apply output limit
        return dict(BERT_dis)

    def get_similar_courses_from_job_desc(self, job_desc, limit=-1, threshold=0.0, course_types=()):
        """
        Input a job description (string). Output a dictionary of similar courses (in decreasing similarity)
            Dictionary format {course_id : similarity score}.
        May limit output count and minimum cosine similarity threshold.
        May choose output course type from a subset of ["Core", "Elective", "GE"].
        """
        job_df = pd.DataFrame()
        job_df["job_desc"] = [job_desc]
        job_df = Preprocess_jobs(job_df).data
        bert_vector_job = embed_text(job_df.iloc[0]["job_desc"], self.model, self.tokenizer).detach().numpy()

        if course_types:
            selected_courses = self.all_courses[self.all_courses["Category"].isin(course_types)]
        else:
            selected_courses = self.all_courses

        BERT_dis = selected_courses.apply(
            lambda row: [row.name, cosine_similarity(row["bert_vector"], bert_vector_job)], axis=1)
        BERT_dis = list(BERT_dis)
        BERT_dis = list(filter(lambda x: x[1] >= threshold, BERT_dis))  # Apply minimum similarity threshold
        BERT_dis.sort(key=lambda x: x[1], reverse=True)
        if limit >= 0:
            return dict(BERT_dis[:limit])  # Apply output limit
        return dict(BERT_dis)

    def get_similar_courses_from_job_type(self, job_type, limit=-1, threshold=0.0, course_types=()):
        """
        Input a job type (string).
        Output a dictionary of courses based on average similarity score across the job_type
            Dictionary format {course_id : similarity score}.
        May limit output count and minimum cosine similarity threshold.
        May limit output course type to be from a subset of ["Core", "Elective", "GE"].
        """
        if job_type not in self.all_jobs["job_type"].unique():
            print(f"There is no job description for {job_type}")
            return

        if course_types:
            selected_courses = self.all_courses[self.all_courses["Category"].isin(course_types)]
        else:
            selected_courses = self.all_courses

        job_data = self.all_jobs[self.all_jobs["job_type"] == job_type]  # Filter job_type
        temp = []  # Store data before averaging
        for i, job in enumerate(job_data["job_title"]):
            # Compute similarity from each job to all courses
            BERT_dis = selected_courses.apply(
                lambda row: [row.name, cosine_similarity(row["bert_vector"], job_data.iloc[i]["bert_vector"])], axis=1)
            temp.append(dict(list(BERT_dis)))

        result = {}
        for i, course in enumerate(selected_courses.index):
            # Take average of similarity scores for all jobs of job_type
            result[course] = np.mean([d[course] for d in temp])
        result = list(result.items())
        result = list(filter(lambda x: x[1] >= threshold, result))  # Apply minimum similarity threshold
        result.sort(key=lambda x: x[1], reverse=True)
        if limit >= 0:
            return dict(result[:limit])  # Apply output limit
        return dict(result)

    def compare_programs(self, school, program, min_similarity=0.93, course_types=()):
        """
        Compare program with all others. Returns courses from others with no similar (< min_similarity) in program.
        Returns a list of [course_id, similarity score] that doesn't meet min_similarity with any course in program.
        """
        program_courses = self.all_courses.loc[(self.all_courses["School"] == school) & (self.all_courses["Major"] == program)]
        if course_types:
            selected_courses = self.all_courses[self.all_courses["Category"].isin(course_types)]
        else:
            selected_courses = self.all_courses

        res = []
        for i, course_id in enumerate(selected_courses.index):
            BERT_dis = program_courses.apply(
                lambda row: [row.name, cosine_similarity(row["bert_vector"], selected_courses.loc[course_id, "bert_vector"])], axis=1)
            BERT_dis = list(BERT_dis)
            max_similarity = max(x[1] for x in BERT_dis)
            if max_similarity < min_similarity:
                res.append([course_id, max_similarity])
        res.sort(key=lambda x: x[1])  # courses with least similarity first
        return res


if __name__ == '__main__':  # Code for testing
    mdl = BERT_Model(pd.read_csv('Scraping/data/module_details_labelled.csv'), pd.read_csv('Scraping/data/job_offers_categorized.csv'))
    # print(mdl.get_similar_courses("NUS", "CHS", "DSA1101", "Introduction to Data Science"))
    # print(mdl.get_similar_courses("NUS", "CHS", "DSA1101", "Introduction to Data Science", limit=2))
    # print(mdl.get_similar_courses("NUS", "CHS", "DSA1101", "Introduction to Data Science", threshold=0.9))

    test_job_desc = """
    About the job
About The Team

The SeaMoney team enables and drives innovation by providing a range of financial products and services, including its mobile wallet, ShopeePay, to both individuals and SMEs. Its mission is to better the lives of individuals and businesses in the region with financial services through technology. SeaMoney is a part of Sea Limited, a leading global consumer internet company. In addition to SeaMoney, Seaâ€™s other core businesses include leading e-commerce platform, Shopee and digital entertainment arm, Garena.

Job Description

Drive business intelligence needs for seller e-commerce insurance business market expansion across multiple markets through data-driven insights and decision making to inform our short and long term business strategy
Adopt and lead an evidence-based, data-driven approach towards end to end process and business analysis for the implementation of seller e-commerce insurance businesses across markets, including understanding and analysis of data sets from both Shopee and Seamoney domains
Support in ad hoc crucial data-related business measures and initiatives essential to proper business functioning, and develop a long term strategy towards scaling such initiatives for a more automated and holistic solution
Analyze financial impact to topline and bottomline from seller e-commerce insurance initiatives across multiple regional markets for ongoing business growth planning
Drive regular business performance reporting for key management and financial reporting, and for data-driven actionable business decisions and initiatives to ongoing business optimization across both commercial and operational aspects

Requirements

Bachelorâ€™s degree and above in Computer Science/Engineering, Business Analytics, Information Technology, Statistics and other related fields
1~5 years relevant working experience in business analytics related roles
Proficient in data and analytics related technical skills, including MySQL, Presto SQL, Python, and Spark
Motivated by, and capable of, analyzing and driving solutions to complex problems around both e-commerce operations and insurance domains
Deeply curious about ways to improve the topline and bottomline of Shopee business through insurance, by taking a data-driven approach in decision making, working closely with regional and local business teams 
Excited about, and have appreciation for, working with and managing multiple stakeholders in a project, including effective working method with various regional and local teams across multiple Shopee markets
    """
    # print(mdl.get_similar_courses_from_job_desc(test_job_desc, threshold=0.9))

    # print(mdl.get_similar_courses_from_job_type("Quantitative Researcher", limit=20, course_types=["Core", "Elective"]))

    print(mdl.compare_programs("NUS", "Data Science and Analytics", course_types=["Core"]))

