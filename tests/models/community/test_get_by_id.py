#  base
from tests.base.base_test_case import BaseTestCase

# factories
from tests.factories.community_factory import CommunityFactory

# models
from app.models.community import Community

# errors
from app.errors.errors import NotFoundError


class TestGetById(BaseTestCase):
    def test_get_by_id(self):
        community_to_find = CommunityFactory()

        community = Community.get_by_id(community_to_find.id)

        self.assertEqual(community.id, community_to_find.id)

    def test_get_by_id__not_found(self):
        with self.assertRaises(NotFoundError):
            Community.get_by_id(1)