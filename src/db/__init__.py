from flask import g, current_app
from pymongo import MongoClient

import catalog
import schedule


def get_db():
    """ Get MongoClient for current application
    :returns New MongoClient if there is none in the current application context, otherwise existing MongoClient

    Example:
        from werkzeug.local import LocalProxy
        db = LocalProxy(get_db)
    """
    if not hasattr(g, 'mongo_client'):
        g.mongo_client = MongoClient(current_app.config.get("MONGO_HOST"), port=current_app.config.get("MONGO_PORT"))
    return g.mongo_client
