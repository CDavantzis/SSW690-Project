""" Run Local Development Server """
from app import flask_app, db
from config import DevConfig, DevLocDBConfig

if __name__ == "__main__":
    flask_app.config.from_object(DevConfig)

    if flask_app.config.get("BEFORE_RUN_UPDATE_COURSES"):
        db.catalog.courses.update_db()
        print "catalog.courses has been updated"
    if flask_app.config.get("BEFORE_RUN_UPDATE_DEGREES"):
        db.catalog.degrees.update_db()
        print "catalog.degrees has been updated"
    if flask_app.config.get("BEFORE_RUN_UPDATE_SCHEDULE"):
        db.schedule.update_db()
        print "schedule semesters have been updated"

    flask_app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
