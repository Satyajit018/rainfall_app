# -*- coding: utf-8 -*-
"""st_rainfall.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BXNfFT7XIR6VhbaKBmOEJKH-2SaOC_66
"""

import streamlit as st
import numpy as np
import tensorflow as tf
import pandas as pd
import pickle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.optimizers import Adam
from keras.models import load_model

#import data
data_in=pd.read_csv('changed_input.csv')  # input csv file with columns of input variables
data_out=pd.read_csv('changed_output.csv') #output csv file with column of results
X_all=np.array(data_in)
y_all=np.array(data_out)

#import more data
cities = pd.read_csv('cali_input_.csv')
lat = cities['lat'].values
lon = cities['long'].values
area = cities['area'].values

#sidebar code
st.sidebar.markdown("## Select Data Intensity and Slope Angle")
names = cities['Region'].values
select_event = st.sidebar.selectbox(' Which city do you want to modify?', names)
str_t0 = st.sidebar.slider('Intensity(mm/hr)', 1, 100, 4)
t0 = np.log(float(str_t0))
slope_angle = st.sidebar.slider('Slope Angle(degrees)', 20, 35, 28)
#modify data using sidebar
city_index = names.tolist().index(select_event)
X_all[440+city_index, 0] = t0
X_all[440+city_index, 1] = slope_angle
#model code
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
# normalize the data attributes
X_all = scaler_X.fit_transform(X_all)
X=np.array(X_all[1:353,:]) #specify portion of data to use for training
y_all = scaler_y.fit_transform(y_all)
y=np.array(y_all[1:353,:]) #repeat here
#X_all.shape

model = load_model('rainfall_model.h5')
test_x=X_all[440:456,:] # specify testing dataset outside of training dataset
predictions=model.predict(test_x, batch_size=10, verbose=0)
y_pred=scaler_y.inverse_transform(predictions)
print(y_pred)

#title and graphs
st.title('Rainfall-induced Landslide simulator')
st.markdown("""
 * Use the menu to the left to modify the data
 * Your plots will appear below
""")

failure = [10**x for x in y_pred]
data = failure
col1, col2 = st.beta_columns(2)
col1.dataframe(failure)
col2.dataframe(names)
st.line_chart(data)