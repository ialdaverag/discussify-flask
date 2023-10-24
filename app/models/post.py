from app.extensions.database import db
from app.errors.errors import NotFoundError
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

    @classmethod
    def get_by_user_and_post(self, user, post):
        vote = PostVote.query.filter_by(user=user, post=post).first()

        return vote

    def is_upvote(self):
        return self.direction == 1
    
    def is_downvote(self):
        return self.direction == -1
    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
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

    bookmarkers = db.relationship('User', secondary=post_bookmarks, backref='bookmarks')
    comments = db.relationship('Comment', cascade='all, delete', backref='post', lazy='dynamic')
    post_votes = db.relationship('PostVote', cascade='all, delete', backref='post')

    @classmethod
    def get_by_id(self, id):
        post = Post.query.get(id)

        if post is None:
            raise NotFoundError('Post not found')
        
        return post
    
    def belongs_to(self, user):
        return self.owner is user
    
    def is_bookmarked_by(self, user):
        return user in self.bookmarkers
