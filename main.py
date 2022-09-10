from flask import Flask,request
from flask_restful import Resource, Api
import pickle
import pandas as pd
from flask_cors import CORS
import numpy as np


app = Flask(__name__)
#
CORS(app)
# creating an API object
api = Api(app)

@app.route('/')
def index():
    return 'ssdfsdsdf'





@app.route('/api', methods =['GET'])
def api():
    return 'Hello World'

@app.route('/predict', methods =['POST'])
def predict():

    #Loads pickle files for list of data types
    objects = pickle.load(open('objects', 'rb'))
    float64s = pickle.load(open('float64s','rb'))

    #Loads data into dataframe
    value = request.json
    # return str(value)
    # df = pd.read_csv('exercise_26_test.csv')
    df = pd.DataFrame.from_dict(value)
    df = df.replace('',np.nan)          #replaces '' with NaN


    #Checks to see if data size and type matches what is expected
    if df.shape[1] != 100:
        return 'Unexpected size of input'
    if df.columns[df.dtypes == 'object'].tolist() != objects or df.columns[df.dtypes == 'float64'].tolist() != float64s:
        return 'Mismatch variable types'





    #Loads model, scalar and imputer pickle files. Also list of variable names from feature selection
    model = pickle.load(open('model', 'rb'))
    scaler = pickle.load(open('scaler','rb'))
    imputer = pickle.load(open('imputer','rb'))
    variables = pickle.load(open('variables','rb'))



    #From notebook. Formats dollar and percent.
    df['x12'] = df['x12'].str.replace('$', '')
    df['x12'] = df['x12'].str.replace(',', '')
    df['x12'] = df['x12'].str.replace(')', '')
    df['x12'] = df['x12'].str.replace('(', '-')
    df['x12'] = df['x12'].astype(float)
    df['x63'] = df['x63'].str.replace('%', '')
    df['x63'] = df['x63'].astype(float)



    #Imputes and scales after dropping nonnumerical fields. One hot encodes those nonnumerical fields
    test_imputed = pd.DataFrame(imputer.fit_transform(df.drop(columns=[ 'x5', 'x31', 'x81', 'x82'])), columns=df.drop(columns=[ 'x5', 'x31', 'x81', 'x82']).columns)
    test_imputed_std = pd.DataFrame(scaler.fit_transform(test_imputed), columns=test_imputed.columns)

    dumb5 = pd.get_dummies(df['x5'], drop_first=True, prefix='x5', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb5], axis=1, sort=False)

    dumb31 = pd.get_dummies(df['x31'], drop_first=True, prefix='x31', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb31], axis=1, sort=False)

    dumb81 = pd.get_dummies(df['x81'], drop_first=True, prefix='x81', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb81], axis=1, sort=False)

    dumb82 = pd.get_dummies(df['x82'], drop_first=True, prefix='x82', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb82], axis=1, sort=False)


    del dumb5, dumb31, dumb81, dumb82

    #After one hot encoding, if desired fields for model not encoded, create them with 0 values
    for var in variables:
        if var not in test_imputed_std:
            test_imputed_std[var] = 0

    prediction = model.predict(test_imputed_std[variables])
    #
    return str(prediction)






if __name__ == '__main__':
    app.run(debug=True, host ='127.0.0.1', port='1313')