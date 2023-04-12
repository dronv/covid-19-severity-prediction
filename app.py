import numpy as np
from flask import Flask, jsonify, request, render_template
import pickle
import plotly.graph_objs as go
import pandas as pd
import requests

app = Flask(__name__,static_url_path='/static')
model_rf_ward = pickle.load(open('models/new_rf_ward.pkl','rb'))

@app.route('/')
def home():
    response = requests.get('https://api.opencovid.ca/summary?loc=ON')
    if response.ok:
        data = response.json()
        print(data)
        return render_template('index.html', data= data)
    else:
        data = 'error : Failed to fetch data'
        return render_template('index.html', data= data)

@app.route('/reportform')
def form():
    return render_template('report_based_form.html')

@app.route('/reportForm', methods=['POST'])
def reportForm():
    features = []
    for value in request.form.values():
        features.append(value)
    print(features)
    features = [np.array(features)]
    prediction = model_rf_ward.predict(features)
    output = prediction[0]
    output = output.item()

    fig = (go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = output,
    mode = "gauge+number+delta",
    title = {'text': "Covid-Meter"},
    gauge = {'axis': {'range': [0, 3],'tickwidth': 1, 'tickcolor': "darkblue"},
             'bar': {'color': "darkblue"},
             'steps' : [
                 {'range': [0,1], 'color': "limegreen"},
                 {'range': [1, 2], 'color': "yellow"},
                 {'range': [2, 3], 'color': "red"}],
             'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 2.9}}))
    )
    fig.show(renderer="browser")

    if(output == 0): 
        return render_template('report_based_form.html', prediction_value={output}, prediction_text="Risk Prediction: Low")
    elif(output == 1):
        return render_template('report_based_form.html', prediction_value={output}, prediction_text="Risk Prediction: mild")
    elif(output == 2):
        return render_template('report_based_form.html', prediction_value={output}, prediction_text="Risk Prediction: moderate")
    elif(output == 3):
        return render_template('report_based_form.html', prediction_value={output}, prediction_text="Risk Prediction: Severe")
    else:
        return render_template('report_based_form.html', prediction_value={output}, prediction_text="Something went wrong! Please try again!")
   
if __name__ == "__main__":
    app.run(host='0.0.0.0')