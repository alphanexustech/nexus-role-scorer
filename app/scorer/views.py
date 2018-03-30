from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import requests, json

from . import controllers

# mongo dependencies
import pymongo
from flask_pymongo import ObjectId

# bson
import json
from bson import json_util

scorer = Blueprint('scorer', __name__)

@scorer.route('/', methods=['GET'])
def default():
    return controllers.default()

@scorer.route('/freqdist/', methods=['GET'])
def get_frequency_distribution():
    return jsonify(controllers.get_frequency_distribution())

@scorer.route('/memberdist/', methods=['GET'])
def get_member_distribution():
    return jsonify(controllers.get_member_distribution())
