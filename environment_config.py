import os

from dotenv import load_dotenv, find_dotenv


class EnvironmentConfig:
    load_dotenv(find_dotenv())

    MODE_DEBUGGER = os.environ.get('MODE_DEBUGGER', False)
    PORT = os.environ.get('PORT', 8080)
    TEMPLATE_DIR = os.environ.get('TEMPLATE_DIR', 'web/templates')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'M#lOkNdmResearchPerudAxaGS=GgEPl)&9_$JFNCE&djMPB30zwRwvMDQxFq&tT=)')

    DATABASE = os.environ.get('DATABASE', 'sqlite:///epidemiologic.db')
