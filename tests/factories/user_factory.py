# factory-boy
import factory

# Models
from app.models.user import User
from app.models.user import UserStats

# Factories
from .base_factory import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    is_verified = factory.Faker('boolean')
    created_at = factory.Faker('date_time')
    updated_at = factory.Faker('date_time')
    
    @factory.post_generation
    def set_stats(obj, create, extracted, **kwargs):
        if not create:
            return

        obj.stats.followers_count = 0
        obj.stats.following_count = 0
        obj.stats.communities_count = 0
        obj.stats.posts_count = 0
        obj.stats.comments_count = 0
        obj.stats.subscriptions_count = 0
        obj.stats.moderations_count = 0