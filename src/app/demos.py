from flask import Blueprint, render_template, jsonify
from app import mongo_client

demos = Blueprint('demos', __name__, template_folder='templates/demos', url_prefix='/demos')


@demos.route('/js_tree/courses')
def js_tree_courses():
    """ Courses jsTree Demo """
    return render_template('/js_tree/courses.html')


@demos.route('/js_tree/schedule')
def js_tree_schedule():
    """ Schedule jsTree Demo """
    return render_template('/js_tree/schedule.html')
