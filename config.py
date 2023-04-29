import os
from dotenv import load_dotenv
load_dotenv(override=True)

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:27L54ch[cE+{PD7?@35.205.61.54:5432/papagei-sql'
SECRET_KEY = os.environ.get('SECRET')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.environ.get('FOLDER_PATH')