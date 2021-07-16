# -*- coding: utf-8 -*-
"""kmmmmmmmmmm (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XiaRCnziSEqr0hBSmHNvXzb_dLipvpaP

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

!pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip
!pip install pandas-profiling==2.7.1

from pandas_profiling import ProfileReport

import tensorflow as tf
# import tensorflow_data_validation as tfdv
import pandas as pd

from sklearn.model_selection import train_test_split

from tensorflow_metadata.proto.v0 import schema_pb2

# print('TFDV Version: {}'.format(tfdv.__version__))
print('Tensorflow Version: {}'.format(tf.__version__))

data_train = pd.read_csv('/kaggle/input/protonx-tf03-linear-regression/trainDataset.csv', header=0)
data_train.head()

data_test = pd.read_csv('/kaggle/input/protonx-tf03-linear-regression/submissionDataset.csv', header=0)
data_test.head()

print('Number of Training Examples = {} columns'.format(data_train.shape[0]))
print('Number of Test Examples = {} columns\n'.format(data_test.shape[0]))

print(data_train.columns)
print(data_test.columns)

train_profile = ProfileReport(data_train, title='Train Dataset Profiling Report')
train_profile

map_to_uniqueness = {}
for cols in data_train.columns: 
    map_to_uniqueness[cols] = data_train[cols].nunique()
print(map_to_uniqueness)

null_values = {}
for cols in data_train.columns:
    null_values[cols] = data_train[cols].isnull().sum()
print(null_values)

import seaborn as sns
import matplotlib.pyplot as plt
cor = data_train.corr()
f, ax = plt.subplots(figsize=(15, 15))
sns.heatmap(cor, vmax=.8, square=True, annot= True);

X_train = data_train.drop(['id','weekday','cnt','atemp'], axis = 1)
#                           ,'id','holiday','weekday','workingday')
y_train = data_train['cnt']

X_test = data_test.drop(['id','weekday','cnt','atemp'], axis = 1)
#                           ,'id','holiday','weekday','workingday')
y_test = data_test['cnt']
print(X_train)
print(y_train)

# numerical_cols = ["windspeed", "temp", "hum"]
# cat_cols = [cols for cols in data_train.columns.to_list() if cols not in numerical_cols]

# data_train[cat_cols] = data_train[cat_cols].astype('category')
# data_test[cat_cols] = data_test[cat_cols].astype('category')

# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression, Ridge, Lasso
# from xgboost import XGBRegressor
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error
# from sklearn.metrics import mean_squared_log_error


# X_train, X_valid, y_train, y_valid = train_test_split(data_train.drop(['id','weekday','cnt','atemp'], axis = 1), data_train.pop("cnt"), random_state=5, test_size = 0.2)

X_test = data_test.drop(['id','weekday','cnt'], axis = 1)
y_test = data_test['cnt']

print(X_test)
print(y_test)

features = ['season','yr','mnth','hr','holiday','workingday','weathersit','temp','hum', 'windspeed']
target = 'cnt'



!pip install xgboost==1.0.1

import pandas as pd
from sklearn import preprocessing

from sklearn.preprocessing import MinMaxScaler
min_max_scaler = MinMaxScaler()

column_names_to_normalize = ['mnth', 'hr', 'holiday', 'weathersit', 'workingday']
x = X_train[column_names_to_normalize].values
x_scaled = min_max_scaler.fit_transform(x)
normalized_features = pd.DataFrame(x_scaled, columns=column_names_to_normalize, index = X_train.index)
X_train[column_names_to_normalize] = normalized_features

from sklearn.preprocessing import StandardScaler
standard_scaler = StandardScaler()

column_names_to_standardize = ['season', 'yr','temp','hum','windspeed']
x = X_train[column_names_to_standardize].values
x_scaled = standard_scaler.fit_transform(x)

standardized_features = pd.DataFrame(x_scaled, columns=column_names_to_standardize, index = X_train.index)
X_train[column_names_to_standardize] = standardized_features

import matplotlib.pyplot as plt
import seaborn as sns
ff,ax = plt.subplots(figsize = (14,14))
mask = np.triu(np.ones_like(data_train.corr(),dtype='int64'))
sns.heatmap(data_train.corr(),annot=True,linewidths=.5,mask = mask,cmap=sns.diverging_palette(10,240,n=200))

plt.show()

features = ['season','mnth','yr','hr','workingday','weathersit','temp','hum','windspeed']
target = 'cnt'

from sklearn.ensemble import RandomForestRegressor

#Create classifier object with default hyperparameters
clf = RandomForestRegressor(n_estimators = 1000,max_depth=100)  

#Fit our classifier using the training features and the training target values
clf.fit(data_train[features],data_train[target])

# from xgboost import XGBRegressor

# #Create classifier object with default hyperparameters
# clf = XGBRegressor()  

# #Fit our classifier using the training features and the training target values
# clf.fit(data_train[features],data_train[target])

predictions = clf.predict(data_test[features])

predictions

submission = pd.DataFrame({'id':data_test['id'],'cnt':predictions})

submission.head()

filename = 'submission.csv'

submission.to_csv(filename,index=False)

print('Saved file: ' + filename)