import streamlit as st
import pickle
import pandas as pd
import numpy as np
from datetime import datetime

# Load model
model = pickle.load(open("flight_rf.pkl", "rb"))

st.title("Flight Fare Prediction App")

# Input fields
st.subheader("Enter Flight Details")

# Date of Journey
date_dep = st.datetime_input("Departure Time", value=datetime.now())
date_arr = st.datetime_input("Arrival Time", value=datetime.now())

# Total Stops
Total_stops = st.selectbox("Total Stops", [0, 1, 2, 3, 4])

# Airline
airlines = ['Jet Airways','IndiGo','Air India','Multiple carriers','SpiceJet','Vistara',
            'GoAir','Multiple carriers Premium economy','Jet Airways Business',
            'Vistara Premium economy','Trujet']
airline = st.selectbox("Airline", airlines)

# Source
sources = ['Delhi', 'Kolkata', 'Mumbai', 'Chennai']
Source = st.selectbox("Source", sources)

# Destination
destinations = ['Cochin','Delhi','New_Delhi','Hyderabad','Kolkata']
Destination = st.selectbox("Destination", destinations)

# Compute duration
dur_hour = abs(date_arr.hour - date_dep.hour)
dur_min = abs(date_arr.minute - date_dep.minute)

# Journey details
Journey_day = date_dep.day
Journey_month = date_dep.month
Dep_hour = date_dep.hour
Dep_min = date_dep.minute
Arrival_hour = date_arr.hour
Arrival_min = date_arr.minute

# Airline one-hot encoding
airline_dict = {name: 0 for name in airlines}
airline_dict[airline] = 1

# Source one-hot encoding
s_Delhi = int(Source == 'Delhi')
s_Kolkata = int(Source == 'Kolkata')
s_Mumbai = int(Source == 'Mumbai')
s_Chennai = int(Source == 'Chennai')

# Destination one-hot encoding
d_Cochin = int(Destination == 'Cochin')
d_Delhi = int(Destination == 'Delhi')
d_New_Delhi = int(Destination == 'New_Delhi')
d_Hyderabad = int(Destination == 'Hyderabad')
d_Kolkata = int(Destination == 'Kolkata')

if st.button("Predict Fare"):
    final_input = [
        Total_stops,
        Journey_day,
        Journey_month,
        Dep_hour,
        Dep_min,
        Arrival_hour,
        Arrival_min,
        dur_hour,
        dur_min,
        airline_dict['Air India'],
        airline_dict['GoAir'],
        airline_dict['IndiGo'],
        airline_dict['Jet Airways'],
        airline_dict['Jet Airways Business'],
        airline_dict['Multiple carriers'],
        airline_dict['Multiple carriers Premium economy'],
        airline_dict['SpiceJet'],
        airline_dict['Trujet'],
        airline_dict['Vistara'],
        airline_dict['Vistara Premium economy'],
        s_Chennai,
        s_Delhi,
        s_Kolkata,
        s_Mumbai,
        d_Cochin,
        d_Delhi,
        d_Hyderabad,
        d_Kolkata,
        d_New_Delhi
    ]

    prediction = model.predict([final_input])
    output = round(prediction[0], 2)
    st.success(f"Predicted Flight Price: ₹{output}")