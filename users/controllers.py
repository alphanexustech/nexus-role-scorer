from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import requests, json

# Databases
from config.databases import boilerplate_database

# Configuration
from config import configurations

# mongo dependencies
import pymongo
from flask_pymongo import ObjectId

# bson
import json
from bson import json_util

# Date
from datetime import datetime

def default():
    return 'Hello Users!'

def save_record(collection, content):

    # IDEA: Not the best way to create a collection if it doesn't exist
    try:
        boilerplate_database.db.create_collection(collection)
    except Exception as e:
        print(e)

    collection = boilerplate_database.db[collection]

    collection.insert(content)
    return {"message": 'Record Saved'}

def get_record(collection, query):

    cursor = boilerplate_database.db[collection].find(query);
    if cursor:
        return json.loads(json_util.dumps(cursor[0]))
    else:
        return {"message": 'The database is empty'}

def get_records(collection, query):

    data = []
    cursor = boilerplate_database.db[collection].find(query);

    for i in cursor:
        data.append(i);
    if len(data) > 0:
        return json.loads(json_util.dumps(data))
    else:
        return {"message": 'The database is empty'}

def delete_record(collection, query):

    data = []
    cursor = boilerplate_database.db[collection].remove(query);

    return {"message": 'Record Deleted'}
