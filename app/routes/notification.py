# Flask
from flask import Blueprint, request, jsonify

# Flask-JWT-Extended
from flask_jwt_extended import jwt_required, current_user

# Webargs
from webargs.flaskparser import use_args

# Managers
from app.managers.notification import NotificationManager

# Schemas
from app.schemas.notification import NotificationSchema, NotificationReadSchema

# Errors
from app.errors.errors import ValidationError

notification_routes = Blueprint('notification', __name__)


@notification_routes.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get notifications for the current user."""
    try:
        # Get pagination arguments from request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        is_read = request.args.get('is_read', type=bool)
        
        args = {
            'page': page,
            'per_page': per_page,
            'is_read': is_read
        }
        
        notifications = NotificationManager.get_user_notifications(current_user, args)
        
        schema = NotificationSchema(many=True)
        notifications_data = schema.dump(notifications.items)
        
        return jsonify({
            'notifications': notifications_data,
            'pagination': {
                'page': notifications.page,
                'pages': notifications.pages,
                'per_page': notifications.per_page,
                'total': notifications.total,
                'has_next': notifications.has_next,
                'has_prev': notifications.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notification_routes.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """Get count of unread notifications for the current user."""
    try:
        count = NotificationManager.get_unread_count(current_user)
        return jsonify({'unread_count': count}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notification_routes.route('/<int:notification_id>/read', methods=['PATCH'])
@jwt_required()
def mark_as_read(notification_id):
    """Mark a notification as read."""
    try:
        notification = NotificationManager.mark_notification_as_read(current_user, notification_id)
        
        schema = NotificationSchema()
        notification_data = schema.dump(notification)
        
        return jsonify({
            'message': 'Notification marked as read',
            'notification': notification_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@notification_routes.route('/mark-all-read', methods=['PATCH'])
@jwt_required()
def mark_all_as_read():
    """Mark all notifications for the current user as read."""
    try:
        NotificationManager.mark_all_as_read(current_user)
        
        return jsonify({
            'message': 'All notifications marked as read'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notification_routes.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification."""
    try:
        NotificationManager.delete_notification(current_user, notification_id)
        
        return jsonify({
            'message': 'Notification deleted'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400