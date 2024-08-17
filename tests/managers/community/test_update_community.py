# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Managers
from app.managers.community import CommunityManager

# Errors
from app.errors.errors import NameError
from app.errors.errors import OwnershipError


class TestUpdateCommunity(BaseTestCase):
    def test_update_community(self): 
        # Create a user to be the creator of the community
        community = CommunityFactory()

        # Get the owner of the community
        user = community.owner

        # Define community data
        data = {
            'name': 'Test Community',
            'about': 'This is a test community',
        }

        # Update the community
        community = CommunityManager.update(user, community, data)

        # Assert that the community data is correct
        self.assertEqual(community.name, data['name'])
        self.assertEqual(community.about, data['about'])


    def test_update_community_already_existent_name(self):
        # Create two communities
        community1 = CommunityFactory()
        community2 = CommunityFactory()

        # Get the owner of the community
        user = community2.owner

        # Define community data
        data = {
            'name': community1.name,
            'about': 'This is a test community',
        }

        # Attempt to create a community with the same name
        with self.assertRaises(NameError):
            CommunityManager.update(user, community2, data)
            
    def test_update_community_not_being_the_owner(self):
        # Create a user to be the creator of the community
        community = CommunityFactory()

        # Create another user
        user = UserFactory()

        # Define community data
        data = {
            'name': 'Test Community',
            'about': 'This is a test community',
        }

        # Attempt to update the community
        with self.assertRaises(OwnershipError):
            CommunityManager.update(user, community, data)