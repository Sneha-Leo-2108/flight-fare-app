import streamlit as st
import pickle
import numpy as np
from datetime import datetime

# Load the trained model
with open("flight_rf/flight_rf.pkl", "rb") as f:

    model = pickle.load(f)

st.title("✈️ Flight Fare Prediction App")

# Input form
st.header("Enter flight details")

airline = st.selectbox("Airline", [
    'Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers',
    'SpiceJet', 'Vistara', 'GoAir', 'Multiple carriers Premium economy',
    'Jet Airways Business', 'Vistara Premium economy', 'Trujet'
])

source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai', 'Banglore'])

destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata', 'Banglore'])

dep_time = st.time_input("Departure Time", value=datetime.now().time())
arr_time = st.time_input("Arrival Time", value=datetime.now().time())

stops = st.selectbox("Total Stops", ['non-stop', '1 stop', '2 stops', '3 stops', '4 stops'])

# Preprocessing
def preprocess(dep, arr, stops, airline, source, destination):
    dep_hour = dep.hour
    dep_min = dep.minute
    arr_hour = arr.hour
    arr_min = arr.minute
    dur_hour = abs(arr_hour - dep_hour)
    dur_min = abs(arr_min - dep_min)

    stop_dict = {'non-stop': 0, '1 stop': 1, '2 stops': 2, '3 stops': 3, '4 stops': 4}
    stops_val = stop_dict[stops]

    # One-hot encoding manually
    airline_list = ['Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
                    'Multiple carriers', 'Multiple carriers Premium economy',
                    'SpiceJet', 'Trujet', 'Vistara', 'Vistara Premium economy']
    airline_encoded = [1 if airline == name else 0 for name in airline_list]

    source_list = ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']
    source_encoded = [1 if source == name else 0 for name in source_list]

    dest_list = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi']
    destination_encoded = [1 if destination == name else 0 for name in dest_list]

    features = [dep_hour, dep_min, arr_hour, arr_min, dur_hour, dur_min, stops_val] + \
               airline_encoded + source_encoded + destination_encoded

    return np.array(features).reshape(1, -1)

# Predict
if st.button("Predict Fare"):
    features = preprocess(dep_time, arr_time, stops, airline, source, destination)
    fare = model.predict(features)[0]
    st.success(f"Predicted Fare: ₹{int(fare):,}")
