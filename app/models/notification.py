# Datetime
from datetime import datetime

# Extensions
from app.extensions.database import db

# Errors
from app.errors.errors import NotFoundError


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'follow', 'comment', 'community_join', etc.
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # recipient
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # who triggered the notification
    
    # Optional references to related entities
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'), nullable=True)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], back_populates='notifications')
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_notifications')
    post = db.relationship('Post', back_populates='notifications')
    comment = db.relationship('Comment', back_populates='notifications')
    community = db.relationship('Community', back_populates='notifications')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def mark_as_read(self):
        self.is_read = True
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        notification = db.session.get(cls, id)
        
        if not notification:
            raise NotFoundError('Notification not found.')
        
        return notification

    @classmethod
    def get_by_user(cls, user, args):
        page = args.get('page', 1)
        per_page = args.get('per_page', 20)
        is_read = args.get('is_read')

        query = cls.query.filter_by(user_id=user.id)
        
        if is_read is not None:
            query = query.filter_by(is_read=is_read)
        
        notifications = query.order_by(cls.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return notifications

    @classmethod
    def mark_all_as_read_for_user(cls, user):
        """Mark all notifications for a user as read."""
        cls.query.filter_by(user_id=user.id, is_read=False).update({'is_read': True})
        db.session.commit()

    @classmethod
    def get_unread_count_for_user(cls, user):
        """Get count of unread notifications for a user."""
        return cls.query.filter_by(user_id=user.id, is_read=False).count()