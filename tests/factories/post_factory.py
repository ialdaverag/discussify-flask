# factory-boy
import factory

# Models
from app.models.user import Post

# Factories
from .base_factory import BaseFactory
from .user_factory import UserFactory
from .community_factory import CommunityFactory


class PostFactory(BaseFactory):
    class Meta:
        model = Post

    id = factory.Sequence(lambda n: n + 1)
    title = factory.Faker('sentence')
    content = factory.Faker('text')
    created_at = factory.Faker('date_time')
    updated_at = factory.Faker('date_time')

    # Relationship with User
    owner = factory.SubFactory(UserFactory)

    # Relationship with Community
    community = factory.SubFactory(CommunityFactory)

    @factory.post_generation
    def set_stats(obj, create, extracted, **kwargs):
        if not create:
            return

        obj.stats.comments_count = 0
        obj.stats.bookmarks_count = 0
        obj.stats.upvotes_count = 0
        obj.stats.downvotes_count = 0