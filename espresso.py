#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    print("Running espresso via app.run()")
    app.run()
