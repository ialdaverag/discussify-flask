# Flask-SocketIO
from flask_socketio import emit

# Extensions  
from app.extensions.socketio import socketio

# Models
from app.models.notification import Notification
from app.models.user import User

# Schemas
from app.schemas.notification import NotificationSchema

# Errors
from app.errors.errors import NotFoundError
from app.errors.errors import UnauthorizedError


class NotificationManager:
    @staticmethod
    def create_notification(title, message, notification_type, user_id, sender_id=None, 
                          post_id=None, comment_id=None, community_id=None):
        """Create a new notification and emit it via socket."""
        notification = Notification(
            title=title,
            message=message,
            type=notification_type,
            user_id=user_id,
            sender_id=sender_id,
            post_id=post_id,
            comment_id=comment_id,
            community_id=community_id
        )
        notification.save()
        
        # Emit notification via socket to the user's room
        NotificationManager.emit_notification(user_id, notification)
        
        return notification
    
    @staticmethod
    def emit_notification(user_id, notification):
        """Emit a notification to a specific user via socket."""
        schema = NotificationSchema()
        notification_data = schema.dump(notification)
        
        # Emit to user's room (users join rooms when they connect)
        socketio.emit(
            'new_notification', 
            notification_data, 
            room=f'user_{user_id}'
        )
    
    @staticmethod
    def create_follow_notification(follower, followed):
        """Create notification when a user follows another user."""
        title = "New Follower"
        message = f"{follower.username} started following you"
        
        return NotificationManager.create_notification(
            title=title,
            message=message,
            notification_type='follow',
            user_id=followed.id,
            sender_id=follower.id
        )
    
    @staticmethod
    def create_comment_notification(comment, post_owner):
        """Create notification when someone comments on a post."""
        title = "New Comment"
        message = f"{comment.owner.username} commented on your post"
        
        return NotificationManager.create_notification(
            title=title,
            message=message,
            notification_type='comment',
            user_id=post_owner.id,
            sender_id=comment.owner.id,
            post_id=comment.post.id,
            comment_id=comment.id
        )
    
    @staticmethod 
    def create_reply_notification(reply, parent_comment_owner):
        """Create notification when someone replies to a comment."""
        title = "New Reply"
        message = f"{reply.owner.username} replied to your comment"
        
        return NotificationManager.create_notification(
            title=title,
            message=message,
            notification_type='reply',
            user_id=parent_comment_owner.id,
            sender_id=reply.owner.id,
            post_id=reply.post.id,
            comment_id=reply.id
        )
    
    @staticmethod
    def create_community_join_notification(user, community):
        """Create notification when someone joins a community."""
        # Notify community owner
        title = "New Community Member"
        message = f"{user.username} joined your community {community.name}"
        
        return NotificationManager.create_notification(
            title=title,
            message=message,
            notification_type='community_join',
            user_id=community.owner.id,
            sender_id=user.id,
            community_id=community.id
        )
    
    @staticmethod
    def get_user_notifications(user, args):
        """Get notifications for a user."""
        return Notification.get_by_user(user, args)
    
    @staticmethod
    def mark_notification_as_read(user, notification_id):
        """Mark a notification as read."""
        notification = Notification.get_by_id(notification_id)
        
        if notification.user_id != user.id:
            raise UnauthorizedError('You can only mark your own notifications as read.')
        
        notification.mark_as_read()
        return notification
    
    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications for a user as read."""
        Notification.mark_all_as_read_for_user(user)
    
    @staticmethod
    def get_unread_count(user):
        """Get count of unread notifications for a user."""
        return Notification.get_unread_count_for_user(user)
    
    @staticmethod
    def delete_notification(user, notification_id):
        """Delete a notification."""
        notification = Notification.get_by_id(notification_id)
        
        if notification.user_id != user.id:
            raise UnauthorizedError('You can only delete your own notifications.')
        
        notification.delete()
        return True