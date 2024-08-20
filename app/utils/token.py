# Flask
from flask import current_app

# itsdangerous
from itsdangerous import URLSafeTimedSerializer


def generate_verification_token(email, salt=None):
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))

    return serializer.dumps(email, salt=salt)


def confirm_verification_token(token, max_age=(30*60), salt=None):
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    
    try:
        email = serializer.loads(token, max_age=max_age, salt=salt)
    except:
        return False

    return email