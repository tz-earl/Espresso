#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import logging

from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify
from flask_cors import CORS, cross_origin

from sqlalchemy import exc as sqlalchemy_exc
from werkzeug import exceptions as werkzeug_exc

from auth0_tokens import AuthError, requires_auth, requires_scope

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

DEF_MAX_STR_LEN = 255 # The default max string length
MAX_COMMENT_LEN = 1000 # Max length of comments in reviews

class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(DEF_MAX_STR_LEN), nullable=False)
    street = db.Column(db.String(DEF_MAX_STR_LEN))
    suite = db.Column(db.String(DEF_MAX_STR_LEN))
    city = db.Column(db.String(DEF_MAX_STR_LEN))
    state = db.Column(db.String(DEF_MAX_STR_LEN))
    zip_code = db.Column(db.String(DEF_MAX_STR_LEN))
    phone_num = db.Column(db.String(DEF_MAX_STR_LEN))
    website = db.Column(db.String(DEF_MAX_STR_LEN))
    email = db.Column(db.String(DEF_MAX_STR_LEN))
    date_established = db.Column(db.String(DEF_MAX_STR_LEN))
    creator = db.Column(db.String(DEF_MAX_STR_LEN), nullable=False)

    reviews = db.relationship('Review', backref='rest_reviewed', lazy=True, uselist=True)


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(DEF_MAX_STR_LEN))  # The author's name (aka author id) is from Auth0.
    date = db.Column(db.Date)
    rating = db.Column(db.SmallInteger)
    comment = db.Column(db.String(MAX_COMMENT_LEN))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

RESTAURANTS_API_BASE = '/api/v2/restaurants'
REVIEWS_API_BASE = '/api/v2/reviews'
API_VERSION = '2.0'


@app.route('/', methods=['GET'])
def index():
    return 'Hello from espresso'


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


