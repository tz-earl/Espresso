#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import logging

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify
from flask_cors import CORS

from sqlalchemy import exc as sqlalchemy_exc
from werkzeug import exceptions as werkzeug_exc

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# These values for the origins argument to CORS are just examples
# of what might be allowed as far as the origins of requestors.
CORS(app, supports_credentials=True, origins=['http://127.0.0.1:*', 'http://localhost:*'])


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    street = db.Column(db.String)
    suite = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)
    phone_num = db.Column(db.String)
    website = db.Column(db.String)
    email = db.Column(db.String)
    date_established = db.Column(db.String)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

RESTAURANTS_API_V1_BASE = '/api/v1/restaurants'
API_VERSION = 'v1'

@app.route('/', methods=['GET'])
def index():
    return 'Hello from espresso'

def restaurant_to_dict(rest):
    """Convert a Restaurant object to a dictionary"""
    rest_item = {'id': rest.id, 'name': rest.name, 'street': rest.street, 'suite': rest.suite,
                 'city': rest.city, 'state': rest.state, 'zip_code': rest.zip_code,
                 'phone_num': rest.phone_num, 'website': rest.website, 'email': rest.email,
                 'date_established': rest.date_established
                 }
    return rest_item

def retrieve_restaurant(rest_id):
    """Given a restaurant id, retrieve it from the model/database"""
    rest = ret_val = http_status = None
    try:
        rest = Restaurant.query.get(rest_id)
    except (sqlalchemy_exc.ProgrammingError, sqlalchemy_exc.DataError) as ex:
        logging.error(f'Failed to retrieve restaurant for id {rest_id}')
        logging.error(f'Exception was thrown: {str(ex)}')
        ret_val = {'success': False,
                   'id': rest_id,
                   'restaurant': None,
                   'message': f'Server failure: restaurant with id number {rest_id} could not be retrieved',
                   'api_version': API_VERSION
                   }
        if isinstance(ex, sqlalchemy_exc.ProgrammingError):
            http_status = 500
        elif isinstance(ex, sqlalchemy_exc.DataError):
            http_status = 400
    else:
        if not rest:
            ret_val = {'success': False, 'id': rest_id, 'restaurant': None,
                       'message': f'No restaurant with id {rest_id} found',
                       'api_version': API_VERSION
                      }
            http_status = 404

    return (rest, ret_val, http_status)

@app.route(RESTAURANTS_API_V1_BASE, methods=['GET'])
def restaurants():
    try:
        restaurants = Restaurant.query.filter_by().order_by(Restaurant.id)
        rest_list = []
        for rest in restaurants:
            rest_item = restaurant_to_dict(rest)
            rest_list.append(rest_item)
    except Exception as ex:
        logging.error('Failed to retrieve list of restaurants for "/restaurants" endpoint')
        logging.error(f'Exception was thrown: {str(ex)}')
        ret_val = {'success': False,
            'restaurants': None,
            'message': 'Server failure: list of restaurants could not be retrieved',
            'api_version': API_VERSION
            }
        return jsonify(ret_val), 500

    ret_val = {'success': True, 'restaurants': rest_list, 'message': None, 'api_version': API_VERSION}
    return jsonify(ret_val), 200

@app.route(RESTAURANTS_API_V1_BASE + '/<rest_id>', methods=['GET'])
def restaurant_by_id(rest_id):
    rest, ret_val, http_status = retrieve_restaurant(rest_id)
    if ret_val:  # Something went awry
        return jsonify(ret_val), http_status

    rest_item = restaurant_to_dict(rest)
    ret_val = {'success': True, 'id': rest_id, 'restaurant': rest_item, 'message': None,
               'api_version': API_VERSION
              }
    return jsonify(ret_val), 200

