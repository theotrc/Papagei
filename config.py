import os
from dotenv import load_dotenv



load_dotenv(override=True)

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('OVHDB')
SECRET_KEY = os.environ.get('SECRET')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.environ.get('FOLDER_PATH')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')

stripe_keys = {
  'secret_key': os.environ.get('STRIPE_SECRET_KEY'),
  'publishable_key': os.environ.get('STRIPE_PUBLISHABLE_KEY')
}