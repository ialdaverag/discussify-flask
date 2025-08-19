# utils
from app.utils.password import hash_password

# tests
from tests.routes.test_route import TestRoute

# factories
from tests.factories.user_factory import UserFactory


class TestLogIn(TestRoute):
    route = '/auth/login'

    def test_log_in(self):
        user = UserFactory(password=hash_password('Password1234.'))

        # Data to be sent
        json = {
            'username': user.username,
            'password': 'Password1234.'
        }

        # Log in
        response = self.client.post(
            self.route,
            json=json,
        )

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Get the data
        data = response.json

        # Assert access token is in data
        self.assertIn('access_token', data)

        # Assert cookies
        cookies = response.headers.getlist('Set-Cookie')
        self.assertTrue(any('refresh_token' in cookie for cookie in cookies), 'Refresh token cookie not set.')

    def test_log_in_missing_username(self) -> None:
        # Create a user
        UserFactory(password=hash_password('Password1234.'))

        # Data to be sent
        json = {
            'password': 'Password1234.'
        }

        # Log in
        response = self.client.post(
            self.route,
            json=json,
        )

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Assert the response data
        data = response.json

        # Assert errors is in data
        self.assertIn('errors', data)

        # Get errors from the response data
        errors = data['errors']

        # Assert the errors structure
        self.assertIn('username', errors)

        # Assert the errors values
        self.assertEqual(errors['username'], ['Missing data for required field.'])

    def test_log_in_missing_password(self) -> None:
        # Create a user
        UserFactory(password=hash_password('Password1234.'))

        # Data to be sent
        json = {
            'username': 'username'
        }

        # Log in
        response = self.client.post(
            self.route,
            json=json,
        )

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Assert the response data
        data = response.json

        # Assert errors is in data
        self.assertIn('errors', data)

        # Get errors from the response data
        errors = data['errors']

        # Assert the errors structure
        self.assertIn('password', errors)

        # Assert the errors values
        self.assertEqual(errors['password'], ['Missing data for required field.'])

    def test_log_in_wrong_username(self) -> None:
        # Create a user
        UserFactory(password=hash_password('Password1234.'))

        # Data to be sent
        json = {
            'username': 'invalid_username',
            'password': 'Password1234.'
        }

        # Log in
        response = self.client.post(
            self.route,
            json=json,
        )

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Assert the response data
        data = response.json

        # Assert the error message
        self.assertEqual(data['message'], 'User not found.')

    def test_log_in_wrong_password(self) -> None:
        # Create a user
        user = UserFactory(password=hash_password('Password1234.'))

        # Data to be sent
        json = {
            'username': user.username,
            'password': 'IncorrectPassword1234.'
        }

        # Log in
        response = self.client.post(
            self.route,
            json=json,
        )

        # Assert the response status code
        self.assertStatusCode(response, 401)

        # Assert the response data
        data = response.json

        # Assert the error message
        self.assertEqual(data['message'], 'Incorrect password.')
