from app.insert_data import generate_data
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

@app.route('/eximius/api/inputcandidatedetail', methods=['POST'])
def candidateonboardingemail():
    email_id = request.json.get("email")
    mobile = request.json.get("mobile")
    name = request.json.get("name")
    workauth = request.json.get("workauth")
    annualrate = request.json.get("annualrate")
    hourlyrate = request.json.get("hourlyrate")
    relocate = request.json.get("relocate")
    location = request.json.get("location")

    status = generate_data(email_id,mobile,name,workauth,annualrate,hourlyrate,relocate,location)
    if status:
        return jsonify({"message":"success"})
    else:
        return jsonify({"message":"failure"})

@app.route('/eximius/api/getData/findcandidatedetail', methods=['POST'])
def findcandidatedetail():

    email_id = request.json.get("email")
    if email_id is None or email_id.strip() == "":
        print("NO")
        return jsonify({"message": "No candidate ID provided"}), 404
    else:
        status, results =  database_obj.check_email_exists(email= email_id)

        if results:
            return jsonify(results)  # Assuming only one item corresponds to the job_id
        else:
            return jsonify({"message": "No data exist"}), 404    

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)