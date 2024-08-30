# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import Community


class TestIsNameAvailable(BaseTestCase):
    def test_is_name_available_true(self):
        # Create a name
        name = 'random'

        # Check if the name is available
        is_name_available = Community.is_name_available(name)

        # Assert that the name is not available
        self.assertTrue(is_name_available)

    def test_is_name_available_false(self):
        # Create a community
        community = CommunityFactory()

        # Get the name of the community
        name = community.name

        # Check if the name is available
        is_name_available = Community.is_name_available(name)

        # Assert that the name is available
        self.assertFalse(is_name_available)
