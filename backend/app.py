
# This imports the required libraries for numerical operations, model deserialization, data manipulation, and web API construction
import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# This initializes the Flask application instance for the SuperKart API
superkart_api = Flask("SuperKart")

# This loads the serialized machine learning pipeline from the specified joblib file
model = joblib.load("superkart_model.joblib")

# This defines the root endpoint returning a welcome message for the API
@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart System"

# This defines an endpoint to predict sales for a single product
@superkart_api.post('/v1/predict')
def predict_sales():
    # This retrieves the JSON payload from the incoming HTTP request
    data = request.get_json()

    # This constructs a feature dictionary mapping input payload values to model features
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Product_Id_char': data['Product_Id_char'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Product_Type_Category': data['Product_Type_Category']
    }

    # This converts the single sample dictionary into a single-row pandas DataFrame
    input_data = pd.DataFrame([sample])

    # This runs prediction on the input DataFrame and extracts the scalar prediction value
    prediction = model.predict(input_data).tolist()[0]

    # This returns the prediction wrapped in a JSON response
    return jsonify({'Sales': prediction})

# Define an endpoint to predict sales for a batch of products
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    # This retrieves the uploaded CSV file object from the HTTP request files
    file = request.files['file']

    # This reads the uploaded CSV file directly into a pandas DataFrame
    input_data = pd.read_csv(file)

    # This generates predictions for all records in the input batch
    predictions = model.predict(input_data).tolist()

    # This constructs an output dictionary mapping row indices to rounded prediction values
    output_dict = {str(i): round(pred, 2) for i, pred in enumerate(predictions)}

    # This returns the dictionary mapping indices to predictions
    return output_dict


# This executes the Flask development server in debug mode when run as the main script
if __name__ == '__main__':
    superkart_api.run(debug=True)
