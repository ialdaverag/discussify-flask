# FBase
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import OwnershipError

# Models
from app.models.community import Community


class TestDeleteCommunity(BaseTestCase):
    def test_delete_community(self):
        # Create a community
        community = CommunityFactory()

        # Get the owner of the community
        user = community.owner

        # Get the community to delete
        community_to_delete = Community.get_by_id(community.id)

        # Delete the community
        user.delete_community(community_to_delete)

        # Assert that the community was deleted
        self.assertNotIn(community, user.communities)

        # Assert that the community was deleted from the database
        self.assertNotIn(community, user.subscriptions)

        # Assert that the community was deleted from the database
        self.assertNotIn(community, user.moderations)

    def test_delete_community_not_being_the_owner(self):
        # Create a user to be the creator of the community
        community = CommunityFactory()

        # Create another user
        user = UserFactory()

        # Attempt to delete the community
        with self.assertRaises(OwnershipError):
            user.delete_community(community)