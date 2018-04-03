from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import requests, json

from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

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

def get_bucketed_frequency_distribution():
    rcd_cursor = role_corpus.db[configurations.freq_dist_collection].find({});
    frequency_distribution = {}
    for i in rcd_cursor:
        if len(i['roles']) not in frequency_distribution:
            frequency_distribution[len(i['roles'])] = [i['word']]
        else:
            frequency_distribution[len(i['roles'])].append(i['word'])

    return {
        "status": "OK",
        "frequency_distribution": frequency_distribution
    }


def get_role_stop_words():
    data = get_bucketed_frequency_distribution()
    buckets = data['frequency_distribution']
    stopwords = []
    # Add words that show up in over half of the roles.
    for bucket in buckets:
        if bucket > 444:
            stopwords += buckets[bucket]
    # Add words that show up in just once.
    stopwords += buckets[1]
    return {
        "status": "OK",
        "role_stop_words": stopwords,
        "length_role_stop_words": len(stopwords)
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

def get_bucketed_member_distribution():
    rcd_cursor = role_corpus.db[configurations.membership_collection].find({});
    member_distribution = {}
    for i in rcd_cursor:
        if len(i['data']) not in member_distribution:
            member_distribution[len(i['data'])] = [i['role']]
        else:
            member_distribution[len(i['data'])].append(i['role'])

    return {
        "status": "OK",
        "member_distribution": member_distribution
    }

def score_text(role_set=None, doc=None):
    result = get_role_stop_words()
    role_stop_words = result['role_stop_words']
    result = get_frequency_distribution()
    freqdist = result['frequency_distribution']
    if role_set == 'all_roles':
        if doc:

            lang = 'english'
            # Stop Words
            stop_words = stopwords.words(lang)
            list_of_words = [i.lower() for i in wordpunct_tokenize(doc) if i.lower() not in stop_words]

            for word in list_of_words:
                if word in freqdist:
                    print(freqdist[word])
                    print(word)

            return {
                "status": "OK",
            }
        else:
            return {
                "status": "OK",
                "message": "The document is missing."
            }
    else:
        return {
            "status": "OK",
            "message": "Not Implemented"
        }
