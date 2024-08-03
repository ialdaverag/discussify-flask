# Factories
from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import OwnershipError
from app.errors.errors import NameError


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
        community = user.update_community(community, **data)

        # Assert that the community data is correct
        self.assertEqual(community.name, data['name'])
        self.assertEqual(community.about, data['about'])


    def test_update_community_already_existent_name(self):
        # Create two communities
        community1 = CommunityFactory()
        community2 = CommunityFactory()

        # Get the owner of the community
        user = community2.owner

        # Attempt to create a community with the same name
        with self.assertRaises(NameError):
            user.update_community(
                community2,
                name=community1.name, 
                about=community1.about
            )
            
    def test_update_community_not_being_the_owner(self):
        # Create a user to be the creator of the community
        community = CommunityFactory()

        # Create another user
        user = UserFactory()

        # Attempt to update the community
        with self.assertRaises(OwnershipError):
            user.update_community(
                community=community,
                name='Test Community', 
                about='This is a test community'
            )
