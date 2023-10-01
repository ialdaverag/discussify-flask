from app.extensions.database import db

from app.models.comment import Comment

post_bookmarks = db.Table(
    'post_bookmarks',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)


class PostVote(db.Model):
    __tablename__ = 'post_votes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    direction = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='votes')
    #post = db.relationship('Post', backref='votes')


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    bookmarkers = db.relationship('User', secondary=post_bookmarks, backref='bookmarks')
    comments = db.relationship('Comment', cascade='all, delete', backref='post', lazy='dynamic')
    post_votes = db.relationship('PostVote', cascade='all, delete', backref='post')