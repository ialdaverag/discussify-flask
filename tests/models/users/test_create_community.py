# Factories
from tests.base.base_test_case import BaseTestCase
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import NameError


class TestCreateCommunity(BaseTestCase):
    def test_create_community(self): 
        # Create a user to be the creator of the community
        user = UserFactory()

        # Define community data
        community_data = {
            'name': 'Test Community',
            'about': 'This is a test community',
        }

        # Create the community
        community = user.create_community(**community_data)

        # Check that the community was created
        self.assertIsNotNone(community)

        # Check that the community data is correct
        self.assertEqual(community.name, community_data['name'])
        self.assertEqual(community.about, community_data['about'])

        # Check that the community owner is the user
        self.assertEqual(community.owner, user)

        # Check that the community is in the user's communities
        self.assertIn(community, user.communities)

        # Check that the community is in the user's subscribed communities
        self.assertIn(community, user.subscriptions)

        # Check that the community is in the user's moderated communities
        self.assertIn(community, user.moderations)

    def test_create_community_already_existent_name(self):
        # Create a user to be the creator of the community
        user = UserFactory()

        # Create a community
        community = CommunityFactory()

        # Attempt to create a community with the same name
        with self.assertRaises(NameError):
            user.create_community(
                name=community.name, 
                about=community.about
        )
