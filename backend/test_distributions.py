from conftests import client
import pandas as pd
import json
from launch import lda_model, dictionary
from lda import assign_cluster


job_df = pd.read_csv("./data/job_offers_categorized.csv")
job_dist_df = pd.read_csv("./data/average_topic_distribution_for_jobs.csv")
major_dist_df = pd.read_csv("./data/average_topic_distribution_for_majors.csv")

# /distribution endpoint
def test_distribution_no_desc(client):
    response = client.get("/distribution")
    assert response.status_code == 400
    assert response.text == "fill in description"

def test_distribution_valid_desc(client):
    response = client.get("/distribution", query_string = {"description": job_df["job_desc"].iloc[0]})
    assert response.status_code == 200
    answer = response.json
    dominant_topic, topic_keywords, result = assign_cluster(job_df["job_desc"].iloc[0], lda_model, dictionary)
    # no need to compare exact probabilities as LDA model is stochastic and there will be slight changes
    # however, dominant topic and topic keywords should still be the same
    assert dominant_topic == answer["dominant_topic"]
    assert topic_keywords == answer["topic_keywords"]

# /job-distribution endpoint
def test_job_distribution_no_job(client):
    response = client.get("/job-distribution")
    assert response.status_code == 400
    assert response.text == "job not provided"

def test_job_distribution_invalid_job(client):
    response = client.get("/job-distribution", query_string = {"job": "test123"})
    assert response.status_code == 400
    assert response.text == "job test123 not found"

def test_job_distribution_valid_job(client):
    response = client.get("/job-distribution", query_string = {"job": "Data Analyst"})
    assert response.status_code == 200
    assert len(job_dist_df[job_dist_df["job_type"] == "Data Analyst"]) == len(json.loads(response.json))


# /major-distribution endpoint
def test_major_distribution_no_university(client):
    response = client.get("/major-distribution")
    assert response.status_code == 400
    assert response.text == "university not provided"

def test_major_distribution_invalid_university(client):
    response = client.get("/major-distribution", query_string = {"university": "easteregg"})
    assert response.status_code == 400
    assert response.text == "university easteregg not within supported list"

def test_major_distribution_valid_university_no_major(client):
    response = client.get("/major-distribution", query_string = {"university": "NUS"})
    assert response.status_code == 400
    assert response.text == "major not provided"

def test_major_distribution_valid_university_invalid_major(client):
    response = client.get("/major-distribution", query_string = {"university": "NUS", "major": "pikachu"})
    assert response.status_code == 400
    assert response.text == "major pikachu not found for NUS"

def test_major_distribution_valid_university_valid_major(client):
    response = client.get("/major-distribution", query_string = {"university": "NUS", "major": "Data Science and Analytics"})
    assert response.status_code == 200
    assert len(major_dist_df[(major_dist_df["School"] == "NUS") & (major_dist_df["Major"] == "Data Science and Analytics")]) == len(json.loads(response.json))