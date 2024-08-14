# Flask-JWT-Extended
from flask_jwt_extended import current_user

# app.extensions
from app.extensions.database import db

# app.models
from app.models.community import Community
from app.models.community import CommunitySubscriber
from app.models.community import CommunityModerator
from app.models.community import CommunityBan
from app.models.post import Post
from app.models.post import PostBookmark
from app.models.post import PostVote
from app.models.comment import Comment
from app.models.comment import CommentBookmark
from app.models.comment import CommentVote

# app.errors
from app.errors.errors import NotFoundError
from app.errors.errors import FollowError
from app.errors.errors import NameError
from app.errors.errors import NotInError
from app.errors.errors import ModeratorError
from app.errors.errors import OwnershipError
from app.errors.errors import SubscriptionError
from app.errors.errors import BanError
from app.errors.errors import UnauthorizedError
from app.errors.errors import BookmarkError
from app.errors.errors import VoteError


class Follow(db.Model):
    __tablename__ = 'follows'

    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='followed')
    followed = db.relationship('User', foreign_keys=[followed_id], back_populates='followers')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_follower_and_followed(cls, follower, followed):
        follow = cls.query.filter_by(follower=follower, followed=followed).first()

        return follow
    
    @classmethod
    def get_followers(cls, user):
        followers = cls.query.filter_by(followed_id=user.id).all()

        return [follow.follower for follow in followers]
    
    @classmethod
    def get_followed(cls, user):
        followed = cls.query.filter_by(follower_id=user.id).all()
        
        return [follow.followed for follow in followed]



