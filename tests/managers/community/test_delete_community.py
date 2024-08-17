# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Models
from app.models.community import Community

# Managers
from app.managers.community import CommunityManager

# Errors
from app.errors.errors import OwnershipError


class TestDeleteCommunity(BaseTestCase):
    def test_delete_community(self):
        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        owner = community.owner

        # Get the community to delete
        community_to_delete = Community.get_by_id(community.id)

        # Delete the community
        CommunityManager.delete(owner, community_to_delete)

        # Assert that the community was deleted
        self.assertNotIn(community, owner.communities)

        # Assert that the owner's stats were updated
        communities_count = owner.stats.communities_count

        self.assertEqual(communities_count, 0)

    def test_delete_community_not_being_the_owner(self):
        # Create a user to be the creator of the community
        community = CommunityFactory()

        # Create another user
        user = UserFactory()

        # Attempt to delete the community
        with self.assertRaises(OwnershipError):
            CommunityManager.delete(user, community)