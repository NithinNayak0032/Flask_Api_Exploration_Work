from flask import Flask
from flask_restx import Api,Resource
from model import  Corona_Virus
from db import db
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database,database_exists
import csv

app = Flask(__name__);
api = Api(app);
engine = create_engine("postgres://postgres:@localhost/covid_db");
if not database_exists(engine.url):
    create_database(engine.url);
else:
    pass;
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres:@localhost/covid_db"

@app.before_first_request
def create_tables():
    db.create_all()

class ETL(Resource):

    def post(self):

      with open("/home/nithin/Downloads/archive (1)/covid_19_data.csv","r") as f:

        row = csv.reader(f);
        next(row,None);
        for rows in row:
            if len(rows)>0:
                print(rows)
                record = Corona_Virus(rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7]);
                Corona_Virus.save_to_db(record);



class State(Resource):

    def get(self):

        data = Corona_Virus.get_by_state_death();
        return data,200

db.init_app(app)
api.add_resource(ETL,'/insert_data');
api.add_resource(State,'/get_state_death/')
app.run();
