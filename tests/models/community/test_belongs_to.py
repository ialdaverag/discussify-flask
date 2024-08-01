# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory


class TestBelongsTo(BaseTestCase):
    def test_belongs_to_true(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory(owner=user)

        # Assert that the user belongs to the community
        self.assertTrue(community.belongs_to(user))

    def test_belongs_to_false(self):
        # Create a user
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Assert that the user does not belong to the community
        self.assertFalse(community.belongs_to(user))
