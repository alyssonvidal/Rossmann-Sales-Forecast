import pickle
import pandas as pd
from flask             import Flask, request, Response
from rossmann.Rossmann import Rossmann  
import xgboost as xgb
from xgboost import XGBRegressor
import os


# loading model
#model = pickle.load(open('/Users/Alysson/Documents/Projects/Rossmann-Sales-Forecast/model/model_xgb_tunned.pkl', 'rb')) #handler local
model = pickle.load(open('model/model_xgb_tunned.pkl', 'rb'))#handler cloud

# initialize API
app = Flask( __name__ )
@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predict():
    test_json = request.get_json()   
    if test_json: # there is data
        if isinstance( test_json, dict ): # unique example
            test_raw = pd.DataFrame( test_json, index=[0] )            
        else: # multiple example
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys()) 
                   
        pipeline = Rossmann() 
        df1 = pipeline.data_cleaning( test_raw )  
        df2 = pipeline.feature_engineering( df1 )
        df3 = pipeline.data_preparation( df2 )
        df_response = pipeline.get_prediction( model, test_raw, df3 )

        return df_response
         
    else:
        Response('{}', status = 200, mimetype = 'application/json')
        
if __name__=="__main__":
    #app.run(debug=True)
    port = os.environ.get('PORT',5000)
    app.run('0.0.0.0',port=port)
    #app.run('127.0.0.1')#ssh -R 80:localhost:8080 nokey@localhost.run
