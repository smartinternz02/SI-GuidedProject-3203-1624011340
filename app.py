import numpy as np
from flask import Flask, request, jsonify, render_template
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "CDgOsYuXYeCK8qRj5z43WXj-x0_9S_H5ZczG0MyuE5Jy"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

import pickle
app = Flask(__name__)
model = pickle.load(open('university.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('Demo2.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    min max scaling
    min1=[290.0, 92.0, 1.0, 1.0, 1.0,  6.8, 0.0]
    max1=[340.0, 120.0, 5.0, 5.0, 5.0, 9.92, 1.0]
    '''
    k = [float(x) for x in request.form.values()]
    payload_scoring = {"input_data": [{"field": [["GRE Score","TOEFL Score","University Rating","SOP","LOR","CGPA","Research"]],
   "values": [[k[0],k[1],k[2],k[3],k[4],k[5],k[6]]]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/73850817-1cdd-4b69-8914-48fc9741e164/predictions?version=2021-07-05', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    pred = predictions['predictions'][0]['values'][0][0]
    '''
    p = []
    for i in range(7):
        l=((k[i]-min1[i])/(k[i]-max1[i]))
        p.append(l)
    prediction = model.predict([k])
    print(prediction)
    output=prediction[0]
    '''
    if(pred==False):
        return render_template('noChance.html', prediction_text='You Dont have a chance')
    else:
         return render_template('chance.html', prediction_text='You have a chance')
if __name__ == "__main__":
    app.run(debug=True)