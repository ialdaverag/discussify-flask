# flask_jwt_extended
from flask_jwt_extended import create_access_token

# utils
from app.utils.password import hash_password

# tests
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.user_factory import UserFactory


class TestLogOut(BaseTestCase):
    route = 'auth/logout'

    def test_log_out_successfully(self):
        # Create a user
        user = UserFactory(password=hash_password('Password1234.'))

        # Log in the user
        access_token = create_access_token(identity=user.id)

        # Log out the user
        response = self.client.post(
            self.route,
            headers={'Authorization': f'Bearer {access_token}'},
        )

        # assert response status code
        self.assertEqual(response.status_code, 200)

        # assert response data
        data = response.json

        # assert response message
        self.assertIn('message', data)

        # assert response message content
        self.assertEqual(data['message'], 'Successfully logged out.')
    