import os

cwd = os.path.dirname(os.path.abspath(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////{}/test.db".format(cwd)
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = "list"
