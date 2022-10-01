import pickle
import pandas as pd
from flask             import Flask, request, Response
from rossmann.Rossmann import Rossmann  
#import json
#import requests
import xgboost as xgb
from xgboost import XGBRegressor


# loading model
model = pickle.load(open('model/model_xgb_tunned.pkl', 'rb'))


# initialize API
app = Flask( __name__ )

@app.route('/preparation/predict', methods=['POST'])
def rossmann_predict():
    test_json = request.get_json()

    print("Teste")
   
    if test_json: # there is data
        if isinstance( test_json, dict ): # unique example
            test_raw = pd.DataFrame( test_json, index=[0] )
            
        else: # multiple example
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys())            


        
        pipeline = Rossmann() 
        df1 = pipeline.data_cleaning( test_raw )  
        df2 = pipeline.feature_engineering( df1 )
        df3 = pipeline.data_preparation( df2 )
        
        #prediction
        df_response = pipeline.get_prediction( model, test_raw, df3 )

    else:
        print("toma no cu")

    return df_response
        


if __name__=="__main__":
    app.run(debug=True)#app.run('127.0.0.1')#