from flask import Flask, render_template, request
from jinja2 import Template
import requests
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.config['SECRET_KEY'] = ';lkjfdsa'

API_KEY = "MHgWdG6I183QDehzQpEp1ZYFmSjJqOytO8ICj7Xl"
API_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    filters = request.form
    params = {
        "api_key": API_KEY,
        "per_page": 100,
        "_fields": ",".join([
        "school.name",
        "latest.cost.tuition.out_of_state",
        "latest.admissions.admission_rate.overall",
        "latest.student.size",
        "school.city",
        "school.state", 
        "latest.admissions.sat_scores.average.overall",
        "id"
    ]),
    }

    state = request.form.get("states")
    min_tuition = int(request.form.get("min_tuition")) if request.form.get("min_tuition") is not None else None
    max_tuition = int(request.form.get("max_tuition")) if request.form.get("max_tuition") is not None else None
    min_admission_rate = float(request.form.get("min_admission_rate")) if request.form.get("min_admission_rate") is not None else None
    max_admission_rate = float(request.form.get("max_admission_rate")) if request.form.get("max_admission_rate") is not None else None
    min_size = int(request.form.get("min_size")) if request.form.get("min_size") is not None else None
    max_size = int(request.form.get("max_size")) if request.form.get("max_size") is not None else None
    min_sat = int(request.form.get("min_sat")) if request.form.get("min_sat") is not None else None
    max_sat = int(request.form.get("max_sat")) if request.form.get("max_sat") is not None else None

    if state:
        params["school.state"] = state
    if min_tuition and max_tuition:
        params["latest.cost.tuition.out_of_state__range"] = f"{min_tuition}..{max_tuition}"
    if min_admission_rate and max_admission_rate:
        params["latest.admissions.admission_rate.overall__range"] = f"{min_admission_rate / 100}..{max_admission_rate / 100}"
    if min_size and max_size:
        params["latest.student.size__range"] = f"{min_size}..{max_size}"
    if min_sat and max_sat:
        params["latest.admissions.sat_scores.average.overall__range"] = f"{min_sat}..{max_sat}"
            
    response = requests.get(API_URL, params=params)
    response_data = response.json()
    colleges = response_data.get("results", [])
    print("API response status code:", response.status_code)
    print("API response data:", response.json())
    return render_template("search_results.html", colleges=colleges)

@app.route("/api_credits")
def api_credits():
    return render_template("api_credits.html")

@app.route("/college/<int:college_id>")
def college_profile(college_id):
    params = {
        "api_key": API_KEY,
        "id": college_id,
        "_fields": ",".join([
            "school.name",
            "latest.cost.tuition.in_state",
            "latest.cost.tuition.out_of_state",
            "latest.admissions.admission_rate.overall",
            "latest.student.size",
            "latest.student.enrollment.all",
            "school.city",
            "school.state",
            "latest.admissions.sat_scores.average.overall",
            "latest.aid.federal_loan_rate",
            "latest.completion.completion_rate_4yr_150nt_pooled",
            "latest.academics.program_percentage.agriculture",
            "latest.academics.program_percentage.resources",
            "latest.academics.program_percentage.architecture",
            "latest.academics.program_percentage.ethnic_cultural_gender",
            "latest.academics.program_percentage.communication",
            "latest.academics.program_percentage.communications_technology",
            "latest.academics.program_percentage.computer",
            "latest.academics.program_percentage.personal_culinary",
            "latest.academics.program_percentage.education",
            "latest.academics.program_percentage.engineering",
            "latest.academics.program_percentage.engineering_technology",
            "latest.academics.program_percentage.language",
            "latest.academics.program_percentage.family_consumer_science",
            "latest.school.school_url",
            "school.men_only",
            "school.women_only",
            "id"
        ]),
    }
    response = requests.get(API_URL, params=params)
    college = response.json().get("results", [])[0]
    top_majors = format_significant_majors(college)[:5]
    print("API response status code:", response.status_code)
    print("API response data:", response.json())
    return render_template("college_profile.html", college=college, top_majors=top_majors)

def format_significant_majors(college):
    majors = []
    for key, value in college.items():
        if key.startswith('latest.academics.program_percentage'):
            formatted_key = key.replace('latest.academics.program_percentage.','').replace('_', ' ').title()
            majors.append((formatted_key, value))
    majors.sort(key=lambda x: x[1], reverse=True)
    return majors


if __name__ == "__main__":
    app.run(debug=True)