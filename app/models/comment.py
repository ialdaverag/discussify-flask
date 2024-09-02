# Flask-JWT-Extended
from flask_jwt_extended import current_user

# Extensions
from app.extensions.database import db

# Decorators
from app.decorators.filtered_users_select import filtered_users_select
from app.decorators.filtered_users import filtered_users
from app.decorators.filtered_comments import filtered_comments

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
    @filtered_comments
    def get_bookmarks_by_user(cls, user):
        query = db.select(cls).where(cls.user_id == user.id)

        bookmarks = db.session.scalars(query).all()

        bookmarks = [bookmark.comment for bookmark in bookmarks]

        return bookmarks


class CommentVote(db.Model):
    __tablename__ = 'comment_votes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    direction = db.Column(db.Integer, nullable=False)

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
    @filtered_comments
    def get_upvoted_comments_by_user(cls, user):
        query = db.select(cls).where(cls.user_id == user.id, cls.direction == 1)

        upvotes = db.session.scalars(query).all()

        upvotes = [upvote.comment for upvote in upvotes]

        return upvotes
    
    @classmethod
    @filtered_comments
    def get_downvoted_comments_by_user(cls, user):
        query = db.select(cls).where(cls.user_id == user.id, cls.direction == -1)

        downvotes = db.session.scalars(query).all()

        downvotes = [downvote.comment for downvote in downvotes]

        return downvotes
    
    @classmethod
    def get_upvoters_by_comment(cls, comment, args):
        from app.models.user import User

        page = args.get('page')
        per_page = args.get('per_page')

        @filtered_users_select
        def get_query():
            query = (
                db.select(User)
                .join(cls, User.id == cls.user_id)
                .where(cls.comment_id == comment.id, cls.direction == 1)
            )

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

        page = args.get('page')
        per_page = args.get('per_page')

        @filtered_users_select
        def get_query():
            query = (
                db.select(User)
                .join(cls, User.id == cls.user_id)
                .where(cls.comment_id == comment.id, cls.direction == -1)
            )

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
    comment_bookmarkers = db.relationship('CommentBookmark', back_populates='comment')

    # Post
    post = db.relationship('Post', back_populates='comments')

    # Comment
    replies = db.relationship('Comment', backref=db.backref('comment', remote_side=[id]), lazy='dynamic')

    # CommentVote
    comment_votes = db.relationship('CommentVote', back_populates='comment', cascade='all, delete')

    # Stats
    stats = db.relationship('CommentStats', uselist=False, back_populates='comment')

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
        comment = db.session.get(cls, id)

        if comment is None:
            raise NotFoundError('Comment not found.')
        
        return comment
    
    @classmethod
    @filtered_comments
    def get_all(cls):
        query = db.select(cls)

        comments =  db.session.scalars(query).all()

        return comments
    
    @classmethod
    @filtered_comments
    def get_all_by_user(cls, user):
        query = db.select(cls).where(cls.user_id == user.id)

        comments = db.session.scalars(query).all()

        return comments
    
    @classmethod
    @filtered_comments
    def get_all_root_comments_by_post(cls, post):
        query = db.select(cls).where(cls.comment_id == None, cls.post_id == post.id)

        root_comments = db.session.scalars(query).all()

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
        return self.owner.id == user.id
    
    def is_bookmarked_by(self, user):
        bookmark = CommentBookmark.get_by_user_and_comment(user, self)

        return bookmark is not None

    def is_upvoted_by(self, user):
        vote = CommentVote.get_by_user_and_comment(user, self)

        return vote.is_upvote() if vote else False

    def is_downvoted_by(self, user):
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
def increment_upvotes_count_on_comment_stats(mapper, connection, target):
    from app.models.comment import CommentStats

    comment_stats_table = CommentStats.__table__

    update_query = comment_stats_table.update().where(
        comment_stats_table.c.comment_id == target.comment_id
    ).values(
        upvotes_count=comment_stats_table.c.upvotes_count + 1
    )

    connection.execute(update_query)


@db.event.listens_for(CommentVote, 'after_delete')
def decrement_upvotes_count_on_comment_stats(mapper, connection, target):
    from app.models.comment import CommentStats

    comment_stats_table = CommentStats.__table__

    update_query = comment_stats_table.update().where(
        comment_stats_table.c.comment_id == target.comment_id
    ).values(
        upvotes_count=comment_stats_table.c.upvotes_count - 1
    )

    connection.execute(update_query)


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
