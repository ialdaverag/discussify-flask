#!/usr/bin/env python3
"""
Run the Discussify Flask app with notification system

This script shows how to run the Flask app with SocketIO support.
"""

import os
import sys

# Add the app directory to Python path
sys.path.insert(0, '/home/runner/work/discussify-flask/discussify-flask')

def run_app():
    """Run the Flask app with SocketIO."""
    
    # Set up environment
    os.environ['DATABASE_URI'] = 'sqlite:///discussify_notifications.db'
    os.environ['FLASK_ENV'] = 'development'
    
    try:
        from app.app import create_app
        from app.extensions.socketio import socketio
        from app.extensions.database import db
        
        # Import all models to ensure they're registered
        from app.models.user import User, Follow, Block, UserStats
        from app.models.community import Community, CommunitySubscriber, CommunityModerator, CommunityBan, CommunityStats
        from app.models.post import Post, PostBookmark, PostVote, PostStats
        from app.models.comment import Comment, CommentBookmark, CommentVote, CommentStats
        from app.models.notification import Notification
        
        print("🚀 Starting Discussify with Notification System...")
        
        # Create the Flask app
        app = create_app()
        
        with app.app_context():
            # Create database tables
            db.create_all()
            print("✅ Database tables created/verified")
        
        print("\n🔔 Notification System Features:")
        print("  • Real-time notifications via WebSockets")
        print("  • Persistent storage in database")
        print("  • REST API for notification management")
        print("  • Automatic notifications for user actions")
        
        print("\n🌐 Available endpoints:")
        print("  • GET /notification/ - Get user notifications")
        print("  • GET /notification/unread-count - Get unread count")
        print("  • PATCH /notification/<id>/read - Mark as read")
        print("  • DELETE /notification/<id> - Delete notification")
        
        print("\n⚡ WebSocket events:")
        print("  • 'new_notification' - Real-time notification delivery")
        print("  • 'connect' - User authentication via JWT")
        
        print(f"\n📊 Server starting on http://localhost:5000")
        print("   WebSocket endpoint: http://localhost:5000/socket.io/")
        print("\n   Press Ctrl+C to stop the server")
        
        # Run the app with SocketIO
        socketio.run(
            app, 
            debug=True, 
            host='0.0.0.0', 
            port=5000,
            allow_unsafe_werkzeug=True  # For development only
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting app: {e}")

if __name__ == '__main__':
    run_app()