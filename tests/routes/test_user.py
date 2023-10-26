from ..base_test_case import BaseTestCase
from tests.utils.login import login

from app.models.user import User

from app.extensions.database import db
from app.utils.password import hash_password


class UserTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        user = User(username='test', email='test@example.com', password=hash_password('TestPassword123'))
        user2 = User(username='test2', email='test2@example.com', password=hash_password('TestPassword132'))
        user3 = User(username='test3', email='test3@example.com', password=hash_password('TestPassword132'))

        db.session.add_all([user, user2, user3])
        db.session.commit()

        self.user = user
        self.user2 = user2
        self.user3 = user3

class ReadUserTests(UserTests):
    def test_read_user(self):
        user = self.user.username

        route = f'/user/{user}'

        response = self.client.get(
            route
        )

        self.assertEqual(200, response.status_code)

    def test_read_non_existent_user(self):
        user = 'non_existent'

        route = f'/user/{user}'

        response = self.client.get(
            route
        )

        self.assertEqual(404, response.status_code)

class ReadUsersTests(UserTests):
    def test_read_user(self):
        route = '/user/'

        response = self.client.get(
            route
        )

        self.assertEqual(200, response.status_code)