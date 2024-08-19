from app.models.community import Community
from app.models.community import CommunitySubscriber
from app.models.community import CommunityModerator
from app.models.community import CommunityBan

from app.errors.errors import NameError
from app.errors.errors import OwnershipError
from app.errors.errors import BanError
from app.errors.errors import SubscriptionError
from app.errors.errors import ModeratorError
from app.errors.errors import UnauthorizedError


class CommunityManager:
    @staticmethod
    def create(user, data):
        # Get the data
        name = data.get('name')

        # Raise an error if the name is not available
        if not Community.is_name_available(name):
            raise NameError('Name already taken.')

        # Create the community
        community = Community(**data, owner=user)
        community.save()

        # Add the creator as a subscriber
        CommunitySubscriber(user=user, community=community).save()

        # Add the creator as a moderator
        CommunityModerator(user=user, community=community).save()

        return community
    
    @staticmethod
    def read():
        pass

    @staticmethod
    def read_all():
        pass
    
    @staticmethod
    def update(user, community, data):
        if not community.belongs_to(user):
            raise OwnershipError('You are not the owner of this community.')
        
        name = data.get('name')
        about = data.get('about')

        if name and name != community.name:
            if not Community.is_name_available(name):
                raise NameError('Name already taken.')

            community.name = name

        if about:
            community.about = about

        community.save()

        return community

    def delete(user, community):
        if not community.belongs_to(user):
            raise OwnershipError('You are not the owner of this community.')
        
        community.delete()


class SubscriptionManager:
    @staticmethod
    def create(user, community):
        if user.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if user.is_subscribed_to(community):
            raise SubscriptionError('You are already subscribed to this community.')

        CommunitySubscriber(user=user, community=community).save()

    @staticmethod
    def read_subscriptions_by_user(user):
        subscriptions = CommunitySubscriber.get_subscriptions_by_user(user)

        return subscriptions

    @staticmethod
    def delete(user, community):
        if community.belongs_to(user):
            raise OwnershipError('You are the owner of this community and cannot unsubscribe.')
        
        if not user.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')
        
        if user.is_moderator_of(community):
            community.remove_moderator(user)

        CommunitySubscriber.get_by_user_and_community(user, community).delete()


class ModerationManager:
    @staticmethod
    def create(owner, community, user):
        if not community.belongs_to(owner):
            raise OwnershipError('You are not the owner of this community.')

        if user.is_banned_from(community):
            raise BanError('The user is banned from this community.')
        
        if not user.is_subscribed_to(community):
            raise SubscriptionError('The user is not subscribed to this community.')

        if user.is_moderator_of(community):
            raise ModeratorError('The user is already a moderator of this community.')

        CommunityModerator(user=user, community=community).save()

    @staticmethod
    def delete(owner, community, user):
        if not community.belongs_to(owner):
            raise OwnershipError('You are not the owner of this community.')
        
        if community.belongs_to(user):
            raise OwnershipError('You are the owner of this community and cannot unmod yourself.')
        
        if not user.is_moderator_of(community):
            raise ModeratorError('The user is not a moderator of this community.')
        
        CommunityModerator.get_by_user_and_community(user, community).delete()


class BanManager:
    @staticmethod
    def create(moderator, community, user):
        if not moderator.is_moderator_of(community):
            raise UnauthorizedError('You are not a moderator of this community.')
        
        if moderator is user:
            raise BanError('You cannot ban yourself.')
        
        if user.is_banned_from(community):
            raise BanError('The user is already banned from the community.')
        
        if user is community.owner:
            raise BanError('You cannot ban the owner of the community.')
        
        if user in community.moderators:
            community.remove_moderator(user)
        
        if not user.is_subscribed_to(community):
            raise SubscriptionError('The user is not subscribed to this community.')


    @staticmethod
    def delete(moderator, community, user):
        if not moderator.is_moderator_of(community):
            raise UnauthorizedError('You are not a moderator of this community.')
        
        if not user.is_banned_from(community):
            raise BanError('The user is not banned from the community.')
        
        CommunityBan.get_by_user_and_community(user, community).delete()

class TransferManager:
    @staticmethod
    def create(owner, community, user):
        if not community.belongs_to(owner):
            raise OwnershipError('You are not the owner of this community.')
        
        if user == owner:
            raise OwnershipError('You are already the owner of this community.')
        
        if user.is_banned_from(community):
            raise BanError('You cannot transfer the community to a banned user.')
        
        if not user.is_subscribed_to(community):
            raise SubscriptionError('The user is not subscribed to this community.')
        
        if not user.is_moderator_of(community):
            CommunityModerator(user=user, community=community).save()

        community.change_ownership_to(user)
