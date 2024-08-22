# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import CommunityModerator


class TestGetModerationsByUser(BaseTestCase):
    def test_get_moderations_by_user(self):
        # Number of communities to create
        n = 5

        # Create a user
        user = UserFactory()

        # Create a list of communities
        communities = CommunityFactory.create_batch(n)

        # Make the user a moderator of the communities
        for community in communities:
            CommunityModerator(community=community, user=user).save()

        # Get the moderations
        moderations = CommunityModerator.get_moderations_by_user(user)

        # Assert that moderations is a list
        self.assertIsInstance(moderations, list)

        # Assert the number of moderations
        self.assertEqual(len(moderations), n)

    def test_get_moderations_by_user_empty(self):
        # Create a user
        user = UserFactory()

        # Get the moderations
        moderations = CommunityModerator.get_moderations_by_user(user)

        # Assert that moderations is a list
        self.assertIsInstance(moderations, list)

        # Assert that the moderations is an empty list
        self.assertEqual(moderations, [])