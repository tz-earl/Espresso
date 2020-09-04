import os
import sys

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs. For debugging purposes.
basedir = os.path.abspath(os.path.dirname(__file__))

# Database credentials and set up
# N.B. A user password is required, otherwise, you get a runtime exception
# when programmatically opening the Postgres database.
try:
    db_user = os.environ['ESPRESSO_DB_USER']
    db_password = os.environ['ESPRESSO_DB_PASSWORD']
    db_host = os.environ['ESPRESSO_DB_HOST']
    db_database_name = os.environ['ESPRESSO_DB_DATABASE_NAME']
except KeyError as ex:
    print("The espresso app requires four environment variables: " \
            "ESPRESSO_DB_USER  ESPRESSO_DB_PASSWORD  ESPRESSO_DB_HOST  ESPRESSO_DB_DATABASE_NAME")
    print(f"Environment variable {ex.args[0]} is missing")
    print(f"Please set {ex.args[0]} and restart the app")
else:
    db_url = f"postgres+psycopg2://{db_user}:{db_password}@{db_host}/{db_database_name}"

SQLALCHEMY_DATABASE_URI = db_url
SQLALCHEMY_TRACK_MODIFICATIONS = False
