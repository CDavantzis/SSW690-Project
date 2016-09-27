from pymongo import MongoClient
import catalog
import schedule

client = MongoClient()

catalog.create(client)
schedule.update_mongodb(client)
