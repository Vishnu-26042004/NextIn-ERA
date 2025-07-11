# train_model.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Sample dataset
data = {
    'location': ['Downtown', 'Suburb', 'Suburb', 'Downtown', 'Rural', 'Rural', 'Suburb', 'Downtown'],
    'size_sqft': [850, 1500, 1200, 1000, 900, 1100, 1300, 900],
    'year_built': [2000, 1995, 2010, 2015, 1980, 1975, 2020, 2018],
    'price': [300000, 350000, 320000, 310000, 200000, 180000, 360000, 305000]
}

df = pd.DataFrame(data)

# Features and Target
X = df[['location', 'size_sqft', 'year_built']]
y = df['price']

# Preprocessing (One-hot encode the 'location' feature)
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), ['location']),
        ('num', 'passthrough', ['size_sqft', 'year_built'])
    ])

# Build pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Train model
model.fit(X, y)

# Save trained model
joblib.dump(model, 'house_price_model.pkl')
print("✅ Model trained and saved as 'house_price_model.pkl'")