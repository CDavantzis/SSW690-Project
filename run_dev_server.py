""" Run Local Development Server """
from src import app


if __name__ == "__main__":
    # Todo: Implement external configuration
    # flask_app.config.from_object(DevelopmentConfig)
    app.run(threaded=True)
