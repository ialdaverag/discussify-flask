# Factory-boy
import factory

# Models
from app.models.comment import CommentBookmark

# Factories
from .base_factory import BaseFactory
from .user_factory import UserFactory
from .comment_factory import CommentFactory


class CommentBookmarkFactory(BaseFactory):
    class Meta:
        model = CommentBookmark

    user = factory.SubFactory(UserFactory)
    comment = factory.SubFactory(CommentFactory)
    created_at = factory.Faker('date_time')