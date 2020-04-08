import os
from abc import ABC

from dotenv import load_dotenv, find_dotenv


class IEnvironmentConfig(ABC):
    pass


class EnvironmentConfig(IEnvironmentConfig):
    load_dotenv(find_dotenv())

    MODE_DEBUGGER = os.environ.get('MODE_DEBUGGER', False)
    PORT = os.environ.get('PORT', 8080)
    TEMPLATE_DIR = os.environ.get('TEMPLATE_DIR', 'web/templates')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'M#lOkNdmResearchPerudAxaGS=GgEPl)&9_$JFNCE&djMPB30zwRwvMDQxFq&tT=)')

    DATABASE = os.environ.get('DATABASE', 'postgres://lzecrhmvjdmomw:6d306d01bb52a3f77d0104f41373a3489d410a0fd0a138c1166c1e4b328bf56e@ec2-18-235-97-230.compute-1.amazonaws.com:5432/dcenvoo97jcr6u')

    HOST_URL = os.environ.get('HOST_URL', 'http://localhost:3000/')

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 465)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', False)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
