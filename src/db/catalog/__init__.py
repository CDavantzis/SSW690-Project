import os
from pymongo import MongoClient

catalog_dir = os.path.dirname(os.path.relpath(__file__))

def create(client): 
    print 'Dropping catalog db...'
    client.drop_database('catalog')

    for file in os.listdir(catalog_dir):
        file = os.path.join(catalog_dir, file)
        if not file.endswith('.json'):
            continue 


        collection = os.path.basename(file[:file.find('.json')])
        print 'Adding collection %s to db...' % collection
        os.system('mongoimport --db catalog --collection ' + collection + ' --file ' + file + ' --jsonArray')



