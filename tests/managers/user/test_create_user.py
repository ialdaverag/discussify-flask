# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory

# Managers
from app.managers.user import UserManager

# Errors
from app.errors.errors import NameError


class TestCreateUser(BaseTestCase):
    def test_create_user(self):
        # Define user data
        data = {
            'username': 'test_user',
            'email': 'user@email.com',
            'password': 'password',
        }

        # Create the user
        user = UserManager.create(data)

        # Assert that the user was created
        self.assertIsNotNone(user)

        # Assert that the user data is correct
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.email, data['email'])


    def test_create_user_already_existent_username(self):
        # Create a user
        user = UserFactory()

        # Define user data
        data = {
            'username': user.username,
            'email': 'user@email.com',
            'password': 'password',
        }

        # Try to create the user
        with self.assertRaises(NameError):
            UserManager.create(data)

    def test_create_user_already_existent_email(self):
        # Create a user
        user = UserFactory()

        # Define user data
        data = {
            'username': 'test_user',
            'email': user.email,
            'password': 'password',
        }

        # Try to create the user
        with self.assertRaises(NameError):
            UserManager.create(data)