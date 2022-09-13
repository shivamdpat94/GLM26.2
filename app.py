

from flask import Flask,request
from flask_restful import Resource, Api
import pickle
import pandas as pd
from flask_cors import CORS
import numpy as np


app = Flask(__name__)
CORS(app)
api = Api(app)




#GET
@app.route('/')
def index():
    return 'Vist /predict Endpoint'








#MODEL API
@app.route('/predict', methods =['POST'])
def predict():
    variables = ['x5_saturday',
 'x81_July',
 'x81_December',
 'x31_japan',
 'x81_October',
 'x5_sunday',
 'x31_asia',
 'x81_February',
 'x91',
 'x81_May',
 'x5_monday',
 'x81_September',
 'x81_March',
 'x53',
 'x81_November',
 'x44',
 'x81_June',
 'x12',
 'x5_tuesday',
 'x81_August',
 'x81_January',
 'x62',
 'x31_germany',
 'x58',
 'x56']                                         #Variables to be fed into the model (x25)
    float64s = ['x0',
 'x1',
 'x2',
 'x3',
 'x4',
 'x6',
 'x7',
 'x8',
 'x9',
 'x10',
 'x11',
 'x13',
 'x14',
 'x15',
 'x16',
 'x17',
 'x18',
 'x19',
 'x20',
 'x21',
 'x22',
 'x23',
 'x24',
 'x25',
 'x26',
 'x27',
 'x28',
 'x29',
 'x30',
 'x32',
 'x33',
 'x34',
 'x35',
 'x36',
 'x37',
 'x38',
 'x39',
 'x40',
 'x41',
 'x42',
 'x43',
 'x44',
 'x45',
 'x46',
 'x47',
 'x48',
 'x49',
 'x50',
 'x51',
 'x52',
 'x53',
 'x54',
 'x55',
 'x56',
 'x57',
 'x58',
 'x59',
 'x60',
 'x61',
 'x62',
 'x64',
 'x65',
 'x66',
 'x67',
 'x68',
 'x69',
 'x70',
 'x71',
 'x72',
 'x73',
 'x74',
 'x75',
 'x76',
 'x77',
 'x78',
 'x79',
 'x80',
 'x83',
 'x84',
 'x85',
 'x86',
 'x87',
 'x88',
 'x89',
 'x90',
 'x91',
 'x92',
 'x93',
 'x94',
 'x95',
 'x96',
 'x97',
 'x98',
 'x99']                                             #Fields that should be Float64
    objects = ['x5', 'x12', 'x31', 'x63', 'x81', 'x82']         #Fields that should be Object type




    #Loads pickle files for  model, scalar and imputer.
    model = pickle.load(open('model', 'rb'))
    scaler = pickle.load(open('scaler','rb'))
    imputer = pickle.load(open('imputer','rb'))





    #Loads data into dataframe.
    value = request.json
    try:
        df = pd.DataFrame.from_dict(value)
    except:
        try:
            df = pd.DataFrame.from_dict([value])
        except:
            return 'Structure of input appears to be incorrect'







    #Checks to see if data size matches what it should be
    if df.shape[1] != 100:
        return 'Unexpected size of input'

    #Converts empty values in Float64 fields from object to NAN in cases where all values of numeric column is empty for all rows.
    df[float64s] = df[float64s].replace('',np.nan)


    #Check to see if data types are correct by comparing to lists from python notebook
    if df.columns[df.dtypes == 'object'].tolist() != objects or df.columns[df.dtypes == 'float64'].tolist() != float64s:
        return 'Mismatch variable types'



    #From notebook. Formats dollar and percent.
    df['x12'] = df['x12'].str.replace('$', '')
    df['x12'] = df['x12'].str.replace(',', '')
    df['x12'] = df['x12'].str.replace(')', '')
    df['x12'] = df['x12'].str.replace('(', '-')
    df['x12'] = df['x12'].astype(float)
    df['x63'] = df['x63'].str.replace('%', '')
    df['x63'] = df['x63'].astype(float)








    #Imputes and scales numerical fields.
    test_imputed = pd.DataFrame(imputer.transform(df.drop(columns=['x5', 'x31', 'x81', 'x82'])), columns=df.drop(columns=['x5', 'x31', 'x81', 'x82']).columns)
    test_imputed_std = pd.DataFrame(scaler.transform(test_imputed), columns=test_imputed.columns)

    #One Hot Encodes the dropped fields and appends them back
    dumb5 = pd.get_dummies(df['x5'], drop_first=True, prefix='x5', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb5], axis=1, sort=False)

    dumb31 = pd.get_dummies(df['x31'], drop_first=True, prefix='x31', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb31], axis=1, sort=False)

    dumb81 = pd.get_dummies(df['x81'], drop_first=True, prefix='x81', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb81], axis=1, sort=False)

    dumb82 = pd.get_dummies(df['x82'], drop_first=True, prefix='x82', prefix_sep='_', dummy_na=True)
    test_imputed_std = pd.concat([test_imputed_std, dumb82], axis=1, sort=False)

    del dumb5, dumb31, dumb81, dumb82





    # After one hot encoding, if desired fields for model not created/encoded, create them with 0 values for all rows
    for var in variables:
        if var not in test_imputed_std:
            test_imputed_std[var] = 0




    #Retrieve probability by running inputs into model. Classify 0 if less than .712, else 1, Concatenate both values with inputs and sort alphabetically. Convert to JSON
    result = pd.DataFrame(test_imputed_std[variables])
    result['phat'] = model.predict(test_imputed_std[variables])
    result['business_outcome'] = np.where(result['phat'].lt(0.712), 0, 1)
    result = result.reindex(sorted(result.columns), axis=1)
    result = result.to_json(orient="records")

    return result




#port was set to 1313 but there were on and off periods where host could not connect to containerized API. 5000 seems more consistent
if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000',debug=True,)