def restaurant_to_dict(rest):
    """Convert a Restaurant object to a dictionary"""
    rest_item = {'id': rest.id, 'name': rest.name, 'street': rest.street, 'suite': rest.suite,
                 'city': rest.city, 'state': rest.state, 'zip_code': rest.zip_code,
                 'phone_num': rest.phone_num, 'website': rest.website, 'email': rest.email,
                 'date_established': rest.date_established, 'creator': rest.creator
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

def get_dict_value_trunc(some_dict, which_prop, default=None, max_length=DEF_MAX_STR_LEN):
    """Get a key value from a dict and truncate its length if too long"""
    prop_value = some_dict.get(which_prop, default)
    if isinstance(prop_value, str):
        return prop_value[:max_length]
    else:
        return prop_value


@app.route(RESTAURANTS_API_BASE, methods=['GET'])
@cross_origin()
@requires_auth
def restaurants():
    if not requires_scope('read:restaurants'):
        raise AuthError({"success": False,
                         "message": "No access to this resource"}, 403)

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


@app.route(RESTAURANTS_API_BASE + '/<rest_id>', methods=['GET'])
@cross_origin()
@requires_auth
def restaurant_by_id(rest_id):
    if not requires_scope('read:restaurants'):
        raise AuthError({"success": False,
                         "message": "No access to this resource"}, 403)

    rest, ret_val, http_status = retrieve_restaurant(rest_id)
    if ret_val:  # Something went awry
        return jsonify(ret_val), http_status

    rest_item = restaurant_to_dict(rest)
    ret_val = {'success': True, 'id': rest_id, 'restaurant': rest_item, 'message': None,
               'api_version': API_VERSION
              }
    return jsonify(ret_val), 200


@app.route(RESTAURANTS_API_BASE + '/create', methods=['POST'])
@cross_origin()
@requires_auth
def restaurant_create():
    if not requires_scope('create:restaurants'):
        raise AuthError({"success": False,
                         "message": "No access to this resource"}, 403)

    json_dict = None
    try:
        json_dict = request.json
    except werkzeug_exc.BadRequest as ex:
        logging.error('Could not decode the json content')
        logging.error(str(ex))
        ret_val = {'success': False, 'id': None, 'message': str(ex), 'api_version': API_VERSION}
        return jsonify(ret_val), 400

    name = get_dict_value_trunc(json_dict, 'name')  # name is required, validate this
    if not name:
        ret_val = {'success': False, 'id': None, 'message': f'Name of restaurant is required',
                   'api_version': API_VERSION
                  }
        return jsonify(ret_val), 400

    creator = get_dict_value_trunc(json_dict, 'creator')  # creator is required, validate this
    if not creator:
        ret_val = {'success': False, 'id': None, 'message': f'Creator of restaurant is required',
                   'api_version': API_VERSION
                  }
        return jsonify(ret_val), 400

    rest = Restaurant(name=name, creator=creator)

    rest.street = get_dict_value_trunc(json_dict, 'street')
    rest.suite = get_dict_value_trunc(json_dict, 'suite')
    rest.city = get_dict_value_trunc(json_dict, 'city')
    rest.state = get_dict_value_trunc(json_dict, 'state')
    rest.zip_code = get_dict_value_trunc(json_dict, 'zip_code')
    rest.phone_num = get_dict_value_trunc(json_dict, 'phone_num')
    rest.website = get_dict_value_trunc(json_dict, 'website')
    rest.email = get_dict_value_trunc(json_dict, 'email')
    rest.date_established = get_dict_value_trunc(json_dict, 'date_established')

    db.session.add(rest)
    db.session.commit()

    ret_val = {'success': True,
               'id': rest.id,
               'message': f'Restaurant created with name: {rest.name}',
               'api_version': API_VERSION
               }
    return jsonify(ret_val), 200


@app.route(RESTAURANTS_API_BASE + '/<rest_id>', methods=['PUT'])
@cross_origin()
@requires_auth
def restaurant_update(rest_id):
    if not requires_scope('update:restaurants'):
        raise AuthError({"success": False,
                         "message": "No access to this resource"}, 403)

    rest, ret_val, http_status = retrieve_restaurant(rest_id)
    if ret_val:  # Something went awry
        return jsonify(ret_val), http_status

    json_dict = None
    try:
        json_dict = request.json
    except werkzeug_exc.BadRequest as ex:
        logging.error('Could not decode the json content')
        logging.error(str(ex))
        ret_val = {'success': False, 'id': rest.id, 'restaurant': None, 'message': str(ex),
                   'api_version': API_VERSION
                  }
        return jsonify(ret_val), 400

    rest.name = get_dict_value_trunc(json_dict, 'name', rest.name)
    rest.street = get_dict_value_trunc(json_dict, 'street', rest.street)
    rest.suite = get_dict_value_trunc(json_dict, 'suite', rest.suite)
    rest.city = get_dict_value_trunc(json_dict, 'city', rest.city)
    rest.state = get_dict_value_trunc(json_dict, 'state', rest.state)
    rest.zip_code = get_dict_value_trunc(json_dict, 'zip_code', rest.zip_code)
    rest.phone_num = get_dict_value_trunc(json_dict, 'phone_num', rest.phone_num)
    rest.website = get_dict_value_trunc(json_dict, 'website', rest.website)
    rest.email = get_dict_value_trunc(json_dict, 'email', rest.email)
    rest.date_established = get_dict_value_trunc(json_dict, 'date_established', rest.date_established)

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


@app.route(RESTAURANTS_API_BASE + '/<rest_id>', methods=['DELETE'])
@cross_origin()
@requires_auth
def restaurant_delete(rest_id):
    if not requires_scope('delete:restaurants'):
        raise AuthError({"success": False,
                         "message": "No access to this resource"}, 403)

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


def review_to_dict(rev):
    """Convert a Review object to a dictionary"""
    review_item = {'id': rev.id, 'author': rev.author, 'date': rev.date, 'rating': rev.rating,
                   'comment': rev.comment, 'restaurant_id': rev.restaurant_id
                  }
    return review_item


@app.route(REVIEWS_API_BASE, methods=['GET'])
@cross_origin()
@requires_auth
def reviews():
    if not requires_scope('read:reviews'):
        raise AuthError({"success": False,
                         "message": "No access to this resource"}, 403)

    try:
        reviews = Review.query.filter_by().order_by(Review.id)
        reviews_list = []
        for rev in reviews:
            review_item = review_to_dict(rev)
            reviews_list.append(review_item)
    except Exception as ex:
        logging.error('Failed to retrieve list of reviews for "/reviews" endpoint')
        logging.error(f'Exception was thrown: {str(ex)}')
        ret_val = {'success': False,
            'reviews': None,
            'message': 'Server failure: list of reviews could not be retrieved',
            'api_version': API_VERSION
            }
        return jsonify(ret_val), 500

    ret_val = {'success': True, 'reviews': reviews_list, 'message': None, 'api_version': API_VERSION}
    return jsonify(ret_val), 200


@app.errorhandler(400)
def bad_request(error):
    logging.error(error)
    ret_val = {'success': False,
               'message': str(error)
               }
    return jsonify(ret_val), 400


@app.errorhandler(404)
def not_found(error):
    logging.error(error)
    ret_val = {'success': False,
               'message': 'Resource was not found, check the url',
               }
    return jsonify(ret_val), 404


@app.errorhandler(405)
def method_not_allowed(error):
    logging.error(error)
    ret_val = {'success': False,
               'message': 'Method not allowed for the requested URL',
               }
    return jsonify(ret_val), 405


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    print("Running espresso via app.run()")
    app.run()
