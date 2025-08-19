# tests
from tests.routes.test_route import TestRoute

# factories
from tests.factories.user_factory import UserFactory

# models
from app.models.user import Block

# utils
from tests.utils.tokens import get_access_token


class TestReadUser(TestRoute):
    route = '/user/{}'

    def test_read_user_anonymous(self):
        # Create a user
        user = UserFactory()

        # Get the user
        response = self.GETRequest(self.route.format(user.username))

        # Assert response status code
        self.assertStatusCode(response, 200)

        # Get response data
        data = response.json

        # Assert the response data
        self.assertIn('id', data)
        self.assertIn('username', data)
        self.assertIn('email', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert user data
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['username'], user.username)
        self.assertEqual(data['email'], user.email)
        self.assertEqual(data['created_at'], user.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(data['updated_at'], user.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_user(self):
        # Create a user
        user = UserFactory()

        access_token = get_access_token(user)

        # Get the user
        response = self.GETRequest(self.route.format(user.username), token=access_token)

        # Assert response status code
        self.assertStatusCode(response, 200)

        # Get response data
        data = response.json

        # Assert the response data
        self.assertIn('id', data)
        self.assertIn('username', data)
        self.assertIn('email', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert user data
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['username'], user.username)
        self.assertEqual(data['created_at'], user.created_at.strftime('%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(data['updated_at'], user.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

    def test_read_user_blocked_by_owner(self):
        # Create a user
        user = UserFactory()

        # Create a user
        owner = UserFactory()

        # Block the user
        Block(blocker=owner, blocked=user).save()

        # Get the access token
        access_token = get_access_token(owner)

        # Get the user
        response = self.GETRequest(self.route.format(user.username), token=access_token)

        # Assert response status code
        self.assertStatusCode(response, 400)

        # Get response data
        data = response.json

        # Assert the message
        self.assertEqual(data['message'], 'You cannot view this user.')    

    def test_read_user_owner_blocked_by_user(self):
        # Create a user
        user = UserFactory()

        # Create a user
        owner = UserFactory()

        # Block the owner
        Block(blocker=user, blocked=owner).save()

        # Get the access token
        access_token = get_access_token(user)

        # Get the user
        response = self.GETRequest(self.route.format(owner.username), token=access_token)

        # Assert response status code
        self.assertStatusCode(response, 400)

        # Get response data
        data = response.json

        # Assert the message
        self.assertEqual(data['message'], 'You cannot view this user.')
    
    def test_read_user_not_found(self):
        # Get the user
        response = self.GETRequest('/user/inexistent')

        # Assert response status code
        self.assertStatusCode(response, 404)

        # Get response data
        data = response.json

        # Assert the emessage
        self.assertEqual(data['message'], 'User not found.')