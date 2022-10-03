import pickle
import pandas as pd
import numpy as np
import datetime
import inflection

class Rossmann(object):
    def __init__(self):
        self.home_path='/Users/Alysson/Documents/Projects/Rossmann-Sales-Forecast/scr/'
        
    def data_cleaning(self, data):     
        snakecase = lambda x: inflection.underscore(x)
        cols_new = list(map( snakecase, data.columns))
        data.columns = cols_new
        
        data['date'] = pd.to_datetime(data['date'])

        data[['competition_open_since_month','competition_open_since_year']] = data[['competition_open_since_month','competition_open_since_year']].fillna(data[['competition_open_since_month', 'competition_open_since_year']].median())
        data['competition_distance'] = data['competition_distance'].fillna(7000)
        data= data.fillna(0)        
                
        data = data.astype({"store": 'int32', 
                            "day_of_week": 'int8', 
                            #"customers": 'int32',
                            "open": 'int8',
                            "promo": 'int8',
                            "promo2": 'int8',
                            "promo2_since_week": 'int32',
                            "promo2_since_year": 'int32',
                            "competition_distance": 'int32',
                            "competition_open_since_month": 'int32',
                            "competition_open_since_year": 'int32'}) 
        return data
              
       
    def feature_engineering(self, data ):
        data['day'] = data['date'].dt.day
        data['month'] = data['date'].dt.month
        data['year'] = data['date'].dt.year
        data['day_of_year'] = data['date'].dt.dayofyear
        
        #Calculate competition open time in months
        data['competition_open_since'] = 12 * (data['date'].dt.year - data['competition_open_since_year']) + (data['date'].dt.month - data['competition_open_since_month'])
        data['competition_open_since'] = data['competition_open_since'].apply(lambda x: x if x > 0 else 0)
        
        #Calculate promo2 open time in weeks
        data['promo_open_since'] = 12 * (data['date'].dt.year - data.promo2_since_year) + (data['date'].dt.isocalendar().week - data.promo2_since_week) / 4.0
        data['promo_open_since'] = data['promo_open_since'].apply(lambda x: x if x > 0 else 0)
        
        data = data.astype({"day": 'int8', 
                            "month": 'int32', 
                            "year": 'int32',
                            "day_of_year": 'int32',
                            "competition_open_since": 'int32',
                            "promo_open_since": 'int32'})
        
             
        return data
        
        
    def data_preparation(self, data):    
        
        assortment_dict = {'a': 1,  'b': 2, 'c': 3}
        data['assortment'] = data['assortment'].map(assortment_dict)

        store_dict = {'c': 1,  'd': 2, 'a': 3, 'b':4}
        data['store_type'] = data['store_type'].map(store_dict)         
     
        
        data['promo_interval'].replace("Mar,Jun,Sept,Dec", 3, inplace=True)
        data['promo_interval'].replace("Feb,May,Aug,Nov", 2, inplace=True)
        data['promo_interval'].replace("Jan,Apr,Jul,Oct", 1, inplace=True)
        data['promo_interval'].replace("0", 0, inplace=True)
        
        data['state_holiday'].replace("a", 1, inplace=True)
        data['state_holiday'].replace("b", 1, inplace=True)
        data['state_holiday'].replace("c", 1, inplace=True)
        data['state_holiday'].replace("0", 0, inplace=True)  
        
        data = data.astype({"state_holiday": 'int8', 
                            "school_holiday": 'int8', 
                            "store_type": 'int8',
                            "assortment": 'int8'})         
        
        default_features = ['store', 
                     'day_of_week', 'day', 'month',#'year',
                     'day_of_year',
                     'competition_distance',
                     'competition_open_since',
                     'promo',
                     'promo_open_since',
                     #'is_promo_month',
                     'promo2',
                     #'competition_open_since_month','competition_open_since_year',    
                     'promo2_since_week',
                     'school_holiday', 
                     'promo_interval',                
                     'assortment',
                     'store_type'
                     #'open'
                    ]  
    

        return data[default_features]

        
    def get_prediction( self, model, original_data, test_data ):
        #prediction
        pred = model.predict( test_data )
        
        #retorna o dataset recebido, com a coluna prediction preenchida
        original_data['prediction'] = np.expm1( pred )
        
        return original_data.to_json( orient='records', date_format='iso' )