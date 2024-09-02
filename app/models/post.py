# Flask-JWT-Extended
from flask_jwt_extended import current_user

# Extensions
from app.extensions.database import db

# Errors
from app.errors.errors import NotFoundError

# Models
from app.models.comment import Comment

# Decorators
from app.decorators.filtered_users_select import filtered_users_select
from app.decorators.filtered_users import filtered_users
from app.decorators.filtered_posts import filtered_posts


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
    @filtered_posts
    def get_bookmarks_by_user(cls, user):
        from app.models.post import Post 

        query = (
            db.select(Post)
            .join(cls, Post.id == cls.post_id)
            .where(cls.user_id == user.id)
        )

        bookmarks = db.session.scalars(query).all()

        return bookmarks


class PostVote(db.Model):
    __tablename__ = 'post_votes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    direction = db.Column(db.Integer, nullable=False)

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

        page = args.get('page')
        per_page = args.get('per_page')

        @filtered_users_select
        def get_query():
            query = (
                db.select(User)
                .join(cls, User.id == cls.user_id)
                .where(cls.post_id == post.id, cls.direction == 1)
            )

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

        page = args.get('page')
        per_page = args.get('per_page')

        @filtered_users_select
        def get_query():
            query = (
                db.select(User)
                .join(cls, User.id == cls.user_id)
                .where(cls.post_id == post.id, cls.direction == -1)
            )

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
    @filtered_posts
    def get_upvoted_posts_by_user(cls, user):
        query = db.select(cls).where(cls.user_id == user.id, cls.direction == 1)

        upvotes = db.session.scalars(query).all()

        posts = [upvote.post for upvote in upvotes]

        return posts
    
    @classmethod
    @filtered_posts
    def get_downvoted_posts_by_user(cls, user):
        query = db.select(cls).where(cls.user_id == user.id, cls.direction == -1)

        downvotes = db.session.scalars(query).all()

        posts = [downvote.post for downvote in downvotes]

        return posts
    
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
    bookmarkers = db.relationship('PostBookmark', back_populates='post')

    # Community
    community = db.relationship('Community', back_populates='posts')

    # Comment
    comments = db.relationship('Comment', cascade='all, delete', back_populates='post', lazy='dynamic')

    # PostVote
    post_votes = db.relationship('PostVote', cascade='all, delete', back_populates='post')

    # Stats
    stats = db.relationship('PostStats', uselist=False, back_populates='post')

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
    @filtered_posts
    def get_all(cls):
        query = db.select(cls)

        posts = db.session.scalars(query).all()

        return posts
    
    @classmethod
    @filtered_posts
    def get_all_by_community(cls, community):
        query = db.select(cls).where(cls.community_id == community.id)

        posts = db.session.scalars(query).all()

        return posts
    
    @classmethod
    @filtered_posts
    def get_all_by_user(cls, user):
        query = db.select(cls).where(cls.user_id == user.id)

        posts = db.session.scalars(query).all()

        return posts
    
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
