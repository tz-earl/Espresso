import os
from dotenv import load_dotenv, find_dotenv


def set_environment_vars():
    """Set the env vars to have values for testing,
    in particular for the test database
    """
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    # Note that this testing apparently runs in its own environment,
    # so there is no need to save and restore env variables.
    try:
        os.environ['ESPRESSO_DB_USER'] = os.environ['ESPRESSO_TEST_DB_USER']
        os.environ['ESPRESSO_DB_PASSWORD'] = os.environ['ESPRESSO_TEST_DB_PASSWORD']
        os.environ['ESPRESSO_DB_HOST'] = os.environ['ESPRESSO_TEST_DB_HOST']
        os.environ['ESPRESSO_DB_DATABASE_NAME'] = os.environ['ESPRESSO_TEST_DB_DATABASE_NAME']
    except KeyError as ex:
        print("\nTesting requires these environment variables: " \
              "ESPRESSO_TEST_DB_USER  ESPRESSO_TEST_DB_PASSWORD  "
              "ESPRESSO_TEST_DB_HOST  ESPRESSO_TEST_DB_DATABASE_NAME")
        print(f"Environment variable {ex.args[0]} is missing")
        print(f"Please set {ex.args[0]}, check the others, and retry the testing\n")
        raise
