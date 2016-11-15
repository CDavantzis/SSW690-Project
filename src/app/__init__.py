import os

from flask import Flask, render_template, jsonify, abort, request
from werkzeug.local import LocalProxy
from context import get_db

flask_app = Flask(__name__)
mongo_client = LocalProxy(get_db)

import db
from demos import demos
flask_app.register_blueprint(demos)


@flask_app.url_defaults
def hashed_static_file_url(endpoint, values):
    """


    :param endpoint:
    :param values:
    :return:

    source:
    https://gist.github.com/Ostrovski/f16779933ceee3a9d181

    """
    if 'static' == endpoint or endpoint.endswith('.static'):
        filename = values.get('filename')
        if filename:
            static_folder = flask_app.static_folder
            blueprint = endpoint.rsplit('.', 1)[0] if '.' in endpoint else request.blueprint
            if blueprint and flask_app.blueprints[blueprint].static_folder:
                static_folder = flask_app.blueprints[blueprint].static_folder
            filepath = os.path.join(static_folder, filename)
            if os.path.exists(filepath):
                values['_'] = int(os.stat(filepath).st_mtime)


def static_file_hash(filename):
    return int(os.stat(filename).st_mtime)


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
    letter = request.args.get('letter')
    number = request.args.get('number')

    if (letter is None) or (number is None):
        abort(400)

    r = mongo_client.catalog.courses.find_one({"letter": letter,
                                               "number": number},
                                              {'_id': False})
    if r is not None:
        return jsonify(r)

    abort(404)


@flask_app.route('/api/schedule/semesters', methods=['GET'])
def get_scheduled_semesters():
    """ List all semesters available in schedule database """
    # TODO: Sort properly and provide full semester name
    # ^ Possibly store this information in a separate collection
    return jsonify(results=list(db.schedule.get_semesters()))


@flask_app.route('/api/schedule/list')
def get_scheduled_courses():
    """ List all courses in database for a specified semester """
    return jsonify(results=list(db.schedule.get_all()))


@flask_app.route('/api/schedule/tree')
def get_scheduled_course_tree():
    """ List all courses in database for a specified semester in a tree """

    items = []
    for item in db.schedule.get_tree():
        item['id'] = item.get('_id').get('prefix') + ' ' + item.get('_id').get('number')
        items.append(item)


    return jsonify(results=items)


@flask_app.route('/api/schedule/combinations', methods=['POST'])
def get_scheduled_course_combinations():
    """ Get the course info for specified courses """
    call_numbers = request.form.getlist('call_numbers[]')
    d = db.schedule.working_class_combinations_calendar(call_numbers=call_numbers)
    return jsonify(list(d))
