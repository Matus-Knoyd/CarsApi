from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required,
    get_jwt_claims,jwt_optional,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)

from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from strings.messages import get_message

user_schema = UserSchema(exclude=('password',))
user_schema_admin = UserSchema()

class User(Resource):
    @classmethod
    @jwt_optional
    def get(cls, email):
        claims = get_jwt_claims()
        user = UserModel.find_by_email(email)
        
        if not user:
            return {"message": get_message('user_not_found')}, 404 # NOT FOUND
        if user and claims and claims['is_admin']:
            return user_schema_admin.dump(user), 200 # OK
        
        return user_schema.dump(user), 200 # OK
    
    @classmethod
    @jwt_required
    def delete(cls,email):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": get_message('admin_required')}, 401 # UNAUTHORIZED

        user = UserModel.find_by_email(email)
        if not user:
            return {"message": get_message('user_not_found')}, 404 # NOT FOUND
        
        user.delete_from_db()
        return {"message": get_message('user_deleted')}, 200 # OK

        
class Users(Resource):
    @classmethod
    @jwt_optional
    def get(cls):
        claims = get_jwt_claims()
        if claims and claims['is_admin']:
            return {'users': user_schema_admin.dump(UserModel.find_all(), many=True)}, 200 # OK
        
        return {'users': user_schema.dump(UserModel.find_all(), many=True)}, 200 # OK


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema_admin.load(request.get_json()) # tiez je to user
        user = UserModel.find_by_email(user_data.email)

        if user and safe_str_cmp(user.password, user_data.password):
            access_token = create_access_token(identity=user.email, fresh=True)
            refresh_token = create_refresh_token(user.email)
            
            return {"access_token": access_token, "refresh_token": refresh_token}, 200 #200 OK

        return {"message": get_message('invalid_credentials')}, 401 #UNAUTHORIZED

class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema_admin.load(request.get_json())

        if UserModel.find_by_email(user.email):
            return {"message": get_message('user_username_exists')}, 400 # BAD REQUEST
        
        user.save_to_db()

        return {"message": get_message('user_created')}, 201 # CREATED

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": get_message('logged_out')}, 200