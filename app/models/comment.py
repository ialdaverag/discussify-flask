from flask_jwt_extended import current_user

from app.extensions.database import db
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
        bookmark = CommentBookmark.query.filter_by(user_id=user.id, comment_id=comment.id).first()

        return bookmark
    
    @classmethod
    def get_bookmarks_by_user(cls, user):
        bookmarks = CommentBookmark.query.filter_by(user_id=user.id).all()

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

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user_and_comment(cls, user, comment):
        vote = CommentVote.query.filter_by(user_id=user.id, comment_id=comment.id).first()

        return vote
    
    @classmethod
    def get_upvoted_comments_by_user(cls, user):
        upvotes = CommentVote.query.filter_by(user_id=user.id, direction=1).all()

        return upvotes
    
    @classmethod
    def get_downvoted_comments_by_user(cls, user):
        downvotes = CommentVote.query.filter_by(user_id=user.id, direction=-1).all()

        return downvotes
    
    @classmethod
    def get_upvoters_by_comment(cls, comment):
        upvotes = CommentVote.query.filter_by(comment_id=comment.id, direction=1).all()

        return [upvote.user for upvote in upvotes]
    
    @classmethod
    def get_downvoters_by_comment(cls, comment):
        downvotes = CommentVote.query.filter_by(comment_id=comment.id, direction=-1).all()

        return [downvote.user for downvote in downvotes]
    
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
    stats = db.relationship('CommentStats', backref='comment', uselist=False, cascade='all, delete')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.stats = CommentStats(comment=self)

    @classmethod
    def get_by_id(cls, id):
        comment = db.session.get(Comment, id)

        if comment is None:
            raise NotFoundError('Comment not found.')
        
        return comment
    
    @classmethod
    def get_all(cls):
        return db.session.scalars(db.select(Comment)).all()
    
    @property
    def bookmarked(self):
        return self.is_bookmarked_by(current_user)
    
    @property
    def upvoted(self):
        return self.is_upvoted_by(current_user)
    
    @property
    def downvoted(self):
        return self.is_downvoted_by(current_user)
    
    def belongs_to(self, user):
        return self.owner is user
    
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
