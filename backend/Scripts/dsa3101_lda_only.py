# -*- coding: utf-8 -*-
"""DSA3101_LDA_only.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VhFRMqXyvgLcLojael6bXmJL6lF2ClIG

# Word2Vec and LDA
https://www.kaggle.com/code/jl18pg052/word-embedding-word2vec-topic-modelling-lda

### Extracting informations from Text using Text Mining Techniques

Import Libraries
"""

import pandas as pd
import numpy as np
import re, nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
'''
import spacy
nlp = spacy.load('en_core_web_sm')
'''
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import gensim
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
from collections import Counter
nltk.download('punkt')
import ast

# globals start
topic_labels = {
    0: 'Project Management',
    1: 'Algorithms and Numerical Methods',
    2: 'Machine Learning',
    3: 'Math and Statistics'
}
# globals end

# Functions start
"""Text Cleaning"""
def cleaned_text(text):
    clean = re.sub("\n"," ",text) # removes line breaks and newlines
    clean=clean.lower() # converts into lowercase
    clean=re.sub(r"[~.,%/:;?_&+*=!-]"," ",clean) # removes punctuations
    clean=re.sub("[^a-z]"," ",clean) # removes non-alphabetical char
    clean=clean.lstrip() # removes leading whitespace
    clean=re.sub("\s{2,}"," ",clean) #s single spaces throughout
    return clean

def word_lemmatizer(text):
    lem_text = [WordNetLemmatizer().lemmatize(i,pos='v') for i in text]
    return lem_text

def process_input_file(file):
    """Import `module_details_labelled.csv` Dataset"""
    data = pd.read_csv(file)
    """#### Dataset Description

    #### Getting Relevant modules (not part of core curriculum and GE)
    """
    # get only core modules (now includes electives)
    core1 = ['Core', 'Elective']
    data_core = data.loc[data['Category'].isin(core1)]
    data_core["cleaned_descriptions"] = data_core["Course_Description"].apply(cleaned_text)

    # Joins words into sentences
    data_core["cleaned_descriptions"] = data_core["cleaned_descriptions"].apply(lambda x: ' '.join([word for word in x.split() if len(word)>3]))

    """Tokenise words before lemmatising"""
    data_core["tokenized"]=data_core["cleaned_descriptions"].apply(lambda x: nltk.word_tokenize(x))
    data_core["lemmatized"]=data_core["tokenized"].apply(lambda x: word_lemmatizer(x))

    # joins lemmatized words into sentences
    data_core["lemmatize_joined"]=data_core["lemmatized"].apply(lambda x: ' '.join(x))

    stop = stopwords.words('english')
    words_to_stop = ["also", "students", "course", "introduce", "content", \
                     "include", "introducing", "used","weeks", "allow", "knowledge", "concisely", "page", "harvest", "skills",\
                     "basic","use","task","state","introduction", \
                     "design","techniques","concepts","theory","application","process","understand","analytics", \
                     "develop","apply","relate","value","cover","simple","must","will","course","courses"]
    stop.extend(words_to_stop)

    # lemmatise our stop words
    # stop_df = pd.Series(stop)
    # stop_df = stop_df.apply(lambda x: word_lemmatizer([x])[0])
    # stop = list(stop_df)

    data_core["stop_removed_descriptions"] = data_core["lemmatize_joined"].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    data_core['stop_removed_descriptions'] = data_core['stop_removed_descriptions'].str.replace(r'\bML\b', 'machine learning', regex=True)

    data_core['Number_of_words_for_cleaned'] = data_core['stop_removed_descriptions'].apply(lambda x:len(str(x).split()))

    """### Topic Modelling using LDA

    The input will be in the form of document-term matrix, and we will convert that using the below piece of code.
    """

    lemmatized_stuff = data_core["lemmatized"] # when not removing stopwords

    dictionary = corpora.Dictionary(lemmatized_stuff)
    doc_term_matrix = [dictionary.doc2bow(rev) for rev in lemmatized_stuff]

    """Running models to determine optimal number of topics."""
    LDA = gensim.models.ldamodel.LdaModel

    """### Using optimal number of topics = 4
    After trial and error, we decided on 4 as the number of optimal topics.
    """

    lda_model = LDA(corpus=doc_term_matrix, id2word=dictionary, num_topics=4, random_state=100,
                    chunksize=200, passes=100, minimum_probability = 0)
    return (lda_model,doc_term_matrix,dictionary,lemmatized_stuff)

