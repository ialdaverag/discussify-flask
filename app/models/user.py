from extensions.database import db

from models.community import Community
from models.community import community_subscribers
from models.community import community_moderators

from models.post import Post


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    communities = db.relationship('Community', backref='owner', lazy='dynamic')
    posts = db.relationship('Post', backref='owner', lazy='dynamic')

    #subscriptions = db.relationship('Community', secondary=community_subscribers, backref='subscribers')
    #moderations = db.relationship('Community', secondary=community_moderators, backref='moderators')