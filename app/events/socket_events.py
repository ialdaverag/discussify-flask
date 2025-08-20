# Flask-SocketIO
from flask_socketio import emit, join_room, leave_room, disconnect

# Flask-JWT-Extended
from flask_jwt_extended import decode_token, get_jwt_identity

# Extensions
from app.extensions.socketio import socketio

# Models
from app.models.user import User


@socketio.on('connect')
def handle_connect(auth):
    """Handle user connection to socket."""
    try:
        # Extract token from auth data
        if not auth or 'token' not in auth:
            disconnect()
            return False
        
        # Decode JWT token
        token = auth['token']
        try:
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
        except Exception:
            disconnect()
            return False
        
        # Get user
        user = User.query.get(user_id)
        if not user:
            disconnect()
            return False
        
        # Join user-specific room for notifications
        join_room(f'user_{user_id}')
        
        emit('connected', {
            'message': f'Connected as {user.username}',
            'user_id': user_id
        })
        
        print(f"User {user.username} connected to socket")
        
    except Exception as e:
        print(f"Connection error: {e}")
        disconnect()
        return False


@socketio.on('disconnect')
def handle_disconnect():
    """Handle user disconnection."""
    print("User disconnected from socket")


@socketio.on('join_notifications')
def handle_join_notifications(data):
    """Handle user joining their notification room."""
    try:
        if 'token' not in data:
            emit('error', {'message': 'Token required'})
            return
        
        token = data['token']
        try:
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
        except Exception:
            emit('error', {'message': 'Invalid token'})
            return
        
        join_room(f'user_{user_id}')
        emit('joined_notifications', {
            'message': 'Joined notification room',
            'room': f'user_{user_id}'
        })
        
    except Exception as e:
        emit('error', {'message': str(e)})


@socketio.on('leave_notifications')
def handle_leave_notifications(data):
    """Handle user leaving their notification room."""
    try:
        if 'token' not in data:
            emit('error', {'message': 'Token required'})
            return
        
        token = data['token']
        try:
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
        except Exception:
            emit('error', {'message': 'Invalid token'})
            return
        
        leave_room(f'user_{user_id}')
        emit('left_notifications', {
            'message': 'Left notification room',
            'room': f'user_{user_id}'
        })
        
    except Exception as e:
        emit('error', {'message': str(e)})