from conftests import client
import pandas as pd
import json
from scipy.stats import entropy

questions_df = pd.read_csv("Questions/quiz_questions.csv")
major_dist_df = pd.read_csv("./data/average_topic_distribution_for_majors.csv")
# /quiz-questions endpoint
def test_quiz_no_limit(client):
    response = client.get("/quiz-questions")
    assert response.status_code == 200
    assert len(questions_df) == len(json.loads(response.json))

def test_quiz_with_limit(client):
    response = client.get("/quiz-questions", query_string = {"limit": 5})
    assert response.status_code == 200
    assert len(json.loads(response.json)) == 5

# /quiz-results endpoint
def test_quiz_results_invalid_results(client):
    response = client.post("/quiz-results", json = json.dumps("hi123"))
    assert response.status_code == 400
    assert response.text == "number of questions selected for each question category required"

def test_quiz_results_insufficient_categories(client):
    response = client.post("/quiz-results", json = {1: 2, 3: 5})
    assert response.status_code == 400
    assert response.text == "invalid topic indices"

def test_quiz_results_with_results(client):
    response = client.post("/quiz-results", json = {0: 5, 1: 2, 2: 2, 3: 1})
    assert response.status_code == 200
    best,quiz_distribution = [],[0.5, 0.2, 0.2, 0.1]
    # use KL divergence strat to return closest 3 majors
    for row in major_dist_df.itertuples():
        # ignore 0 index
        row_distribution = list(map(float,[row[5],row[3],row[4],row[6]]))
        best.append([row[1],row[2],entropy(quiz_distribution,row_distribution)])
    best.sort(key = lambda x: x[2])
    assert best[:3] == response.json
