from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    fresh_jwt_required, 
    get_jwt_claims,
    jwt_required,
    jwt_optional,
    get_jwt_identity
)    

from models.owner import OwnerModel
from schemas.owner import OwnerSchema
from strings.messages import get_message

owner_schema = OwnerSchema()
owners_schema_not_logged_user = OwnerSchema(only=('id','name','surname'))
owners_schema_logged_user = OwnerSchema(exclude=('cars',))

class Owner(Resource):
    @classmethod
    @jwt_required
    def get(cls,id_):
        owner = OwnerModel.find_by_id(id_)
        if not owner:
            return {"message": get_message('owner_not_found')}, 404 # NOT FOUND
        
        return owner_schema.dump(owner), 200 # OK
    
    
class OwnerRegister(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        owner =  owner_schema.load(request.get_json())
       
        if OwnerModel.find_by_identity(owner.identity):
            return {"message": get_message('owner_already_exists')}, 400 # BAD REQUEST
        
        owner.save_to_db()

        return {"message": get_message('owner_created')}, 201 # CREATED


class Owners(Resource):
    @classmethod
    @jwt_optional
    def get(cls):
        identity = get_jwt_identity()
        owners = OwnerModel.find_all()
        
        if identity:
            return {'owners': owners_schema_logged_user.dump(owners, many=True)}, 200
        
        return {'ownners': owners_schema_not_logged_user.dump(owners,many=True),
                'message' : get_message('login_for_details')}, 200


