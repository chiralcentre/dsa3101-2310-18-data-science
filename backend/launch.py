from flask import Flask, request, render_template, redirect, jsonify, make_response
import pandas as pd
from lda import *
from similarity_measures import *
from scipy.stats import entropy
from datetime import datetime
import json

from flask_cors import CORS  # Import the CORS module
app = Flask(__name__)
CORS(app)  # Initialize CORS with your Flask app

app.json.sort_keys = False  # Keep output sorted when using jsonify
# Initialize BERT model
model = BERT_Model(pd.read_pickle("./data/module_details_labelled.pkl"), pd.read_pickle("./data/job_offers_categorized.pkl"))

pd.options.mode.chained_assignment = None  # Suppress SettingWithCopyWarning for pandas

university_mappings = {"NUS": ["Data Science and Analytics", "Business Analytics", "Quantitative Finance", "Statistics", "Data Science and Economics", "CHS"],
                    "NTU": ["Data Science and Artificial Intelligence", "Economics and Data Science"],
                    "SMU": ["Data Science and Analytics", "Quantitative Finance", "Information Systems (Business Analytics)"]}

job_types = ['Data Analyst', 'Data Scientist', 'Quantitative Researcher', 'Quantitative Analyst', 'Business Analyst']

clusters = ["Math-based Optimization (ML)", "Mathematical and Statistical Analysis (Theory-based)", "Project Management", "Machine Learning"]

lda_model, doc_term_matrix, dictionary, lemmatized_stuff = process_input_file("./data/module_details_labelled.csv")

'''
courses_defaults = {"university": ["NUS", "NTU", "SMU"],
                    "major": ["Data Science and Analytics", "Business Analytics", "Quantitative Finance", "Statistics", "Data Science and Economics",
                              "CHS", "Data Science and Artificial Intelligence", "Economics and Data Science", "Information Systems (Business Analytics)"]}
'''

@app.route("/modules", methods = ["GET"])
def modules():
    df = pd.read_pickle("./data/module_details_labelled.pkl")
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
    df = pd.read_pickle("./data/job_offers_categorized.pkl")
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
        ans = {}
        for key,value in result:
            ans[key] = float(value) # convert to float to prevent float32 typeError
        return jsonify({"dominant_topic": dominant_topic, "topic_keywords": topic_keywords, "distribution": ans})

@app.route("/job-distribution", methods = ["GET"])
def job_distribution():
    df = pd.read_csv("./data/average_topic_distribution_for_jobs.csv")
    # if no job is specified, return everything
    job = request.args.get("job", None)
    if job == None:
        return make_response("job not provided", 400)
    elif job not in job_types:
        return make_response(f"job {job} not found", 400)
    else:
        return jsonify(df[df["job_type"] == job].to_json(orient = "records", index = False))
    
@app.route("/course-distribution", methods = ["GET"])
def course_distribution():
    df = pd.read_csv("./data/average_topic_distribution_for_majors.csv")
    uni = request.args.get("university", None)
    major = request.args.get("major", None)
    if uni == None:
        return make_response("university not provided", 400)
    elif uni not in university_mappings:
        return make_response(f"university {uni} not within supported list",400)
    if major == None:
        return make_response("major not provided", 400)
    elif major not in university_mappings[uni]:
        return make_response(f"major {major} not found for {uni}", 400)
    return jsonify(df[(df["School"] == uni) & (df["Major"] == major)].to_json(orient = "records", index = False))

@app.route("/quiz-questions", methods = ["GET"])
def quiz_questions():
    df = pd.read_csv("Questions/quiz_questions.csv")
    limit = int(request.args.get('limit', default = len(df)))
    limit = min(limit, len(df))
    return jsonify(df.iloc[:limit].to_json(orient = "records", index = False))

# return top 3 majors closest to quiz distribution
@app.route("/quiz-results", methods = ["POST"])
def quiz_results():
    df = pd.read_csv("./data/average_topic_distribution_for_majors.csv")
    answers = request.json
    if answers == None:
        return make_response("number of questions selected for each question category required", 400)
    keys = {int(k) for k in answers}
    if keys != set(topic_labels.keys()): 
        return make_response("Invalid topic indices", 400)
    total = sum(answers.values())
    quiz_distribution = [0,0,0,0]
    for key in answers:
        quiz_distribution[int(key)] = float(answers[key] / total)
    best = []
    # use KL divergence strat to return closest 3 majors
    for row in df.itertuples():
        # ignore 0 index
        row_distribution = list(map(float,[row[5],row[3],row[4],row[6]]))
        best.append((row[1],row[2],entropy(quiz_distribution,row_distribution)))
    best.sort(key = lambda x: x[2])
    return jsonify(best[:3])


