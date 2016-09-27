from flask import Flask, render_template, jsonify
from werkzeug.local import LocalProxy
import db
app = Flask(__name__)
mongo_client = LocalProxy(db.get_db)


@app.before_first_request
def on_server_load():
    if app.config.get("ON_LOAD_UPDATE_COURSES"):
        db.catalog.courses.update_db(mongo_client)
        print "catalog.courses has been updated"
    if app.config.get("ON_LOAD_UPDATE_DEGREES"):
        db.catalog.degrees.update_db(mongo_client)
        print "catalog.degrees has been updated"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_courses')
def get_courses():
    return jsonify(results=list(mongo_client.catalog.courses.find({}, {'_id': False})))
