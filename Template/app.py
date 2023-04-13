from flask import Flask, render_template, request, session
import requests
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
# app.config['SECRET_KEY'] = ';lkjfdsa'

API_KEY = "MHgWdG6I183QDehzQpEp1ZYFmSjJqOytO8ICj7Xl"
API_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"

@app.route("/")
def index():
    return render_template("index_Vlissara.html")

@app.route("/search", methods=["POST"])
def search():
    filters = request.form
    params = {
        "api_key": API_KEY,
        "per_page": 100,
        "_fields": ",".join([
        "school.name",
        "latest.cost.tuition.in_state",
        "latest.admissions.admission_rate.overall",
        "latest.student.size",
        "school.city",
        "school.state",
        "school.school_url"
        ]),
    }

    state = request.form.get("states")
    min_tuition = int(request.form.get("min_tuition")) if request.form.get("min_tuition") else None
    max_tuition = int(request.form.get("max_tuition")) if request.form.get("max_tuition") else None
    min_admission_rate = float(request.form.get("min_admission_rate")) if request.form.get("min_admission_rate") else None
    max_admission_rate = float(request.form.get("max_admission_rate")) if request.form.get("max_admission_rate") else None
    min_size = int(request.form.get("min_size")) if request.form.get("min_size") else None
    max_size = int(request.form.get("max_size")) if request.form.get("max_size") else None

    if state:
        params["school.state"] = state
    if min_tuition and max_tuition:
        params["latest.cost.tuition.in_state__range"] = f"{min_tuition}..{max_tuition}"
    if min_admission_rate and max_admission_rate:
        params["latest.admissions.admission_rate.overall__range"] = f"{min_admission_rate / 100}..{max_admission_rate / 100}"
    if min_size and max_size:
        params["latest.student.size__range"] = f"{min_size}..{max_size}"
    
    response = requests.get(API_URL, params=params)
    response_data = response.json()

    colleges = response_data.get("results", [])
    print("API response status code:", response.status_code)
    print("API response data:", response.json())
    return render_template("search_results.html", colleges=colleges)

if __name__ == "__main__":
    app.run(debug=True)