# tests
from tests.routes.test_route import TestRoute

# factories
from tests.factories.user_factory import UserFactory


class SignUpTests(TestRoute):
    route = '/auth/signup'

    def test_sign_up(self) -> None:
        # Data to be sent
        json = {
            'username': 'user',
            'email': 'user@email.com',
            'password': 'Password1234.' 
        }

        # Sign Up
        response = self.POSTRequest(
            self.route,
            json=json,
        )

        # Assert the response status code
        self.assertStatusCode(response, 201)

        # Get the response data
        data = response.json

        # Assert the user data structure
        self.assertIn('id', data)
        self.assertIn('email', data)
        self.assertIn('username', data)
        self.assertIn('following', data)
        self.assertIn('follower', data)
        self.assertIn('stats', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert the user data values
        self.assertEqual(data['email'], 'user@email.com')
        self.assertEqual(data['username'], 'user')

        # Get the stats data from the response data
        stats_data = data['stats']

        # Assert the stats data structure
        self.assertIn('id', stats_data)
        self.assertIn('following_count', stats_data)
        self.assertIn('followers_count', stats_data)
        self.assertIn('communities_count', stats_data)
        self.assertIn('posts_count', stats_data)
        self.assertIn('comments_count', stats_data)
        self.assertIn('subscriptions_count', stats_data)
        self.assertIn('moderations_count', stats_data)

        # Assert the stats data values
        self.assertEqual(stats_data['following_count'], 0)
        self.assertEqual(stats_data['followers_count'], 0)
        self.assertEqual(stats_data['communities_count'], 0)
        self.assertEqual(stats_data['posts_count'], 0)
        self.assertEqual(stats_data['comments_count'], 0)
        self.assertEqual(stats_data['subscriptions_count'], 0)
        self.assertEqual(stats_data['moderations_count'], 0)

    def test_sign_up_missing_username(self) -> None:
        # Data to be sent
        json = {
            'email': 'user@email.com',
            'password': 'Password1234.',
        }

        # Sign Up
        response = self.POSTRequest(
            self.route,
            json=json,
        )

        # Assert the response status code
        self.assertStatusCode(response, 400)

        # Get the response data
        data = response.json

        # Assert errors is in data
        self.assertIn('errors', data)

        # Get errors from the response data
        errors = data['errors']

        # assert errors structure
        self.assertIn('username', errors)

        # assert errors values
        self.assertEqual(errors['username'], ['Missing data for required field.'])

    def test_sign_up_missing_email(self) -> None:
        content_type='application/json'
        json = {
            'username': 'user',
            'password': 'Password1234.',
        }

        response = self.POSTRequest(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertStatusCode(response, 400)

        # assert response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('email', errors)

        # assert errors values
        self.assertEqual(errors['email'], ['Missing data for required field.'])

    def test_sign_up_missing_password(self) -> None:
        content_type='application/json'
        json = {
            'user': {
                'username': 'user',
                'email': 'user@email.com'
            }
        }

        response = self.POSTRequest(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertStatusCode(response, 400)

        # assert response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('password', errors)

        # assert errors values
        self.assertEqual(errors['password'], ['Missing data for required field.'])

    def test_sign_up_invalid_username(self) -> None:
        content_type='application/json'
        json = {
            'username': 'us',
            'email': 'user@email.com',
            'password': 'Password1234.',
        }

        response = self.POSTRequest(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertStatusCode(response, 400)

        # assert response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('username', errors)

        # assert errors values
        self.assertEqual(errors['username'], ['Username must be between 3 and 20 characters.'])


    def test_sign_up_invalid_email(self) -> None:
        content_type='application/json'
        json = {
            'username': 'user',
            'email': 'useremail.com',
            'password': 'password',
        }

        response = self.POSTRequest(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertStatusCode(response, 400)

        # assert response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('email', errors)

        # assert errors values
        self.assertEqual(errors['email'], ["Not a valid email address."])

    def test_sign_up_fails_with_short_password(self) -> None:
        content_type='application/json'
        json = {
            'username': 'user',
            'email': 'user@email.com',
            'password': 'Pass123',
        }

        response = self.POSTRequest(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertStatusCode(response, 400)

        # assert response data
        data = response.json

        self.assertIn('errors', data)
        errors = data['errors']

        # assert errors structure
        self.assertIn('password', errors)

        # assert errors values
        self.assertEqual(errors['password'], ['Password must be between 8 and 40 characters.'])

    def test_sign_up_already_registered_username(self) -> None:
        user = UserFactory()

        content_type='application/json'
        json = {
            'username': user.username,
            'email': 'user@email.com',
            'password': 'Password1234.',
        }

        response = self.POSTRequest(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertStatusCode(response, 400)

        # assert response data
        data = response.json

        # assert response structure
        self.assertIn('message', data)

        # assert response data values
        self.assertEqual(data['message'], 'Username already taken.')

    def test_sign_up_fails_already_registered_email(self) -> None:
        user: UserFactory = UserFactory()

        content_type='application/json'
        json = {
            'username': 'user',
            'email': user.email,
            'password': 'Password1234.',
        }

        response = self.POSTRequest(
            self.route,
            content_type=content_type,
            json=json,
        )

        # assert response status code
        self.assertStatusCode(response, 400)

        # assert response data
        data = response.json

        # assert response structure
        self.assertIn('message', data)

        # assert response data values
        self.assertEqual(data['message'], 'Email already taken.')
