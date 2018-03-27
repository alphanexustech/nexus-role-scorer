from app import app
from flask_pymongo import PyMongo

app.config['BOILER_DBNAME'] = 'boilerplate_database'
boilerplate_database = PyMongo(app, config_prefix='BOILER_DBNAME')
