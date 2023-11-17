from conftests import client
import pandas as pd
import json

df = pd.read_csv("./data/job_offers_categorized.csv")

def test_no_job(client):
    response = client.get("/jobs")
    assert response.status_code == 200
    assert len(df) == len(json.loads(response.json))

def test_invalid_job(client):
    response = client.get("/jobs", query_string = {"job": "test123"})
    assert response.status_code == 400
    assert response.text == "job test123 not found"

def test_valid_job(client):
    response = client.get("/jobs", query_string = {"job": "Data Analyst"})
    assert response.status_code == 200
    assert len(df[df["job_type"] == "Data Analyst"]) == len(json.loads(response.json))