# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import Community

# Errors
from app.errors.errors import NotFoundError


class TestGetById(BaseTestCase):
    def test_get_by_name(self):
        # Create a community
        community = CommunityFactory()

        # Get the community by name
        community_to_find = Community.get_by_name(community.name)

        # Assert that the community is the one we are looking for
        self.assertEqual(community_to_find.name, community.name)

    def test_get_by_id__not_found(self):
        # Attempt to get a community that does not exist
        with self.assertRaises(NotFoundError):
            Community.get_by_name('not_found')