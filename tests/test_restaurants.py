import os
import json

import unittest

from espresso import db


def set_environment_vars():
    """Set the env vars to have values for testing"""

    # Note that this testing apparently runs in its own environment,
    # so there is no need to save and restore env variables.
    try:
        os.environ['ESPRESSO_DB_USER'] = os.environ['ESPRESSO_TEST_DB_USER']
        os.environ['ESPRESSO_DB_PASSWORD'] = os.environ['ESPRESSO_TEST_DB_PASSWORD']
        os.environ['ESPRESSO_DB_HOST'] = os.environ['ESPRESSO_TEST_DB_HOST']
        os.environ['ESPRESSO_DB_DATABASE_NAME'] = os.environ['ESPRESSO_TEST_DB_DATABASE_NAME']
    except KeyError as ex:
        print("\nTesting requires four environment variables: " \
              "ESPRESSO_TEST_DB_USER  ESPRESSO_TEST_DB_PASSWORD  "
              "ESPRESSO_TEST_DB_HOST  ESPRESSO_TEST_DB_DATABASE_NAME")
        print(f"Environment variable {ex.args[0]} is missing")
        print(f"Please set {ex.args[0]} and restart the testing\n")
        raise


class RestaurantsTestCases(unittest.TestCase):

    def setUp(self):
        set_environment_vars()

        # N.B. We must set the environment variables to test values
        # _before_ importing the app, otherwise, those env vars will
        # still have their normal values when instantiating the app.
        from espresso import app

        self.app = app
        self.test_client = app.test_client()
        self.test_count = 0
        # DEBUGGING: print(f"Using database uri: {self.app.config['SQLALCHEMY_DATABASE_URI']}")

        db.drop_all()
        db.create_all()

    def test_no_restaurants(self):
        resp = self.test_client.get('/restaurants')
        self.assertEqual(resp.status_code, 200)

        resp_dict = json.loads(resp.data)
        self.assertTrue('success' in resp_dict)
        self.assertEqual(resp_dict['success'], True)
        self.assertTrue('restaurants' in resp_dict)
        self.assertEqual(type(resp_dict['restaurants']), list)
        self.assertEqual(len(resp_dict['restaurants']), 0)
