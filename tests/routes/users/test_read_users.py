# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestReadUsers(BaseTestCase):
    route = '/user/'

    def test_read_users(self):
        # create multiple users using batch
        users = UserFactory.create_batch(size=5)

        # get the users
        response = self.client.get(self.route)

        # assert response status code
        self.assertEqual(response.status_code, 200)

        # get response data
        data = response.json

        # assert the number of users
        self.assertEqual(len(data), len(users))

        # assert each user
        for i, user in enumerate(users):
            self.assertEqual(data[i]['id'], user.id)
            self.assertEqual(data[i]['username'], user.username)
            self.assertEqual(data[i]['email'], user.email)
            self.assertEqual(data[i]['created_at'], user.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
            self.assertEqual(data[i]['updated_at'], user.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_users_empty(self):
        # get the users
        response = self.client.get(self.route)

        # assert response status code
        self.assertEqual(response.status_code, 200)

        # get response data
        data = response.json

        # assert the user
        self.assertEqual(len(data), 0)