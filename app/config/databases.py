from app import app
from flask_pymongo import PyMongo

app.config['ROLECORPUS_DBNAME'] = 'role-corpus'
role_corpus = PyMongo(app, config_prefix='ROLECORPUS')
