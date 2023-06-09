# -*- coding: utf-8 -*-
"""OCDS - Lab 11.2 - ANN - Regressor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_5XwLtWtDAT_nzUgBDjQD6S7sjDXrLA3

## ANN - Regression
"""

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from keras.models import Sequential
from keras.layers import Dense
from scikeras.wrappers import KerasRegressor # pip install scikeras[tensorflow]
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

# Reading data 
import pandas as pd

from google.colab import files
file = files.upload()
import io
data = pd.read_csv(io.BytesIO(file['mart.csv']))

'''data = pd.read_csv("D:/APU/CT108-3-3 - OCDS/Lab Sessions/Lab11 - Neural Netwrok/mart.csv")
data.head()'''

data.head()

data.isnull().sum()

data.dtypes

data['Item_Weight'].fillna((data['Item_Weight'].mean()), inplace=True)
data['Item_Visibility'] = data['Item_Visibility'].replace(0,np.mean(data['Item_Visibility']))
data['Outlet_Establishment_Year'] = 2013 - data['Outlet_Establishment_Year']

data['Outlet_Size'].fillna('Small',inplace=True)

data = data.iloc [ : , 1: 12]
# creating dummy variables to convert categorical into numeric values
mylist = list(data.select_dtypes(include=['object']).columns)
dummies = pd.get_dummies(data[mylist], prefix= mylist)
data.drop(mylist, axis=1, inplace = True)
X = pd.concat([data,dummies], axis =1 )
y = X.iloc [ :, 4 ]
# drop the response variable
X = X.drop('Item_Outlet_Sales',1)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

X_train.shape

def baseline_model(optimizer='adam'):
    model = Sequential()
    model.add(Dense(units = 10, kernel_initializer = 'uniform', activation = 'relu', input_dim = 45)) # input layer
    model.add(Dense(units = 10, kernel_initializer = 'uniform', activation = 'relu'))
    model.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'linear')) # output layer
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
    return model

# Grid Search
epochs = [50, 100, 150]
batches = [16, 32, 64, 128]
optimizers = ['rmsprop', 'adam']

# Create hyperparameter options
hyperparameters = dict(optimizer = optimizers, epochs = epochs, batch_size = batches)
regressor = KerasRegressor(model = baseline_model) 
  
grid_search = GridSearchCV(estimator = regressor, param_grid = hyperparameters, cv = 5)

grid_search = grid_search.fit(X_train, y_train)

best_param = grid_search.best_params_
best_score = grid_search.best_score_

print(best_score)
print (best_param)

model = Sequential()
model.add(Dense(units = 10, kernel_initializer = 'uniform', activation = 'relu', input_dim = 45)) # input layer
model.add(Dense(units = 10, kernel_initializer = 'uniform', activation = 'relu'))
model.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'linear')) # output layer
model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mse'])

model.fit(X_train, y_train, validation_data = (X_test, y_test), batch_size = 16, epochs = 150, verbose = 1)

y_predict = model.predict(X_test)

from sklearn.metrics import mean_squared_error
mean_squared_error(y_predict, y_test)