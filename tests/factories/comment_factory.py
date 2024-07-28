# factory boy
import factory

# models
from app.models.user import Comment

# factories
from .base_factory import BaseFactory
from .user_factory import UserFactory
from .post_factory import PostFactory


class CommentFactory(BaseFactory):
    class Meta:
        model = Comment

    id = factory.Sequence(lambda n: n + 1)
    content = factory.Faker('text')
    created_at = factory.Faker('date_time')
    updated_at = factory.Faker('date_time')

    # Relationship with User
    owner = factory.SubFactory(UserFactory)

    # Relationship with Post
    post = factory.SubFactory(PostFactory)
