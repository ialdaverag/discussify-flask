from app.models.user import User
from app.models.user import Follow

from app.errors.errors import NameError
from app.errors.errors import FollowError

from app.utils.password import hash_password

class UserManager:
    @staticmethod
    def create(data):
        # Get the username form the data
        username = data.get('username')

        # Check if the username is already taken
        if not User.is_username_available(username):
            raise NameError('Username already taken.')
        
        # Get the email from the data
        email = data.get('email')

        # Check if the email is already taken
        if not User.is_email_available(email):
            raise NameError('Email already taken.')
        
        # Get the password from the data
        password = data.get('password')
        
        # Create a new user
        user = User(username=username, email=email, password=hash_password(password))
        user.save()

        return user

    @staticmethod
    def read(username):
        user = User.get_by_username(username)

        return user
        

    @staticmethod
    def read_all():
        users = User.get_all()

        return users


class FollowManager:
    @staticmethod
    def create(user, target):
        if target == user:
            raise FollowError('You cannot follow yourself.')

        if user.is_following(target):
            raise FollowError('You are already following this user.')
        
        Follow(
            follower=user, 
            followed=target
        ).save()

    @staticmethod
    def read_followed(user):
        following = Follow.get_followed(user)
        
        return following
    
    @staticmethod
    def read_followers(user):
        followers = Follow.get_followers(user)
        
        return followers

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
