import json

import unittest

from set_environment_vars import set_environment_vars
from get_auth0_token import auth_header_cru_restaurants
from get_auth0_token import auth_header_all_permissions


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
        from espresso import RESTAURANTS_API_BASE
        from espresso import DEF_MAX_STR_LEN

        self.app = app
        self.test_client = app.test_client()
        # DEBUGGING: print(f"Using database uri: {self.app.config['SQLALCHEMY_DATABASE_URI']}")

        self.API_BASE = RESTAURANTS_API_BASE
        self.DEFAULT_MAX_STRING = DEF_MAX_STR_LEN

        db.drop_all()
        db.create_all()

    def test_get_no_restaurants(self):
        """Test getting list of restaurants when there are none"""
        resp = self.test_client.get(self.API_BASE, headers=auth_header_cru_restaurants)
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
        db.session.add(Restaurant(name=name_1, creator='test-user@gmail.com'))
        name_2 = 'Restaurant Français'
        db.session.add(Restaurant(name=name_2, creator='test-user@gmail.com'))
        db.session.commit()

        resp = self.test_client.get(self.API_BASE, headers=auth_header_cru_restaurants)
        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.data)
        self.assertEqual(len(resp_dict['restaurants']), 2)
        self.assertEqual(resp_dict['restaurants'][0]['name'], name_1)
        self.assertEqual(resp_dict['restaurants'][1]['name'], name_2)

    def test_get_restaurant_by_id(self):
        """Test getting a specific restaurant by its id number"""
        from espresso import db
        from espresso import Restaurant

        name = 'Restaurant Greco'
        db.session.add(Restaurant(name=name, creator='test-user@gmail.com'))
        db.session.commit()

        # Since this is a freshly created table, the first id should be 1
        resp = self.test_client.get(self.API_BASE + '/1', headers=auth_header_cru_restaurants)
        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.data)
        self.assertEqual(resp_dict['restaurant']['name'], name)

    def test_get_restaurant_by_id_none(self):
        """Test getting a restaurant by a non-existent id number"""
        from espresso import db
        from espresso import Restaurant

        name = 'Restaurant Greco'
        db.session.add(Restaurant(name=name, creator='test-user@gmail.com'))
        db.session.commit()

        # Since this is a freshly created table, the only id should be 1.
        # id 2 does not exist.
        resp = self.test_client.get(self.API_BASE + '/2', headers=auth_header_cru_restaurants)
        self.assertEqual(resp.status_code, 404)

    def test_get_restaurant_by_id_not_number(self):
        """Test getting a restaurant by a non-integer id number"""
        resp = self.test_client.get(self.API_BASE + '/hello', headers=auth_header_cru_restaurants)
        self.assertEqual(resp.status_code, 400)

    def test_get_restaurant_404_not_found(self):
        """Test getting a restaurant with a non-existent subpath"""
        resp = self.test_client.get(self.API_BASE + '/1/hello', headers=auth_header_cru_restaurants)
        self.assertEqual(resp.status_code, 404)

    def test_get_restaurant_405_method_not_allowed(self):
        """Test using POST method that is not allowed"""
        resp = self.test_client.post(self.API_BASE, headers=auth_header_cru_restaurants)
        self.assertEqual(resp.status_code, 405)
        resp_dict = json.loads(resp.data)
        self.assertEqual(resp_dict['success'], False)

    def test_get_restaurant_unauthorized(self):
        """Test get request that lacks authorization header"""
        resp = self.test_client.get(self.API_BASE, headers={})
        self.assertEqual(resp.status_code, 401)
        resp_dict = json.loads(resp.data)
        self.assertEqual(resp_dict['success'], False)

    def test_create_restaurant_with_name_creator_only(self):
        """Test creation of a restaurant with only the name and creator fields"""
        headers = {'Content-Type': 'application/json'}
        headers.update(auth_header_cru_restaurants)
        name = 'Restaurant Chinois'
        info = {'name': name, 'creator': 'nobody@gmail.com'}
        resp = self.test_client.post(self.API_BASE + '/create', headers=headers, data=json.dumps(info))

        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.data)
        self.assertEqual(name in resp_dict['message'], True)

    def test_create_restaurant_with_all_fields(self):
        """Test creation of a restaurant with fields provided"""
        headers = {'Content-Type': 'application/json'}
        headers.update(auth_header_cru_restaurants)
        name = 'Restaurant Chinois'
        street = '999 Sutter St'
        suite = '510'
        city = 'Wood-Ridge'
        state = 'NJ'
        zip_code = '07075'
        phone_num = '201-555-7777'
        website = 'www.chinois-nj.com'
        email = 'chinois-nj@gmail.com'
        date_established = '2014'
        creator = 'some-user@gmail.com'
        info = {'name': name, 'street': street, 'suite': suite,
                'city': city, 'state': state, 'zip_code': zip_code,
                'phone_num': phone_num, 'website': website, 'email': email,
                'date_established': date_established, 'creator': creator
               }
        resp = self.test_client.post(self.API_BASE + '/create', headers=headers, data=json.dumps(info))

        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.data)
        self.assertEqual(resp_dict['id'], 1)
        self.assertEqual(name in resp_dict['message'], True)

        # Retrieve the restaurant and assert that all fields are as created
        resp = self.test_client.get(self.API_BASE + '/1', headers=auth_header_cru_restaurants)

        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.data)
        self.assertEqual(resp_dict['restaurant']['id'], 1)
        self.assertEqual(resp_dict['restaurant']['name'], name)
        self.assertEqual(resp_dict['restaurant']['street'], street)
        self.assertEqual(resp_dict['restaurant']['suite'], suite)
        self.assertEqual(resp_dict['restaurant']['city'], city)
        self.assertEqual(resp_dict['restaurant']['state'], state)
        self.assertEqual(resp_dict['restaurant']['zip_code'], zip_code)
        self.assertEqual(resp_dict['restaurant']['phone_num'], phone_num)
        self.assertEqual(resp_dict['restaurant']['website'], website)
        self.assertEqual(resp_dict['restaurant']['email'], email)
        self.assertEqual(resp_dict['restaurant']['date_established'], date_established)
        self.assertEqual(resp_dict['restaurant']['creator'], creator)

    def test_create_restaurant_no_name(self):
        """Test creation of a restaurant with missing name field"""
        headers = {'Content-Type': 'application/json'}
        headers.update(auth_header_cru_restaurants)
        info = {'creator': 'nobody@gmail.com', 'city': 'Chicago'}
        resp = self.test_client.post(self.API_BASE + '/create', headers=headers, data=json.dumps(info))
        self.assertEqual(resp.status_code, 400)

    def test_create_restaurant_no_creator(self):
        """Test creation of a restaurant with missing creator field"""
        headers = {'Content-Type': 'application/json'}
        headers.update(auth_header_cru_restaurants)
        info = {'name': 'Ping Yan', 'city': 'Chicago'}
        resp = self.test_client.post(self.API_BASE + '/create', headers=headers, data=json.dumps(info))
        self.assertEqual(resp.status_code, 400)

    def test_create_restaurant_unauthorized(self):
        """Test post request that lacks authorization header"""
        headers = {'Content-Type': 'application/json'}
        info = {'name': 'Restaurant Pho 2000', 'creator': 'test-user@gmail.com'}
        resp = self.test_client.post(self.API_BASE + '/create', headers=headers, data=json.dumps(info))

        self.assertEqual(resp.status_code, 401)

    def test_create_restaurant_field_too_long(self):
        """Test that a string field value that is too long is truncated"""
        headers = {'Content-Type': 'application/json'}
        headers.update(auth_header_cru_restaurants)
        name = 'Restaurant Chinois' + ('z' * self.DEFAULT_MAX_STRING)  # Make the name too long
        info = {'name': name, 'creator': 'nobody@gmail.com'}
        resp = self.test_client.post(self.API_BASE + '/create', headers=headers, data=json.dumps(info))

        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.data)
        # The too-long name should not be in the message
        self.assertEqual(name in resp_dict['message'], False)

    def test_update_restaurant(self):
        """Test update of an existing restaurant's website and email address"""
        from espresso import db
        from espresso import Restaurant

        name = 'Restaurant Mexicano'
        zip_code = "94110"
        db.session.add(Restaurant(name=name, creator='test-user@gmail.com', zip_code=zip_code))
        db.session.commit()

        headers = {'Content-Type': 'application/json'}
        headers.update(auth_header_cru_restaurants)
        website = 'www.mexicano-nj.com'
        email = 'mexicano-nj@gmail.com'
        info = {'website': website, 'email': email}
        resp = self.test_client.put(self.API_BASE + '/1', headers=headers, data=json.dumps(info))

        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.data)
        self.assertEqual(resp_dict['id'], 1)
        self.assertEqual(name in resp_dict['message'], True)

        resp = self.test_client.get(self.API_BASE + '/1', headers=auth_header_cru_restaurants)

        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.data)
        self.assertEqual(resp_dict['restaurant']['id'], 1)
        self.assertEqual(resp_dict['restaurant']['website'], website)
        self.assertEqual(resp_dict['restaurant']['email'], email)
        self.assertEqual(resp_dict['restaurant']['zip_code'], zip_code) # Make sure this has not changed

    def test_update_restaurant_blank_name(self):
        """Test update of a restaurant with the name field an empty string"""
        from espresso import db
        from espresso import Restaurant

        name = 'Restaurant Mexicano'
        db.session.add(Restaurant(name=name, creator='test-user@gmail.com'))
        db.session.commit()

        headers = {'Content-Type': 'application/json'}
        headers.update(auth_header_cru_restaurants)
        info = {'name': ''}
        resp = self.test_client.put(self.API_BASE + '/1', headers=headers, data=json.dumps(info))
        self.assertEqual(resp.status_code, 400)

    def test_update_restaurant_unauthorized(self):
        """Test put request that lacks authorization header"""
        from espresso import db
        from espresso import Restaurant

        name = 'Restaurant Pho 2000'
        db.session.add(Restaurant(name=name, creator='test-user@gmail.com'))
        db.session.commit()

        headers = {'Content-Type': 'application/json'}
        info = {'name': 'Php 2048'}
        resp = self.test_client.put(self.API_BASE + '/1', headers=headers, data=json.dumps(info))
        self.assertEqual(resp.status_code, 401)

    def test_delete_restaurant(self):
        """Test deleting a specific restaurant by its id number"""
        from espresso import db
        from espresso import Restaurant

        name = 'Restaurant Greco'
        db.session.add(Restaurant(name=name, creator='test-user@gmail.com'))
        db.session.commit()

        # Since this is a freshly created table, the first id should be 1
        resp = self.test_client.delete(self.API_BASE + '/1', headers=auth_header_all_permissions)
        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.data)
        self.assertEqual(resp_dict['success'], True)

        resp = self.test_client.get(self.API_BASE + '/1', headers=auth_header_all_permissions)
        self.assertEqual(resp.status_code, 404)
        resp_dict = json.loads(resp.data)
        self.assertEqual(resp_dict['success'], False)

    def test_delete_restaurant_by_id_none(self):
        """Test deleting a restaurant by a non-existent id number"""
        # Since this is a freshly created table, there are no restaurants
        resp = self.test_client.delete(self.API_BASE + '/1', headers=auth_header_all_permissions)
        self.assertEqual(resp.status_code, 404)

    def test_delete_restaurant_unauthorized(self):
        """Test delete request that lacks authorization header"""
        from espresso import db
        from espresso import Restaurant

        name = 'Restaurant Pandemic Plaza'
        db.session.add(Restaurant(name=name, creator='test-user@gmail.com'))
        db.session.commit()

        # Since this is a freshly created table, the first id should be 1
        resp = self.test_client.delete(self.API_BASE + '/1', headers={})
        self.assertEqual(resp.status_code, 401)

    def test_delete_restaurant_forbidden(self):
        """Test delete request for user who lacks authorization to delete"""
        from espresso import db
        from espresso import Restaurant

        name = 'Restaurant Pandemic Plaza'
        db.session.add(Restaurant(name=name, creator='test-user@gmail.com'))
        db.session.commit()

        # Since this is a freshly created table, the first id should be 1
        resp = self.test_client.delete(self.API_BASE + '/1', headers=auth_header_cru_restaurants)
        self.assertEqual(resp.status_code, 403)