@app.route(RESTAURANTS_API_V1_BASE + '/create', methods=['POST'])
def restaurant_create():
    json_dict = None
    try:
        json_dict = request.json
    except werkzeug_exc.BadRequest as ex:
        logging.warning('Could not decode the json content')
        logging.warning(str(ex))
        ret_val = {'success': False, 'id': None, 'message': str(ex), 'api_version': API_VERSION}
        return jsonify(ret_val), 400

    name = json_dict.get('name', None)  # name is required, validate this
    if not name:
        ret_val = {'success': False, 'id': None, 'message': f'Name of restaurant is required',
                   'api_version': API_VERSION
                  }
        return jsonify(ret_val), 400

    rest = Restaurant(name=name)

    rest.street = json_dict.get('street', None)
    rest.suite = json_dict.get('suite', None)
    rest.city = json_dict.get('city', None)
    rest.state = json_dict.get('state', None)
    rest.zip_code = json_dict.get('zip_code', None)
    rest.phone_num = json_dict.get('phone_num', None)
    rest.website = json_dict.get('website', None)
    rest.email = json_dict.get('email', None)
    rest.date_established = json_dict.get('date_established', None)

    db.session.add(rest)
    db.session.commit()

    ret_val = {'success': True,
               'id': rest.id,
               'message': f'Restaurant created with name: {rest.name}',
               'api_version': API_VERSION
               }
    return jsonify(ret_val), 200

@app.route(RESTAURANTS_API_V1_BASE + '/<rest_id>', methods=['PUT'])
def restaurant_update(rest_id):
    rest, ret_val, http_status = retrieve_restaurant(rest_id)
    if ret_val:  # Something went awry
        return jsonify(ret_val), http_status

    json_dict = None
    try:
        json_dict = request.json
    except werkzeug_exc.BadRequest as ex:
        logging.warning('Could not decode the json content')
        logging.warning(str(ex))
        ret_val = {'success': False, 'id': rest.id, 'restaurant': None, 'message': str(ex),
                   'api_version': API_VERSION
                  }
        return jsonify(ret_val), 400

    rest.name = json_dict.get('name', rest.name)
    rest.street = json_dict.get('street', rest.street)
    rest.suite = json_dict.get('suite', rest.suite)
    rest.city = json_dict.get('city', rest.city)
    rest.state = json_dict.get('state', rest.state)
    rest.zip_code = json_dict.get('zip_code', rest.zip_code)
    rest.phone_num = json_dict.get('phone_num', rest.phone_num)
    rest.website = json_dict.get('website', rest.website)
    rest.email = json_dict.get('email', rest.email)
    rest.date_established = json_dict.get('date_established', rest.date_established)

    # Restaurant name may not be blank
    if not rest.name:
        ret_val = {'success': False, 'id': rest.id, 'restaurant': None,
                   'message': f'Name of restaurant may not be blank',
                   'api_version': API_VERSION
                  }
        return jsonify(ret_val), 400

    db.session.add(rest)
    db.session.commit()

    ret_val = {'success': True,
               'id': rest.id,
               'restaurant': None,
               'message': f"Restaurant updated: {rest.name}",
               'api_version': API_VERSION
               }
    return jsonify(ret_val), 200

@app.route(RESTAURANTS_API_V1_BASE + '/<rest_id>', methods=['DELETE'])
def restaurant_delete(rest_id):
    rest, ret_val, http_status = retrieve_restaurant(rest_id)
    if ret_val:  # Something went awry
        return jsonify(ret_val), http_status

    db.session.delete(rest)
    db.session.commit()

    ret_val = {'success': True,
               'id': rest_id,
               'restaurant': None,
               'message': f'Restaurant deleted: {rest.name}',
               'api_version': API_VERSION
               }
    return jsonify(ret_val), 200

@app.errorhandler(400)
def bad_request(error):
    logging.warning(error)
    ret_val = {'success': False,
               'message': str(error)
               }
    return jsonify(ret_val), 400

@app.errorhandler(404)
def not_found(error):
    logging.warning(error)
    ret_val = {'success': False,
               'message': 'Resource was not found, check the url',
               }
    return jsonify(ret_val), 404

@app.errorhandler(405)
def method_not_allowed(error):
    logging.warning(error)
    ret_val = {'success': False,
               'message': 'Method not allowed for the requested URL',
               }
    return jsonify(ret_val), 405

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    print("Running espresso via app.run()")
    app.run()
