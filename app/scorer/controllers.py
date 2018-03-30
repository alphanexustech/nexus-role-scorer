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
    rcd_cursor = role_corpus.db[configurations.freq_dist_collection].find({});
    frequency_distribution = {}
    for i in rcd_cursor:
        frequency_distribution[i['word']] = i['roles']
    return {
        "status": "OK",
        "frequency_distribution": frequency_distribution
    }

def get_sorted_frequency_distribution():
    rcd_cursor = role_corpus.db[configurations.freq_dist_collection].find({});
    frequency_distribution = {}
    for i in rcd_cursor:
        frequency_distribution[i['word']] = len(i['roles'])
    return {
        "status": "OK",
        "frequency_distribution": frequency_distribution
    }

def get_member_distribution():
    rcd_cursor = role_corpus.db[configurations.membership_collection].find({});
    member_distribution = {}
    for i in rcd_cursor:
        member_distribution[i['role']] = i['data']
    return {
        "status": "OK",
        "member_distribution": member_distribution
    }

def get_stop_words():
    return {
        "status": "OK",
    }
