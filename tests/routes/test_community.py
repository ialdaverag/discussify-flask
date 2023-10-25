from ..base_test_case import BaseTestCase
from tests.utils.login import login

from app.models.user import User
from app.models.community import Community

from app.extensions.database import db
from app.utils.password import hash_password


class CommunityTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        user = User(username='test', email='test@example.com', password=hash_password('TestPassword123'))
        user2 = User(username='test2', email='test2@example.com', password=hash_password('TestPassword132'))
        user3 = User(username='test3', email='test3@example.com', password=hash_password('TestPassword132'))

        db.session.add_all([user, user2, user3])
        db.session.commit()
    
        community = user.create_community(name='TestCommunity', about='A community created for tests')
        community2 = user2.create_community(name='TestCommunity2',about='Another community created for tests')

        self.user = user
        self.user2 = user2
        self.user3 = user3
        self.community = community
        self.community2 = community2


class CreateCommunityTests(CommunityTests):
    def test_create_community(self):
        access_token = login(user=self.user)
        
        route = 'community/'
        content_type='application/json'
        json = {
            'name': 'NewCommunity',
            'about': 'A new community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(201, response.status_code)

    def test_create_community_no_name(self):
        access_token = login(user=self.user)
        
        route = 'community/'
        content_type='application/json'
        json = {
            'about': 'A new community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_create_community_name_taken(self):
        access_token = login(user=self.user)
        
        route = 'community/'
        content_type='application/json'
        json = {
            'name': 'TestCommunity',
            'about': 'A new community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_create_community_incorrect_name(self):
        access_token = login(user=self.user)
        
        route = 'community/'
        content_type='application/json'
        json = {
            'name': 'Test Community',
            'about': 'A new community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(400, response.status_code)


class ReadCommunityTests(CommunityTests):
    def test_read_community(self):
        community = self.community.name

        response = self.client.get(f'/community/{community}')

        self.assertEqual(200, response.status_code)

    def test_read_non_existent_community(self):
        community = 'non_existent'

        response = self.client.get(f'/community/{community}')

        self.assertEqual(404, response.status_code)


class ReadCommunitiesTests(CommunityTests):
    def test_read_communities(self):
        response = self.client.get('/community/')

        self.assertEqual(200, response.status_code)


class UpdateCommunityTests(CommunityTests):
    def test_update_community(self):
        access_token = login(user=self.user)
        community = self.community.name
        
        route = f'community/{community}'
        content_type='application/json'
        json = {
            'name': 'UpdatedCommunity',
            'about': 'A updated community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.patch(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(200, response.status_code)

    def test_update_non_existent_community(self):
        access_token = login(user=self.user)
        community = 'non_existent'
        
        route = f'community/{community}'
        content_type='application/json'
        json = {
            'name': 'UpdatedCommunity',
            'about': 'A updated community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.patch(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_update_community_incorrect_owner(self):
        access_token = login(user=self.user2)
        community = self.community.name

        route = f'community/{community}'
        content_type='application/json'
        json = {
            'name': 'UpdatedCommunity',
            'about': 'A updated community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.patch(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(403, response.status_code)

    def test_update_community_incorrect_name(self):
        access_token = login(user=self.user)
        community = self.community.name
        
        route = f'community/{community}'
        content_type='application/json'
        json = {
            'name': 'Updated Community',
            'about': 'A updated community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.patch(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(400, response.status_code)
    
    def test_update_community_name_taken(self):
        access_token = login(user=self.user2)
        
        route = f'community/{self.community2.name}'
        content_type='application/json'
        json = {
            'name': 'TestCommunity',
            'about': 'A new community for tests'
        }
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.patch(
            route, 
            content_type=content_type, 
            json=json,
            headers=headers
        )

        self.assertEqual(400, response.status_code)


class DeleteCommunityTests(CommunityTests):
    def test_delete_community(self):
        access_token = login(user=self.user)
        community = self.community.name
        
        route = f'community/{community}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.delete(
            route, 
            headers=headers
        )

        self.assertEqual(204, response.status_code)

    def test_delete_non_existent_community(self):
        access_token = login(user=self.user)
        community = 'non_existent'
        
        route = f'community/{community}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.delete(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_delete_community_incorrect_owner(self):
        access_token = login(user=self.user)
        community = self.community2.name

        route = f'community/{community}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.delete(
            route, 
            headers=headers
        )

        self.assertEqual(403, response.status_code)

class SubscribeToCommunityTests(CommunityTests):
    def setUp(self) -> None:
        super().setUp()

        community = self.community
        community.append_subscriber(self.user2)

        community2 = self.community2
        community2.append_banned(self.user3)

    def test_subscribe_to_community(self):
        access_token = login(user=self.user)
        community = self.community2.name
        
        route = f'community/{community}/subscribe'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(204, response.status_code)

    def test_subscribe_to_non_existent_community(self):
        access_token = login(user=self.user)
        community = 'non_existent'
        
        route = f'community/{community}/subscribe'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_subscribe_to_community_banned(self):
        access_token = login(user=self.user3)
        community = self.community2.name

        route = f'community/{community}/subscribe'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_subscribe_to_community_already_subscribed(self):
        access_token = login(user=self.user2)
        community = self.community.name

        route = f'community/{community}/subscribe'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)


class UbsubscribeToCommunityTests(CommunityTests):
    def setUp(self) -> None:
        super().setUp()

        community = self.community
        community.append_subscriber(self.user2)

    def test_unsubscribe_to_community(self):
        access_token = login(user=self.user2)
        community = self.community.name
        
        route = f'community/{community}/unsubscribe'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(204, response.status_code)

    def test_unsubscribe_to_community_not_subscribed(self):
        access_token = login(user=self.user)
        community = self.community2.name

        route = f'community/{community}/unsubscribe'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_unsusbcribe_to_non_existent_community(self):
        access_token = login(user=self.user)
        community = 'non_existent'
        
        route = f'community/{community}/unsubscribe'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_unsusbcribe_to_community_owner(self):
        access_token = login(user=self.user)
        community = self.community.name

        route = f'community/{community}/unsubscribe'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(403, response.status_code)


class ModTests(CommunityTests):
    def setUp(self) -> None:
        super().setUp()

        community = self.community
        community.append_subscriber(self.user2)
        community.append_moderator(self.user3)

        community2 = self.community2
        community2.append_banned(self.user3)

    def test_mod_to_community(self):
        access_token = login(user=self.user)
        community = self.community.name
        user_to_mod = self.user2.username

        route = f'community/{community}/mod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(204, response.status_code)

    def test_mod_to_non_existent_community(self):
        access_token = login(user=self.user)
        community = 'non_existent'
        user_to_mod = self.user2.username

        route = f'community/{community}/mod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_mod_not_mod(self):
        access_token = login(user=self.user)
        community = self.community2.name
        user_to_mod = self.user3.username

        route = f'community/{community}/mod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(403, response.status_code)

    def test_mod_to_non_existent_user(self):
        access_token = login(user=self.user)
        community = self.community.name
        user_to_mod = 'user5'

        route = f'community/{community}/mod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_mod_to_not_subscribed_user(self):
        access_token = login(user=self.user2)
        community = self.community2.name
        user_to_mod = self.user.username

        route = f'community/{community}/mod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_mod_to_banned_user(self):
        access_token = login(user=self.user2)
        community = self.community2.name
        user_to_mod = self.user3.username

        route = f'community/{community}/mod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_mod_to_community_already_mod(self):
        access_token = login(user=self.user)
        community = self.community.name
        user_to_mod = self.user3.username

        route = f'community/{community}/mod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)


class UnmodTests(CommunityTests):
    def setUp(self) -> None:
        super().setUp()

        community = self.community
        community.append_subscriber(self.user2)
        community.append_moderator(self.user3)

        community2 = self.community2
        community2.append_banned(self.user3)

    def test_unmod_to_community(self):
        access_token = login(user=self.user)
        community = self.community.name
        user_to_mod = self.user3.username

        route = f'community/{community}/unmod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(204, response.status_code)

    def test_unmod_to_non_existent_communtiy(self):
        access_token = login(user=self.user)
        community = 'non_existent'
        user_to_mod = self.user3.username

        route = f'community/{community}/unmod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_unmod_to_non_existent_user(self):
        access_token = login(user=self.user)
        community = self.community.name
        user_to_mod = 'user5'

        route = f'community/{community}/unmod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_unmod_to_community_owner(self):
        access_token = login(user=self.user)
        community = self.community.name
        user_to_mod = self.user.username

        route = f'community/{community}/unmod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(403, response.status_code)

    def test_unmod_to_community_already_moderator(self):
        access_token = login(user=self.user2)
        community = self.community2.name
        user_to_mod = self.user3.username

        route = f'community/{community}/unmod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_unmod_to_community_not_mod(self):
        access_token = login(user=self.user)
        community = self.community.name
        user_to_mod = self.user2.username

        route = f'community/{community}/unmod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_unmod_to_community_not_being_mod(self):
        access_token = login(user=self.user2)
        community = self.community.name
        user_to_mod = self.user3.username

        route = f'community/{community}/unmod/{user_to_mod}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(403, response.status_code)

    
class BanTests(CommunityTests):
    def setUp(self) -> None:
        super().setUp()

        community = self.community
        community.append_subscriber(self.user2)
        community.append_moderator(self.user3)

        community2 = self.community2
        community2.append_banned(self.user3)

    def test_ban_user_from_community(self):
        access_token = login(user=self.user)
        community = self.community.name
        user_to_ban = self.user2.username

        route = f'community/{community}/ban/{user_to_ban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(204, response.status_code)

    def test_ban_user_from_non_existent_community(self):
        access_token = login(user=self.user)
        community = 'non_existent'
        user_to_ban = self.user2.username

        route = f'community/{community}/ban/{user_to_ban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_ban_non_existent_user_from_community(self):
        access_token = login(user=self.user)
        community = self.community.name
        user_to_ban = 'non_existent'

        route = f'community/{community}/ban/{user_to_ban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_ban_user_from_community_not_being_mod(self):
        access_token = login(user=self.user2)
        community = self.community.name
        user_to_ban = self.user3.username

        route = f'community/{community}/ban/{user_to_ban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(401, response.status_code)

    def test_ban_user_already_banned_from_community(self):
        access_token = login(user=self.user2)
        community = self.community2.name
        user_to_ban = self.user3.username

        route = f'community/{community}/ban/{user_to_ban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_ban_user_not_subscribed_to_community(self):
        access_token = login(user=self.user2)
        community = self.community2.name
        user_to_ban = self.user.username

        route = f'community/{community}/ban/{user_to_ban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_ban_user_already_banned_from_community(self):
        access_token = login(user=self.user3)
        community = self.community.name
        user_to_ban = self.user.username

        route = f'community/{community}/ban/{user_to_ban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)

    def test_ban_user_themselves(self):
        access_token = login(user=self.user3)
        community = self.community.name
        user_to_ban = self.user3.username

        route = f'community/{community}/ban/{user_to_ban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)

class UnbanTests(CommunityTests):
    def setUp(self) -> None:
        super().setUp()

        community = self.community
        community.append_subscriber(self.user2)
        community.append_moderator(self.user3)

        community2 = self.community2
        community2.append_banned(self.user3)

    def test_unban_user_from_community(self):
        access_token = login(user=self.user2)
        community = self.community2.name
        user_to_unban = self.user3.username

        route = f'community/{community}/unban/{user_to_unban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(204, response.status_code)

    def test_unban_user_from_non_existent_community(self):
        access_token = login(user=self.user2)
        community = 'non_existent'
        user_to_unban = self.user3.username

        route = f'community/{community}/unban/{user_to_unban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_unban_non_existent_user_from_community(self):
        access_token = login(user=self.user2)
        community = self.community2.name
        user_to_unban = 'non_existent'

        route = f'community/{community}/unban/{user_to_unban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_unban_user_from_community_being_not_mod(self):
        access_token = login(user=self.user)
        community = self.community2.name
        user_to_unban = self.user3.username

        route = f'community/{community}/unban/{user_to_unban}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(401, response.status_code)


class TransferTests(CommunityTests):
    def setUp(self) -> None:
        super().setUp()

        community = self.community
        community.append_subscriber(self.user2)
        community.append_moderator(self.user3)

        community2 = self.community2
        community2.append_banned(self.user3)

    def test_transfer_community_to_user(self):
        access_token = login(user=self.user)
        community = self.community.name
        user = self.user2.username

        route = f'community/{community}/transfer/{user}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(204, response.status_code)

    def test_transfer_non_existent_community_to_user(self):
        access_token = login(user=self.user)
        community = 'non_existent'
        user = self.user2.username

        route = f'community/{community}/transfer/{user}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_transfer_community_to_non_existent_user(self):
        access_token = login(user=self.user)
        community = self.community.name
        user = 'non_existent'

        route = f'community/{community}/transfer/{user}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(404, response.status_code)

    def test_transfer_community_to_user_being_not_owner(self):
        access_token = login(user=self.user2)
        community = self.community.name
        user = self.user3.username

        route = f'community/{community}/transfer/{user}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(403, response.status_code)

    def test_transfer_community_to_user_not_subscribed(self):
        access_token = login(user=self.user2)
        community = self.community2.name
        user = self.user.username

        route = f'community/{community}/transfer/{user}'
        headers={
            'Authorization': f'Bearer {access_token}'
        }

        response = self.client.post(
            route, 
            headers=headers
        )

        self.assertEqual(400, response.status_code)


class ReadCommunitySubscribersTests(CommunityTests):
    def test_read_community_subscribers(self):
        community = self.community.name

        response = self.client.get(f'/community/{community}')

        self.assertEqual(200, response.status_code)

    def test_read_non_existent_community_subscribers(self):
        community = 'non_existent'

        response = self.client.get(f'/community/{community}')

        self.assertEqual(404, response.status_code)