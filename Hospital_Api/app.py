from flask import Flask
from flask_restx import Api,Resource
from flask_jwt_extended import JWTManager
from resources.users import UserLogin,User,UserRegister,ListUser
from resources.hospitals import HospitalRegister,ListHospital,ListGroup,HospitalDetail
from db import db
from ma import ma
import datetime
import os
import configparser

configuartion_path = os.path.dirname(os.path.abspath(__file__))+"/config/config.ini"
config = configparser.ConfigParser()
config.read(configuartion_path);

app = Flask(__name__);

#Fetching required details from config file
app.config['SQLALCHEMY_DATABASE_URI']        = config['Database']['database_uri'];
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"]                 = config['Key']['secret_key']

#Instantiating jwt and app object from their classes
jwt = JWTManager(app)
api = Api(app);

#Routes For Apis
api.add_resource(UserRegister, "/create_user");
api.add_resource(User, "/user/<int:user_id>");
api.add_resource(UserLogin, "/login");
api.add_resource(ListUser,"/list_all_user");
api.add_resource(HospitalRegister,"/create_hospital")
api.add_resource(ListHospital,"/list_all_hospital")
api.add_resource(ListGroup,"/list_all_groups");
api.add_resource(HospitalDetail,"/edit_details/<int:hid>")

if __name__ == "__main__":

    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
