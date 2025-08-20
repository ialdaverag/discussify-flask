# Tests
from tests.base.base_pagination_test import BasePaginationTest

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunitySubscriber, CommunityModerator
from app.models.user import Block

# Utils
from tests.utils.tokens import get_access_token


class TestReadSubscribers(BasePaginationTest):
    route = '/community/{}/subscribers'
    route_with_args = '/community/{}/subscribers?page={}&per_page={}'

    def test_read_subscribers(self):
        # Number of subscribers
        n = 5

        # Create a community and subscribers
        community = CommunityFactory()
        self.create_community_subscribers(community, n)

        # Read the community subscribers
        response = self.GETRequest(self.route.format(community.name))

        # Assert standard pagination response for users
        self.assert_standard_pagination_response(response, expected_total=n, data_key='users')

    def test_read_subscribers_args(self):
        # Number of subscribers
        n = 5

        # Create a community and subscribers
        community = CommunityFactory()
        self.create_community_subscribers(community, n)

        # Read the community subscribers with pagination
        response = self.GETRequest(self.route_with_args.format(community.name, 1, 5))

        # Assert paginated response
        self.assert_paginated_response(
            response=response,
            page=1, 
            per_page=5, 
            expected_total=n, 
            data_key='users'
        )

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_as_user(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(self.route.format(community.name), token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_as_user_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_as_user_with_blocked(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(self.route.format(community.name), token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b)

    def test_read_subscribers_as_user_with_blocked_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b)

    def test_read_subscribers_as_user_with_blockers(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(self.route.format(community.name), token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b)

    def test_read_subscribers_as_user_with_blockers_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b)

    def test_read_subscribers_as_user_with_blocked_and_blockers(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Number of blockers
        c = 2

        # Make some subscribers block the user
        for subscriber in subscribers[-c:]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(self.route.format(community.name), token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

       # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n - b - c
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b - c)

    def test_read_subscribers_as_user_with_blocked_and_blockers_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Number of blockers
        c = 2

        # Make some subscribers block the user
        for subscriber in subscribers[-c:]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the user access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

       # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n - b - c
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n - b - c)

    def test_read_subscribers_as_moderator(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(self.route.format(community.name), token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_as_moderator_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_as_moderator_with_blocked(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(self.route.format(community.name), token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_as_moderator_with_blocked_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_as_moderator_with_blockers(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(self.route.format(community.name), token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_as_moderator_with_blockers_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_as_moderator_with_blocked_and_blockers(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Number of blockers
        c = 2

        # Make some subscribers block the user
        for subscriber in subscribers[-c:]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(self.route.format(community.name), token=access_token)

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=10,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_as_moderator_with_blocked_and_blockers_args(self):
        # Number of subscribers
        n = 5

        # Create multiple subscribers
        subscribers = UserFactory.create_batch(n)

        # Create a community
        community = CommunityFactory()

        # Append the subscribers to the community
        for subscriber in subscribers:
            CommunitySubscriber(community=community, user=subscriber).save()

        # Create a user
        user = UserFactory()

        # Make the user a moderator of the community
        CommunityModerator(community=community, user=user).save()

        # Number of subscribers to block
        b = 2

        # Block some subscribers
        for subscriber in subscribers[:b]:
            Block(blocker=user, blocked=subscriber).save()

        # Number of blockers
        c = 2

        # Make some subscribers block the user
        for subscriber in subscribers[-c:]:
            Block(blocker=subscriber, blocked=user).save()

        # Get the moderator access token
        access_token = get_access_token(user)

        # Read the community subscribers
        response = self.GETRequest(
            self.route_with_args.format(community.name, 1, 5),
            headers={'Authorization': f'Bearer {access_token}'}
        )

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=1,
            expected_per_page=5,
            expected_total=n
        )

        # Get the users
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, n)

    def test_read_subscribers_empty(self):
        # Create a community
        community = CommunityFactory()

        # Read the community subscribers
        response = self.GETRequest(self.route.format(community.name))

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=10,
            expected_total=0
        )

        # Get response data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, expected_count=0)

    def test_read_subscribers_empty_args(self):
        # Create a community
        community = CommunityFactory()

        # Read the community subscribers
        response = self.GETRequest(self.route_with_args.format(community.name, 1, 5))

        # Assert that the response status code is 200
        self.assertStatusCode(response, 200)

        # Get response pagination
        pagination = response.json

        # Assert pagination
        assert_pagination_structure(
            self,
            pagination,
            expected_page=1,
            expected_pages=0,
            expected_per_page=5,
            expected_total=0
        )

        # Get response data
        data = pagination['users']

        # Assert list
        assert_user_list(self, data, expected_count=0)

    def test_read_subscribers_nonexistent_community(self):
        # Try to get subscribers of a nonexistent community
        response = self.GETRequest(self.route.format('nonexistent'))

        # Assert the response status code
        self.assertStatusCode(response, 404)

        # Get response data
        data = response.json

        # Assert keys in the response data
        self.assertIn('message', data)

        # Assert the message
        self.assertEqual(data['message'], 'Community not found.')
