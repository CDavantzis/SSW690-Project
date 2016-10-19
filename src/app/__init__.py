from flask import Flask, render_template, jsonify
from werkzeug.local import LocalProxy
from context import get_db


flask_app = Flask(__name__)
mongo_client = LocalProxy(get_db)

import db
from demos import demos
flask_app.register_blueprint(demos)


@flask_app.route('/')
def home():
    return render_template('index.html')


@flask_app.route('/get_courses')
@flask_app.route('/api/courses/list')
def get_courses():
    """

    :return:
    """
    return jsonify(results=list(db.catalog.courses.get_all()))


@flask_app.route('/api/tree/courses_v2')
@flask_app.route('/api/courses/tree')
def get_course_tree():
    """

    :return:
    """
    return jsonify(results=list(db.catalog.courses.get_tree()))
