# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import Community

# Errors
from app.errors.errors import NotFoundError


class TestGetById(BaseTestCase):
    def test_get_by_id(self):
        # Create a community
        community_to_find = CommunityFactory()

        # Get the community by id
        community = Community.get_by_id(community_to_find.id)

        # Assert that the community is the one we are looking for
        self.assertEqual(community.id, community_to_find.id)

    def test_get_by_id__not_found(self):
        # Attempt to get a community that does not exist
        with self.assertRaises(NotFoundError):
            Community.get_by_id(1)
