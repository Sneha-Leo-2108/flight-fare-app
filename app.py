import streamlit as st
import pickle
import numpy as np
import datetime
import zipfile
import os

# Load the trained model
with zipfile.ZipFile("flight_rf.zip", "r") as zip_ref:
    zip_ref.extractall()

# Load the model
with open("flight_rf.pkl", "rb") as file:
    model = pickle.load(file)

# Input form
with st.form("flight_form"):
    airline = st.selectbox("Airline", ["IndiGo", "Air India", "Jet Airways", "SpiceJet", "Vistara"])
    source = st.selectbox("Source", ["Delhi", "Kolkata", "Mumbai", "Chennai"])
    destination = st.selectbox("Destination", ["Cochin", "Delhi", "Hyderabad", "Kolkata", "New Delhi"])
    journey_date = st.date_input("Journey Date", datetime.date.today())
    dep_hour = st.slider("Departure Hour", 0, 23, 9)
    dep_min = st.slider("Departure Minute", 0, 59, 0)
    arr_hour = st.slider("Arrival Hour", 0, 23, 12)
    arr_min = st.slider("Arrival Minute", 0, 59, 30)
    stops = st.selectbox("Total Stops", [0, 1, 2, 3])

    submit = st.form_submit_button("Predict")

if submit:
    duration_hours = abs(arr_hour - dep_hour)
    duration_mins = abs(arr_min - dep_min)
    journey_day = journey_date.day
    journey_month = journey_date.month

    airline_map = ["Air India", "IndiGo", "Jet Airways", "SpiceJet", "Vistara"]
    source_map = ["Chennai", "Delhi", "Kolkata", "Mumbai"]
    destination_map = ["Cochin", "Delhi", "Hyderabad", "Kolkata", "New Delhi"]

    airline_features = [1 if airline == a else 0 for a in airline_map]
    source_features = [1 if source == s else 0 for s in source_map]
    destination_features = [1 if destination == d else 0 for d in destination_map]

    final_input = [stops, journey_day, journey_month, dep_hour, dep_min,
                   arr_hour, arr_min, duration_hours, duration_mins] + \
                   airline_features + source_features + destination_features

    prediction = model.predict(np.array(final_input).reshape(1, -1))

    st.success(f"Estimated Fare: ₹{int(prediction[0])}")
