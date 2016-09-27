from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_courses')
def get_courses():
    client = MongoClient('ec2-52-91-131-69.compute-1.amazonaws.com', port=27017)
    db = client.catalog
    courses = db.courses
    course_list = []
    for course in courses.find({}):
    	d = dict(course)
    	del d['_id']
        course_list.append(d)

    return jsonify(results=course_list)






if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
