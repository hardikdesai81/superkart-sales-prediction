
# This imports the core dependencies for environment retrieval, UI rendering, data tabularization, and HTTP client requests
import os
import streamlit as st
import pandas as pd
import requests

# This establishes the target URL for the backend API server with fallback defaults
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:7860").rstrip("/")

# This sets the main application title displayed in the user interface
st.title("SuperKart System")

# This creates a dedicated UI subsection header for single record real-time inference
st.subheader("Online Prediction")

# This displays guidance text describing required feature inputs for prediction
st.write("Enter the product and store details below to predict the total sales.")

# This collects input feature values through numeric controls and interactive selection menus
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.34)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.123)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=123.45)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
Product_Id_char = st.selectbox("Product ID Character", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=99)
Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

# This constructs the feature payload dictionary matching the model schema expectations
product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

# This handles single record prediction trigger and backend API network communication
if st.button("Predict", type='primary'):
    # This sends an HTTP POST request containing JSON feature payload to the single prediction endpoint
    response = requests.post(
        f"{BACKEND_URL}/v1/predict",
        json=product_data
    )
    # This parses successful responses and displays formatted prediction results or failure notices
    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Sales"]
        st.success(f"Predicted Product Store Sales Total: ${predicted_sales:.2f}")
    else:
        st.error("Unable to connect to the prediction API.")

# This creates a dedicated UI subsection header for batch CSV processing
st.subheader("Batch Prediction")

# This renders a file uploader component accepting tabular CSV datasets
uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

# This manages batch file processing triggers and response dataset formatting
if uploaded_file is not None:
    if st.button("Predict for Batch", type='primary'):
        # This sends an HTTP POST request transmitting the file payload to the batch endpoint
        response = requests.post(
            f"{BACKEND_URL}/v1/predictbatch",
            files={"file": uploaded_file}
        )
        # This parses batch predictions and formats the outputs into dynamic UI tables
        if response.status_code == 200:
            results = response.json()
            st.success("Predictions completed successfully!")
            try:
                # This normalizes response payload structures into pandas DataFrames for tabular rendering
                if isinstance(results, list):
                    df = pd.DataFrame(results)
                elif isinstance(results, dict):
                    if all(not isinstance(v, (list, dict)) for v in results.values()):
                        df = pd.DataFrame([results])
                    else:
                        df = pd.DataFrame(results)
                else:
                    df = pd.DataFrame({"Result": [results]})

                # This renders full-width interactive data tables containing batch predictions
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                # This catches table rendering errors and falls back to raw JSON display
                st.error(f"Unable to display results as a table: {e}")
                st.json(results)
        else:
            st.error("Unable to connect to the prediction API.")
