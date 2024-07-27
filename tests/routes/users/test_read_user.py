# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestReadUser(BaseTestCase):
    route = '/user/<string:username>'

    def test_read_user(self):
        # create a user
        user = UserFactory()

        # get the user
        response = self.client.get(f'/user/{user.username}')

        # assert response status code
        self.assertEqual(response.status_code, 200)

        # get response data
        data = response.json

        # assert the user
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['username'], user.username)
        self.assertEqual(data['email'], user.email)
        self.assertEqual(data['created_at'], user.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(data['updated_at'], user.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_user_not_found(self):
        # get the user
        response = self.client.get('/user/inexistent')

        # assert response status code
        self.assertEqual(response.status_code, 404)

        # get response data
        data = response.json

        # assert the error
        self.assertEqual(data['message'], 'User not found.')