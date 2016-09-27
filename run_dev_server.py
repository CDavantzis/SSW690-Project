""" Run Local Development Server """
from src import app
from config import BaseConfig

if __name__ == "__main__":
    app.config.from_object(BaseConfig)
    app.run(threaded=True, debug=False)

