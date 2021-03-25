import os,sys,inspect
from db import db
import datetime

class Hospital(db.Model):

    __tablename__        = "hospital_details";
    hid                  = db.Column(db.Integer,primary_key=True,autoincrement=True);
    hospital_group       = db.Column(db.String(500),nullable=False);
    hospital_name        = db.Column(db.String(500),nullable=False);
    created_on           = db.Column(db.DateTime,default= datetime.datetime.utcnow);
    updated_on           = db.Column(db.DateTime,default= datetime.datetime.utcnow)


    def __init__(self,hospital_group,hospital_name):

        self.hospital_group = hospital_group;
        self.hospital_name  = hospital_name;

    @classmethod
    def find_by_hospital(cls,hospital_name):
        try:

            return cls.query.filter_by(hospital_name=hospital_name).first();

        except Exception as e:

            print(e);

    # Function to list  user details based on id
    @classmethod
    def find_by_hid(cls,hid):

        return cls.query.filter_by(hid=hid).first();

    def save_details(self):

        db.session.add(self);
        db.session.commit();

    @classmethod
    def list_all_group(cls):

        return cls.query.with_entities(cls.hospital_group);

    @classmethod
    def list_group_hospital(cls):

        record = cls.query.with_entities(cls.hospital_group,cls.hospital_name);
        return record;

    @classmethod
    def list_all_hospital(cls):

        return cls.query.with_entities(cls.hospital_name);

    def delete_data(self):

        db.session.delete(self);
        db.session.commit();

    @classmethod
    def update_hospital_name(cls,id,hospital_name):

        try:
            record              = cls.query.filter_by(hid=id).first();
            record.hospital_name = hospital_name;
            record.updated_on    = datetime.datetime.utcnow()
            db.session.commit();
            return record

        except Exception as e:
            print(e);

    @classmethod
    def update_hospital_group(cls, id, hospital_group):

        try:
            record = cls.query.filter_by(hid=id).first();
            record.hospital_group = hospital_group;
            record.updated_on = datetime.datetime.utcnow()
            db.session.commit();
            return record

        except Exception as e:
            print(e);

    @classmethod
    def list_id_name(cls,group_name):

        try:
            local_list = [];
            record = db.session.query(cls)
            for golum in record:
                if(golum.hospital_group==group_name):
                 my_dict = {}
                 print(golum)
                 my_dict['hid'] = golum.hid;
                 my_dict['hname'] = golum.hospital_name;
                 local_list.append(my_dict);
            return local_list;

        except Exception as e:
            print(e);




