import os
from dotenv import load_dotenv
load_dotenv(override=True)

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://postgres:27L54ch[cE+{PD7?@35.187.188.161:5432/Papagei-db'
SECRET_KEY = os.environ.get('SECRET')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.environ.get('FOLDER_PATH')
