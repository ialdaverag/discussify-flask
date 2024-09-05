# Models
from app.models.user import User
from app.models.user import Follow
from app.models.user import Block

# Errors
from app.errors.errors import NameError
from app.errors.errors import FollowError
from app.errors.errors import BlockError

# Utils
from app.utils.password import hash_password

class UserManager:
    @staticmethod
    def create(data):
        username = data.get('username')

        if not User.is_username_available(username):
            raise NameError('Username already taken.')
        
        email = data.get('email')

        if not User.is_email_available(email):
            raise NameError('Email already taken.')
        
        password = data.get('password')
        
        user = User(username=username, email=email, password=hash_password(password))
        user.save()

        return user

    @staticmethod
    def read(user, target):
        if user and (user.is_blocking(target) or user.is_blocked_by(target)):
            raise BlockError('You cannot view this user.')

        return target

    @staticmethod
    def read_all(user, args):
        paginated_users = User.get_all(args)

        return paginated_users


class FollowManager:
    @staticmethod
    def create(user, target):    
        if user.is_blocking(target) or user.is_blocked_by(target):
            raise BlockError('You cannot follow this user.')

        if user.is_following(target):
            raise FollowError('You are already following this user.')
        
        if target == user:
            raise FollowError('You cannot follow yourself.')
        
        Follow(
            follower=user, 
            followed=target
        ).save()

    @staticmethod
    def read_followed(user, args):
        paginated_following = Follow.get_followed(user, args)
        
        return paginated_following
    
    @staticmethod
    def read_followers(user, args):
        paginated_followers = Follow.get_followers(user, args)
        
        return paginated_followers

    @staticmethod
    def delete(user, target):
        if target == user:
            raise FollowError('You cannot unfollow yourself.')
        
        if not user.is_following(target):
            raise FollowError('You are not following this user.')
        
        Follow.get_by_follower_and_followed(
            follower=user, 
            followed=target
        ).delete()


class BlockManager:
    @staticmethod
    def create(user, target):
        if target == user:
            raise BlockError('You cannot block yourself.')
        
        if user.is_blocking(target):
            raise BlockError('You are already blocking this user.')
        
        if user.is_following(target):
            Follow.get_by_follower_and_followed(
                follower=user, 
                followed=target
            ).delete()

        if user.is_followed_by(target):
            Follow.get_by_follower_and_followed(
                follower=target, 
                followed=user
            ).delete()
        
        Block(
            blocker=user, 
            blocked=target
        ).save()

    @staticmethod
    def read_blocked(user, args):
        paginated_blocked = Block.get_blocked_with_args(user, args)
        
        return paginated_blocked

    @staticmethod
    def delete(user, target):
        if not user.is_blocking(target):
            raise BlockError('You are not blocking this user.')
        
        if target == user:
            raise BlockError('You cannot unblock yourself.')
        
        Block.get_by_blocker_and_blocked(
            blocker=user, 
            blocked=target
        ).delete()
