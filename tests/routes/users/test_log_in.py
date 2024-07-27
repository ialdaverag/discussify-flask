# utils
from app.utils.password import hash_password

# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestLogIn(BaseTestCase):
    route = 'auth/login'

    def test_log_in_successfully(self):
        user = UserFactory(password=hash_password('Password1234.'))

        content_type='application/json'
        json = {
            'username': user.username,
            'password': 'Password1234.'
        }

        response = self.client.post(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertEqual(response.status_code, 200)

        # assert response data
        data = response.json

        # assert user data structure
        self.assertIn('access_token', data)

        # assert cookies
        cookies = response.headers.getlist('Set-Cookie')
        self.assertTrue(any('refresh_token' in cookie for cookie in cookies), 'Refresh token cookie not set.')

    def test_authentication_fails_without_username(self) -> None:
        UserFactory(password=hash_password('Password1234.'))

        content_type='application/json'
        json = {
            'password': 'Password1234.'
        }

        response = self.client.post(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # assert response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('username', errors)

        # assert errors values
        self.assertEqual(errors['username'], ['Missing data for required field.'])

    def test_authentication_fails_without_password(self) -> None:
        UserFactory(password=hash_password('Password1234.'))

        content_type='application/json'
        json = {
            'username': 'username'
        }

        response = self.client.post(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertEqual(response.status_code, 400)

        # assert response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('password', errors)

        # assert errors values
        self.assertEqual(errors['password'], ['Missing data for required field.'])

    def test_authentication_fails_with_inexistent_username(self) -> None:
        UserFactory(password=hash_password('Password1234.'))

        content_type='application/json'
        json = {
            'username': 'invalid_username',
            'password': 'Password1234.'
        }

        response = self.client.post(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertEqual(response.status_code, 404)

        # assert response data
        data = response.json

        # assert error message
        self.assertEqual(data['message'], 'User not found.')

    def test_authentication_fails_with_incorrect_password(self) -> None:
        user = UserFactory(password=hash_password('Password1234.'))

        content_type='application/json'
        json = {
            'username': user.username,
            'password': 'IncorrectPassword1234.'
        }

        response = self.client.post(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertEqual(response.status_code, 401)

        # assert response data
        data = response.json

        # assert error message
        self.assertEqual(data['message'], 'Incorrect password.')
