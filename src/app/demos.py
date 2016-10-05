from flask import Blueprint, render_template, abort


demos = Blueprint('simple_page', __name__, template_folder='templates/demos', url_prefix='/demos')


@demos.route('/angular_ui_tree')
def angular_ui_tree():
    return render_template('angular_ui_tree.html')


@demos.route('/js_tree')
def js_tree():
    return render_template('js_tree.html')

