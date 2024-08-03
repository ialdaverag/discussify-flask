# factory boy
import factory

# models
from app.models.post import PostVote

# factories
from .base_factory import BaseFactory
from .user_factory import UserFactory
from .post_factory import PostFactory


class PostVoteFactory(BaseFactory):
    class Meta:
        model = PostVote

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    direction = factory.Iterator([1, -1])