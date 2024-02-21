from flask import Flask, render_template, redirect, request
import joblib
app = Flask(__name__)

rfc = joblib.load('rfc.pkl')
unique = ['itching', 'skin rash', 'nodal skin eruptions', 'dischromic  patches', 'continuous sneezing', 'shivering', 'chills', 'watering from eyes', 'stomach pain', 'acidity', 'ulcers on tongue', 'vomiting', 'cough', 'chest pain', 'yellowish skin', 'nausea', 'loss of appetite', 'abdominal pain', 'yellowing of eyes', 'burning micturition', 'spotting  urination', 'passage of gases', 'internal itching', 'indigestion', 'muscle wasting', 'patches in throat', 'high fever', 'extra marital contacts', 'fatigue', 'weight loss', 'restlessness', 'lethargy', 'irregular sugar level', 'blurred and distorted vision', 'obesity', 'excessive hunger', 'increased appetite', 'polyuria', 'sunken eyes', 'dehydration', 'diarrhoea', 'breathlessness', 'family history', 'mucoid sputum', 'headache', 'dizziness', 'loss of balance', 'lack of concentration', 'stiff neck', 'depression', 'irritability', 'visual disturbances', 'back pain', 'weakness in limbs', 'neck pain', 'weakness of one body side', 'altered sensorium', 'dark urine', 'sweating', 'muscle pain', 'mild fever', 'swelled lymph nodes', 'malaise', 'red spots over body', 'joint pain', 'pain behind the eyes', 'constipation',
          'toxic look (typhos)', 'belly pain', 'yellow urine', 'receiving blood transfusion', 'receiving unsterile injections', 'coma', 'stomach bleeding', 'acute liver failure', 'swelling of stomach', 'distention of abdomen', 'history of alcohol consumption', 'fluid overload', 'phlegm', 'blood in sputum', 'throat irritation', 'redness of eyes', 'sinus pressure', 'runny nose', 'congestion', 'loss of smell', 'fast heart rate', 'rusty sputum', 'pain during bowel movements', 'pain in anal region', 'bloody stool', 'irritation in anus', 'cramps', 'bruising', 'swollen legs', 'swollen blood vessels', 'prominent veins on calf', 'weight gain', 'cold hands and feets', 'mood swings', 'puffy face and eyes', 'enlarged thyroid', 'brittle nails', 'swollen extremeties', 'abnormal menstruation', 'muscle weakness', 'anxiety', 'slurred speech', 'palpitations', 'drying and tingling lips', 'knee pain', 'hip joint pain', 'swelling joints', 'painful walking', 'movement stiffness', 'spinning movements', 'unsteadiness', 'pus filled pimples', 'blackheads', 'scurring', 'bladder discomfort', 'foul smell of urine', 'continuous feel of urine', 'skin peeling', 'silver like dusting', 'small dents in nails', 'inflammatory nails', 'blister', 'red sore around nose', 'yellow crust ooze']

import pymongo
import pandas as pd

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db=myclient.new_database
data=db.my_data


@app.route('/')
def hello():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def marks():
    print("ob")
    if request.method == 'POST':
        f = request.form.getlist('symptom')
        headache = overweight = alcohol = fever = runny = ""
        headache = request.form.getlist('headache')
        if len(headache):
            headache = headache[0]
        overweight = request.form.getlist('overweight')
        if len(overweight):
            overweight = overweight[0]
        alcohol = request.form.getlist('alcohol')
        if len(alcohol):
            alcohol = alcohol[0]
        fever = request.form.getlist('fever')
        if len(fever):
            fever = fever[0]
        runny = request.form.getlist('runny nose')
        if len(runny):
            runny = runny[0]

        cols = [0]*131
        if(headache == "Yes"):
            idx = unique.index("headache")
            cols[idx] = 1

        if(overweight == "Yes"):
            idx = unique.index("obesity")
            cols[idx] = 1

        if(fever == "Yes"):
            idx = unique.index("high fever")
            cols[idx] = 1

        if(runny == "Yes"):
            idx = unique.index("runny nose")
            cols[idx] = 1

        if(alcohol == "Yes"):
            idx = unique.index("history of alcohol consumption")
            cols[idx] = 1

        for i in range(0, len(unique)):
            if unique[i] in f:
                cols[i] = 1

        pred = rfc.predict([cols])
        pred = pred[0]
        pred = pred.strip()
        print(pred)
        dff=data.find_one({'Disease':pred})
        

        des = dff['Description']
        p1 = dff['Precaution_1']
        p2 = dff['Precaution_2']
        p3 = dff['Precaution_3']
        p4 = dff['Precaution_4']
        t = dff['test']

        cnt = 0
        for i in range(0, len(cols)):
            if cols[i] == 1:
                cnt += 1

        if cnt < 5:
            pred = ""

    return render_template("ind.html", pred=pred, des=des, pre1=p1, pre2=p2, pre3=p3, pre4=p4, test=t)


if __name__ == '__main__':
    app.run(debug=True)


