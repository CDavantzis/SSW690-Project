from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_courses')
def get_courses():
    client = MongoClient()
    db = client.catalog
    courses = db.courses
    course_list = []
    for course in courses.find({}):
        course_list.append(course['letter'] + ' ' + course['number'])

    return jsonify(results=course_list)






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
