# Datetime
from datetime import datetime
from datetime import timedelta
from datetime import timezone

# Flask-JWT-Extended
from flask_jwt_extended import current_user

# Extensions
from app.extensions.database import db

# Errors
from app.errors.errors import NotFoundError

# Models
from app.models.comment import Comment

# Decorators
from app.decorators.filters import filtered_users
from app.decorators.filters import filtered_posts


class PostBookmark(db.Model):
    __tablename__ = 'post_bookmarks'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # User
    user = db.relationship('User', back_populates='bookmarks')

    # Post
    post = db.relationship('Post', back_populates='bookmarkers')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_post(cls, user, post):
        bookmark = db.session.get(cls, (user.id, post.id))

        return bookmark
    
    @classmethod
    def get_bookmarks_by_user(cls, user, args):
        from app.models.post import Post
        from app.models.post import PostStats

        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        @filtered_posts
        def get_query():
            # Get the posts marked as bookmarks and join with PostStats
            query = (
                db.select(Post)
                .join(cls, Post.id == cls.post_id)
                .join(PostStats, Post.id == PostStats.post_id)
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

            # Determine the order column
            if sort_by == 'upvotes':
                order_column = PostStats.upvotes_count
            elif sort_by == 'comments':
                order_column = PostStats.comments_count
            else:  # Default to 'created_at'
                order_column = Post.created_at

            # Apply sorting
            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query
        
        query = get_query()

        paginated_bookmarks = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return paginated_bookmarks



class PostVote(db.Model):
    __tablename__ = 'post_votes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    direction = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # User
    user = db.relationship('User', back_populates='post_votes')

    # Post
    post = db.relationship('Post', back_populates='post_votes')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_post(cls, user, post):
        vote = db.session.get(cls, (user.id, post.id))

        return vote
    
    @classmethod
    def get_upvoters_by_post(cls, post, args):
        from app.models.user import User
        from app.models.user import UserStats

        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        @filtered_users
        def get_query():
            query = (
                db.select(User)
                .join(cls, User.id == cls.user_id)
                .join(UserStats, User.id == UserStats.user_id)
                .where(cls.post_id == post.id, cls.direction == 1)
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
        
        query = get_query()

        upvoters = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return upvoters
    
    @classmethod
    def get_downvoters_by_post(cls, post, args):
        from app.models.user import User
        from app.models.user import UserStats

        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        @filtered_users
        def get_query():
            query = (
                db.select(User)
                .join(cls, User.id == cls.user_id)
                .join(UserStats, User.id == UserStats.user_id)
                .where(cls.post_id == post.id, cls.direction == -1)
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
        
        query = get_query()

        downvoters = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return downvoters
    
    @classmethod
    def get_upvoted_posts_by_user(cls, user, args):
        from app.models.post import Post
        from app.models.post import PostStats

        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        @filtered_posts
        def get_query():
            query = (
                db.select(Post)
                .join(cls, Post.id == cls.post_id)
                .join(PostStats, Post.id == PostStats.post_id)
                .where(cls.user_id == user.id, cls.direction == 1)
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

            if sort_by == 'upvotes':
                order_column = PostStats.upvotes_count
            elif sort_by == 'comments':
                order_column = PostStats.comments_count
            else:
                order_column = Post.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query
        
        query = get_query()

        paginated_upvoted_posts = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return paginated_upvoted_posts
    
    @classmethod
    def get_downvoted_posts_by_user(cls, user, args):
        from app.models.post import Post
        from app.models.post import PostStats

        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        @filtered_posts
        def get_query():
            query = (
                db.select(Post)
                .join(cls, Post.id == cls.post_id)
                .join(PostStats, Post.id == PostStats.post_id)
                .where(cls.user_id == user.id, cls.direction == -1)
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
                    query = query.filter(Post.created_at >= start_date)

            if sort_by == 'upvotes':
                order_column = PostStats.upvotes_count
            elif sort_by == 'comments':
                order_column = PostStats.comments_count
            else:
                order_column = Post.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query
        
        query = get_query()

        paginated_downvoted_posts = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return paginated_downvoted_posts
    
    def is_upvote(self):
        return self.direction == 1
    
    def is_downvote(self):
        return self.direction == -1


class PostStats(db.Model):
    __tablename__ = 'post_stats'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), unique=True)
    comments_count = db.Column(db.Integer, default=0)
    bookmarks_count = db.Column(db.Integer, default=0)
    upvotes_count = db.Column(db.Integer, default=0)
    downvotes_count = db.Column(db.Integer, default=0)

    # Post
    post = db.relationship('Post', back_populates='stats', uselist=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # User
    owner = db.relationship('User', back_populates='posts')
    bookmarkers = db.relationship('PostBookmark', 
                                 back_populates='post',
                                 cascade='all, delete-orphan')

    # Community
    community = db.relationship('Community', back_populates='posts')

    # Comment
    comments = db.relationship('Comment', 
                              cascade='all, delete-orphan', 
                              back_populates='post', 
                              lazy='dynamic')

    # PostVote
    post_votes = db.relationship('PostVote', 
                                cascade='all, delete-orphan', 
                                back_populates='post')

    # Stats
    stats = db.relationship('PostStats', 
                           uselist=False, 
                           back_populates='post',
                           cascade='all, delete-orphan')
    
    # Notifications
    notifications = db.relationship('Notification', back_populates='post', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.stats = PostStats(post=self)
        self.stats.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        post = db.session.get(cls, id)

        if post is None:
            raise NotFoundError('Post not found.')
        
        return post
    
    @classmethod
    def get_all(cls, args):
        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter', 'all')
        sort_by = args.get('sort_by', 'created_at')
        sort_order = args.get('sort_order', 'desc')

        @filtered_posts
        def get_query():
            query = db.select(cls).join(PostStats, cls.id == PostStats.post_id)

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

            if sort_by == 'upvotes':
                order_column = PostStats.upvotes_count
            elif sort_by == 'comments':
                order_column = PostStats.comments_count
            else:
                order_column = cls.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query

        query = get_query()

        paginated_posts = db.paginate(
            query, 
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        return paginated_posts

    @classmethod
    def get_all_by_community(cls, community, args):
        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order') 

        @filtered_posts
        def get_query(community):
            query = db.select(cls).join(PostStats, cls.id == PostStats.post_id).where(cls.community_id == community.id)

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

            if sort_by == 'upvotes':
                order_column = PostStats.upvotes_count
            elif sort_by == 'comments':
                order_column = PostStats.comments_count
            else:
                order_column = cls.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query

        query = get_query(community=community)

        paginated_posts = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return paginated_posts
    
    @classmethod
    def get_all_by_user(cls, user, args):
        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        @filtered_posts
        def get_query(user):
            query = db.select(cls).join(PostStats, cls.id == PostStats.post_id).where(cls.user_id == user.id)

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

            if sort_by == 'upvotes':
                order_column = PostStats.upvotes_count
            elif sort_by == 'comments':
                order_column = PostStats.comments_count
            else:
                order_column = cls.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query

        query = get_query(user=user)

        paginated_posts = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return paginated_posts
    
    @property
    def bookmarked(self):
        if current_user:
            return self.is_bookmarked_by(current_user)

        return None
    
    @property
    def upvoted(self):
        if current_user:
            return self.is_upvoted_by(current_user)

        return None
    
    @property
    def downvoted(self):
        if current_user:
            return self.is_downvoted_by(current_user)

        return None
    
    def belongs_to(self, user):
        return self.owner.id == user.id
    
    def is_bookmarked_by(self, user):
        bookmark = PostBookmark.get_by_user_and_post(user, self)
        
        return bookmark is not None
    
    def is_upvoted_by(self, user):
        vote = PostVote.get_by_user_and_post(user, self)

        return vote.is_upvote() if vote else False
    
    def is_downvoted_by(self, user):
        vote = PostVote.get_by_user_and_post(user, self)

        return vote.is_downvote() if vote else False
    
    def read_root_comments(self):
        root_comments = db.session.scalars(
            db.select(Comment).where(Comment.post_id == self.id, Comment.parent_id.is_(None))
        ).all()

        return root_comments


@db.event.listens_for(Post, 'after_insert')
def increment_posts_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.user_id
    ).values(
        posts_count=user_stats_table.c.posts_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(Post, 'after_delete')
def decrement_posts_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.user_id
    ).values(
        posts_count=user_stats_table.c.posts_count - 1
    )

    connection.execute(update_query)


@db.event.listens_for(Post, 'after_insert')
def increment_posts_count_on_community_stats(mapper, connection, target):
    from app.models.community import CommunityStats

    community_stats_table = CommunityStats.__table__

    update_query = community_stats_table.update().where(
        community_stats_table.c.community_id == target.community_id
    ).values(
        posts_count=community_stats_table.c.posts_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(Post, 'after_delete')
def decrement_posts_count_on_community_stats(mapper, connection, target):
    from app.models.community import CommunityStats

    community_stats_table = CommunityStats.__table__

    update_query = community_stats_table.update().where(
        community_stats_table.c.community_id == target.community_id
    ).values(
        posts_count=community_stats_table.c.posts_count - 1
    )

    connection.execute(update_query)


@db.event.listens_for(PostVote, 'after_insert')
def increment_votes_count_on_post_stats(mapper, connection, target):
    from app.models.post import PostStats

    post_stats_table = PostStats.__table__

    if target.direction == 1:  # upvote
        update_query = post_stats_table.update().where(
            post_stats_table.c.post_id == target.post_id
        ).values(
            upvotes_count=post_stats_table.c.upvotes_count + 1
        )
    elif target.direction == -1:  # downvote
        update_query = post_stats_table.update().where(
            post_stats_table.c.post_id == target.post_id
        ).values(
            downvotes_count=post_stats_table.c.downvotes_count + 1
        )

    connection.execute(update_query)


@db.event.listens_for(PostVote, 'after_delete')
def decrement_votes_count_on_post_stats(mapper, connection, target):
    from app.models.post import PostStats

    post_stats_table = PostStats.__table__

    if target.direction == 1:  # upvote
        update_query = post_stats_table.update().where(
            post_stats_table.c.post_id == target.post_id
        ).values(
            upvotes_count=post_stats_table.c.upvotes_count - 1
        )
    elif target.direction == -1:  # downvote
        update_query = post_stats_table.update().where(
            post_stats_table.c.post_id == target.post_id
        ).values(
            downvotes_count=post_stats_table.c.downvotes_count - 1
        )

    connection.execute(update_query)


@db.event.listens_for(PostVote.direction, 'set')
def update_votes_count_on_post_stats(target, value, oldvalue, initiator):
    from app.models.post import PostStats

    post_stats_table = PostStats.__table__

    if oldvalue is not None and oldvalue != value:  # the vote direction has changed
        if value == 1:  # changed to upvote
            update_query = post_stats_table.update().where(
                post_stats_table.c.post_id == target.post_id
            ).values(
                upvotes_count=post_stats_table.c.upvotes_count + 1,
                downvotes_count=post_stats_table.c.downvotes_count - 1
            )
        elif value == -1:  # changed to downvote
            update_query = post_stats_table.update().where(
                post_stats_table.c.post_id == target.post_id
            ).values(
                upvotes_count=post_stats_table.c.upvotes_count - 1,
                downvotes_count=post_stats_table.c.downvotes_count + 1
            )

        db.session.execute(update_query)


@db.event.listens_for(PostBookmark, 'after_insert')
def increment_bookmarks_count_on_post_stats(mapper, connection, target):
    post_stats_table = PostStats.__table__

    update_query = post_stats_table.update().where(
        post_stats_table.c.post_id == target.post_id
    ).values(
        bookmarks_count=post_stats_table.c.bookmarks_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(PostBookmark, 'after_delete')
def decrement_bookmarks_count_on_post_stats(mapper, connection, target):
    post_stats_table = PostStats.__table__

    update_query = post_stats_table.update().where(
        post_stats_table.c.post_id == target.post_id
    ).values(
        bookmarks_count=post_stats_table.c.bookmarks_count - 1
    )

    connection.execute(update_query)
