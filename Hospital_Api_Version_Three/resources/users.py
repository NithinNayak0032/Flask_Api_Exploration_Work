from flask_restx import Resource
from flask import request,jsonify
from models.users import UserModel
from ma import ma
from marshmallow import ValidationError
from schemas.users import UserSchemas
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

user_schema = UserSchemas()

#Class Mapping to route to create user
class UserRegister(Resource):

    @classmethod
    def post(cls,user_id:int):

        try:
            data  = request.get_json();
            user  = user_schema.load(request.get_json());
            check = UserModel.find_role_by_id(id=user_id);

        except ValidationError as err:
            return err.messages, 400

        if(check['role']!='admin'):
            return {"message": "Permission_Denied"}, 400;

        elif(check['role']=='admin'):

         if (UserModel.find_by_username(user.username)):
             return {"message": "USER_ALREADY_EXISTS"}, 400;

         record = UserModel(data['username'],data['password'],data['role'],data['access_to']);
         record.save_to_db();
         return {"message": "CREATED_SUCCESSFULLY"}, 201

#Class Mapping to route to fetch user details and deleting the user
class User(Resource):

        @classmethod
        @jwt_required()
        def get(cls, user_id: int):
            user = UserModel.find_by_id(user_id)
            if not user:
                return {"message": "USER_NOT_FOUND"}, 404

            return user_schema.dump(user), 200

        @classmethod
        @jwt_required()
        def put(cls,user_id:int):
            user = UserModel.find_by_id(user_id)
            if not user:
                return {"message": "USER_NOT_FOUND"}, 404
            else:
                data = request.get_json();
                UserModel.update_password(user_id,data["password"]);
                return {"message":"Password Changed"}

#Class Mapping To Route to edit roles
class EditRole(Resource):

    @classmethod
    def put(cls,user_id:int):
        try:
            check = UserModel.find_role_by_id(id=user_id);
            if(check['role']!="admin"):
                return {"msg":"Permission Denied!!"};
            else:
                data = request.get_json();
                UserModel.update_role(data['id'], data['role']);
                return {"msg": "Data Updated"}, 201

        except Exception as e:
            print(e);
            return {"msg": "Failed To Update"}, 400

#Class Mapping To Route to edit user names
class EditName(Resource):

    @classmethod
    def put(cls, user_id: int):
        try:
            check = UserModel.find_role_by_id(id=user_id);
            if (check['role'] != "admin"):
                return {"msg": "Permission Denied!!"};
            else:
                data = request.get_json();
                user = UserModel.find_by_id(data['id']);
                if not user:
                    return {"message": "USER_NOT_FOUND"}, 404

                UserModel.update_username(data['id'], data['username']);
                return {"msg": "Data Updated"}, 201

        except Exception as e:
            print(e);
            return {"msg": "Failed To Update"}, 400

#Class Mapping To Route to edit access
class EditAccessTo(Resource):

    @classmethod
    def put(cls, user_id: int):
        try:
            check = UserModel.find_role_by_id(id=user_id);
            if (check['role'] != "admin"):
                return {"msg": "Permission Denied!!"};
            else:
                data = request.get_json();
                user = UserModel.find_by_id(data['id']);
                if not user:
                    return {"message": "USER_NOT_FOUND"}, 404

                UserModel.update_access(data['id'], data['access_to']);
                return {"msg": "Data Updated"}, 201

        except Exception as e:
            print(e);
            return {"msg": "Failed To Update"}, 400

#Class Mapping to route to delete user
class RemoveUser(Resource):

    @classmethod
    def delete(cls, user_id: int):

        check = UserModel.find_role_by_id(id=user_id);
        if (check['role']!= "admin"):
            return {"msg": "Permission Denied!!"};
        else:
            data = request.get_json();
            user = UserModel.find_by_id(data['id'])
            if not user:
             return {"message": "USER_NOT_FOUND"}, 404
            user.delete_from_db()
            return {"message": "USER_DELETED"}, 200

#Class Mapping To route for user details validation
class UserLogin(Resource):

    @classmethod
    def post(cls):
        try:
            user_json = request.get_json();
            shiden = UserModel.find_role_by_username(user_json['username']);
            user_json['role'] = shiden['role'];
            user_json['access_to'] = shiden['access_to'];
            user_data = user_schema.load(user_json)

        except ValidationError as err:
            return err.messages, 400

        user = UserModel.find_by_username(user_data.username);
        if((user) and (user.password_is_valid(user_json['password']))):
         access_token = create_access_token(identity=user_data.username)
         return jsonify(access_token=access_token);

        else:
            return {"msg":"Please check username and password"}

#Class Mapping to route being utilied for listing of users
class ListUser(Resource):

    @classmethod
    @jwt_required()
    def get(cls):
        records = UserModel.list_all();
        user_list = [];
        for i in records:
            my_dict ={}
            my_dict['id']        = i.id
            my_dict['username']  = i.username;
            my_dict['role']      = i.role;
            my_dict['access_to'] = i.access_to;
            user_list.append(my_dict);

        return user_list;










