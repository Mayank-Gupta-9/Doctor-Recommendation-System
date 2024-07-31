from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load and preprocess the data
file_path = 'Specialist.xlsx'  # Make sure the Specialist.xlsx file is in the same directory as app.py
data = pd.read_excel(file_path)

def preprocess_data(data):
    if data.columns[0].startswith('Unnamed'):
        data = data.drop(columns=[data.columns[0]])
    data.columns = [col.strip().lower().replace(' ', '_') for col in data.columns]
    return data

data_cleaned = preprocess_data(data)

def recommend_specialist(input_symptoms, data):
    input_symptoms = [symptom.strip().lower().replace(' ', '_') for symptom in input_symptoms]
    invalid_symptoms = [symptom for symptom in input_symptoms if symptom not in data.columns]
    if invalid_symptoms:
        return f"Invalid symptoms: {invalid_symptoms}"
    matching_rows = data[input_symptoms].sum(axis=1) == len(input_symptoms)
    recommended_specialists = data.loc[matching_rows, 'disease'].unique()
    return recommended_specialists

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        input_symptoms = [symptom.strip() for symptom in symptoms.split(",")]
        try:
            recommendations = recommend_specialist(input_symptoms, data_cleaned)
        except ValueError as e:
            return render_template('index.html', error=str(e))
    
    return render_template('index.html', recommendations=list(recommendations))

if __name__ == '__main__':
    app.run(debug=True)
