# factory boy
import factory

# models
from app.models.comment import CommentVote

# factories
from .base_factory import BaseFactory
from .user_factory import UserFactory
from .comment_factory import CommentFactory

class CommentVoteFactory(BaseFactory):
    class Meta:
        model = CommentVote

    user = factory.SubFactory(UserFactory)
    comment = factory.SubFactory(CommentFactory)
    direction = factory.Iterator([1, -1]) 