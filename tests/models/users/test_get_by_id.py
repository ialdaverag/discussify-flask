# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Models
from app.models.user import User

# Errors
from app.errors.errors import NotFoundError


class TestGetById(BaseTestCase):
    def test_get_by_id(self):
        # Create a user
        user = UserFactory()

        # Get the user by id
        user_by_id = User.get_by_id(user.id)

        # Assert that the user is the same as the user by id
        self.assertEqual(user, user_by_id)

    def test_get_by_id_nonexistent(self):
        # Attempt to get a user by id
        with self.assertRaises(NotFoundError):
            User.get_by_id(1)

