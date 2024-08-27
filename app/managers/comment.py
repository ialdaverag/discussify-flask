# Models
from app.models.comment import Comment
from app.models.comment import CommentBookmark
from app.models.comment import CommentVote

# Errors
from app.errors.errors import BanError
from app.errors.errors import SubscriptionError
from app.errors.errors import NotInError
from app.errors.errors import OwnershipError
from app.errors.errors import BookmarkError
from app.errors.errors import VoteError
from app.errors.errors import BlockError

# Decorators
from app.decorators.filtered_users import filtered_users


class CommentManager:
    @staticmethod
    def create(user, post, data, comment=None):
        owner = post.owner

        if user.is_blocking(owner) or user.is_blocked_by(owner):
            raise BlockError('You cannot comment on this post.')
        
        community = post.community

        if user.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if not user.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')
        
        if comment is not None:
            if comment not in post.comments:
                raise NotInError('The comment to reply is not in the post.')
            
        content = data.get('content')
        
        new_comment = Comment(content=content, post=post, owner=user, comment=comment)
        new_comment.save()

        return new_comment
    
    @staticmethod
    def read(user, comment):
        owner = comment.owner
        
        if user and (user.is_blocking(owner) or user.is_blocked_by(owner)):
            raise BlockError('You cannot view this comment.')

        return comment

    @staticmethod
    def read_all():
        comments = Comment.get_all()

        return comments

    @staticmethod
    def update(user, comment, data):
        if not comment.belongs_to(user):
            raise OwnershipError('This comment is not yours.')
        
        community = comment.post.community
        
        if user.is_banned_from(community):
            raise BanError('You are banned from this community.')
        
        content = data.get('content')
        
        new_content = content

        comment.content = new_content or comment.content

        return comment
    
    @staticmethod
    def delete(user, comment):
        community = comment.post.community

        if not (comment.belongs_to(user) or user.is_moderator_of(community)):
            raise OwnershipError('You cannot delete this comment.')
        
        comment.delete()

        return comment
    

class CommentBookmarkManager:
    @staticmethod
    def create(user, comment):
        owner = comment.owner

        if user.is_blocking(owner) or user.is_blocked_by(owner):
            raise BlockError('You cannot bookmark this comment.')
        
        if comment.is_bookmarked_by(user):
            raise BookmarkError('Comment already bookmarked.')
        
        CommentBookmark(user=user, comment=comment).save()

    @staticmethod
    def read_bookmarked_comments_by_user(user):
        bookmarks = CommentBookmark.get_bookmarks_by_user(user)

        return bookmarks
    
    @staticmethod
    def delete(user, comment):
        if not comment.is_bookmarked_by(user):
            raise BookmarkError('Comment not bookmarked.')
        
        CommentBookmark.get_by_user_and_comment(user=user, comment=comment).delete()


class CommentVoteManager:
    @staticmethod
    def create(user, comment, direction):
        owner = comment.owner

        if user.is_blocking(owner) or user.is_blocked_by(owner):
            raise BlockError('You cannot vote on this comment.')
    
        if direction == 1:
            community = comment.post.community

            if user.is_banned_from(community):
                raise BanError('You are banned from this community.')

            if not user.is_subscribed_to(community):
                raise SubscriptionError('You are not subscribed to this community.')

            vote = CommentVote.get_by_user_and_comment(user=user, comment=comment)

            if vote:
                if vote.is_downvote():
                    vote.direction = 1
                    vote.save()
                else:
                    raise VoteError('Comment already upvoted.')
            else:
                new_vote = CommentVote(user=user, comment=comment, direction=1)
                new_vote.save()
        elif direction == -1:
            community = comment.post.community

            if user.is_banned_from(community):
                raise BanError('You are banned from this community.')

            if not user.is_subscribed_to(community):
                raise SubscriptionError('You are not subscribed to this community.')

            vote = CommentVote.get_by_user_and_comment(user=user, comment=comment)

            if vote:
                if vote.is_upvote():
                    vote.direction = -1
                    vote.save()
                else:
                    raise VoteError('You have already downvoted this post.')
            else:
                new_vote = CommentVote(user=user, comment=comment, direction=-1)
                new_vote.save()


    @staticmethod
    def read_upvoted_comments_by_user(user):
        upvotes = CommentVote.get_upvoted_comments_by_user(user)

        return upvotes
    

    @staticmethod
    def read_downvoted_comments_by_user(user):
        downvotes = CommentVote.get_downvoted_comments_by_user(user)

        return downvotes

    @staticmethod
    @filtered_users
    def read_upvoters_by_comment(comment):
        upvoters = CommentVote.get_upvoters_by_comment(comment)

        return upvoters
    
    @staticmethod
    @filtered_users
    def read_downvoters_by_comment(comment):
        downvoters = CommentVote.get_downvoters_by_comment(comment)

        return downvoters
        
    @staticmethod
    def delete(user, comment):
        community = comment.post.community

        if user.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if not user.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')

        vote = CommentVote.get_by_user_and_comment(user=user, comment=comment)

        if vote:
            vote.delete()
        else:
            raise VoteError('You have not voted on this comment.')
