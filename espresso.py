#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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

@app.route('/restaurants', methods=['GET'])
def restaurants():
    try:
        restaurants = Restaurant.query.filter_by().order_by(Restaurant.id)
        rest_list = []
        for rest in restaurants:
            rest_item = restaurant_to_dict(rest)
            rest_list.append(rest_item)
    except Exception as ex:
        print('Failed to retrieve list of restaurants for "/restaurants" endpoint')
        print(f'Exception was thrown: {str(ex)}')
        ret_val = {'success': False,
            'message': 'Server failure: list of restaurants could not be retrieved',
            'error-string': str(ex)
            }
        return jsonify(ret_val), 500
    else:
        ret_val = {'success': True, 'restaurants': rest_list}
        return jsonify(ret_val), 200

@app.route('/restaurants/<rest_id>', methods=['GET'])
def restaurant_by_id(rest_id):
    try:
        rest = Restaurant.query.get(rest_id)
    except Exception as ex:
        print(f'Failed to retrieve restaurant for "/restaurants/{rest_id}" endpoint')
        ret_val = {'success': False,
            'message': f'Server failure: restaurant with id number {rest_id} could not be retrieved',
            'error-string': str(ex)
            }
        return jsonify(ret_val), 500
    else:
        if rest:
            rest_item = restaurant_to_dict(rest)
            ret_val = {'success': True, 'restaurant': rest_item}
            return jsonify(ret_val), 200
        else:
            ret_val = {'success': False, 'message': f'No restaurant with id {rest_id} found'}
            return jsonify(ret_val), 404

@app.errorhandler(404)
def not_found(error):
    ret_val = {'success': False,
               'message': 'Resource was not found, check the url',
               'error-string': str(error)
               }
    return jsonify(ret_val), 404

@app.errorhandler(405)
def method_not_allowed(error):
    ret_val = {'success': False,
               'message': 'Method not allowed for the requested URL',
               'error-string': str(error)
               }
    return jsonify(ret_val), 405

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    print("Running espresso via app.run()")
    app.run()
