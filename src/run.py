""" Run Web Server """
from app import flask_app
import config
import argparse
import sys


def local_server():
    """ Launch local server
    """
    flask_app.config.from_object(config.DevConfig)
    flask_app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
    sys.exit(1)


def public_server():
    """ Launch public server

        Note: Do not use in production
        See http://flask.pocoo.org/docs/0.11/deploying/#deployment

    """
    flask_app.config.from_object(config.ExtConfig)
    # IMPORTANT: DEBUG MUST NEVER BE TRUE ON EXTERNALLY VISIBLE SERVERS!
    flask_app.run(host='0.0.0.0', port=80, threaded=True, debug=False)
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--public",  action="store_true")
    args = parser.parse_args()
    if args.public:
        public_server()
    local_server()
