from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import requests, json

from . import controllers

# Configuration
from config import configurations

# mongo dependencies
import pymongo
from flask_pymongo import ObjectId

# bson
import json
from bson import json_util

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
def get_users():
    query = {}
    return jsonify(controllers.get_records(configurations.users_collection, query))

@users.route('/<id>/', methods=['GET'])
def get_user(id=None):
    query = {
        "age": 30,
    }
    return jsonify(controllers.get_record(configurations.users_collection, query))

@users.route('/', methods=['POST'])
def save_user():
    data = request.get_json()
    return jsonify(controllers.save_record(configurations.users_collection, data))

@users.route('/', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    return jsonify(controllers.delete_record(configurations.users_collection, data))
