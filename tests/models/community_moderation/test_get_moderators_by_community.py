# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator


class TestGetModeratorsByCommunity(BaseTestCase):
    def test_get_moderators_by_community(self):
        # Number of users to create
        n = 5

        # Create a community
        community = CommunityFactory()

        # Create a list of users
        users = UserFactory.create_batch(n)

        # Make the users moderators of the community
        for user in users:
            CommunityModerator(community=community, user=user).save()

        # Get the moderators
        moderators = CommunityModerator.get_moderators_by_community(community)

        # Assert that moderators is a list
        self.assertIsInstance(moderators, list)

        # Assert the number of moderators
        self.assertEqual(len(moderators), n)

    def test_get_moderators_by_community_empty(self):
        # Create a community
        community = CommunityFactory()

        # Get the moderators
        moderators = CommunityModerator.get_moderators_by_community(community)

        # Assert that moderators is a list
        self.assertIsInstance(moderators, list)

        # Assert that the moderators is an empty list
        self.assertEqual(moderators, [])