import os

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs. For debugging purposes.
basedir = os.path.abspath(os.path.dirname(__file__))

# Database credentials and set up
# N.B. A user password is required, otherwise, you get a runtime exception
db_url = "postgres+psycopg2://dbusername:password@localhost:5432/espresso"
SQLALCHEMY_DATABASE_URI = db_url
SQLALCHEMY_TRACK_MODIFICATIONS = False
