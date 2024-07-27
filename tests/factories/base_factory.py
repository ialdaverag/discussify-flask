# factory boy
from factory.alchemy import SQLAlchemyModelFactory

# extensions
from app.extensions.database import db


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
        
