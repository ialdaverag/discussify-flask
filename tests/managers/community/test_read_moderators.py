# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Managers
from app.managers.community import ModerationManager

# Models
from app.models.community import CommunityModerator


class TestReadModerators(BaseTestCase):
    def test_read_moderators(self):
        # Number of moderators
        n = 5
        
        # Create a community
        community = CommunityFactory()

        # Create some moderators
        moderators = UserFactory.create_batch(n)

        # Make the moderators moderators of the community
        for moderator in moderators:
            CommunityModerator(community=community, user=moderator).save()

        # Read the moderators of the community
        moderators_to_read = ModerationManager.read_moderators_by_community(community)

        # Assert the number of moderators
        self.assertEqual(len(moderators_to_read), n)

        # Assert the moderators are the same
        self.assertEqual(moderators, moderators_to_read)

    def test_read_moderators_no_moderators(self):
        # Create a community
        community = CommunityFactory()

        # Read the moderators of the community
        moderators = ModerationManager.read_moderators_by_community(community)

        # Assert that there are no moderators
        self.assertEqual(len(moderators), 0)

        # Assert that the moderators are an empty list
        self.assertEqual(moderators, [])