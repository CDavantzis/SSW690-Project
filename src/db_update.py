#!/usr/bin/env python

""" Database Update """
import argparse
from app import flask_app, db

try:
    import config_private as config
except ImportError:
    import config_public as config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--courses",  action="store_true")
    parser.add_argument("--degrees",  action="store_true")
    parser.add_argument("--schedule",  action="store_true")
    args = parser.parse_args()

    flask_app.config.from_object(config.BaseConfig)
    with flask_app.app_context():
        db.update(update_courses=args.courses, update_degrees=args.degrees, update_schedule=args.schedule)


