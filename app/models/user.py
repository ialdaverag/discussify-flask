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

    def is_following(self, other):
        return other in self.followed
