

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
    return 'TESTING'





@app.route('/api', methods =['GET'])
def api():
    return 'ANOTHER TEST'




#MODEL API
@app.route('/predict', methods =['POST'])
def predict():

    #Loads pickle files for list of data types and model, scalar and imputer pickle files. Also list of variable names from feature selection
    objects = pickle.load(open('objects', 'rb'))            #Fields that should be Object type
    float64s = pickle.load(open('float64s','rb'))           #Fields that should be Float64
    model = pickle.load(open('model', 'rb'))
    scaler = pickle.load(open('scaler','rb'))
    imputer = pickle.load(open('imputer','rb'))
    variables = pickle.load(open('variables','rb'))         #Variables to be fed into the model (25)

    #Loads data into dataframe


    # df = pd.read_csv('exercise_26_train.csv').drop(columns =['y'])

    value = request.json
    try:
        df = pd.DataFrame.from_dict(value)
    except:
        try:
            df = pd.DataFrame.from_dict([value])
        except:
            return 'Improper Structure Format'

    #Checks to see if data size and type matches what is expected
    if df.shape[1] != 100:
        return 'Unexpected size of input'


    #Checks and adjusts datatypes
    df[float64s] = df[float64s].replace('',np.nan)                                          #replaces '' in fields that should be numeric with NaN
    try:                                                                #Convert everything that should be a float to a float in case inputs are all strings. If not possible, type mismatch.
        df[float64s] = df[float64s].astype(float)
    except:
        return 'Mismatch variable types_1'
    if df.columns[df.dtypes == 'object'].tolist() != objects or df.columns[df.dtypes == 'float64'].tolist() != float64s:        #Another Type Mismatch check
        return 'Mismatch variable types_2'



    #From notebook. Formats dollar and percent.
    df['x12'] = df['x12'].str.replace('$', '')
    df['x12'] = df['x12'].str.replace(',', '')
    df['x12'] = df['x12'].str.replace(')', '')
    df['x12'] = df['x12'].str.replace('(', '-')
    df['x12'] = df['x12'].astype(float)
    df['x63'] = df['x63'].str.replace('%', '')
    df['x63'] = df['x63'].astype(float)








    #Imputes and scales after dropping nonnumerical fields.
    test_imputed = pd.DataFrame(imputer.transform(df.drop(columns=['x5', 'x31', 'x81', 'x82'])), columns=df.drop(columns=['x5', 'x31', 'x81', 'x82']).columns)


    # test_imputed = pd.DataFrame(df.drop(columns=['x5', 'x31', 'x81', 'x82']))
    test_imputed_std = pd.DataFrame(scaler.transform(test_imputed), columns=test_imputed.columns)

    #One Hot Encodes the dropped numeric fields and appends them back
    dumb5 = pd.get_dummies(df['x5'], drop_first=True, prefix='x5', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb5], axis=1, sort=False)

    dumb31 = pd.get_dummies(df['x31'], drop_first=True, prefix='x31', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb31], axis=1, sort=False)

    dumb81 = pd.get_dummies(df['x81'], drop_first=True, prefix='x81', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb81], axis=1, sort=False)

    dumb82 = pd.get_dummies(df['x82'], drop_first=True, prefix='x82', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb82], axis=1, sort=False)


    del dumb5, dumb31, dumb81, dumb82

    # After one hot encoding, if desired fields for model not encoded, create them with 0 values for all rows
    for var in variables:
        if var not in test_imputed_std:
            test_imputed_std[var] = 0


    result = pd.DataFrame(test_imputed_std[variables])
    result['phat'] = model.predict(test_imputed_std[variables])
    result['business_outcome'] = np.where(result['phat'].lt(0.712), 0, 1)
    result = result.reindex(sorted(result.columns), axis=1)
    result = result.to_json(orient="records")

    return result





if __name__ == "__main__":
    app.run(host='0.0.0.0',port='1313',debug=True,)