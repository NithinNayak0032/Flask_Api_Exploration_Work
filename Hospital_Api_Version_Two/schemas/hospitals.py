from ma import ma
from models.hospitals import Hospital

#Data Serialization and Deserialization using Marshmallow
class HospitalSchemas(ma.ModelSchema):

    class Meta:
        model = Hospital
        load_only = ("hospital_name",)
        dumo_only = ("hospital_name",)

#Data Serialization and Deserialization using Marshmallow
class HospitalGroupSchemas(ma.ModelSchema):
    class Meta:
        model = Hospital
        load_only = ("hospital_group",)
        dump_only = ("hospital_group",)