class UserStats(db.Model):
    __tablename__ = 'user_stats'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    followers_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    communities_count = db.Column(db.Integer, default=0)
    posts_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    subscriptions_count = db.Column(db.Integer, default=0)
    moderations_count = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates='stats')

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # User
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], back_populates='followed', lazy='dynamic', cascade='all, delete-orphan')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id], back_populates='follower', lazy='dynamic', cascade='all, delete-orphan')

    # Community
    communities = db.relationship('Community', back_populates='owner', lazy='dynamic', cascade='all, delete')
    subscriptions = db.relationship('CommunitySubscriber', back_populates='user')
    moderations = db.relationship('CommunityModerator', back_populates='user')
    bans = db.relationship('CommunityBan', back_populates='user')

    # Post
    posts = db.relationship('Post', back_populates='owner', lazy='dynamic')
    bookmarks = db.relationship('PostBookmark', back_populates='user')
    post_votes = db.relationship('PostVote', back_populates='user')

    # Comment
    comments = db.relationship('Comment', back_populates='owner', lazy='dynamic')
    comment_bookmarks = db.relationship('CommentBookmark', back_populates='user')
    comment_votes = db.relationship('CommentVote', back_populates='user')

    # Stats
    stats = db.relationship('UserStats', uselist=False, back_populates='user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stats = UserStats(user=self)
        self.stats.save()

    @staticmethod
    def is_username_available(username):
        return User.query.filter_by(username=username).first() is None
    
    @staticmethod
    def is_email_available(email):
        return User.query.filter_by(email=email).first() is None
    
    @classmethod
    def get_by_username(cls, username):
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar()

        if user is None:
            raise NotFoundError('User not found.')

        return user
    
    @classmethod
    def get_by_id(cls, id):
        user = db.session.get(User, id)

        if user is None:
            raise NotFoundError('User not found.')

        return user
    
    @classmethod
    def get_all(cls):
        return db.session.scalars(db.select(User)).all()
    
    @property
    def following(self):
        if current_user and current_user != self:  
            return current_user.is_following(self)
        
        return None
    
    @property
    def follower(self):
        if current_user and current_user != self:
            return current_user.is_followed_by(self)
        
        return None
    
    def is_following(self, other):
        follow = Follow.get_by_follower_and_followed(follower=self, followed=other)

        return follow is not None
    
    def is_followed_by(self, other):
        follow = Follow.get_by_follower_and_followed(follower=other, followed=self)

        return follow is not None
    
    def follow(self, other): 
        if other is self:
            raise FollowError('You cannot follow yourself.')

        if self.is_following(other):
            raise FollowError('You are already following this user.')
        
        new_follow = Follow(follower=self, followed=other)
        new_follow.save()

    def unfollow(self, other):
        if other is self:
            raise FollowError('You cannot unfollow yourself.')
        
        if not self.is_following(other):
            raise FollowError('You are not following this user.')
        
        follow = Follow.get_by_follower_and_followed(follower=self, followed=other)
        follow.delete()
    
    def create_community(self, name, about = ''):
        name_available = Community.is_name_available(name)

        if not name_available:
            raise NameError('Name already taken.')

        community = Community(name=name, about=about, owner=self)
        db.session.add(community)
        db.session.commit()

        CommunitySubscriber(user=self, community=community).save()
        CommunityModerator(user=self, community=community).save()

        return community

    def update_community(self, community, name, about):
        if not community.belongs_to(self):
            raise OwnershipError('You are not the owner of this community.')
        
        new_name = name

        if new_name is not None:
            existing_community = Community.query.filter_by(name=new_name).first()

            if existing_community and existing_community != community:
                raise NameError('Name already taken.')

            community.name = new_name

        new_about = about

        community.about = new_about or community.about

        db.session.commit()

        return community
        
    def delete_community(self, community):
        if not community.belongs_to(self):
            raise OwnershipError('You are not the owner of this community.')
        
        db.session.delete(community)
        db.session.commit()

    def is_owner_of(self, community):
        return self is community.owner

    def is_subscribed_to(self, community):
        subscription = CommunitySubscriber.get_by_user_and_community(self, community)

        return subscription is not None

    def subscribe_to(self, community):
        if self.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if self.is_subscribed_to(community):
            raise SubscriptionError('You are already subscribed to this community.')

        subscription = CommunitySubscriber(user=self, community=community)
        subscription.save()

    def unsubscribe_to(self, community):
        if community.belongs_to(self):
            raise OwnershipError('You are the owner of this community and cannot unsubscribe.')
        
        if not self.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')
        
        if self.is_moderator_of(community):
            community.remove_moderator(self)

        subscription = CommunitySubscriber.get_by_user_and_community(self, community)
        subscription.delete()

    def is_moderator_of(self, community):
        moderation = CommunityModerator.get_by_user_and_community(self, community)

        return moderation is not None
    
    def appoint_moderator(self, user, community):
        if not community.belongs_to(self):
            raise OwnershipError('You are not the owner of this community.')

        if user.is_banned_from(community):
            raise BanError('The user is banned from this community.')
        
        if not user.is_subscribed_to(community):
            raise SubscriptionError('The user is not subscribed to this community.')

        if user.is_moderator_of(community):
            raise ModeratorError('The user is already a moderator of this community.')

        CommunityModerator(user=user, community=community).save()

    def dismiss_moderator(self, user, community):
        if not community.belongs_to(self):
            raise OwnershipError('You are not the owner of this community.')
        
        if community.belongs_to(user):
            raise OwnershipError('You are the owner of this community and cannot unmod yourself.')
        
        if not user.is_moderator_of(community):
            raise ModeratorError('The user is not a moderator of this community.')
        
        CommunityModerator.get_by_user_and_community(user, community).delete()
        
    def is_banned_from(self, community):
        ban = CommunityBan.get_by_user_and_community(self, community)

        return ban is not None

    def ban_from(self, user, community):
        if not self.is_moderator_of(community):
            raise UnauthorizedError('You are not a moderator of this community.')
        
        if self is user:
            raise BanError('You cannot ban yourself.')
        
        if user.is_banned_from(community):
            raise BanError('The user is already banned from the community.')
        
        if user is community.owner:
            raise BanError('You cannot ban the owner of the community.')
        
        if user in community.moderators:
            community.remove_moderator(user)
        
        if not user.is_subscribed_to(community):
            raise SubscriptionError('The user is not subscribed to this community.')
        
        CommunityBan(user=user, community=community).save()

    def unban_from(self, user, community):
        if not self.is_moderator_of(community):
            raise UnauthorizedError('You are not a moderator of this community.')
        
        if not user.is_banned_from(community):
            raise BanError('The user is not banned from the community.')
        
        CommunityBan.get_by_user_and_community(user, community).delete()

    def transfer_community(self, community, user):
        if not community.belongs_to(self):
            raise OwnershipError('You are not the owner of this community.')
        
        if user is self:
            raise OwnershipError('You are already the owner of this community.')
        
        if user.is_banned_from(community):
            raise BanError('You cannot transfer the community to a banned user.')
        
        if not user.is_subscribed_to(community):
            raise SubscriptionError('The user is not subscribed to this community.')
        
        if not user.is_moderator_of(community):
            CommunityModerator(user=user, community=community).save()

        community.change_ownership_to(user)

    def create_post(self, title, content, community):
        if self.is_banned_from(community):
            raise BanError('You are banned from this community.')
        
        if not self.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')
        
        post = Post(title=title, content=content, community=community, owner=self)

        db.session.add(post)
        db.session.commit()

        return post
    
    def update_post(self, post, title, content):
        if not post.belongs_to(self):
            raise OwnershipError('You are not the owner of this post.')
        
        new_title = title
        new_content = content
        
        post.title = new_title or post.title
        post.content = new_content or post.title

        db.session.commit()

        return post
    
    def delete_post(self, post):
        if not (post.belongs_to(self) or self.is_moderator_of(post.community)):
            raise OwnershipError('You are not the owner of this post.')
        
        db.session.delete(post)
        db.session.commit()

    def bookmark_post(self, post):
        if post.is_bookmarked_by(self):
            raise BookmarkError('Post already bookmarked.')
        
        PostBookmark(user=self, post=post).save()

    def unbookmark_post(self, post):
        if not post.is_bookmarked_by(self):
            raise BookmarkError('Post not bookmarked.')
        
        PostBookmark.get_by_user_and_post(user=self, post=post).delete()

    def upvote_post(self, post):
        community = post.community

        if self.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if not self.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')

        vote = PostVote.get_by_user_and_post(user=self, post=post)

        if vote:
            if vote.is_downvote():
                vote.direction = 1
                db.session.commit()
            else:
                raise VoteError('Post already upvoted.')
        else:
            new_vote = PostVote(user=self, post=post, direction=1)
            new_vote.create()

    def downvote_post(self, post):
        community = post.community
        if self.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if not self.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')

        vote = PostVote.get_by_user_and_post(user=self, post=post)

        if vote:
            if vote.is_upvote():
                vote.direction = -1
                db.session.commit()
            else:
                raise VoteError('Post already downvoted.')
        else:
            new_vote = PostVote(user=self, post=post, direction=-1)
            new_vote.create()

    def cancel_post_vote(self, post):
        community = post.community

        if self.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if not self.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')

        vote = PostVote.get_by_user_and_post(user=self, post=post)

        if vote:
            vote.delete()
        else:
            raise VoteError('You have not voted on this post.')

    def create_comment(self, content, post, comment=None):
        community = post.community

        if self.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if not self.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')
        
        if comment is not None:
            if comment not in post.comments:
                raise NotInError('The comment to reply is not in the post.')
        
        new_comment = Comment(content=content, post=post, owner=self, comment=comment)

        db.session.add(new_comment)
        db.session.commit()

        return new_comment

    def update_comment(self, content, comment):
        if not comment.belongs_to(self):
            raise OwnershipError('This comment is not yours.')
        
        community = comment.post.community
        
        if self.is_banned_from(community):
            raise BanError('You are banned from this community.')
        
        new_content = content

        comment.content = new_content or comment.content

        return comment

    def delete_comment(self, comment):
        if not (comment.belongs_to(self) or self.is_moderator_of(comment.post.community)):
            raise OwnershipError('You are not the owner of this comment.')
        
        db.session.delete(comment)
        db.session.commit()

    def bookmark_comment(self, comment):
        if comment.is_bookmarked_by(self):
            raise BookmarkError('Comment already bookmarked.')
        
        CommentBookmark(user=self, comment=comment).save()

    def unbookmark_comment(self, comment):
        if not comment.is_bookmarked_by(self):
            raise BookmarkError('Comment not bookmarked.')
        
        CommentBookmark.get_by_user_and_comment(user=self, comment=comment).delete()

    def upvote_comment(self, comment):
        community = comment.post.community

        if self.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if not self.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')

        vote = CommentVote.get_by_user_and_comment(user=self, comment=comment)

        if vote:
            if vote.is_downvote():
                vote.direction = 1
                db.session.commit()
            else:
                raise VoteError('Comment already upvoted.')
        else:
            new_vote = CommentVote(user=self, comment=comment, direction=1)
            new_vote.create()

    def downvote_comment(self, comment):
        community = comment.post.community

        if self.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if not self.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')

        vote = CommentVote.get_by_user_and_comment(user=self, comment=comment)

        if vote:
            if vote.is_upvote():
                vote.direction = -1
                db.session.commit()
            else:
                raise VoteError('You have already downvoted this post.')
        else:
            new_vote = CommentVote(user=self, comment=comment, direction=-1)
            new_vote.create()

    def cancel_comment_vote(self, comment):
        community = comment.post.community

        if self.is_banned_from(community):
            raise BanError('You are banned from this community.')

        if not self.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community.')

        vote = CommentVote.get_by_user_and_comment(user=self, comment=comment)

        if vote:
            vote.delete()
        else:
            raise VoteError('You have not voted on this comment.')


@db.event.listens_for(Follow, 'after_insert')
def increment_following_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.follower_id
    ).values(
        following_count=user_stats_table.c.following_count + 1
    )

    connection.execute(update_query)

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.followed_id
    ).values(
        followers_count=user_stats_table.c.followers_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(Follow, 'after_delete')
def decrement_following_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.follower_id
    ).values(
        following_count=user_stats_table.c.following_count - 1
    )

    connection.execute(update_query)

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.followed_id
    ).values(
        followers_count=user_stats_table.c.followers_count - 1
    )

    connection.execute(update_query)

