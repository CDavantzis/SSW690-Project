from pymongo import MongoClient
import catalog
import schedule

client = MongoClient()
catalog.courses.update_db(client)
catalog.degrees.update_db(client)
schedule.update_db(client)
