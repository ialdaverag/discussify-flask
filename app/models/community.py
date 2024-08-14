from flask_jwt_extended import current_user
from sqlalchemy import func

from app.extensions.database import db
from app.errors.errors import NotFoundError

class CommunitySubscriber(db.Model):
    __tablename__ = 'community_subscribers'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', foreign_keys=[user_id], back_populates='subscriptions')
    community = db.relationship('Community', foreign_keys=[community_id], back_populates='subscribers')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_user_and_community(user, community):
        return CommunitySubscriber.query.filter_by(user=user, community=community).first()
    

class CommunityModerator(db.Model):
    __tablename__ = 'community_moderators'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', foreign_keys=[user_id], back_populates='moderations')
    community = db.relationship('Community', foreign_keys=[community_id], back_populates='moderators')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_user_and_community(user, community):
        return CommunityModerator.query.filter_by(user=user, community=community).first()


class CommunityBan(db.Model):
    __tablename__ = 'community_bans'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', foreign_keys=[user_id], back_populates='bans')
    community = db.relationship('Community', foreign_keys=[community_id], back_populates='banned')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_user_and_community(user, community):
        return CommunityBan.query.filter_by(user=user, community=community).first()


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
    subscribers = db.relationship('CommunitySubscriber', back_populates='community')
    moderators = db.relationship('CommunityModerator', back_populates='community')
    banned = db.relationship('CommunityBan', back_populates='community')

    # Post
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


@db.event.listens_for(Community, 'after_insert')
def increment_communities_count_on_user_stats(mapper, connection, target):
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


@db.event.listens_for(CommunitySubscriber, 'after_insert')
def increment_subscribers_count_on_community_stats(mapper, connection, target):

    community_stats_table = CommunityStats.__table__

    
    update_query = community_stats_table.update().where(
        community_stats_table.c.community_id == target.community_id
    ).values(
        subscribers_count=community_stats_table.c.subscribers_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(CommunitySubscriber, 'after_delete')
def decrement_subscribers_count_on_community_stats(mapper, connection, target):

    community_stats_table = CommunityStats.__table__
    
    update_query = community_stats_table.update().where(
        community_stats_table.c.community_id == target.community_id
    ).values(
        subscribers_count=community_stats_table.c.subscribers_count - 1
    )

    connection.execute(update_query)


@db.event.listens_for(CommunitySubscriber, 'after_insert')
def increment_subscriptions_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.user_id
    ).values(
        subscriptions_count=user_stats_table.c.subscriptions_count + 1
    )

    connection.execute(update_query)

@db.event.listens_for(CommunitySubscriber, 'after_delete')
def decrement_subscriptions_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats
    
    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.user_id
    ).values(
        subscriptions_count=user_stats_table.c.subscriptions_count - 1
    )

    connection.execute(update_query)


@db.event.listens_for(CommunityModerator, 'after_insert')
def increment_moderators_count_on_community_stats(mapper, connection, target):

    community_stats_table = CommunityStats.__table__

    update_query = community_stats_table.update().where(
        community_stats_table.c.community_id == target.community_id
    ).values(
        moderators_count=community_stats_table.c.moderators_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(CommunityModerator, 'after_delete')
def decrement_moderators_count_on_community_stats(mapper, connection, target):

    community_stats_table = CommunityStats.__table__

    update_query = community_stats_table.update().where(
        community_stats_table.c.community_id == target.community_id
    ).values(
        moderators_count=community_stats_table.c.moderators_count - 1
    )

    connection.execute(update_query)


@db.event.listens_for(CommunityModerator, 'after_insert')
def increment_moderations_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.user_id
    ).values(
        moderations_count=user_stats_table.c.moderations_count + 1
    )

    connection.execute(update_query)

@db.event.listens_for(CommunityModerator, 'after_delete')
def decrement_moderations_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats
    
    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.user_id
    ).values(
        moderations_count=user_stats_table.c.moderations_count - 1
    )

    connection.execute(update_query)


@db.event.listens_for(CommunityBan, 'after_insert')
def increment_banned_users_count_on_community_stats(mapper, connection, target):

    community_stats_table = CommunityStats.__table__

    update_query = community_stats_table.update().where(
        community_stats_table.c.community_id == target.community_id
    ).values(
        banned_count=community_stats_table.c.banned_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(CommunityBan, 'after_delete')
def decrement_banned_users_count_on_community_stats(mapper, connection, target):

    community_stats_table = CommunityStats.__table__

    update_query = community_stats_table.update().where(
        community_stats_table.c.community_id == target.community_id
    ).values(
        banned_count=community_stats_table.c.banned_count - 1
    )

    connection.execute(update_query)