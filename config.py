import os
from dotenv import load_dotenv
load_dotenv(override=True)

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SECRET_KEY = os.environ.get('SECRET')
print(SECRET_KEY)
SQLALCHEMY_TRACK_MODIFICATIONS = False
