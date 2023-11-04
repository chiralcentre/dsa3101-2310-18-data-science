from flask import Flask, request, render_template, redirect, jsonify, make_response
import pandas as pd
import csv

app = Flask(__name__)

university_mappings = {"NUS": ["Data Science and Analytics", "Business Analytics", "Quantitative Finance", "Statistics", "Data Science and Economics", "CHS"],
                    "NTU": ["Data Science and Artificial Intelligence", "Economics and Data Science"],
                    "SMU": ["Data Science and Analytics", "Quantitative Finance", "Information Systems (Business Analytics)"]}
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

    

