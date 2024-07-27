from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate
from marshmallow import post_load

from app.utils.password import hash_password


class UserStatsSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    following_count = fields.Integer()
    followers_count = fields.Integer()
    communities_count = fields.Integer()
    posts_count = fields.Integer()
    comments_count = fields.Integer()
    subscriptions_count = fields.Integer()
    moderations_count = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=20, error='Username must be between 3 and 20 characters.'),
            validate.Regexp(
                r'^[a-zA-Z0-9_]*$', 
                error='Username must consist of letters, numbers, and underscores only.')
        ],
        #error_messages={'required': 'Please provide a name.'}
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(min=8, max=40, error='Password must be between 8 and 40 characters.'),
            validate.Regexp(
                r'^(?=.*[A-Z!@#$%^&*()_+{}\[\]:;<>,.?~\/-])[A-Za-z0-9!@#$%^&*()_+{}\[\]:;<>,.?~\/-]*[0-9][A-Za-z0-9!@#$%^&*()_+{}\[\]:;<>,.?~\/-]*$',
                error='Password must contain at least one uppercase letter or a special character, and at least one number.'
            )
        ]
    )
    following = fields.Boolean(dump_only=True)
    follower = fields.Boolean(dump_only=True)
    stats = fields.Nested(UserStatsSchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def hash_password(self, data, **kwargs):
        if 'password' in data:
            data['password'] = hash_password(data['password'])

        return data
    

me_schema = UserSchema(exclude=('email',))
user_schema = UserSchema()
users_schema = UserSchema(many=True)