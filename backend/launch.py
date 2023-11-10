from flask import Flask, request, render_template, redirect, jsonify, make_response
import pandas as pd
import csv
from Scripts.dsa3101_lda_only import topic_labels, process_input_file,assign_cluster

app = Flask(__name__)

university_mappings = {"NUS": ["Data Science and Analytics", "Business Analytics", "Quantitative Finance", "Statistics", "Data Science and Economics", "CHS"],
                    "NTU": ["Data Science and Artificial Intelligence", "Economics and Data Science"],
                    "SMU": ["Data Science and Analytics", "Quantitative Finance", "Information Systems (Business Analytics)"]}

job_types = ['Data Analyst', 'Data Scientist', 'Quantitative Researcher', 'Quantitative Analyst', 'Business Analyst']

clusters = ["Math-based Optimization (ML)", "Mathematical and Statistical Analysis (Theory-based)", "Project Management", "Machine Learning"]

lda_model,doc_term_matrix,dictionary,lemmatized_stuff = process_input_file("Scraping/data/module_details_labelled.csv")

'''
courses_defaults = {"university": ["NUS", "NTU", "SMU"],
                    "major": ["Data Science and Analytics", "Business Analytics", "Quantitative Finance", "Statistics", "Data Science and Economics",
                              "CHS", "Data Science and Artificial Intelligence", "Economics and Data Science", "Information Systems (Business Analytics)"]}
'''

@app.route("/modules", methods = ["GET"])
def modules():
    df = pd.read_pickle("Scraping/data/module_details_labelled.pkl")
    # if no university is specified, return everything
    uni = request.args.get("university", None)
    if uni == None:
        return jsonify(df.to_json(orient = "records", index = False))
    elif uni not in university_mappings:
        return make_response(f"university {uni} not within supported list, try again", 400)
    # note that a major must be provided in conjunction with a university
    major = request.args.get("major", None)
    if major == None:
        return jsonify(df[df["School"] == uni].to_json(orient = "records", index = False))
    elif major not in university_mappings[uni]:
        return make_response(f"major {major} not found for {uni}, try again", 400)
    else:
        return jsonify(df[(df["School"] == uni) & (df["Major"] == major)].to_json(orient = "records", index = False))

@app.route("/jobs", methods = ["GET"])
def jobs():
    df = pd.read_pickle("Scraping/data/job_offers_categorized.pkl")
    # if no job is specified, return everything
    job = request.args.get("job", None)
    if job == None:
        return jsonify(df.to_json(orient = "records", index = False))
    elif job not in job_types:
        return make_response(f"job {job} not found", 400)
    else:
        return jsonify(df[df["job_type"] == job].to_json(orient = "records", index = False))

# pass in description for anything - a job, course description, and get the corresponding topic distribution
@app.route("/distribution", methods = ["GET"])
def distribution():
    description = request.args.get("description", None)
    if description == None:
        return make_response(f"fill in description", 400)
    else:
        dominant_topic, topic_keywords, result = assign_cluster(description, lda_model, dictionary)
        for key in result:
            result[key] = float(result[key]) # convert to float to prevent float32 typeError
        return jsonify({"dominant_topic": dominant_topic, "topic_keywords": topic_keywords, "distribution": result})

@app.route("/quiz-questions", methods = ["GET"])
def quiz_questions():
    df = pd.read_csv("Questions/quiz_questions.csv")
    limit = int(request.args.get('limit', default = len(df)))
    limit = min(limit, len(df))
    return jsonify(df.iloc[:limit].to_json(orient = "records", index = False))

@app.route("/quiz-results", methods = ["GET"])
def quiz_results():
    pass

