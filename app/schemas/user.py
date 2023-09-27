from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate
from marshmallow import post_load

from utils.password import hash_password


class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=20, error='username must be between 3 and 20 characters'),
            validate.Regexp(
                r'^[a-zA-Z0-9_]*$', 
                error='username must consist of letters, numbers, and underscores only')
        ]
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(min=8, max=40, error='password must be between 8 and 40 characters'),
            validate.Regexp(
                r'^(?=.*[A-Z!@#$%^&*()_+{}\[\]:;<>,.?~\/-])[A-Za-z0-9!@#$%^&*()_+{}\[\]:;<>,.?~\/-]*[0-9][A-Za-z0-9!@#$%^&*()_+{}\[\]:;<>,.?~\/-]*$',
                error='password must contain at least one uppercase letter or a special character, and at least one number'
            )
        ]
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


    @post_load
    def hash_password(self, data, **kwargs):
        if 'password' in data:
            data['password'] = hash_password(data['password'])

        return data
    

user_schema = UserSchema()
users_schema = UserSchema(many=True)