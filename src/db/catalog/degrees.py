""" Catalog: Degrees Functions """
from pymongo import MongoClient
import bson.json_util


FILE_LOCATION = "degrees.json"
COLLECTION_NAME = "degrees"


def load_data():
    """ Load Data From JSON File

    :return: List representation of local "degrees" data
    :rtype: List
    """
    return bson.json_util.loads(open(FILE_LOCATION).read())


def update_mongodb(client=None):
    """ Update Database With Current JSON Data

    :param client: pymongo MongoClient
    :type client: MongoClient
    :note: If no client provided, initialize default client.

    """
    if client is None:
        client = MongoClient()
    if type(client) != MongoClient:
        raise TypeError("Client provided to 'update_mongodb' was not a MongoClient")

    db = client.catalog
    new_data = load_data()
    if COLLECTION_NAME not in db.collection_names():
        db[COLLECTION_NAME].insert_many(new_data)
    else:
        db.temp.drop()
        db.temp.insert_many(new_data)
        db.temp.aggregate([{"$out": COLLECTION_NAME}])
        db.temp.drop()


if __name__ == "__main__":
    update_mongodb()
