from flask import Flask, request, render_template, redirect, jsonify, make_response
import pandas as pd
from Scripts.dsa3101_lda_only import topic_labels, process_input_file,assign_cluster
from scipy.stats import entropy

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
        ans = {}
        for key,value in result:
            ans[key] = float(value) # convert to float to prevent float32 typeError
        return jsonify({"dominant_topic": dominant_topic, "topic_keywords": topic_keywords, "distribution": ans})

@app.route("/quiz-questions", methods = ["GET"])
def quiz_questions():
    df = pd.read_csv("Questions/quiz_questions.csv")
    limit = int(request.args.get('limit', default = len(df)))
    limit = min(limit, len(df))
    return jsonify(df.iloc[:limit].to_json(orient = "records", index = False))

# return top 3 majors closest to quiz distribution
@app.route("/quiz-results", methods = ["POST"])
def quiz_results():
    df = pd.read_csv("Scraping/data/average_topic_distribution_for_majors.csv")
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



