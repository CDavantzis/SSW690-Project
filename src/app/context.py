from flask import g, current_app
from pymongo import MongoClient


def get_db():
    """ Get current application mongo client

    :returns New MongoClient if there is none in the current application context, otherwise existing MongoClient
    """
    if not hasattr(g, 'mongo_client'):
        g.mongo_client = MongoClient(current_app.config.get("MONGO_HOST"), port=current_app.config.get("MONGO_PORT"))

        g.mongo_client.admin.authenticate(current_app.config.get("MONGO_USER"),
                                          current_app.config.get("MONGO_PASSWORD"),
                                          mechanism=current_app.config.get("MONGO_AUTH_MECH"))


    return g.mongo_client
