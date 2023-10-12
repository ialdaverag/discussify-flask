from app.extensions.database import db

from app.models.community import Community
from app.models.community import community_subscribers
from app.models.community import community_moderators
from app.models.post import Post

from app.errors.errors import NotFoundError
from app.errors.errors import FollowError
from app.errors.errors import NameError
from app.errors.errors import ModeratorError
from app.errors.errors import OwnershipError
from app.errors.errors import SubscriptionError
from app.errors.errors import BanError
from app.errors.errors import UnauthorizedError

follows = db.Table(
    'follows',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    communities = db.relationship('Community', backref='owner', lazy='dynamic')
    posts = db.relationship('Post', backref='owner', lazy='dynamic')
    comments = db.relationship('Comment', backref='owner', lazy='dynamic')
    followed = db.relationship(
        'User',
        secondary=follows,
        primaryjoin=(follows.c.follower_id == id),
        secondaryjoin=(follows.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    @staticmethod
    def is_username_available(username):
        return User.query.filter_by(username=username).first() is None
    
    @staticmethod
    def is_email_available(email):
        return User.query.filter_by(email=email).first() is None
    
    @classmethod
    def get_by_username(cls, username):
        user = User.query.filter_by(username=username).first()

        if user is None:
            raise NotFoundError('User not found')

        return user
    
    @classmethod
    def get_by_id(cls, id):
        user = User.query.get(id)

        if user is None:
            raise NotFoundError('User not found')

        return user
    
    @classmethod
    def get_all(cls):
        return User.query.all()
    
    def is_following(self, other):
        return other in self.followed
    
    def follow(self, other): 
        if other is self:
            raise FollowError('You cannot follow yourself')

        if self.is_following(other):
            raise FollowError('You are already following this user')
        
        self.followed.append(other)
        db.session.commit()

    def unfollow(self, other):
        if other is self:
            raise FollowError('You cannot unfollow yourself')
        
        if not self.is_following(other):
            raise FollowError('You are not following this user')
        
        self.followed.remove(other)
        db.session.commit()
    
    def create_community(self, name, about = ''):
        name_available = Community.is_name_available(name)

        if not name_available:
            raise NameError('Name is already used')

        community = Community(name=name, about=about, owner=self)
        community.subscribers.append(self)
        community.moderators.append(self)

        db.session.add(community)
        db.session.commit()

        return community

    def update_community(self, community, name, about):
        if not community.belongs_to(self):
            raise OwnershipError('')
        
        new_name = name

        if new_name is not None:
            existing_community = Community.query.filter_by(name=new_name).first()

            if existing_community and existing_community != community:
                raise NameError('')

            community.name = new_name

        new_about = about

        community.about = new_about or community.about

        db.session.commit()

        return community
        
    def delete_community(self, community):
        if not community.belongs_to(self):
            raise OwnershipError('You are not the owner of this community')
        
        db.session.delete(community)
        db.session.commit()

    def is_subscribed_to(self, community):
        return self in community.subscribers

    def subscribe_to(self, community):
        if self.is_banned_from(community):
            raise BanError('You are banned from this community')

        if self.is_subscribed_to(community):
            raise SubscriptionError('You are already subscribed to this community')

        community.append_subscriber(self)

    def unsubscribe_to(self, community):
        if community.belongs_to(self):
            raise OwnershipError('You are the owner of this community and cannot unsubscribe')
        
        if not self.is_subscribed_to(community):
            raise SubscriptionError('You are not subscribed to this community')
        
        if self.is_moderator_of(community):
            community.remove_moderator(self)

        community.remove_subscriber(self)

    def is_moderator_of(self, community):
        return self in community.moderators
    
    def appoint_moderator(self, user, community):
        if not community.belongs_to(self):
            raise OwnershipError('You are not the owner of this community')

        if user.is_banned_from(community):
            raise BanError('The user is banned from this community')
        
        if not user.is_subscribed_to(community):
            raise SubscriptionError('The user is not subscribed to this community')

        if user.is_moderator_of(community):
            raise ModeratorError('The user is already a moderator of this community')

        community.append_moderator(user)

    def dismiss_moderator(self, user, community):
        if not community.belongs_to(self):
            raise OwnershipError('You are not the owner of this community')
        
        if community.belongs_to(user):
            raise OwnershipError('You are the owner of this community and cannot unmod yourself')
        
        if not user.is_moderator_of(community):
            raise ModeratorError('The user is not a moderator of this community')
        
        community.remove_moderator(user)
        
    def is_banned_from(self, community):
        return self in community.banned

    def ban_from(self, user, community):
        if not self.is_moderator_of(community):
            raise UnauthorizedError('You are not a moderator of this community')
        
        if self is user:
            raise BanError('You cannot ban yourself')
        
        if user.is_banned_from(community):
            raise BanError('The user is already banned from the community')
        
        if user is community.owner:
            raise BanError('You cannot ban the owner of the community')
        
        if user in community.moderators:
            community.remove_moderator(user)
        
        if not user.is_subscribed_to(community):
            raise SubscriptionError('The user is not subscribed to this community')
        
        community.append_banned(user)

