from extensions.database import db

community_subscribers = db.Table(
    'community_subscribers',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('community_id', db.Integer, db.ForeignKey('communities.id'))
)

community_moderators = db.Table(
    'community_moderators',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('community_id', db.Integer, db.ForeignKey('communities.id'))
)

community_bans = db.Table(
    'community_bans',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('community_id', db.Integer, db.ForeignKey('communities.id'))
)


class Community(db.Model):
    __tablename__ = 'communities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    about = db.Column(db.String(1023), default='')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    subscribers = db.relationship('User', secondary=community_subscribers, backref='subscriptions')
    moderators = db.relationship('User', secondary=community_moderators, backref='moderations')
    banned = db.relationship('User', secondary=community_bans, backref='bans')
    posts = db.relationship('Post', cascade='all, delete', backref='community', lazy='dynamic')