# factory-boy
import factory

# Models
from app.models.comment import CommentVote

# Factories
from .base_factory import BaseFactory
from .user_factory import UserFactory
from .comment_factory import CommentFactory

class CommentVoteFactory(BaseFactory):
    class Meta:
        model = CommentVote

    user = factory.SubFactory(UserFactory)
    comment = factory.SubFactory(CommentFactory)
    direction = factory.Iterator([1, -1]) 