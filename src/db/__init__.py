from flask import  g,current_app
from pymongo import MongoClient


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = MongoClient(current_app.config.get("MONGO_HOST"), port=current_app.config.get("MONGO_PORT"))
    return db
