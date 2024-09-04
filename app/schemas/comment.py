# Marshmallow
from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate

# Schemas
from app.schemas.user import UserSchema
from app.schemas.post import PostSchema
from app.schemas.pagination import PaginationSchema


class CommentPaginationRequestSchema(Schema):
    class Meta:
        ordered = True

    page = fields.Integer(load_default=1)
    per_page = fields.Integer(load_default=10)


class CommentStatsSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    bookmarks_count = fields.Integer()
    upvotes_count = fields.Integer()
    downvotes_count = fields.Integer()


class CommentSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    content = fields.Str(
        required=True,
        validate=validate.Length(
            min=1, 
            error='Content must contain at least 1 character.'
        )
    )
    post_id = fields.Integer(required=True, load_only=True)  # Cambiar a required=False
    comment_id = fields.Integer(load_only=True)
    owner = fields.Nested(UserSchema, dump_only=True)
    post = fields.Nested(PostSchema, dump_only=True)
    bookmarked = fields.Boolean(dump_only=True)
    upvoted = fields.Boolean(dump_only=True)
    downvoted = fields.Boolean(dump_only=True)
    replies = fields.List(fields.Nested(lambda: CommentSchema()))
    stats = fields.Nested(CommentStatsSchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CommentPaginationResponseSchema(PaginationSchema):
    class Meta:
        ordered = True

    comments = fields.Nested(CommentSchema, attribute="items", many=True)


comment_pagination_request_schema = CommentPaginationRequestSchema()
comment_pagination_response_schema = CommentPaginationResponseSchema()
comment_schema = CommentSchema()
comment_update_schema = CommentSchema(only=('content',))
comments_schema = CommentSchema(many=True)
