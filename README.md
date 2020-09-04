# Espresso

Espresso is a learning exercise by Ryan Bacon and myself to build
a small web app from scratch. The app will be like a simple version
of Yelp that collects and displays user reviews of places that serve espresso.

Initially, this project will consist of a backend implemented in Flask,
SQLAlchemy, and PostgreSQL to support an API. The frontend will be a web client
using asynchronous calls to the API.

To run the app using flask on the command line,

`$ export FLASK_APP=espresso.py`  
`$ flask run`

Or you can run via

`$ python3 espresso.py`

Executing within an IDE such as PyCharm is great since it has a
graphical debugger.

The Python modules used are listed in `requirements.txt`
One way to install all of these modules is to do:

`$ pip3 install -r requirements.txt`

We are using PostgreSQL for the backend database. On Ubuntu systems,
PostgreSQL can be installed by the following command. Our current
version is 10.14

`$ sudo apt-get install postgres`

Then you might want to modify the PATH like so:

`$ export PATH=/usr/lib/postgresql/10/bin:$PATH`

For people who like to use command line utilities, Postgres comes
with `psql`. It is very handy for accessing and manipulating
the Postgres databases with its commands as well as
SQL statements.
