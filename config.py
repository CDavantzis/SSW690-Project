class Base(object):

    # Flask
    DEBUG = False
    SECRET_KEY = "CHANGE-THIS-KEY"
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 megabytes

    # MongoDB
    MONGO_HOST = 'ec2-52-91-131-69.compute-1.amazonaws.com'
    MONGO_PORT = 27017

    # Carry out tasks before server is started
    BEFORE_RUN_UPDATE_COURSES = False
    BEFORE_RUN_UPDATE_DEGREES = False
    BEFORE_RUN_UPDATE_SCHEDULE = True


class DevConfig(Base):
    pass


class DevLocDBConfig(DevConfig):
    MONGO_HOST = '127.0.0.1'


class ExtConfig(Base):
    pass

