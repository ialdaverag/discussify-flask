from app.extensions.database import db

from app.models.community import Community
from app.models.community import community_subscribers
from app.models.community import community_moderators
from app.models.post import Post

from app.errors.user import UserNotFoundError
from app.errors.user import UserSelfFollowError
from app.errors.user import UserAlreadyFollowedError
from app.errors.user import UserSelfUnfollowError
from app.errors.user import UserNotFollowedError
from app.errors.user import UserBannedError
from app.errors.user import UserAlreadySubscribedError
from app.errors.user import UserNotSubscribedError
from app.errors.user import UserNotModeratingError
from app.errors.community import CommunityNameAlreadyUsedError
from app.errors.community import CommunityNameAlreadyUsedError
from app.errors.community import CommunityBelongsToUserError
from app.errors.community import CommunityNotBelongsToUserError

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
            raise UserNotFoundError

        return user
    
    @classmethod
    def get_by_id(cls, id):
        user = User.query.get(id)

        if user is None:
            raise UserNotFoundError

        return user
    
    @classmethod
    def get_all(cls):
        return User.query.all()
    
    def is_following(self, other):
        return other in self.followed
    
    def follow(self, other): 
        if other is self:
            raise UserSelfFollowError

        if self.is_following(other):
            raise UserAlreadyFollowedError
        
        self.followed.append(other)
        db.session.commit()

    def unfollow(self, other):
        if other is self:
            raise UserSelfUnfollowError
        
        if not self.is_following(other):
            raise UserNotFollowedError
        
        self.followed.remove(other)
        db.session.commit()
    
    def create_community(self, name, about = ''):
        name_available = Community.is_name_available(name)

        if not name_available:
            raise CommunityNameAlreadyUsedError

        community = Community(name=name, about=about, owner=self)
        community.subscribers.append(self)
        community.moderators.append(self)

        db.session.add(community)
        db.session.commit()

        return community

    def update_community(self, community, name, about):
        if not community.belongs_to(self):
            raise CommunityNotBelongsToUserError
        
        new_name = name

        if new_name is not None:
            existing_community = Community.query.filter_by(name=new_name).first()

            if existing_community and existing_community != community:
                raise CommunityNameAlreadyUsedError

            community.name = new_name

        new_about = about

        community.about = new_about or community.about

        db.session.commit()

        return community
        
    def delete_community(self, community):
        if not community.belongs_to(self):
            raise CommunityNotBelongsToUserError
        
        db.session.delete(community)
        db.session.commit()

    def is_subscribed_to(self, community):
        return self in community.subscribers

    def subscribe_to(self, community):
        if self.is_banned_from(community):
            raise UserBannedError

        if self.is_subscribed_to(community):
            raise UserAlreadySubscribedError

        community.append_subscriber(self)

    def unsubscribe_to(self, community):
        if community.belongs_to(self):
            raise CommunityBelongsToUserError
        
        if not self.is_subscribed_to(community):
            raise UserNotSubscribedError
        
        if self.is_moderator_of(community):
            community.remove_moderator(self)

        community.remove_subscriber(self)
        
    def is_banned_from(self, community):
        return self in community.banned

    def is_moderator_of(self, community):
        return self in community.banned