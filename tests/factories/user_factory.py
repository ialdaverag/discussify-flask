# factory boy
import factory

# models
from app.models.user import User
from app.models.user import UserStats

# factories
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
