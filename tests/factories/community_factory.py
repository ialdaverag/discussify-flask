# factory-boy
import factory

# Models
from app.models.community import Community
from app.models.community import CommunitySubscriber
from app.models.community import CommunityModerator

# Factories
from .base_factory import BaseFactory
from .user_factory import UserFactory


class CommunityFactory(BaseFactory):
    class Meta:
        model = Community

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker('word')
    about = factory.Faker('sentence')
    created_at = factory.Faker('date_time')
    updated_at = factory.Faker('date_time')

    # Relationship with User
    owner = factory.SubFactory(UserFactory)
    
    @factory.post_generation
    def fun(obj, create, extracted, **kwargs):
        if not create:
            return

        obj.stats.subscribers_count = 0
        obj.stats.posts_count = 0
        obj.stats.comments_count = 0
        obj.stats.moderators_count = 0
        obj.stats.banned_count = 0

        # # Add the owner to the list of subscribers
        # CommunitySubscriber(community=obj, user=obj.owner).save()

        # # Add the owner to the list of moderators
        # CommunityModerator(community=obj, user=obj.owner).save()