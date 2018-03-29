from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import requests, json

# Databases
from config.databases import role_corpus

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
    return 'Hello Scorers!'

def get_frequency_distribution():
    rcd_cursor = role_corpus.db['role_list_corpus_frequency_distribution_2018_03_27__013821_'].find({});
    frequency_distribution = {}
    for i in rcd_cursor:
        frequency_distribution[i['word']] = i['roles']
    return {
        "status": "OK",
        "frequency_distribution": frequency_distribution
    }
