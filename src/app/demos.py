from flask import Blueprint, render_template, jsonify
from app import mongo_client

demos = Blueprint('demos', __name__, template_folder='templates/demos', url_prefix='/demos')


@demos.route('/angular_ui_tree')
def angular_ui_tree():
    return render_template('angular_ui_tree.html')


@demos.route('/angular_ui_tree/js')
def angular_ui_tree_js():
    c = mongo_client.catalog.courses.aggregate([{"$sort": {"number": 1}},
                                                {"$group": {"_id": "$letter",
                                                            "nodes": {"$push": {
                                                                "title": {"$concat": ["$letter", "-",
                                                                                      "$number", " ",
                                                                                      "$name"]}}}}},
                                                {"$sort": {"_id": 1}},
                                                {"$project": {"_id": 0, "title": "$_id", "nodes": "$nodes"}}])
    return jsonify(results=list(c))


@demos.route('/js_tree')
def js_tree():
    return render_template('js_tree.html')


@demos.route('/js_tree/js')
def js_tree_js():
    c = mongo_client.catalog.courses.aggregate([{"$sort": {"number": 1}},
                                                {"$group": {"_id": "$letter",
                                                            "nodes": {"$push": {
                                                                "a_attr": {"data-letter": "$letter",
                                                                           "data-number": "$number"},
                                                                "text": {"$concat": ["$letter", "-",
                                                                                     "$number", " ",
                                                                                     "$name"]}}}}},
                                                {"$sort": {"_id": 1}},
                                                {"$project": {"_id": 0, "text": "$_id", "children": "$nodes"}}])
    return jsonify(results=list(c))
