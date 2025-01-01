import streamlit as st
import pickle
import json
import numpy as np

# Global variables for artifacts
__locations = None
__data_columns = None
__model = None

# Function to get estimated price
def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

# Load artifacts
def load_saved_artifacts():
    global __data_columns
    global __locations

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open('./artifacts/bangaluru_house_price.pickle', 'rb') as f:
            __model = pickle.load(f)

# Streamlit frontend
def main():
    st.title("Bengaluru House Price Prediction")

    # Form inputs
    st.sidebar.header("Enter Details")

    total_sqft = st.sidebar.number_input("Total Square Feet", min_value=300, max_value=10000, step=1)
    location = st.sidebar.selectbox("Location", __locations)
    bhk = st.sidebar.slider("BHK", min_value=1, max_value=5, step=1)
    bath = st.sidebar.slider("Bathroom", min_value=1, max_value=5, step=1)

    if st.sidebar.button("Predict Price"):
        price = get_estimated_price(location, total_sqft, bhk, bath)
        st.success(f"Estimated House Price: ₹ {price} Lakhs")

if __name__ == "__main__":
    load_saved_artifacts()
    main()
