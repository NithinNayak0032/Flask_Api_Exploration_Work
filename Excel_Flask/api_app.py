from flask import Flask,Response
from flask_restx import Api,Resource
import pandas as pd
import json

app = Flask(__name__);
api = Api(app);
#Take excel create json response

class Country(Resource):

    @classmethod
    def get(cls):

        df_pandas = pd.read_excel("/home/nithin/Downloads/Vaccine_Data.xlsx");
        df_agg    = df_pandas.groupby('country')['total_vaccinations'].sum().reset_index();
        return json.loads(df_agg.to_json(orient='records'));

class Vaccine(Resource):

    @classmethod
    def get(cls):

        df_pandas = pd.read_excel("/home/nithin/Downloads/Vaccine_Data.xlsx");
        df_agg    = df_pandas.groupby('vaccines')['total_vaccinations'].sum().reset_index();
        return json.loads(df_agg.to_json(orient='records'));


api.add_resource(Country,"/get_country/");
api.add_resource(Vaccine,"/get_vaccine/");
app.run(debug=True);
