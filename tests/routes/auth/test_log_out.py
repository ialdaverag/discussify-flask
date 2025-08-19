# flask_jwt_extended
from flask_jwt_extended import create_access_token

# utils
from app.utils.password import hash_password

# tests
from tests.routes.test_route import TestRoute

# factories
from tests.factories.user_factory import UserFactory


class TestLogOut(TestRoute):
    route = '/auth/logout'

    def test_log_out(self):
        # Create a user
        user = UserFactory(password=hash_password('Password1234.'))

        # Get the access token
        access_token = create_access_token(identity=user.id)

        # Log out
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
        )

        # Assert the response status code
        self.assertStatusCode(response, 200)

        # Assert the response data
        data = response.json

        # Assert the response message
        self.assertIn('message', data)

        # Assert the response message content
        self.assertEqual(data['message'], 'Successfully logged out.')
    