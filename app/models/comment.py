from extensions.database import db

comment_bookmarks = db.Table(
    'comment_bookmarks',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'))
)


class CommentVote(db.Model):
    __tablename__ = 'comment_votes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    direction = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='comment_votes')
    #comment = db.relationship('Comment', backref='comment_votes')


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    replies = db.relationship('Comment', backref=db.backref('comment', remote_side=[id]), lazy='dynamic')
    comment_bookmarkers = db.relationship('User', secondary=comment_bookmarks, backref='comment_bookmarks')
    comment_votes = db.relationship('CommentVote', cascade='all, delete', backref='comment')