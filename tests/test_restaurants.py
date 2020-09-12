import os
import json

import unittest


def set_environment_vars():
    """Set the env vars to have values for testing,
    in particular for the test database
    """

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
    """Test cases for endpoints related to restaurants"""

    def setUp(self):
        """Set up the environment variables for testing,
        instantiate the backend app and its database ORM object"""
        set_environment_vars()

        # Careful! We must set the environment variables to test values
        # _before_ importing the espresso app, otherwise, those env vars will
        # still have their normal values when instantiating the app.
        from espresso import app
        from espresso import db

        self.app = app
        self.test_client = app.test_client()
        # DEBUGGING: print(f"Using database uri: {self.app.config['SQLALCHEMY_DATABASE_URI']}")

        db.drop_all()
        db.create_all()

    def test_get_no_restaurants(self):
        """Test getting list of restaurants when there are none"""
        resp = self.test_client.get('/restaurants')
        self.assertEqual(resp.status_code, 200)

        resp_dict = json.loads(resp.data)
        self.assertTrue('success' in resp_dict)
        self.assertEqual(resp_dict['success'], True)
        self.assertTrue('restaurants' in resp_dict)
        self.assertEqual(type(resp_dict['restaurants']), list)
        self.assertEqual(len(resp_dict['restaurants']), 0)

    def test_get_two_restaurants(self):
        """Test getting list of restaurants when there are two"""
        from espresso import db
        from espresso import Restaurant

        name_1 = 'Restaurant Italiano'
        db.session.add(Restaurant(name=name_1))
        name_2 = 'Restaurant Français'
        db.session.add(Restaurant(name=name_2))
        db.session.commit()

        resp = self.test_client.get('/restaurants')
        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.data)
        self.assertEqual(len(resp_dict['restaurants']), 2)
        self.assertEqual(resp_dict['restaurants'][0]['name'], name_1)
        self.assertEqual(resp_dict['restaurants'][1]['name'], name_2)
