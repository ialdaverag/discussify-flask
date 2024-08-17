from app.models.post import Post
from app.models.post import PostBookmark
from app.models.post import PostVote

from app.errors.errors import BanError
from app.errors.errors import SubscriptionError
from app.errors.errors import OwnershipError
from app.errors.errors import BookmarkError
from app.errors.errors import VoteError


class PostManager:
    @staticmethod
    def create(user, community, data):
        if user.is_banned_from(community):
            raise BanError('You are banned from this community.')
        
        if not user.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')
        
        post = Post(**data, community=community, owner=user)
        post.save()

        return post
    
    @staticmethod
    def read():
        pass

    @staticmethod
    def read_all():
        pass
    
    @staticmethod
    def update(user, post, data):
        if not post.belongs_to(user):
            raise OwnershipError('You are not the owner of this post.')
        
        title = data.get('title')
        content = data.get('content')
        
        if title:
            post.title = title
        
        if content:
            post.content = content
        
        post.save()

        return post
    
    @staticmethod
    def delete(user, post):
        if not post.belongs_to(user):
            raise OwnershipError('You are not the owner of this post.')
        
        post.delete()


class PostBookmarkManager:
    @staticmethod
    def create(user, post):
        if post.is_bookmarked_by(user):
            raise BookmarkError('Post already bookmarked.')

        PostBookmark(
            user=user, 
            post=post
        ).save()
    
    @staticmethod
    def delete(user, post):
        if not post.is_bookmarked_by(user):
            raise BookmarkError('Post not bookmarked.')
        
        PostBookmark.get_by_user_and_post(
            user=user, 
            post=post
        ).delete()


class PostVoteManager:
    @staticmethod
    def create(user, post, direction):
        if direction == 1:
            community = post.community

            if user.is_banned_from(community):
                raise BanError('You are banned from this community.')

            if not user.is_subscribed_to(community):
                raise SubscriptionError('You are not subscribed to this community.')

            vote = PostVote.get_by_user_and_post(user=user, post=post)

            if vote:
                if vote.is_downvote():
                    vote.direction = 1
                    vote.save()
                else:
                    raise VoteError('Post already upvoted.')
            else:
                new_vote = PostVote(user=user, post=post, direction=1)
                new_vote.save()
        elif direction == -1:
            community = post.community

            if user.is_banned_from(community):
                raise BanError('You are banned from this community.')

            if not user.is_subscribed_to(community):
                raise SubscriptionError('You are not subscribed to this community.')

            vote = PostVote.get_by_user_and_post(user=user, post=post)

            if vote:
                if vote.is_upvote():
                    vote.direction = -1
                    vote.save()
                else:
                    raise VoteError('Post already downvoted.')
            else:
                new_vote = PostVote(user=user, post=post, direction=-1)
                new_vote.save()

    @staticmethod
    def delete(user, post):
        community = post.community

        if user.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if not user.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')

        vote = PostVote.get_by_user_and_post(user=user, post=post)

        if vote:
            vote.delete()
        else:
            raise VoteError('You have not voted on this post.')
