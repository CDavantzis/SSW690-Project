""" Catalog: Courses Functions """
import os
import bson.json_util
from app import mongo_client

FILE_NAME = "courses.json"
FILE_LOCATION = os.path.join(os.path.dirname(os.path.relpath(__file__)), FILE_NAME)
COLLECTION_NAME = "courses"


def load_data():
    """ Load Data From JSON File

    :return: List representation of local "courses" data
    :rtype: list
    """
    data = bson.json_util.loads(open(FILE_LOCATION).read())

    # Warn if there are duplicate courses
    h = {}
    for a in data:
        key = (a["letter"], a["number"])
        if key in h:
            print RuntimeWarning("Duplicate course {0}-{1} in courses.json".format(*key))
        h[key] = 1

    return data


def update_db():
    """ Update Database With Current JSON Data """
    db = mongo_client.catalog
    if COLLECTION_NAME not in db.collection_names():
        db[COLLECTION_NAME].insert_many(load_data())
    else:
        db.temp.drop()
        db.temp.insert_many(load_data())
        db.temp.aggregate([{"$out": COLLECTION_NAME}])
        db.temp.drop()


def get_tree():
    return mongo_client.catalog.courses.aggregate([{"$sort": {"number": 1}},
                                                   {"$group": {"_id": "$letter",
                                                               "nodes": {"$push": {
                                                                   "letter": "$letter",
                                                                   "number": "$number",
                                                                   "name": "$name",
                                                                   "title": {"$concat": ["$letter", "-", "$number", " ",
                                                                                         "$name"]}}}}},
                                                   {"$sort": {"_id": 1}}])
