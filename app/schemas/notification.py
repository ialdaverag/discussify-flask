# Marshmallow
from marshmallow import Schema, fields

# Schemas
from app.schemas.user import UserSchema
from app.schemas.post import PostSchema
from app.schemas.comment import CommentSchema
from app.schemas.community import CommunitySchema


class NotificationSchema(Schema):
    class Meta:
        ordered = True
        
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    message = fields.String(required=True)
    type = fields.String(required=True)
    is_read = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    # User fields
    user_id = fields.Integer(required=True)
    sender_id = fields.Integer(allow_none=True)
    
    # Optional entity references
    post_id = fields.Integer(allow_none=True)
    comment_id = fields.Integer(allow_none=True)
    community_id = fields.Integer(allow_none=True)
    
    # Nested objects (optional for detailed responses)
    user = fields.Nested(UserSchema, dump_only=True, exclude=['password'])
    sender = fields.Nested(UserSchema, dump_only=True, exclude=['password'])
    post = fields.Nested(PostSchema, dump_only=True)
    comment = fields.Nested(CommentSchema, dump_only=True)
    community = fields.Nested(CommunitySchema, dump_only=True)


class NotificationCreateSchema(Schema):
    class Meta:
        ordered = True
        
    title = fields.String(required=True)
    message = fields.String(required=True)
    type = fields.String(required=True)
    user_id = fields.Integer(required=True)
    sender_id = fields.Integer(allow_none=True)
    post_id = fields.Integer(allow_none=True)
    comment_id = fields.Integer(allow_none=True)
    community_id = fields.Integer(allow_none=True)


class NotificationReadSchema(Schema):
    class Meta:
        ordered = True
        
    id = fields.Integer(required=True)
    is_read = fields.Boolean(required=True)