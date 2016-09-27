from flask import Flask, render_template, jsonify
from werkzeug.local import LocalProxy
from db import get_db

app = Flask(__name__)
mongo_client = LocalProxy(get_db)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_courses')
def get_courses():
    db = mongo_client.catalog
    courses = db.courses
    course_list = []
    for course in courses.find({}):
        d = dict(course)
        del d['_id']
        course_list.append(d)
    return jsonify(results=course_list)
