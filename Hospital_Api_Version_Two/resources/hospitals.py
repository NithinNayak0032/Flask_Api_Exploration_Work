from flask_restx import Resource
from flask import request
from models.hospitals import Hospital
from schemas.hospitals import  HospitalSchemas,HospitalGroupSchemas
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from metric_computation import AdhocAnalysis
import json


hospital_schema = HospitalSchemas()
group_schema    = HospitalGroupSchemas()

#Class Mapping To route to include hospitals details in db
class HospitalRegister(Resource):

    @classmethod
    def post(cls):


        data          = request.get_json()
        hospital_data = hospital_schema.load(request.get_json());


        if(Hospital.find_by_hospital(hospital_data.hospital_name)):

            return {"message": "Hospital_ALREADY_EXISTS"}, 400

        record = Hospital(data['hospital_group'], data['hospital_name'])
        Hospital.save_details(record)
        return {"message": "Hospital_Added_To_List"}, 201

#Class Mapping to route being utilized to list all hospitals
class ListHospital(Resource):

    @classmethod
    def get(cls):
        try:
         list_of_hospital = Hospital.list_all_hospital();
         my_dict = {}
         hosp_list = [];
         for i in list_of_hospital:
             hosp_list.append(i.hospital_name);
             my_dict['hospitals'] = hosp_list;

         return my_dict,200;

        except Exception as e:
            print(e);
            return {"message":"Failed to fetch hospital list"},400

#Class Mapping to route being utilized to list all hospital groups
class ListGroup(Resource):

    @classmethod
    def get(cls):
        try:
            list_of_hospital = Hospital.list_group_hospital();
            my_list = []
            my_dict = {}
            for i in list_of_hospital:
                my_list.append(i.hospital_group);
            my_list = list(set(my_list));
            my_dict["hospital_groups"] = my_list
            return my_dict,200

        except Exception as e:
            print(e);
            return {"message": "Failed to fetch hospital  group list"}, 400

#Class Mapping to route being utilized to delete and edit hospital details
class HospitalDetail(Resource):

    @classmethod
    def delete(cls,hid:int):
        hosp = Hospital.find_by_hid(hid);
        print(hosp)
        if not hosp:
            return {"message": "Hospital_Not_Found"}, 404

        try:
          hosp.delete_data()
          return {"message": "Hospital_Deleted"}, 200;

        except Exception as e:
            return {"message": "Delete_Operation_Failed"},404

    @classmethod
    def put(cls,hid:int):
        hosp = Hospital.find_by_id(hid);
        if not hosp:
            return {"message": "Hospital_Not_Found"}, 404

        try:
            data = request.get_json();
            Hospital.update_hospital_name(hid,data['hospital_name']);
            return {"msg": "Hospital Updated"}, 200

        except Exception as e:
            print(e);
            return {"msg": "Failed To Update"}, 400

#Class Mapping to route being utilized to edit hospital group
class HospitalUpdate(Resource):

    @classmethod
    def put(cls, hid: int):
        hosp = Hospital.find_by_id(hid);
        if not hosp:
            return {"message": "Hospital_Not_Found"}, 404

        try:
            data = request.get_json();
            Hospital.update_hospital_name(hid, data['hospital_group']);
            return {"msg": "Group Updated"}, 200

        except Exception as e:
            print(e);
            return {"msg": "Failed To Update"}, 400


class HospitalGroupAgg(Resource):

    def get(self):

        try:

         frame = AdhocAnalysis.compute_metric('Hospital_Group')
         my_dict = json.loads(frame.to_json(orient='index',double_precision=2));
         overall_detail = AdhocAnalysis.overall_metric_computation();
         overall_detail.update(my_dict);


         return overall_detail,200

        except Exception as e:
            print(e);
            return {"status":400,"msg":"Failed to get data"},400;

class HospitalGroupMonthlyAgg(Resource):

    @classmethod
    def get(cls,group_name):

     try:

        frame = AdhocAnalysis.compute_metric('Month_Name')
        my_dict = json.loads(frame.to_json(orient='index', double_precision=2));
        local_dict={"monthly_revenue":my_dict}
        overall_detail = AdhocAnalysis.overall_metric_computation();
        hosp_detail = Hospital.list_id_name(group_name);
        overall_detail['hospitals'] = hosp_detail
        overall_detail.update(local_dict);

        return overall_detail, 200

     except Exception as e:
        print(e);
        return {"status": 400, "msg": "Failed to get data"}, 400;






