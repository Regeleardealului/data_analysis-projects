from flask import Flask, request, render_template
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
with open('gold_price_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    final_features = np.array([features])

    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
    return render_template('index.html', prediction_text=f'Estimated Gold Price would be ${output}')
    
if __name__ == '__main__':
    app.run(debug=True)



# >>>>>>>>>>>>>>>>>FOR SEARCHING AFTER A FILE, TO KNOW WHICH ENVIRONMENT SHOULD BE ACTIVATED<<<<<<<<<<<<<<<<<<<<<<<<
# dir /s /b app.py



# >>>>>>>>>>>>>>TO RUN THE CODE<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# conda activate usefullPython_codes 
# cd C:\Users\sogor>cd C:\Users\sogor\OneDrive\Documents\DataScientist_practice\python\gold_price_app
# pip install -r requirements.txt
# python app.py