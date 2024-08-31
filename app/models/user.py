# Flask-JWT-Extended
from flask_jwt_extended import current_user

# SQLAlchemy
from sqlalchemy.orm import aliased

# Extensions
from app.extensions.database import db

# Models
from app.models.community import CommunitySubscriber
from app.models.community import CommunityModerator
from app.models.community import CommunityBan

# Decorators
from app.decorators.filtered_users import filtered_users
from app.decorators.filtered_users_select import filtered_users_select

# Errors
from app.errors.errors import NotFoundError


class Follow(db.Model):
    __tablename__ = 'follows'

    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # User
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
        follow = db.session.get(cls, (follower.id, followed.id))

        return follow
    
    @classmethod
    def get_followed(cls, user, args):
        page = args.get('page')
        per_page = args.get('per_page')


        @filtered_users_select
        def get_query():
            query = (
                db.select(User)
                .join(cls, cls.followed_id == User.id)
                .where(cls.follower_id == user.id)
            )

            return query
        
        query = get_query()

        paginated_followed = db.paginate(
            query, 
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        return paginated_followed
    
    @classmethod
    def get_followers(cls, user, args):
        page = args.get('page')
        per_page = args.get('per_page')
                            
        @filtered_users_select
        def get_query():
            query = (
                db.select(User)
                .join(cls, cls.follower_id == User.id)
                .where(cls.followed_id == user.id)
            )

            return query
        
        query = get_query()

        paginated_followers = db.paginate(
            query, 
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        return paginated_followers

class Block(db.Model):
    __tablename__ = 'blocks'

    blocker_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    blocked_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # User
    blocker = db.relationship('User', foreign_keys=[blocker_id], back_populates='blocked')
    blocked = db.relationship('User', foreign_keys=[blocked_id], back_populates='blockers')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_blocker_and_blocked(cls, blocker, blocked):
        block = db.session.get(cls, (blocker.id, blocked.id))

        return block
    
    @classmethod
    def get_blocked(cls, user):
        query = (
            db.select(User)
            .join(cls, cls.blocked_id == User.id)
            .where(cls.blocker_id == user.id)
        )

        blocked = db.session.scalars(query).all()

        return blocked
    
    @classmethod
    def get_blocked_with_args(cls, user, args):
        query = (
            db.select(User)
            .join(cls, cls.blocked_id == User.id)
            .where(cls.blocker_id == user.id)
        )

        blocked = db.session.scalars(query).all()

        return blocked
    
    @classmethod
    def get_blockers(cls, user):
        query = db.select(cls).where(cls.blocked_id == user.id)
        
        blockers = db.session.scalars(query).all()

        blockers = [block.blocker for block in blockers]

        return blockers


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

    # User
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
    blockers = db.relationship('Block', foreign_keys=[Block.blocked_id], back_populates='blocked', lazy='dynamic', cascade='all, delete-orphan')
    blocked = db.relationship('Block', foreign_keys=[Block.blocker_id], back_populates='blocker', lazy='dynamic', cascade='all, delete-orphan')

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

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def is_username_available(username):
        query = db.select(User).where(User.username == username)

        user = db.session.execute(query).scalar() is None

        return user
    
    @staticmethod
    def is_email_available(email):
        query = db.select(User).where(User.email == email)

        email = db.session.execute(query).scalar() is None

        return email
    
    @classmethod
    def get_by_username(cls, username):
        query = db.select(cls).where(cls.username == username)

        user = db.session.execute(query).scalar()

        if user is None:
            raise NotFoundError('User not found.')

        return user
    
    @classmethod
    def get_by_id(cls, id):
        user = db.session.get(cls, id)

        if user is None:
            raise NotFoundError('User not found.')

        return user
    
    @classmethod
    def get_all(cls, args):
        page = args.get('page')
        per_page = args.get('per_page')

        @filtered_users_select
        def get_query():
            return db.select(cls)
        
        query = get_query()

        paginated_users = db.paginate(
            query, 
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        return paginated_users
    
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
    
    @property
    def blocking(self):
        if current_user and current_user != self:  
            return current_user.is_blocking(self)
        
        return None
    
    @property
    def blocker(self):
        if current_user and current_user != self:
            return current_user.is_blocked_by(self)
        
        return None
    
    def is_following(self, other):
        follow = Follow.get_by_follower_and_followed(follower=self, followed=other)

        return follow is not None
    
    def is_followed_by(self, other):
        follow = Follow.get_by_follower_and_followed(follower=other, followed=self)

        return follow is not None
    
    def is_blocking(self, other):
        block = Block.get_by_blocker_and_blocked(blocker=self, blocked=other)

        return block is not None
    
    def is_blocked_by(self, other):
        block = Block.get_by_blocker_and_blocked(blocker=other, blocked=self)

        return block is not None

    def is_owner_of(self, community):
        return self is community.owner

    def is_subscribed_to(self, community):
        subscription = CommunitySubscriber.get_by_user_and_community(self, community)

        return subscription is not None

    def is_moderator_of(self, community):
        moderation = CommunityModerator.get_by_user_and_community(self, community)

        return moderation is not None
        
    def is_banned_from(self, community):
        ban = CommunityBan.get_by_user_and_community(self, community)

        return ban is not None


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