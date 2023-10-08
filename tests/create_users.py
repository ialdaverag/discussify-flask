from app.models.user import User
from app.extensions.database import db
from app.utils.password import hash_password


def create_users():
    user = User(username='test', email='test@example.com', password=hash_password('TestPassword123'))
    db.session.add(user)
    db.session.commit()