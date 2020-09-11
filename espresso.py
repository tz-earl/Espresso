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

@app.route('/')
def index():
    return 'Hello from espresso'

@app.route('/restaurants')
def restaurants():
    try:
        restaurants = Restaurant.query.all()
    except Exception as ex:
        print('Failed to retrieve list of restaurants for "/restaurants" endpoint')
        print(f'Exception was thrown: {str(ex)}')
        ret_val = {'success': False,
            'message': 'List of restaurants could not be retrieved',
            'error-string': str(ex)
            }
    else:
        rest_list = []
        for rest in restaurants:
            rest_item = {'id':rest.id, 'name':rest.name, 'street':rest.street, 'suite':rest.suite,
                         'city':rest.city, 'state':rest.state, 'zip_code':rest.zip_code,
                         'phone_num':rest.phone_num, 'website':rest.website, 'email':rest.email,
                         'date_established':rest.date_established
                         }
            rest_list.append(rest_item)
        ret_val = {'success': True, 'restaurants': rest_list}
    finally:
        return jsonify(ret_val)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    print("Running espresso via app.run()")
    app.run()
