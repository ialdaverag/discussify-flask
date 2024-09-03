# Models
from app.models.post import Post
from app.models.post import PostBookmark
from app.models.post import PostVote

# Errors
from app.errors.errors import BanError
from app.errors.errors import SubscriptionError
from app.errors.errors import OwnershipError
from app.errors.errors import BookmarkError
from app.errors.errors import VoteError
from app.errors.errors import BlockError

# Decorators
from app.decorators.filtered_users import filtered_users
from app.decorators.filtered_posts import filtered_posts


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
    def read(user, post):
        owner = post.owner

        if user and (user.is_blocking(owner) or user.is_blocked_by(owner)):
            raise BlockError('You cannot view this post.')

        return post
    
    @staticmethod
    def read_all_by_community(community, args):
        paginated_posts = Post.get_all_by_community(community, args)

        return paginated_posts
    
    @staticmethod
    def read_all_by_user(user, args):
        paginated_posts = Post.get_all_by_user(user, args)

        return paginated_posts

    @staticmethod
    def read_all(args):
        paginated_posts = Post.get_all(args)

        return paginated_posts
    
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
        community = post.community

        if not (post.belongs_to(user) or user.is_moderator_of(community)):
            raise OwnershipError('You cannot delete this post.')
        
        post.delete()


class PostBookmarkManager:
    @staticmethod
    def create(user, post):
        owner = post.owner

        if user.is_blocking(owner) or user.is_blocked_by(owner):
            raise BlockError('You cannot bookmark this post.')
        
        if post.is_bookmarked_by(user):
            raise BookmarkError('Post already bookmarked.')

        PostBookmark(
            user=user, 
            post=post
        ).save()

    @staticmethod
    def read_bookmarked_posts_by_user(user, args):
        paginated_bookmarks = PostBookmark.get_bookmarks_by_user(user, args)

        return paginated_bookmarks
    
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
        owner = post.owner

        if user.is_blocking(owner) or user.is_blocked_by(owner):
            raise BlockError('You cannot vote on this post.')

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
    def read_upvoted_posts_by_user(user, args):
        paginated_upvotes = PostVote.get_upvoted_posts_by_user(user, args)

        return paginated_upvotes
    
    @staticmethod
    def read_downvoted_posts_by_user(user, args):
        paginated_downvotes = PostVote.get_downvoted_posts_by_user(user, args)

        return paginated_downvotes
    
    @staticmethod
    def read_upvoters_by_post(post, args):
        paginated_upvoters = PostVote.get_upvoters_by_post(post, args)

        return paginated_upvoters
    
    @staticmethod
    def read_downvoters_by_post(post, args):
        paginated_downvoters = PostVote.get_downvoters_by_post(post, args)

        return paginated_downvoters

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
