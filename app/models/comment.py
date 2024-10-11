# Datetime
from datetime import datetime, timedelta, timezone

# Flask-JWT-Extended
from flask_jwt_extended import current_user

# Extensions
from app.extensions.database import db

# Decorators
from app.decorators.filters import filtered_users
from app.decorators.filters import filtered_comments

# Errors
from app.errors.errors import NotFoundError


class CommentBookmark(db.Model):
    __tablename__ = 'comment_bookmarks'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # User
    user = db.relationship('User', back_populates='comment_bookmarks')

    # Comment
    comment = db.relationship('Comment', back_populates='comment_bookmarkers')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_comment(cls, user, comment):
        bookmark = db.session.get(cls, (user.id, comment.id))

        return bookmark
    
    @classmethod
    def get_bookmarks_by_user(cls, user, args):
        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')
              
        @filtered_comments
        def get_query():
            query = (
                db.select(Comment)
                .join(cls, cls.comment_id == Comment.id)
                .join(CommentStats, Comment.id == CommentStats.comment_id)
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

            if sort_by == 'upvotes':
                order_column = CommentStats.upvotes_count
            else:
                order_column = Comment.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query
        
        query = get_query()

        bookmarks = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return bookmarks


class CommentVote(db.Model):
    __tablename__ = 'comment_votes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    direction = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # User
    user = db.relationship('User', back_populates='comment_votes')

    # Comment
    comment = db.relationship('Comment', back_populates='comment_votes')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_comment(cls, user, comment):
        vote = db.session.get(cls, (user.id, comment.id))

        return vote
    
    @classmethod
    def get_upvoted_comments_by_user(cls, user, args):
        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')
                            
        @filtered_comments
        def get_query():
            query = (
                db.select(Comment)
                .join(cls, cls.comment_id == Comment.id)
                .join(CommentStats, Comment.id == CommentStats.comment_id)
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
                order_column = CommentStats.upvotes_count
            else:
                order_column = Comment.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query
        
        query = get_query()

        upvoted_comments = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return upvoted_comments
    
    @classmethod
    def get_downvoted_comments_by_user(cls, user, args):
        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')
                            
        @filtered_comments
        def get_query():
            query = (
                db.select(Comment)
                .join(cls, cls.comment_id == Comment.id)
                .join(CommentStats, Comment.id == CommentStats.comment_id)
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
                    query = query.filter(cls.created_at >= start_date)

            if sort_by == 'upvotes':
                order_column = CommentStats.upvotes_count
            else:
                order_column = Comment.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query
        
        query = get_query()

        downvoted_comments = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return downvoted_comments
    
    @classmethod
    def get_upvoters_by_comment(cls, comment, args):
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
                .where(cls.comment_id == comment.id, cls.direction == 1)
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

        paginated_upvoters = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return paginated_upvoters
    
    @classmethod
    def get_downvoters_by_comment(cls, comment, args):
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
                .where(cls.comment_id == comment.id, cls.direction == -1)
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

        paginated_downvoters = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return paginated_downvoters
    
    def is_upvote(self):
        return self.direction == 1
    
    def is_downvote(self):
        return self.direction == -1


class CommentStats(db.Model):
    __tablename__ = 'comment_stats'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), unique=True)
    bookmarks_count = db.Column(db.Integer, default=0)
    upvotes_count = db.Column(db.Integer, default=0)
    downvotes_count = db.Column(db.Integer, default=0)

    # Comment
    comment = db.relationship('Comment', back_populates='stats')

    def save(self):
        db.session.add(self)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # User
    owner = db.relationship('User', back_populates='comments')
    comment_bookmarkers = db.relationship('CommentBookmark', 
                                         back_populates='comment',
                                         cascade='all, delete-orphan')

    # Post
    post = db.relationship('Post', back_populates='comments')

    # Comment
    replies = db.relationship('Comment', 
                             backref=db.backref('comment', remote_side=[id]),
                             cascade='all, delete-orphan',
                             lazy='dynamic')

    # CommentVote
    comment_votes = db.relationship('CommentVote', 
                                   back_populates='comment', 
                                   cascade='all, delete-orphan')

    # Stats
    stats = db.relationship('CommentStats', 
                           uselist=False, 
                           back_populates='comment',
                           cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.stats = CommentStats(comment=self)
        self.stats.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        '''
        Get a comment by its ID.
        
        :param id: The comment ID.
        
        :return: The comment object.
        '''

        comment = db.session.get(cls, id)

        if comment is None:
            raise NotFoundError('Comment not found.')
        
        return comment
    
    @classmethod
    def get_all(cls, args):
        '''
        Get all comments.
        
        :param args: The request arguments.
        
        :return: Paginated list of comments
        '''

        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        @filtered_comments
        def get_query():
            query = db.select(cls).join(CommentStats, cls.id == CommentStats.comment_id)

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
                order_column = CommentStats.upvotes_count
            else:
                order_column = cls.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query

        query = get_query()

        paginated_comments = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return paginated_comments
    
    @classmethod
    def get_all_by_user(cls, user, args):
        '''
        Get all comments by a given user.
        
        :param user: The user object.
        :param args: The request arguments.
        
        :return: Paginated list of comments
        '''

        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        @filtered_comments
        def get_query():
            query = db.select(cls).join(CommentStats, cls.id == CommentStats.comment_id).where(cls.user_id == user.id)

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
                order_column = CommentStats.upvotes_count
            else:
                order_column = cls.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

            return query
        
        query = get_query()

        paginated_comments = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return paginated_comments
    
    @classmethod
    def get_all_root_comments_by_post(cls, post, args):
        """
        Get all root comments for a given post.

        :param post: The post object.
        :param args: The request arguments.

        :return: Paginated list of root comments
        """
        
        page = args.get('page')
        per_page = args.get('per_page')
        time_filter = args.get('time_filter')
        sort_by = args.get('sort_by')
        sort_order = args.get('sort_order')

        @filtered_comments
        def get_query(post):
            query = (
                db.select(cls)
                .join(CommentStats, cls.id == CommentStats.comment_id)
                .where(cls.comment_id == None, cls.post_id == post.id)
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
                order_column = CommentStats.upvotes_count
            else:
                order_column = cls.created_at

            if sort_order == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())
            
            return query
        
        query = get_query(post)

        root_comments = db.paginate(
            query,
            page=page,
            per_page=per_page,
            error_out=False
        )

        return root_comments
    
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
        '''
        Check if the comment belongs to a given user.
        
        :param user: The user object.
        
        :return: True if the comment belongs to the user, False otherwise.
        '''

        return self.owner.id == user.id
    
    def is_bookmarked_by(self, user):
        '''
        Check if the comment is bookmarked by a given user.
        
        :param user: The user object.
        
        :return: True if the comment is bookmarked by the user, False otherwise.
        '''

        bookmark = CommentBookmark.get_by_user_and_comment(user, self)

        return bookmark is not None

    def is_upvoted_by(self, user):
        '''
        Check if the comment is upvoted by a given user.
        
        :param user: The user object.
        
        :return: True if the comment is upvoted by the user, False otherwise.
        '''

        vote = CommentVote.get_by_user_and_comment(user, self)

        return vote.is_upvote() if vote else False

    def is_downvoted_by(self, user):
        '''
        Check if the comment is downvoted by a given user.
        
        :param user: The user object.
        
        :return: True if the comment is downvoted by the user, False otherwise.
        '''

        vote = CommentVote.get_by_user_and_comment(user, self)

        return vote.is_downvote() if vote else False
    
    
@db.event.listens_for(Comment, 'after_insert')
def increment_comments_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.user_id
    ).values(
        comments_count=user_stats_table.c.comments_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(Comment, 'after_delete')
def decrement_comments_count_on_user_stats(mapper, connection, target):
    from app.models.user import UserStats

    user_stats_table = UserStats.__table__

    update_query = user_stats_table.update().where(
        user_stats_table.c.user_id == target.user_id
    ).values(
        comments_count=user_stats_table.c.comments_count - 1
    )

    connection.execute(update_query)


@db.event.listens_for(Comment, 'after_insert')
def increment_comments_count_on_community_stats(mapper, connection, target):
    from app.models.community import CommunityStats

    community_stats_table = CommunityStats.__table__

    update_query = community_stats_table.update().where(
        community_stats_table.c.community_id == target.post.community_id
    ).values(
        comments_count=community_stats_table.c.comments_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(Comment, 'after_delete')
def decrement_comments_count_on_community_stats(mapper, connection, target):
    from app.models.community import CommunityStats

    community_stats_table = CommunityStats.__table__

    update_query = community_stats_table.update().where(
        community_stats_table.c.community_id == target.post.community_id
    ).values(
        comments_count=community_stats_table.c.comments_count - 1
    )

    connection.execute(update_query)


@db.event.listens_for(Comment, 'after_insert')
def increment_comments_count_on_post_stats(mapper, connection, target):
    from app.models.post import PostStats

    post_stats_table = PostStats.__table__

    update_query = post_stats_table.update().where(
        post_stats_table.c.post_id == target.post_id
    ).values(
        comments_count=post_stats_table.c.comments_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(Comment, 'after_delete')
def decrement_comments_count_on_post_stats(mapper, connection, target):
    from app.models.post import PostStats

    post_stats_table = PostStats.__table__

    update_query = post_stats_table.update().where(
        post_stats_table.c.post_id == target.post_id
    ).values(
        comments_count=post_stats_table.c.comments_count - 1
    )

    connection.execute(update_query)


@db.event.listens_for(CommentVote, 'after_insert')
def increment_votes_count_on_comment_stats(mapper, connection, target):
    from app.models.comment import CommentStats

    comment_stats_table = CommentStats.__table__

    if target.direction == 1:  # upvote
        update_query = comment_stats_table.update().where(
            comment_stats_table.c.comment_id == target.comment_id
        ).values(
            upvotes_count=comment_stats_table.c.upvotes_count + 1
        )
    elif target.direction == -1:  # downvote
        update_query = comment_stats_table.update().where(
            comment_stats_table.c.comment_id == target.comment_id
        ).values(
            downvotes_count=comment_stats_table.c.downvotes_count + 1
        )

    connection.execute(update_query)


@db.event.listens_for(CommentVote, 'after_delete')
def decrement_votes_count_on_comment_stats(mapper, connection, target):
    from app.models.comment import CommentStats

    comment_stats_table = CommentStats.__table__

    if target.direction == 1:  # upvote
        update_query = comment_stats_table.update().where(
            comment_stats_table.c.comment_id == target.comment_id
        ).values(
            upvotes_count=comment_stats_table.c.upvotes_count - 1
        )
    elif target.direction == -1:  # downvote
        update_query = comment_stats_table.update().where(
            comment_stats_table.c.comment_id == target.comment_id
        ).values(
            downvotes_count=comment_stats_table.c.downvotes_count - 1
        )

    connection.execute(update_query)


@db.event.listens_for(CommentVote.direction, 'set')
def update_votes_count_on_comment_stats(target, value, oldvalue, initiator):
    from app.models.comment import CommentStats

    comment_stats_table = CommentStats.__table__

    if oldvalue is not None and oldvalue != value:  # the vote direction has changed
        if value == 1:  # changed to upvote
            update_query = comment_stats_table.update().where(
                comment_stats_table.c.comment_id == target.comment_id
            ).values(
                upvotes_count=comment_stats_table.c.upvotes_count + 1,
                downvotes_count=comment_stats_table.c.downvotes_count - 1
            )
        elif value == -1:  # changed to downvote
            update_query = comment_stats_table.update().where(
                comment_stats_table.c.comment_id == target.comment_id
            ).values(
                upvotes_count=comment_stats_table.c.upvotes_count - 1,
                downvotes_count=comment_stats_table.c.downvotes_count + 1
            )

        db.session.execute(update_query)



@db.event.listens_for(CommentBookmark, 'after_insert')
def increment_bookmarks_count_on_comment_stats(mapper, connection, target):
    comment_stats_table = CommentStats.__table__

    update_query = comment_stats_table.update().where(
        comment_stats_table.c.comment_id == target.comment_id
    ).values(
        bookmarks_count=comment_stats_table.c.bookmarks_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(CommentBookmark, 'after_delete')
def decrement_bookmarks_count_on_comment_stats(mapper, connection, target):
    comment_stats_table = CommentStats.__table__

    update_query = comment_stats_table.update().where(
        comment_stats_table.c.comment_id == target.comment_id
    ).values(
        bookmarks_count=comment_stats_table.c.bookmarks_count - 1
    )

    connection.execute(update_query)
