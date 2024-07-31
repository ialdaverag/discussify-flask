# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestReadUser(BaseTestCase):
    route = '/user/{}'

    def test_read_user(self):
        # Create a user
        user = UserFactory()

        # Get the user
        response = self.client.get(self.route.format(user.username))

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Get response data
        data = response.json

        # Assert user data
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['username'], user.username)
        self.assertEqual(data['email'], user.email)
        self.assertEqual(data['created_at'], user.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(data['updated_at'], user.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_user_not_found(self):
        # Get the user
        response = self.client.get('/user/inexistent')

        # Assert response status code
        self.assertEqual(response.status_code, 404)

        # Get response data
        data = response.json

        # Assert the error
        self.assertEqual(data['message'], 'User not found.')