def format_topics_sentences(ldamodel, corpus, texts):
    # Init output
    sent_topics_df = pd.DataFrame()
    # Get main topic in each document
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = pd.concat([sent_topics_df, pd.Series([topic_labels[topic_num], round(prop_topic,4), topic_keywords]).to_frame().T], ignore_index = True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)

"""### Determine Topic of a New Document
### input: string;
### output: strings of dominant_topic, topic_keywords, topic_distribution

"""

def preprocess_new_document(document):
    # Step 1: Remove words with length less than or equal to 3
    cleaned_text_document = cleaned_text(document)
    remove_function = lambda x: ' '.join([word for word in x.split() if len(word)>3])
    cleaned_removed_short_words_document = remove_function(cleaned_text_document)

    # Step 2: Tokenize the cleaned text
    tokenized_text_document = nltk.word_tokenize(cleaned_removed_short_words_document)

    # Step 3: Lemmatize the tokens
    lemmatized_text_document =  word_lemmatizer(tokenized_text_document)

    # # Step 4: Remove stopwords
    # stop_removed_text = ' '.join([word for word in lemmatized_text_document if word not in stop])
    # stop_removed_text = re.sub(r'\bML\b', 'machine learning', stop_removed_text)
    # return stop_removed_text

    # Step 4: Joining words together
    joined_text_document = ' '.join([word for word in lemmatized_text_document])

    return joined_text_document

'''
# Example usage of the function
new_document = "This course teaches neural networks, and popular models such as Random Forest and XGBoost."
preprocessed_document = preprocess_new_document(new_document)
print(preprocessed_document)
'''

def get_document_topic(ldamodel, doc_term_matrix):
    global topic_labels
    topic_scores = ldamodel.get_document_topics(doc_term_matrix)

    dominant_topic = max(topic_scores, key=lambda x: x[1])[0]
    topic_keywords = ", ".join([word for word, prop in ldamodel.show_topic(dominant_topic)])

    # relabel topic
    labelled_dominant_topic = topic_labels[dominant_topic]
    return labelled_dominant_topic, topic_keywords

def assign_cluster(new_document, ldamodel, dictionary):
    global topic_labels
    # Preprocess the new document
    preprocessed_doc = preprocess_new_document(new_document)

    # Convert the preprocessed document to a list of tokens
    tokens = preprocessed_doc.split()  # Split the string into tokens

    # Convert the tokens to a bag-of-words vector using the dictionary
    new_bow = dictionary.doc2bow(tokens)

    # Get the dominant topic and keywords for the new document
    dominant_topic, topic_keywords = get_document_topic(ldamodel, new_bow)

    # Topic distribution
    topic_distribution = ldamodel.get_document_topics(new_bow)

    result = []
    for i in range(len(topic_distribution)):
        topic_id, probability = topic_distribution[i]
        topic_label = topic_labels.get(topic_id)
        result.append((topic_label,probability))

    return dominant_topic, topic_keywords, result

    # result here is the topic distribution
    # e.g. Topic Distribution: [('Project Management', 0.3359872), ('Algorithms and Numerical Methods', 0.19626443), ('Machine Learning', 0.4144256), ('Math and Statistics', 0.053322762)]

"""### Let user put in their own document to the LDA model
input: string
output: dictionary, formatting up to approver
"""

def cluster_doc(document,lda_model,dictionary):
    dominant_topic, topic_keywords, topic_distribution = assign_cluster(document, lda_model, dictionary)
    d = {}
    for i in topic_distribution:
        d[i[0]] = round(i[1]*100,1)
    return d

def topic_distribution_for_each_course(course_data,description,lda_model,dictionary):
    course_data["cluster_assigned"]= course_data[description].apply(lambda x: assign_cluster(x, lda_model, dictionary))
    course_data["dominant_topic"] = course_data["cluster_assigned"].apply(lambda x: x[0])
    course_data["topic_keywords"] = course_data["cluster_assigned"].apply(lambda x: x[1])
    course_data["topic_distribution"] = course_data["cluster_assigned"].apply(lambda x: x[2])

def topic_distribution_for_each_job(job_data,job_desc,lda_model,dictionary):
    job_data["cluster_assigned"]= job_data[job_desc].apply(lambda x: assign_cluster(x, lda_model, dictionary))
    job_data["dominant_topic"] = job_data["cluster_assigned"].apply(lambda x: x[0])
    job_data["topic_keywords"] = job_data["cluster_assigned"].apply(lambda x: x[1])
    job_data["topic_distribution"] = job_data["cluster_assigned"].apply(lambda x: x[2])
