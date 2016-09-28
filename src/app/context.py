from flask import g, current_app
from pymongo import MongoClient


def get_db():
    """ Get current application mongo client

    :returns New MongoClient if there is none in the current application context, otherwise existing MongoClient
    """
    if not hasattr(g, 'mongo_client'):
        g.mongo_client = MongoClient(current_app.config.get("MONGO_HOST"), port=current_app.config.get("MONGO_PORT"))
    return g.mongo_client