@app.route("/analysis/similar_courses", methods=["GET"])
# localhost:5000/analysis/similar_courses?university=NUS&major=Data Science and Analytics&course_code=CS2040&course_name=Data Structures and Algorithms
def model_get_similar_courses():
    school = request.args.get("university", None)
    major = request.args.get("major", None)
    course_code = request.args.get("course_code", None)
    course_name = request.args.get("course_name", None)
    if None in (school, major, course_code, course_name):
        return "Please input all course details - school, major, course_code, course_name"
    limit = int(request.args.get("limit", -1))
    threshold = float(request.args.get("threshold", 0.0))  # Between 0 and 1. Higher means more similar
    course_types = request.args.get("course_types", "All")  # "Core Elective GE" or "All"
    if course_types != "All":
        course_types = course_types.split(" ")
    result = model.get_similar_courses(school, major, course_code, course_name, limit, threshold, course_types)
    for course_id, similarity in result.items():
        result[course_id] = str(similarity)  # Convert numeric similarity to string for jsonify
    result = {"parameters": request.args, "result": result}

    with open(f"./data/outputs/get_similar_courses_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.json", "w") as f:
        json.dump(result, f)
    return jsonify(result)


@app.route("/analysis/similar_courses_from_job_desc", methods=["GET"])
# localhost:5000/analysis/similar_courses_from_job_desc?job_desc=Drive business intelligence needs for seller e-commerce insurance business market expansion across multiple markets through data-driven insights and decision making to inform our short and long term business strategy
def model_get_similar_courses_from_job_desc():
    job_desc = request.args.get("job_desc", "")
    limit = int(request.args.get("limit", -1))
    threshold = float(request.args.get("threshold", 0.0))  # Between 0 and 1. Higher means more similar
    course_types = request.args.get("course_types", "All")  # "Core Elective GE" or "All"
    if course_types != "All":
        course_types = course_types.split(" ")
    result = model.get_similar_courses_from_job_desc(job_desc, limit, threshold, course_types)
    for course_id, similarity in result.items():
        result[course_id] = str(similarity)  # Convert numeric similarity to string for jsonify
    result = {"parameters": request.args, "result": result}

    with open(f"./data/outputs/get_similar_courses_from_job_desc_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.json", "w") as f:
        json.dump(result, f)
    return jsonify(result)


@app.route("/analysis/similar_courses_from_job_type", methods=["GET"])
# localhost:5000/analysis/similar_courses_from_job_type?job_type=Data Analyst&course_types=Core Elective
def model_get_similar_courses_from_job_type():
    job_type = request.args.get("job_type", None)
    if not job_type:
        return "Please input job_type"
    limit = int(request.args.get("limit", -1))
    threshold = float(request.args.get("threshold", 0.0))  # Between 0 and 1. Higher means more similar
    course_types = request.args.get("course_types", "All")  # "Core Elective GE" or "All"
    if course_types != "All":
        course_types = course_types.split(" ")
    result = model.get_similar_courses_from_job_type(job_type, limit, threshold, course_types)
    for course_id, similarity in result.items():
        result[course_id] = str(similarity)  # Convert numeric similarity to string for jsonify
    result = {"parameters": request.args, "result": result}

    with open(f"./data/outputs/get_similar_courses_from_job_type_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.json", "w") as f:
        json.dump(result, f)
    return jsonify(result)


@app.route("/analysis/compare_programs", methods=["GET"])
# localhost:5000/analysis/compare_programs?university=NUS&major=Data Science and Analytics&course_types=Core
def model_compare_programs():
    school = request.args.get("university", None)
    major = request.args.get("major", None)
    if None in (school, major):
        return "Please input school and major"
    min_similarity = float(request.args.get("min_similarity", 0.93))  # Between 0 and 1. Higher means more similar
    course_types = request.args.get("course_types", "All")  # "Core Elective GE" or "All"
    if course_types != "All":
        course_types = course_types.split(" ")
    result = model.compare_programs(school, major, min_similarity, course_types)
    result = {course_id: str(similarity_score) for course_id, similarity_score in result}  # Convert numeric similarity to string for jsonify
    result = {"parameters": request.args, "result": result}

    with open(f"./data/outputs/compare_programs_{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.json", "w") as f:
        json.dump(result, f)
    return jsonify(result)
