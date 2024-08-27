# factory-boy
import factory

# Models
from app.models.user import Follow

# Factories
from .base_factory import BaseFactory
from .user_factory import UserFactory


class FollowFactory(BaseFactory):
    class Meta:
        model = Follow

    follower = factory.SubFactory(UserFactory)
    followed = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time')
