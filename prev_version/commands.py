from .database import engine, Base

# just importing all the models is enough to have them created
# flake8: noqa
from .user.model import User, CartItem
from .item.model import Item


def create_db_schema():
    Base.metadata.create_all(bind=engine)
