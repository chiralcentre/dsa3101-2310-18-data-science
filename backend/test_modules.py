from conftests import client
import pandas as pd
import json

df = pd.read_csv("./data/module_details_labelled.csv")

def test_no_university(client):
    response = client.get("/modules")
    assert response.status_code == 200
    assert len(df) == len(json.loads(response.json))

def test_invalid_university(client):
    response = client.get("/modules", query_string = {"university": "test123"})
    assert response.status_code == 400
    assert response.text == "university test123 not within supported list, try again"

def test_valid_university(client):
    response = client.get("/modules", query_string = {"university": "NUS"})
    assert response.status_code == 200
    assert len(df[df["School"] == "NUS"]) == len(json.loads(response.json))

# no university provided means that all module information is returned
def test_major_no_university(client):
    response = client.get("/modules", query_string = {"major": "Data Science and Analytics"})
    assert response.status_code == 200
    assert len(df) == len(json.loads(response.json))

def test_university_invalid_major(client):
    response = client.get("/modules", query_string = {"university": "NUS", "major": "test123"})
    assert response.status_code == 400
    assert response.text == "major test123 not found for NUS, try again"

def test_university_valid_major(client):
    response = client.get("/modules", query_string = {"university": "NUS", "major": "Data Science and Analytics"})
    assert response.status_code == 200
    assert len(df[(df["School"] == "NUS") & (df["Major"] == "Data Science and Analytics")]) == len(json.loads(response.json))