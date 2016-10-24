from flask import Flask, render_template, jsonify, abort
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


@flask_app.route('/api/courses/list')
def get_courses():
    """ List all courses in database """
    return jsonify(results=list(db.catalog.courses.get_all()))


@flask_app.route('/api/courses/tree')
def get_course_tree():
    """ List all courses in database in a tree """
    return jsonify(results=list(db.catalog.courses.get_tree()))


@flask_app.route('/api/courses/info')
def get_course_info():
    """ Get the course info for a specified course """
    abort(501)


@flask_app.route('/api/schedule/semesters', methods=['GET'])
def get_scheduled_semesters():
    """ List all semesters available in schedule database """
    # TODO: Sort properly and provide full semester name
    # ^ Possibly store this information in a separate collection
    return jsonify(results=list(db.schedule.get_semesters()))


@flask_app.route('/api/schedule/list')
def get_scheduled_courses():
    """ List all courses in database for a specified semester """
    abort(501)


@flask_app.route('/api/schedule/tree')
def get_scheduled_course_tree():
    """ List all courses in database for a specified semester in a tree """
    abort(501)


@flask_app.route('/api/schedule/combinations')
def get_scheduled_course_combinations():
    """ Get the course info for specified courses """
    abort(501)
