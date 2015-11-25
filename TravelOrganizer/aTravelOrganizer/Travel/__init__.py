"""
The flask application package.
"""

from flask import Flask, render_template
from Travel.models.Repository import Repository

app = Flask(__name__)


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# Configurations
app.config.from_object('settings')

# Define the database object which is imported
# by modules and controllers

# repo = Repository(app.config['DATABASE_URI']) //backup
# repo = Repository()
repo = Repository(app.config['DATABASE_URI'])

# Build the database:
# This will create the database file


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return 'Could not find what you were looking for', 404

from Travel.views import *
