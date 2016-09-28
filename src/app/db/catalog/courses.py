""" Catalog: Courses Functions """
import os
import bson.json_util
from pymongo import MongoClient
from src.app import flask_app, mongo_client

FILE_NAME = "courses.json"
FILE_LOCATION = os.path.join(os.path.dirname(os.path.relpath(__file__)), FILE_NAME)
COLLECTION_NAME = "courses"


def check_for_duplicates(d):
    h = {}
    for a in d:
        key = (a["letter"], a["number"])
        if key in h:
            return key
        h[key] = 1
    return False


def load_data():
    """ Load Data From JSON File

    :return: List representation of local "courses" data
    :rtype: list
    """
    return bson.json_util.loads(open(FILE_LOCATION).read())


def update_db(client=None):
    """ Update Database With Current JSON Data

    :param client: pymongo MongoClient
    :type client: MongoClient
    :note: If no client provided, initialize default client.

    """
    if client is None:
        with flask_app.app_context():
            db = mongo_client.catalog
    else:
        db = client.catalog

    new_data = load_data()
    duplicate = check_for_duplicates(new_data)
    if duplicate:
        raise RuntimeWarning("Duplicate course {0} in courses.json".format( duplicate))
    if COLLECTION_NAME not in db.collection_names():
        db[COLLECTION_NAME].insert_many(new_data)
    else:
        db.temp.drop()
        db.temp.insert_many(new_data)
        db.temp.aggregate([{"$out": COLLECTION_NAME}])
        db.temp.drop()

if __name__ == "__main__":
    update_db()
