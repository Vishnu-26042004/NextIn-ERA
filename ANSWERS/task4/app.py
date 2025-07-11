# app.py

from flask import Flask, request, render_template
import pandas as pd
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load trained model
model = joblib.load('house_price_model.pkl')

# Available locations (used in dropdown)
locations = ['Downtown', 'Suburb', 'Rural']

@app.route('/', methods=['GET', 'POST'])
def home():
    predicted_price = None

    if request.method == 'POST':
        # Get form data
        location = request.form['location']
        size_sqft = float(request.form['size_sqft'])
        year_built = int(request.form['year_built'])

        # Create input DataFrame
        input_df = pd.DataFrame({
            'location': [location],
            'size_sqft': [size_sqft],
            'year_built': [year_built]
        })

        # Predict using the model
        prediction = model.predict(input_df)[0]
        predicted_price = f"${prediction:,.2f}"

    return render_template('index.html', locations=locations, prediction=predicted_price)

if __name__ == '__main__':
    app.run(debug=True)