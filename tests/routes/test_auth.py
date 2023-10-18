from ..base_test_case import BaseTestCase

from app.models.user import User
from app.extensions.database import db
from app.utils.password import hash_password


class AuthTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        user = User(
            username='test', 
            email='test@example.com', 
            password=hash_password('TestPassword123')
        )
        db.session.add(user)
        db.session.commit()

        self.user = user


class SignUpTests(AuthTests):
    def test_sign_up(self):
        route = 'auth/signup'
        content_type='application/json'
        json = {
            'username': 'user',
            'email': 'user@example.com',
            'password': 'UserPassword123'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(201, response.status_code)

    def test_sign_up_no_username(self):
        route = 'auth/signup'
        content_type='application/json'
        json = {
            'email': 'user@example.com',
            'password': 'UserPassword123'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(400, response.status_code)

    def test_sign_up_no_email(self):
        route = 'auth/signup'
        content_type='application/json'
        json = {
            'username': 'user',
            'password': 'UserPassword123'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(400, response.status_code)

    def test_sign_up_no_password(self):
        route = 'auth/signup'
        content_type='application/json'
        json = {
            'username': 'user',
            'email': 'user@example.com',
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )
        
        self.assertEqual(400, response.status_code)

    def test_sign_up_incorrect_username(self):
        route = 'auth/signup'
        content_type='application/json'
        json = {
            'username': 'us',
            'email': 'user@example.com',
            'password': 'UserPassword123'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(400, response.status_code)

    def test_sign_up_incorrect_password(self):
        route = 'auth/signup'
        content_type='application/json'
        json = {
            'username': 'user',
            'email': 'user@example.com',
            'password': 'userpass'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(400, response.status_code)

    def test_sign_up_incorrect_email(self):
        route = 'auth/signup'
        content_type='application/json'
        json = {
            'username': 'user',
            'email': 'userexample.com',
            'password': 'UserPassword123'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(400, response.status_code)

    def test_sign_up_username_taken(self):
        route = 'auth/signup'
        content_type='application/json'
        json = {
            'username': 'test',
            'email': 'user@example.com',
            'password': 'UserPassword123'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(400, response.status_code)

    def test_sign_up_email_taken(self):
        route = 'auth/signup'
        content_type='application/json'
        json = {
            'username': 'user',
            'email': 'test@example.com',
            'password': 'UserPassword123'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(400, response.status_code)


class LogInTests(AuthTests):
    def test_log_in(self):
        username = self.user.username
        password = 'TestPassword123'

        route = 'auth/login'
        content_type='application/json'
        json = {
            'username': username,
            'password': password
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(200, response.status_code)

    def test_log_in_incorrect_username(self):
        username = 'test2'
        password = 'TestPassword123'

        route = 'auth/login'
        content_type='application/json'
        json = {
            'username': username,
            'password': password
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(401, response.status_code)

    def test_log_in_incorrect_password(self):
        username = 'test'
        password = 'TestPassword321'

        route = 'auth/login'
        content_type='application/json'
        json = {
            'username': username,
            'password': password
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json
        )

        self.assertEqual(401, response.status_code)
    