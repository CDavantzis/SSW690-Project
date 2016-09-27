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
    return jsonify(results=mongo_client.catalog.find({}, {'_id': False}))
