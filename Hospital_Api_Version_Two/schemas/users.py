from ma import ma
from models.users import UserModel

#Data Serialization and Deserialization using Marshmallow
class UserSchemas(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)


