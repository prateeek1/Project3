import pymongo
import pandas as pd

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")


db=myclient.new_database
data=db.my_data

# data.insert_one({'Description':'eff'})

df = pd.read_csv('symptom_Description.csv')
dff = pd.read_csv('symptom_precaution.csv')
len(dff)
test1 = {'Drug Reaction': 'Blood test', 'Malaria': 'Blood smear test', 'Allergy': 'Prick skin testing', 'Hypothyroidism': 'TSH test', 'Psoriasis': 'skin biopsy', 'GERD': 'Upper endoscopy', 'Chronic cholestasis': 'CT scan', 'hepatitis A': 'Hepatitis A IgM', 'Osteoarthristis': 'Blood tests', '(vertigo) Paroymsal  Positional Vertigo': 'Electronystagmography (ENG)', 'Hypoglycemia': 'Blood tests', 'Acne': 'HbA1C test', 'Diabetes': 'Blood sugar test', 'Impetigo': 'Lab test generally are not needed', 'Hypertension': 'Ambulatory monitoring', 'Peptic ulcer diseae': 'Urea breath test', 'Dimorphic hemmorhoids(piles)': 'Lab tests are not needed', 'Common Cold': 'Lab tests are not needed', 'Chicken pox': 'Blood tests', 'Cervical spondylosis': 'Neck X-ray', 'Hyperthyroidism': 'Blood tests',
         'Urinary tract infection': 'Urinalysis', 'Varicose veins': 'Venous Doppler ultrasound', 'AIDS': 'Antigen test', 'Paralysis (brain hemorrhage)': 'CT scan or MRI', 'Typhoid': 'Typhidot test', 'Hepatitis B': 'HBsAg test', 'Fungal infection': 'Mycology blood test', 'Hepatitis C': 'HCV antibody test', 'Migraine': 'MRI or CT scan', 'Bronchial Asthma': 'Spirometry', 'Alcoholic hepatitis': 'Serum bilirubin test and ALT test', 'Jaundice': 'urinalysis and HIDA scan', 'Hepatitis E': 'Anti HEV IgM test', 'Dengue': 'Dengue NS1 Antigen test', 'Hepatitis D': 'Liver function test', 'Heart Attack': 'Echocardiogram test', 'Pneumonia': 'Sputum test', 'Arthritis': 'ESR and CRP test', 'Gastroenteritis': 'Renal function test', 'Tuberculosis': 'TB blood test'}
for i in range(len(dff['Precaution_4'])):
    
    if pd.isna(dff['Precaution_4'][i]):
        dff['Precaution_4'][i] = "Exercise and be physically fit"
        dff['Precaution_3'][i] = "Keep check and control the cholesterol levels"
        dff['Precaution_1'][i] = "Manage Stress"
        dff['Precaution_2'][i] = "Get proper sleep"
    else:
        s = dff['Precaution_4'][i]
        s = s[0].upper()+s[1:]
        dff['Precaution_4'][i] = s
        s = dff['Precaution_3'][i]
        s = s[0].upper()+s[1:]
        dff['Precaution_3'][i] = s
        s = dff['Precaution_2'][i]
        s = s[0].upper()+s[1:]
        dff['Precaution_2'][i] = s
        s = dff['Precaution_1'][i]
        s = s[0].upper()+s[1:]
        dff['Precaution_1'][i] = s

        
        dff['Disease'][i]=dff['Disease'][i].rstrip(' ')
        print(test1[dff['Disease'][i]])

        data.insert_one({
           'Disease':dff['Disease'][i].lstrip(' '),
           'Precaution_1':dff['Precaution_1'][i],
           'Precaution_2':dff['Precaution_2'][i],
           'Precaution_3':dff['Precaution_3'][i],
           'Precaution_4':dff['Precaution_4'][i],
           'Description':df['Description'][i],
           'test':test1[dff['Disease'][i]]
           
        })




pred='Diabetes'
dff=data.find_one({'Disease':pred})
print(dff['Precaution_1'])