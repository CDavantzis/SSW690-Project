from flask import Flask, render_template, jsonify
from werkzeug.local import LocalProxy
from context import get_db

from demos import demos

flask_app = Flask(__name__)
mongo_client = LocalProxy(get_db)
flask_app.register_blueprint(demos)


@flask_app.route('/')
def home():
    return render_template('index.html')


@flask_app.route('/get_courses')
def get_courses():
    c = mongo_client.catalog.courses.find({}, {'_id': False}).sort([("letter", 1), ("number", 1)])
    return jsonify(results=list(c))


@flask_app.route('/api/tree/courses')
def get_course_tree():
    c = mongo_client.catalog.courses.aggregate([{"$sort": {"number": 1}},
                                                {"$group": {"_id": "$letter",
                                                            "nodes": {"$push": {
                                                                "title": {"$concat": ["$letter", "-",
                                                                                      "$number", " ",
                                                                                      "$name"]}}}}},
                                                {"$sort": {"_id": 1}},
                                                {"$project": {"_id": 0, "title": "$_id", "nodes": "$nodes"}}])
    return jsonify(results=list(c))


@flask_app.route('/api/tree/courses_v2')
def get_course_tree_v2():
    c = mongo_client.catalog.courses.aggregate([{"$sort": {"number": 1}},
                                                {"$group": {"_id": "$letter",
                                                            "nodes": {"$push": {
                                                                "a_attr": {"data-letter":"$letter", "data-number": "$number"},
                                                                "text": {"$concat": ["$letter", "-", "$number", " ",
                                                                                     "$name"]}}}}},
                                                {"$sort": {"_id": 1}},
                                                {"$project": {"_id": 0, "text": "$_id", "children": "$nodes"}}])
    return jsonify(results=list(c))
