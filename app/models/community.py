# Flask-JWT-Extended
from flask_jwt_extended import current_user

# Extensions
from app.extensions.database import db

# Decorators
from app.decorators.filtered_users import filtered_users

# Errors
from app.errors.errors import NotFoundError


class CommunitySubscriber(db.Model):
    __tablename__ = 'community_subscribers'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # User
    user = db.relationship('User', foreign_keys=[user_id], back_populates='subscriptions')

    # Community
    community = db.relationship('Community', foreign_keys=[community_id], back_populates='subscribers')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_community(cls, user, community):
        subscription = db.session.get(cls, (user.id, community.id))
        
        return subscription
    
    @classmethod
    def get_subscriptions_by_user(cls, user):
        query = db.select(cls).where(cls.user_id == user.id)

        subscriptions = db.session.scalars(query).all()

        subscriptions = [subscription.community for subscription in subscriptions]

        return subscriptions
    
    @classmethod
    @filtered_users
    def get_subscribers_by_community(cls, community):
        query = db.select(cls).where(cls.community_id == community.id)

        subscribers = db.session.scalars(query).all()

        subscribers = [subscriber.user for subscriber in subscribers]

        return subscribers


class CommunityModerator(db.Model):
    __tablename__ = 'community_moderators'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # User
    user = db.relationship('User', foreign_keys=[user_id], back_populates='moderations')

    # Community
    community = db.relationship('Community', foreign_keys=[community_id], back_populates='moderators')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_community(cls, user, community):
        moderation = db.session.get(cls, (user.id, community.id))

        return moderation
    
    @classmethod
    def get_moderations_by_user(cls, user):
        query = db.select(cls).where(cls.user_id == user.id)

        moderations = db.session.scalars(query).all()

        moderations = [moderation.community for moderation in moderations]

        return moderations
    
    @classmethod
    def get_moderators_by_community(cls, community):
        query = db.select(cls).where(cls.community_id == community.id)

        moderators = db.session.scalars(query).all()

        moderators = [moderator.user for moderator in moderators]

        return moderators


class CommunityBan(db.Model):
    __tablename__ = 'community_bans'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # User
    user = db.relationship('User', foreign_keys=[user_id], back_populates='bans')

    # Community
    community = db.relationship('Community', foreign_keys=[community_id], back_populates='banned')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_community(cls, user, community):
        ban = db.session.get(cls, (user.id, community.id))

        return ban
    
    @classmethod
    def get_bans_by_user(cls, user):
        query = db.select(cls).where(cls.user_id == user.id)

        bans = db.session.scalars(query).all()

        bans = [ban.community for ban in bans]

        return bans
    
    @classmethod
    def get_banned_by_community(cls, community):
        query = db.select(cls).where(cls.community_id == community.id)

        banned_users = db.session.scalars(query).all()

        banned_users = [banned_user.user for banned_user in banned_users]

        return banned_users


class CommunityStats(db.Model):
    __tablename__ = 'community_stats'

    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), unique=True)
    posts_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    subscribers_count = db.Column(db.Integer, default=0)
    moderators_count = db.Column(db.Integer, default=0)
    banned_count = db.Column(db.Integer, default=0)

    # Community
    community = db.relationship('Community', back_populates='stats')

    def save(self):
        db.session.add(self)
        db.session.commit()


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
    stats = db.relationship('CommunityStats', uselist=False, back_populates='community')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.stats = CommunityStats(community=self)
        self.stats.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def is_name_available(name):
        query = db.select(Community).where(Community.name == name)

        community = db.session.execute(query).scalar() is None

        return community
    
    @classmethod
    def get_by_id(cls, id):
        community = db.session.get(Community, id)

        if community is None:
            raise NotFoundError('Community not found.')

        return community
    
    @classmethod
    def get_by_name(cls, name):
        query = db.select(cls).where(cls.name == name)

        community = db.session.execute(query).scalar()

        if community is None:
            raise NotFoundError('Community not found.')

        return community
    
    @classmethod
    def get_all(cls):
        query = db.select(cls)

        communities = db.session.scalars(query).all()

        return communities
    
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
        return self.owner.id == user.id
    
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