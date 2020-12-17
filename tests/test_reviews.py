import json

import unittest

from set_environment_vars import set_environment_vars
from get_auth0_token import auth_header_crud_reviews


class ReviewsTestCases(unittest.TestCase):
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
        from espresso import REVIEWS_API_BASE
        from espresso import DEF_MAX_STR_LEN
        from espresso import MAX_COMMENT_LEN

        self.app = app
        self.test_client = app.test_client()
        # DEBUGGING: print(f"Using database uri: {self.app.config['SQLALCHEMY_DATABASE_URI']}")

        self.API_BASE = REVIEWS_API_BASE
        self.DEF_MAX_STR_LEN = DEF_MAX_STR_LEN
        self.MAX_COMMENT_LEN = MAX_COMMENT_LEN

        db.drop_all()
        db.create_all()

    def test_get_no_reviews(self):
        """Test getting list of all reviews when there are none"""
        resp = self.test_client.get(self.API_BASE, headers=auth_header_crud_reviews)
        self.assertEqual(resp.status_code, 200)

        resp_dict = json.loads(resp.data)
        self.assertTrue('success' in resp_dict)
        self.assertEqual(resp_dict['success'], True)
        self.assertTrue('reviews' in resp_dict)
        self.assertEqual(type(resp_dict['reviews']), list)
        self.assertEqual(len(resp_dict['reviews']), 0)

    def test_get_two_reviews(self):
        """Test getting list of all reviews when there are two"""
        from espresso import db
        from espresso import Restaurant
        from espresso import Review

        # Insert a restaurant, whose id will be 1.
        db.session.add(Restaurant(name='Restaurant Reveille', creator='test-user@gmail.com'))
        db.session.commit()

        author_1 = 'Dina Espresso Drinker'
        db.session.add(Review(author=author_1, date='2020-12-16', rating=3, restaurant_id=1))
        author_2 = 'Terri the Taster'
        db.session.add(Review(author=author_2, date='2020-12-31', rating=5, restaurant_id=1))
        db.session.commit()

        resp = self.test_client.get(self.API_BASE, headers=auth_header_crud_reviews)
        self.assertEqual(resp.status_code, 200)

        resp_dict = json.loads(resp.data)
        self.assertEqual(len(resp_dict['reviews']), 2)
        self.assertEqual(resp_dict['reviews'][0]['author'], author_1)
        self.assertEqual(resp_dict['reviews'][1]['author'], author_2)


if __name__ == "__main__":
    unittest.main()
