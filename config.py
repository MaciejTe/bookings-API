import os

cwd = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////{}/test.db'.format(cwd)
