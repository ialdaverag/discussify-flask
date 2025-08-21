# Datetime
from datetime import datetime
from datetime import timedelta
from datetime import timezone

# Flask-JWT-Extended
from flask_jwt_extended import current_user

# Extensions
from app.extensions.database import db

# Decorators
from app.decorators.filters import filtered_users

# Errors
from app.errors.errors import NotFoundError


class CommunitySubscriber(db.Model):
    __tablename__ = 'community_subscribers'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', back_populates='subscriptions')
    community = db.relationship('Community', back_populates='subscribers')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_community(cls, user, community):
        """
        Get the subscription object by user and community.

        :param user: The user object.
        :param community: The community object.

        :return: The subscription object
        """

        subscription = db.session.get(cls, (user.id, community.id))
        
        return subscription
    
    @classmethod
    def get_subscriptions_by_user(cls, user, args):
        """
        Get a list of communities the user is subscribed to.

        :param user: The user object.

        :return: List of community objects.
        """
        
        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        query = (
            db.select(Community)
            .join(cls, cls.community_id == Community.id)
            .join(CommunityStats, Community.id == CommunityStats.community_id)
            .where(cls.user_id == user.id)
        )

        if time_filter != 'all':
            now = datetime.now(timezone.utc)

            if time_filter == 'day':
                start_date = now - timedelta(days=1)
            elif time_filter == 'week':
                start_date = now - timedelta(weeks=1)
            elif time_filter == 'month':
                start_date = now - timedelta(days=30)
            elif time_filter == 'year':
                start_date = now - timedelta(days=365)
            else:
                start_date = None

            if start_date:
                query = query.filter(cls.created_at >= start_date)

        if sort_by == 'subscribers':
            order_column = CommunityStats.subscribers_count
        elif sort_by == 'posts':
            order_column = CommunityStats.posts_count
        elif sort_by == 'comments':
            order_column = CommunityStats.comments_count
        else:
            order_column = cls.created_at

        if sort_order == 'asc':
            query = query.order_by(order_column.asc())
        else:
            query = query.order_by(order_column.desc())

        paginated_subscriptions = db.paginate(
            query, 
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        return paginated_subscriptions
    
    @classmethod
    def get_subscribers_by_community(cls, community, args):
        """
        Get a list of users subscribed to the community.

        :param community: The community object.
        :param args: The request arguments.

        :return: List of user objects
        """

        from app.models.user import User
        from app.models.user import UserStats

        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        @filtered_users
        def get_query(community):
            query = (
                db.select(User)
                .join(cls, User.id == cls.user_id)
                .join(UserStats, User.id == UserStats.user_id)
                .where(cls.community_id == community.id)
            )

            if time_filter != 'all':
                now = datetime.now(timezone.utc)

                if time_filter == 'day':
                    start_date = now - timedelta(days=1)
                elif time_filter == 'week':
                    start_date = now - timedelta(weeks=1)
                elif time_filter == 'month':
                    start_date = now - timedelta(days=30)
                elif time_filter == 'year':
                    start_date = now - timedelta(days=365)
                else:
                    start_date = None

                if start_date:
                    query = query.filter(cls.created_at >= start_date)

            if sort_by == 'followers':
                order_column = UserStats.followers_count
            elif sort_by == 'communities':
                order_column = UserStats.communities_count
            elif sort_by == 'posts':
                order_column = UserStats.posts_count
            elif sort_by == 'comments':
                order_column = UserStats.comments_count
            else:
                order_column = cls.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())
        
            return query
        
        query = get_query(community)

        paginated_subscribers = db.paginate(
            query, 
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        return paginated_subscribers


class CommunityModerator(db.Model):
    __tablename__ = 'community_moderators'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', back_populates='moderations')
    community = db.relationship('Community', back_populates='moderators')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_community(cls, user, community):
        """
        Get the moderation object by user and community.

        :param user: The user object.
        :param community: The community object.

        :return: The moderation object
        """
        moderation = db.session.get(cls, (user.id, community.id))

        return moderation
    
    @classmethod
    def get_moderations_by_user(cls, user):
        """
        Get a list of communities the user is a moderator of.

        :param user: The user object.

        :return: List of community objects.
        """
        query = db.select(cls).where(cls.user_id == user.id)

        moderations = db.session.scalars(query).all()

        moderations = [moderation.community for moderation in moderations]

        return moderations
    
    @classmethod
    def get_moderators_by_community(cls, community, args):
        """
        Get a list of users who are moderators of the community.
        
        :param community: The community object.
        :param args: The request arguments.

        :return: List of user objects.
        """

        from app.models.user import User
        from app.models.user import UserStats

        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')
        
        query = (
            db.select(User)
            .join(cls, User.id == cls.user_id)
            .join(UserStats, User.id == UserStats.user_id)
            .where(cls.community_id == community.id)
        )

        if time_filter != 'all':
            now = datetime.now(timezone.utc)

            if time_filter == 'day':
                start_date = now - timedelta(days=1)
            elif time_filter == 'week':
                start_date = now - timedelta(weeks=1)
            elif time_filter == 'month':
                start_date = now - timedelta(days=30)
            elif time_filter == 'year':
                start_date = now - timedelta(days=365)
            else:
                start_date = None

            if start_date:
                query = query.filter(cls.created_at >= start_date)

        if sort_by == 'followers':
            order_column = UserStats.followers_count
        elif sort_by == 'communities':
            order_column = UserStats.communities_count
        elif sort_by == 'posts':
            order_column = UserStats.posts_count
        elif sort_by == 'comments':
            order_column = UserStats.comments_count
        else:
            order_column = cls.created_at

        if sort_order == 'asc':
            query = query.order_by(order_column.asc())
        else:
            query = query.order_by(order_column.desc())

        paginated_moderators = db.paginate(
            query, 
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        return paginated_moderators


class CommunityBan(db.Model):
    __tablename__ = 'community_bans'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', back_populates='bans')
    community = db.relationship('Community', back_populates='banned')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_community(cls, user, community):
        """
        Get the ban object by user and community.
        
        :param user: The user object.
        :param community: The community object.
        
        :return: The ban object
        """

        ban = db.session.get(cls, (user.id, community.id))

        return ban
    
    @classmethod
    def get_bans_by_user(cls, user):
        """
        Get a list of communities the user is banned from.
        
        :param user: The user object.
        
        :return: List of community objects.
        """
        query = db.select(cls).where(cls.user_id == user.id)

        bans = db.session.scalars(query).all()

        bans = [ban.community for ban in bans]

        return bans
    
    @classmethod
    def get_banned_by_community(cls, community, args):
        """
        Get a list of users banned from the community.
        
        :param community: The community object.
        :param args: The request arguments.
        
        :return: List of user objects.
        """
        from app.models.user import User
        from app.models.user import UserStats

        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        query = (
            db.select(User)
            .join(cls, User.id == cls.user_id)
            .join(UserStats, User.id == UserStats.user_id)
            .where(cls.community_id == community.id)
        )

        if time_filter != 'all':
            now = datetime.now(timezone.utc)

            if time_filter == 'day':
                start_date = now - timedelta(days=1)
            elif time_filter == 'week':
                start_date = now - timedelta(weeks=1)
            elif time_filter == 'month':
                start_date = now - timedelta(days=30)
            elif time_filter == 'year':
                start_date = now - timedelta(days=365)
            else:
                start_date = None

            if start_date:
                query = query.filter(cls.created_at >= start_date)

        if sort_by == 'followers':
                order_column = UserStats.followers_count
        elif sort_by == 'communities':
            order_column = UserStats.communities_count
        elif sort_by == 'posts':
            order_column = UserStats.posts_count
        elif sort_by == 'comments':
            order_column = UserStats.comments_count
        else:
            order_column = cls.created_at

        if sort_order == 'asc':
            query = query.order_by(order_column.asc())
        else:
            query = query.order_by(order_column.desc())

        banned_users = db.paginate(
            query, 
            page=page, 
            per_page=per_page,
            error_out=False
        )

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

    subscribers = db.relationship('CommunitySubscriber', back_populates='community', cascade="all, delete-orphan")
    moderators = db.relationship('CommunityModerator', back_populates='community', cascade="all, delete-orphan")
    banned = db.relationship('CommunityBan', back_populates='community', cascade="all, delete-orphan")
    stats = db.relationship('CommunityStats', back_populates='community', uselist=False, cascade="all, delete-orphan")

    # Post
    posts = db.relationship('Post', cascade='all, delete', back_populates='community', lazy='dynamic')

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
    def get_all(cls, args):
        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')
        
        query = db.select(cls).join(CommunityStats, cls.id == CommunityStats.community_id)

        if time_filter != 'all':
            now = datetime.now(timezone.utc)

            if time_filter == 'day':
                start_date = now - timedelta(days=1)
            elif time_filter == 'week':
                start_date = now - timedelta(weeks=1)
            elif time_filter == 'month':
                start_date = now - timedelta(days=30)
            elif time_filter == 'year':
                start_date = now - timedelta(days=365)
            else:
                start_date = None

            if start_date:
                query = query.filter(cls.created_at >= start_date)

        if sort_by == 'subscribers':
            order_column = CommunityStats.subscribers_count
        elif sort_by == 'posts':
            order_column = CommunityStats.posts_count
        elif sort_by == 'comments':
            order_column = CommunityStats.comments_count
        else:
            order_column = cls.created_at

        if sort_order == 'asc':
            query = query.order_by(order_column.asc())
        else:
            query = query.order_by(order_column.desc())

        paginated_communities = db.paginate(
            query, 
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        return paginated_communities
    
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