# Functions end

def main():
    lda_model,doc_term_matrix,dictionary,lemmatized_stuff = process_input_file("../Scraping/data/module_details_labelled.csv")
    #lda_model.print_topics()
    #coherence_model_lda = CoherenceModel(model=lda_model, texts=lemmatized_stuff, dictionary=dictionary, coherence='c_v')
    #coherence_lda = coherence_model_lda.get_coherence()

    """### Dominant topic for each Document

    Finalised Topics
    """

    # Topic Labelling
    df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=doc_term_matrix, texts=lemmatized_stuff)

    # Format
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']

    """### Topic Distribution for each course
    ### input: dataframe column
    ### output: adds dataframe column (no output, it will just modify the existing dataframe u fit in; you can save the csv then query from there)
    """

    course_data = pd.read_csv("../Scraping/data/module_details_labelled.csv")
    topic_distribution_for_each_course(course_data,"Course_Description",lda_model,dictionary)

    course_data.to_csv("lda_topic_distribution_for_modules_final.csv") # can save the csv then query the result u want from here
    
    """### Define function that segregate topics and their proportions in each module (course) or job"""

    def segregate(df, i):
        topic_distribution = df.loc[i, 'topic_distribution']
        topic_distribution = ast.literal_eval(topic_distribution) # to convert string to a list of tuples
        #print(topic_distribution)
        for topic, prop in topic_distribution:
            df.loc[i, topic] = prop

    """### Calculating our Results for Different Schools' Majors
    ### input: our data (dataframe)
    ### output: dataframe with all the averages
    """

    modules_df = pd.read_csv("lda_topic_distribution_for_modules_final.csv")

    def average_topic_distribution_for_majors(modules_df):
        new_modules_df = modules_df.loc[modules_df['Category'].isin(['Core', 'Elective'])].copy() # create new df for modules
        new_modules_df = new_modules_df.reset_index(drop=True) # resets index for new new_modules_df
        new_modules_df["Algorithms and Numerical Methods"], new_modules_df['Machine Learning'], new_modules_df['Project Management'], new_modules_df['Math and Statistics'], = 0, 0, 0, 0
        new_modules_df = new_modules_df.astype({'Algorithms and Numerical Methods':'float',
                                              'Machine Learning':'float',
                                              'Project Management':'float',
                                              'Math and Statistics':'float'})

        for i in range(len(new_modules_df)):
            segregate(new_modules_df, i) # segregate topics and proportion in each module/course

        td_majors = round((new_modules_df.groupby(['School', 'Major'])[['Algorithms and Numerical Methods',
                                        'Machine Learning',
                                        'Project Management',
                                        'Math and Statistics']].mean())*100, 1)
        return td_majors

    topic_distribution_majors = average_topic_distribution_for_majors(modules_df)
    topic_distribution_majors.to_csv("average_topic_distribution_for_majors.csv") # can save the csv then query the result u want from here

    """### Topic Distribution for each job role"""

    job_data = pd.read_csv("../Scraping/data/job_offers_categorized.csv")
    topic_distribution_for_each_job(job_data,"job_desc",lda_model,dictionary)
    job_data.to_csv("lda_topic_distribution_for_jobs.csv")

    """### Calculating our Results for Different Job Roles
    ### input: our data (dataframe)
    ### output: dataframe with all the averages
    """

    jobs_df = pd.read_csv("lda_topic_distribution_for_jobs.csv")

    def average_topic_distribution_for_jobs(jobs_df):
        jobs_df["Algorithms and Numerical Methods"], jobs_df['Machine Learning'], jobs_df['Project Management'], jobs_df['Math and Statistics'], = 0, 0, 0, 0
        jobs_df = jobs_df.astype({'Algorithms and Numerical Methods':'float',
                                'Machine Learning':'float',
                                'Project Management':'float',
                                'Math and Statistics':'float'})
        for i in range(len(jobs_df)):
            segregate(jobs_df, i)
        td_jobs = round((jobs_df.groupby(['job_type'])[['Algorithms and Numerical Methods',
                                        'Machine Learning',
                                        'Project Management',
                                        'Math and Statistics']].mean())*100, 1)
        return td_jobs

    topic_distribution_jobs = average_topic_distribution_for_jobs(jobs_df)
    topic_distribution_jobs.to_csv("average_topic_distribution_for_jobs.csv")
    

if __name__ == "__main__":
    main()
