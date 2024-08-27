# factory-boy
import factory

# Models
from app.models.user import Block

# Factories
from .base_factory import BaseFactory
from .user_factory import UserFactory


class BlockFactory(BaseFactory):
    class Meta:
        model = Block

    blocker = factory.SubFactory(UserFactory)
    blocked = factory.SubFactory(UserFactory)
    created_at = factory.Faker('date_time')