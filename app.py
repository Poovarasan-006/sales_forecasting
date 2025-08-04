from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    forecast = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            data = pd.read_csv(file)
            
            # Basic validation
            if 'Sales' not in data.columns:
                return render_template('index.html', forecast=["Error: CSV must contain a 'Sales' column."])
            
            data['Month'] = range(1, len(data)+1)

            # Train simple linear regression
            X = data[['Month']]
            y = data['Sales']
            model = LinearRegression()
            model.fit(X, y)

            # Predict next 3 months
            future_months = np.array([[len(data)+i] for i in range(1, 4)])
            forecast_values = model.predict(future_months)
            
            forecast = [round(val, 2) for val in forecast_values]
    
    return render_template('index.html', forecast=forecast)

if __name__ == '__main__':
    app.run(debug=True)

