from flask import Flask, render_template, jsonify
from werkzeug.local import LocalProxy
from context import get_db

flask_app = Flask(__name__)
mongo_client = LocalProxy(get_db)

import db  # uses m


@flask_app.route('/')
def home():
    return render_template('index.html')


@flask_app.route('/get_courses')
def get_courses():
    c = mongo_client.catalog.courses.find({}, {'_id': False}).sort([("letter", 1), ("number", 1)])
    return jsonify(results=list(c))


@flask_app.route('/api/tree/courses')
def get_course_tree():
    return jsonify(results=list(db.catalog.courses.get_tree()))

