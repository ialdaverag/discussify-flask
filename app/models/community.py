from app.extensions.database import db
from app.errors.errors import NotFoundError

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
    
    @staticmethod
    def is_name_available(name):
        return Community.query.filter_by(name=name).first() is None
    
    @classmethod
    def get_by_id(cls, id):
        #community = Community.query.get(id)
        community = db.session.get(Community, id)

        if community is None:
            raise NotFoundError('Community not found')

        return community
    
    @classmethod
    def get_by_name(cls, name):
        #community = Community.query.filter_by(name=name).first()
        community = db.session.execute(db.select(Community).filter_by(name=name)).scalar()

        if community is None:
            raise NotFoundError('Community not found')

        return community
    
    @classmethod
    def get_all(cls):
        #return Community.query.all()
        return db.session.scalars(db.select(Community)).all()
    
    def belongs_to(self, user):
        return self.owner is user
    
    def change_ownership_to(self, user):
        self.owner = user
        db.session.commit()
    
    def append_subscriber(self, user):
        self.subscribers.append(user)
        db.session.commit()

    def remove_subscriber(self, user):
        self.subscribers.remove(user)
        db.session.commit()

    def append_moderator(self, user):
        self.moderators.append(user)
        db.session.commit()

    def remove_moderator(self, user):
        self.moderators.remove(user)
        db.session.commit()

    def append_banned(self, user):
        self.banned.append(user)
        db.session.commit()

    def remove_banned(self, user):
        self.banned.remove(user)
        db.session.commit()
