class BaseConfig(object):

    # Flask
    DEBUG = False
    SECRET_KEY = "CHANGE-THIS-KEY"
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 megabytes

    # MongoDB
    MONGO_HOST = 'ec2-52-91-131-69.compute-1.amazonaws.com'
    MONGO_PORT = 27017
