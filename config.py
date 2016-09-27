class BaseConfig(object):

    # Flask
    DEBUG = False
    SECRET_KEY = "CHANGE-THIS-KEY"
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 megabytes

    # MongoDB
    MONGO_HOST = 'ec2-52-91-131-69.compute-1.amazonaws.com'
    MONGO_PORT = 27017

    # Carry out tasks before first app request
    ON_LOAD_UPDATE_COURSES = True
    ON_LOAD_UPDATE_DEGREES = True


class DevelopmentConfig(BaseConfig):
    pass


class ExternalConfig(BaseConfig):
    pass

