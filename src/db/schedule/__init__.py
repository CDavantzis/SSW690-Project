""" Schedule Database Functions """
from pymongo import MongoClient
import middleware


def update_mongodb(client=None):
    """ Replicate existing course scheduler database in MongoDB
    :param client: pymongo MongoClient
    :type client: MongoClient
    :note: If no client provided, initialize default client.
    """
    if client is None:
        client = MongoClient()
    if type(client) != MongoClient:
        raise TypeError("Client provided to 'update_mongodb' was not a MongoClient")
    db = client.schedule
    for term in middleware.terms():
        new_data = list(middleware.courses(term[0]))
        if len(new_data) != 0:
            if term[0] not in db.collection_names():
                db[term[0]].insert_many(new_data)
            else:
                db.temp.drop()
                db.temp.insert_many(new_data)
                db.temp.aggregate([{"$out": term[0]}])
                db.temp.drop()


if __name__ == "__main__":
    update_mongodb()

