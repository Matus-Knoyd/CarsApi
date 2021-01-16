from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from db import db
from ma import ma
from strings.messages import get_message
from blacklist import BLACKLIST
from resources.user import (
    UserRegister,
    UserLogin,
    User,
    Users,
    UserLogout,
    TokenRefresh,
)
from resources.owner import (
    Owner,
    Owners,
    OwnerRegister
)

from resources.car import (
    Car, 
    CarRegister, 
    Cars
)

from resources.association import (
    OwnersFinder,
    CarsFinder,
    AssociationAdder
)   

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['SECRET_KEY'] = 'matus'

api = Api(app)
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True  
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] 

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def hanndle_marrshmallow_validationn(err):
    return jsonify(err.messages), 400

@jwt.user_claims_loader
def add_claims_to_jwt(identity):  # identity = user.email
    if 'admin' in identity:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': get_message('token_expired'),
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error): 
    return jsonify({
        'message': get_message('invalid_token'),
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": get_message('authorization_required'),
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": get_message('fresh_token_requiredS'),
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": get_message('token_revoked'),
        'error': 'token_revoked'
    }), 401

api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(User, "/user/<string:email>")
api.add_resource(UserLogout, '/logout')
api.add_resource(Users, "/users")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(Owner, "/owner/<int:id_>")
api.add_resource(CarsFinder, "/owner/<int:id_>/cars")
api.add_resource(Owners, "/owners")
api.add_resource(OwnerRegister,"/owner/register")
api.add_resource(Car, "/car/<int:id_>")
api.add_resource(OwnersFinder, "/car/<int:id_>/owners")
api.add_resource(CarRegister, "/car/register")
api.add_resource(Cars, "/cars")
api.add_resource(AssociationAdder,"/association")


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)