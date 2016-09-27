""" Run Local Development Server """
from src import app
from config import DevelopmentConfig

if __name__ == "__main__":
    app.config.from_object(DevelopmentConfig)
    app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
