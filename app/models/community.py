from flask_jwt_extended import current_user
from sqlalchemy import func

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


class CommunityStats(db.Model):
    __tablename__ = 'community_stats'

    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), unique=True)
    posts_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    subscribers_count = db.Column(db.Integer, default=0)
    moderators_count = db.Column(db.Integer, default=0)
    banned_count = db.Column(db.Integer, default=0)

    community = db.relationship('Community', back_populates='stats')


class Community(db.Model):
    __tablename__ = 'communities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    about = db.Column(db.String(1023), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # User
    owner = db.relationship('User', back_populates='communities')

    # Community
    subscribers = db.relationship('User', secondary=community_subscribers, back_populates='subscriptions')
    moderators = db.relationship('User', secondary=community_moderators, back_populates='moderations')
    banned = db.relationship('User', secondary=community_bans, back_populates='bans')

    # Post
    #posts = db.relationship('Post', cascade='all, delete', backref='community', lazy='dynamic')
    posts = db.relationship('Post', cascade='all, delete', back_populates='community', lazy='dynamic')

    # Stats
    stats = db.relationship('CommunityStats', uselist=False, back_populates='community', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.stats = CommunityStats(community=self)

    @staticmethod
    def is_name_available(name):
        return Community.query.filter_by(name=name).first() is None
    
    @classmethod
    def get_by_id(cls, id):
        #community = Community.query.get(id)
        community = db.session.get(Community, id)

        if community is None:
            raise NotFoundError('Community not found.')

        return community
    
    @classmethod
    def get_by_name(cls, name):
        #community = Community.query.filter_by(name=name).first()
        community = db.session.execute(db.select(Community).filter_by(name=name)).scalar()

        if community is None:
            raise NotFoundError('Community not found.')

        return community
    
    @classmethod
    def get_all(cls):
        #return Community.query.all()
        return db.session.scalars(db.select(Community)).all()
    
    @property
    def subscriber(self):
        if current_user:
            return current_user.is_subscribed_to(self)
        
        return None
    
    @property
    def moderator(self):
        if current_user:
            return current_user.is_moderator_of(self)
        
        return None
    
    @property
    def owned_by(self):
        if current_user:
            return current_user.is_owner_of(self)
        
        return None
    
    @property
    def ban(self):
        if current_user:
            return current_user.is_banned_from(self)
        
        return None
    
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


@db.event.listens_for(Community, 'after_insert')
def increment_community_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.user_id
    ).values(
        communities_count=user_stats_table.c.communities_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(Community, 'after_delete')
def decrement_community_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.user_id
    ).values(
        communities_count=user_stats_table.c.communities_count - 1
    )

    connection.execute(update_query)


@db.event.listens_for(Community, 'before_delete')
def decrement_subscriptions_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    for subscriber in target.subscribers:
        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == subscriber.id
        ).values(
            subscriptions_count=user_stats_table.c.subscriptions_count - 1
        )
        connection.execute(update_query)


@db.event.listens_for(Community, 'before_delete')
def decrement_moderations_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    for moderator in target.moderators:
        update_query = user_stats_table.update().where(
            user_stats_table.c.user_id == moderator.id
        ).values(
            moderations_count=user_stats_table.c.moderations_count - 1
        )
        connection.execute(update_query)


@db.event.listens_for(Community.subscribers, 'append')
def increment_subscribers_count_on_community_stats(target, value, initiator):
    target.stats.subscribers_count += 1
    db.session.commit()

@db.event.listens_for(Community.subscribers, 'remove')
def decrement_subscribers_count_on_community_stats(target, value, initiator):
    target.stats.subscribers_count -= 1
    db.session.commit()
    

@db.event.listens_for(Community.moderators, 'append')
def increment_moderators_count_on_community_stats(target, value, initiator):
    target.stats.moderators_count += 1
    db.session.commit()

@db.event.listens_for(Community.moderators, 'remove')
def decrement_moderators_count_on_community_stats(target, value, initiator):
    target.stats.moderators_count -= 1
    db.session.commit()


@db.event.listens_for(Community.banned, 'append')
def increment_banned_count_on_community_stats(target, value, initiator):
    target.stats.banned_count += 1

    db.session.commit()


@db.event.listens_for(Community.banned, 'remove')
def decrement_banned_count_on_community_stats(target, value, initiator):
    target.stats.banned_count -= 1

    db.session.commit()
