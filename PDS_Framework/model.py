from db import db
import pandas as pd
from marshmallow import Schema
import json
from flask_marshmallow import Marshmallow

# Take a csv and push it to postgresql

ma = Marshmallow()

class corona(ma.Schema):

    class Meta:
     fields = ('State','Deaths')

class country(ma.Schema):

    class Meta:
        fields = ('State','Deaths');

class Corona_Virus(db.Model):


    __tablename__     = "corona_data"
    id                = db.Column(db.Integer,primary_key= True);
    Observation_Date  = db.Column(db.DateTime);
    State             = db.Column(db.String(200));
    Country           = db.Column(db.String(200));
    Last_Update       = db.Column(db.DateTime);
    Confirmed         = db.Column(db.Float);
    Deaths            = db.Column(db.Float);
    Recovered         = db.Column(db.Float);


    def __init__(self,id,obs_date,state,country,last_update,confirmed,deaths,recovered):

        self.id               = id;
        self.Observation_Date = obs_date;
        self.State            = state;
        self.Country          = country;
        self.Last_Update      = last_update;
        self.Confirmed        = confirmed;
        self.Deaths           = deaths;
        self.Recovered        = recovered;


    def save_to_db(self):
        #Inserting to table
        db.session.add(self);
        db.session.commit();

    @classmethod
    def get_by_state_death(cls):
        # Fetch all data from postgresql i.e select *
        required_data = cls.query.all();
        obj = corona(many=True)
        w   = obj.dump(required_data);
        df_pandas = pd.DataFrame(w);
        df_agg = df_pandas.groupby('State')['Deaths'].sum().reset_index();
        print(df_agg)
        return (json.loads(df_agg.to_json(orient='records')))





    @classmethod
    def get_by_country_death(cls):

       required_datum =cls.query.all();
       objs           = country(many=True);
       w = objs.dump(required_datum);
       df_pandas = pd.DataFrame(w);
       df_agg = df_pandas.groupby('Country')['Deaths'].sum().reset_index();
       return df_agg.to_json(orient='records'), 200


