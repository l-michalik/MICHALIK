import streamlit as st
import joblib
import numpy as np

joblib = joblib.load('laptop_price_model.pkl')

st.title('Laptop Price Predictor')

st.divider()

st.write('This app predicts the price of a laptop based on its specifications.')

st.divider()

processor_speed = st.number_input('Processor Speed (GHz)', min_value=0.0, max_value=10.0, value=2.5, step=0.1)
ram_size = st.number_input('RAM Size (GB)', min_value=0, max_value=128, value=8, step=1)
storage_capacity = st.number_input('Storage Capacity (GB)', min_value=0, max_value=2000, value=256, step=1)
screen_size = st.number_input('Screen Size (inches)', min_value=10.0, max_value=20.0, value=15.6, step=0.1)
weight = st.number_input('Weight (kg)', min_value=0.0, max_value=5.0, value=1.5, step=0.1)

X = np.array([[processor_speed, ram_size, storage_capacity, screen_size, weight]])

st.divider()

predicion = st.button('Predict Price')

st.divider() 

if predicion:
    
    st.balloons()
    
    x1 = np.array(X)
    
    predicion = joblib.predict(x1)[0]
    
    st.success(f'The predicted price of the laptop is: ${predicion:.2f}')
else:
    st.info('Click the button to predict the price of the laptop.')