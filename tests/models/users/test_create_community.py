# Base
from tests.base.base_test_case import BaseTestCase

# Factories
from tests.factories.user_factory import UserFactory
from tests.factories.community_factory import CommunityFactory

# Errors
from app.errors.errors import NameError


class TestCreateCommunity(BaseTestCase):
    def test_create_community(self): 
        # Create a user to be the creator of the community
        user = UserFactory()

        # Define community data
        data = {
            'name': 'Test Community',
            'about': 'This is a test community',
        }

        # Create the community
        community = user.create_community(**data)

        # Assert that the community was created
        self.assertIsNotNone(community)

        # Assert that the community data is correct
        self.assertEqual(community.name, data['name'])
        self.assertEqual(community.about, data['about'])

        # Assert that the community owner is the user
        self.assertEqual(community.owner, user)

        # Assert that the community is in the user's communities
        self.assertIn(community, user.communities)

        # Assert that the user's stats were updated
        self.assertEqual(user.stats.communities_count, 1)

        # Assert that the community's stats were updated
        self.assertEqual(community.stats.subscribers_count, 1)
        self.assertEqual(community.stats.moderators_count, 1)

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
