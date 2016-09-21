
from pymongo import MongoClient
import catalog
import schedule

client = MongoClient()

catalog.create(client)
schedule.clone_database(client)
