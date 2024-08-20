# factory-boy
import factory

# Models
from app.models.post import PostBookmark

# Factories
from .base_factory import BaseFactory
from .user_factory import UserFactory
from .post_factory import PostFactory


class PostBookmarkFactory(BaseFactory):
    class Meta:
        model = PostBookmark

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    created_at = factory.Faker('date_time')