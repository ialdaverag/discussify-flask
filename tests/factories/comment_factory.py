# factory-boy
import factory

# Models
from app.models.user import Comment

# Factories
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

    @factory.post_generation
    def set_stats(obj, create, extracted, **kwargs):
        if not create:
            return
        
        obj.stats.bookmarks_count = 0
        obj.stats.upvotes_count = 0
        obj.stats.downvotes_count = 0
