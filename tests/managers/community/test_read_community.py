# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory

# Managers
from app.managers.community import CommunityManager

# Errors
from app.errors.errors import NotFoundError


class TestReadCommunity(BaseTestCase):
    def test_read_community(self):
        # Create a community
        community = CommunityFactory()

        # Read the community
        community_to_read = CommunityManager.read(community.name)

        # Check if the community is the same
        self.assertEqual(community, community_to_read)

    def test_read_community_not_found(self):
        # Attempt to read a community that does not exist
        with self.assertRaises(NotFoundError):
            CommunityManager.read('community')