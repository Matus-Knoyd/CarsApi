from ma import ma
from db import db
from models.user import UserModel
from marshmallow import ValidationError

# vlastna validacia (nemusi byt)
def validate_gmail(email):
    if 'gmail' not in email:
        raise ValidationError("Email must contains 'gmail'.")

# vlastna validacia (nemusi byt)
def validate_email(email):
    if '@' not in email:
        raise ValidationError("Email must contains '@'.")

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        dump_only = ('id',)
    
    email = ma.auto_field(validate=[validate_gmail,validate_email])