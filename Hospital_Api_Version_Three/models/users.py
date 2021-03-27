import os,sys,inspect
from db import db
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
import datetime


class UserModel(db.Model):

    __tablename__ = "users";
    id            = db.Column(db.Integer,primary_key=True,autoincrement=True);
    username      = db.Column(db.String(500),unique=True,nullable=False);
    password      = db.Column(db.String(100),nullable=False);
    role          = db.Column(db.String(100),nullable=False);
    access_to     = db.Column(db.String(500),nullable=False);
    created_on    = db.Column(db.DateTime,default=datetime.datetime.utcnow);
    updated_on    = db.Column(db.DateTime,default=datetime.datetime.utcnow);

    #Constructer to intialize values
    def __init__(self,username,password,role,access_to):

        self.username  = username;
        self.password  = Bcrypt().generate_password_hash(password).decode();
        self.role      = role;
        self.access_to = access_to;

    def json(self):

        return{"id":self.id,"username":self.username,"role":self.role,"access_to":self.access_to};

    #Function to check user authentication
    @classmethod
    def find_by_username(cls,username):
        try:

          return cls.query.filter_by(username=username).first();

        except Exception as e:

            print(e);

    #Function to check user identity
    @classmethod
    def find_role_by_id(cls,id):
         record = cls.query.filter_by(id=id).first();

         return {"role":record.role,"access_to":record.access_to}

    #Function to fetch role details of user
    @classmethod
    def find_role_by_username(cls,username):
        record = cls.query.filter_by(username=username).first();
        return {"role": record.role, "access_to": record.access_to}

    #Function to list  user details based on id
    @classmethod
    def find_by_id(cls,id):

       return cls.query.filter_by(id=id).first();

    #Function to list all the user details
    @classmethod
    def list_all(cls):

       try:
        record = cls.query.all();
        return  record;
       except Exception as e:
           print(e);

    # Function to insert data in table
    def save_to_db(self):
        try:
         db.session.add(self);
         db.session.commit();
        except Exception as e:
            print(e);

    #Function to delete data from table
    def delete_from_db(self):
        try:
            db.session.delete(self);
            db.session.commit();
        except Exception as e:
            print(e);

    #Function to update role information of the user
    @classmethod
    def update_role(cls,id,role):
       try:
        record             = cls.query.filter_by(id=id).first();
        record.role        = role;
        record.updated_on  = datetime.datetime.utcnow()
        db.session.commit();
        return record

       except Exception as e:
           print(e);

    #Function to update username of the user
    @classmethod
    def update_username(cls,id,username):
        try:
            record = cls.query.filter_by(id=id).first();
            record.username = username;
            record.updated_on = datetime.datetime.utcnow()
            db.session.commit();
            return record

        except Exception as e:
            print(e);

    #Function to update access info the user
    @classmethod
    def update_access(cls, id, access_to):
        try:
            record            = cls.query.filter_by(id=id).first();
            record.access_to  = access_to;
            record.updated_on = datetime.datetime.utcnow()
            db.session.commit();
            return record

        except Exception as e:
            print(e);

    #Function to reset pssword
    @classmethod
    def update_password(cls,id,password):
        try:
            record            = cls.query.filter_by(id=id).first();
            record.password   = Bcrypt().generate_password_hash(password).decode();
            record.updated_on = datetime.datetime.utcnow()
            db.session.commit();
            return record

        except Exception as e:
            print(e);

    #Function to check password is valid or not
    def password_is_valid(self,password):
        return  Bcrypt().check_password_hash(self.password,password)


