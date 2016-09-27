from flask import Flask, render_template, jsonify
from werkzeug.local import LocalProxy
from context import get_db

app = Flask(__name__)
mongo_client = LocalProxy(get_db)

import db


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_courses')
def get_courses():
    c = mongo_client.catalog.courses.find({}, {'_id': False}).sort([("letter", 1), ("number", 1)])
    return jsonify(results=list(c))
