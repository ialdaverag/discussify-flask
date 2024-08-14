# Tests
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Utils
from tests.utils.tokens import get_access_token


class TestUpdateCommunity(BaseTestCase):
    route = '/community/{}'

    def test_update_community(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        owner = community.owner

        # Get user access token
        access_token = get_access_token(owner)

        # Data to be sent
        json = {
            'name': 'Videogames',
            'about': 'Community for videogame lovers.',
        }

        # Update the community
        response = self.client.patch(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Get the response data
        data = response.json

        # Assert the response data
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('about', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)

        # Assert that the community data is correct
        self.assertEqual(data['name'], 'Videogames')
        self.assertEqual(data['about'], 'Community for videogame lovers.')

        # Assert that the community owner is the user
        self.assertEqual(data['owner']['id'], owner.id)

        # Get the stats data from the response
        stats_data = data['stats']

        # Assert the stats data
        self.assertIn('id', stats_data)
        self.assertIn('subscribers_count', stats_data)
        self.assertIn('moderators_count', stats_data)
        self.assertIn('banned_count', stats_data)
        self.assertIn('posts_count', stats_data)
        self.assertIn('comments_count', stats_data)

        # Assert the stats data values
        self.assertEqual(stats_data['banned_count'], 0)
        self.assertEqual(stats_data['posts_count'], 0)
        self.assertEqual(stats_data['comments_count'], 0)

    def test_update_community_nonexistent(self):
        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'name': 'Videogames',
            'about': 'Community for videogame lovers.',
        }

        # Update the community
        response = self.client.patch(
            self.route.format('inexistent'),
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 404)

        # Get the response data
        data = response.json

        # Assert the error
        self.assertEqual(data['message'], 'Community not found.')

    def test_update_community_not_being_owner(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        user = UserFactory()

        # Get user access token
        access_token = get_access_token(user)

        # Data to be sent
        json = {
            'name': 'Videogames',
            'about': 'Community for videogame lovers.',
        }

        # Update the community
        response = self.client.patch(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 403)

        # Get the response data
        data = response.json

        # Assert the error
        self.assertEqual(data['message'], 'You are not the owner of this community.')

    def test_update_community_invalid_name(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        owner = community.owner

        # Get the user access token
        access_token = get_access_token(owner)

        # Data to be sent
        json = {
            'name': 'Invalid Name',
            'about': 'Community for videogame lovers.',
        }

        # Update the community
        response = self.client.patch(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('errors', data)

        # Get errors from the response data
        errors = data['errors']

        # Assert errors structure
        self.assertIn('name', errors)

        # Assert errors values
        self.assertEqual(errors['name'], ['Name must consist of letters, numbers, and underscores only.'])

    def test_update_community_invalid_about(self):
        # Create a community
        community = CommunityFactory()

        # Create a user
        owner = community.owner

        # Get the user access token
        access_token = get_access_token(owner)

        # Data to be sent
        json = {
            'name': 'Videogames',
            'about': 'Community for videogame lovers.' * 100,
        }

        # Update the community
        response = self.client.patch(
            self.route.format(community.name),
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('errors', data)

        # Get errors from the response data
        errors = data['errors']

        # Assert errors structure
        self.assertIn('about', errors)

        # Assert errors values
        self.assertEqual(errors['about'], ['Maximum 1000 characters.'])
        

    def test_update_community_already_existent_name(self):
        # Create a community
        community1 = CommunityFactory()

        # Create another community
        community2 = CommunityFactory()

        # Get the owner of the second community
        owner = community2.owner

        # Get the user access token
        access_token = get_access_token(owner)

        # Data to be sent
        json = {
            'name': community1.name,
            'about': 'Random description.',
        }

        # Update the community
        response = self.client.patch(
            self.route.format(community2.name),
            headers={'Authorization': f'Bearer {access_token}'},
            json=json
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 400)

        # Get the response data
        data = response.json

        # Assert the error
        self.assertEqual(data['message'], 'Name already taken.')