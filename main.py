from flask import Flask,request
from flask_restful import Resource, Api
import pickle
import pandas as pd
from flask_cors import CORS


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

    value = request.json
    # return str(value)
    df = pd.read_csv('exercise_26_test.csv')

    # df = pd.DataFrame(value)
    if df.shape[1] != 100:
        print("BAD INPUT")







    model = pickle.load(open('model', 'rb'))
    scaler = pickle.load(open('scaler','rb'))
    imputer = pickle.load(open('imputer','rb'))
    variables = pickle.load(open('variables','rb'))
    df['x12'] = df['x12'].str.replace('$', '')
    df['x12'] = df['x12'].str.replace(',', '')
    df['x12'] = df['x12'].str.replace(')', '')
    df['x12'] = df['x12'].str.replace('(', '-')
    df['x12'] = df['x12'].astype(float)
    df['x63'] = df['x63'].str.replace('%', '')
    df['x63'] = df['x63'].astype(float)



    train_imputed = pd.DataFrame(imputer.fit_transform(df.drop(columns=[ 'x5', 'x31', 'x81', 'x82'])),
                                 columns=df.drop(columns=[ 'x5', 'x31', 'x81', 'x82']).columns)
    train_imputed_std = pd.DataFrame(scaler.fit_transform(train_imputed), columns=train_imputed.columns)

    dumb5 = pd.get_dummies(df['x5'], drop_first=True, prefix='x5', prefix_sep='_', dummy_na=True)
    train_imputed_std = pd.concat([train_imputed_std, dumb5], axis=1, sort=False)

    dumb31 = pd.get_dummies(df['x31'], drop_first=True, prefix='x31', prefix_sep='_', dummy_na=True)
    train_imputed_std = pd.concat([train_imputed_std, dumb31], axis=1, sort=False)

    dumb81 = pd.get_dummies(df['x81'], drop_first=True, prefix='x81', prefix_sep='_', dummy_na=True)
    train_imputed_std = pd.concat([train_imputed_std, dumb81], axis=1, sort=False)

    dumb82 = pd.get_dummies(df['x82'], drop_first=True, prefix='x82', prefix_sep='_', dummy_na=True)
    train_imputed_std = pd.concat([train_imputed_std, dumb82], axis=1, sort=False)


    del dumb5, dumb31, dumb81, dumb82






    prediction = model.predict(train_imputed_std[variables])
    #
    return str(prediction)






if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0')