from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('ec2-52-91-131-69.compute-1.amazonaws.com', port=27017)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_courses')
def get_courses():
    db = client.catalog
    courses = db.courses
    course_list = []
    for course in courses.find({}):
        d = dict(course)
        del d['_id']
        course_list.append(d)
    return jsonify(results=course_list)
