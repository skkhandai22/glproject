from app.candidateonboarding import candidateonboarding
from app.cosmos_db import database
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  

database_obj = database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/eximius/api/candidate_onboarding_email', methods=['POST'])
def candidateonboardingemail():
    response = candidateonboarding().get_email()  
    return jsonify(response)

@app.route('/eximius/api/getData/findcandidatedetail', methods=['POST'])
def findcandidatedetail():
    print(request.json)  # Print the entire JSON payload received

    email_id = request.json.get("email")
    if email_id is None or email_id.strip() == "":
        print("NO")
        return jsonify({"message": "No candidate ID provided"}), 404
    else:
        results =  database_obj.find_item(id=email_id)
        print(results)
        if results:
            return jsonify(results)  # Assuming only one item corresponds to the job_id
        else:
            return jsonify({"message": "No data exist"}), 404    

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)