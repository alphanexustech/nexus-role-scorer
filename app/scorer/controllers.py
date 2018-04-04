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

'''
word_count - the total number of words found in the document signaling the role
role_length - the total possible number of roles
'''
def calculate_normalized_role_score(word_count, role_length):
    return word_count/role_length * 100

def calculate_role_density_score(r_role_score, length_words_no_stop):
    r_role_density_score = r_role_score/length_words_no_stop * 100
    return r_role_density_score

'''
word_count - the total number of words found in the document signaling the role
role_length - the total possible number of roles
'''
def calculate_role_scores(word_count, role_length, length_words_no_stop):
    scores = {}
    scores['normalized_role_score'] = calculate_normalized_role_score(word_count, role_length)
    scores['role_density_score'] = calculate_role_density_score(scores['normalized_role_score'], length_words_no_stop)
    return scores

def format_name(name):
    # Handle the other names, but return back a title case format in most cases
    if (name == 'yang di-pertuan agong'):
        return 'Yang di-Pertuan Agong'
    else:
        return name.title()

def process_text(doc=None):
    rsw_result = get_role_stop_words()
    fd_result = get_frequency_distribution()
    md_result = get_member_distribution()
    tokenized_words = wordpunct_tokenize(doc)

    lang = 'english'
    # Stop Words
    stop_words = stopwords.words(lang)
    role_stop_words = rsw_result['role_stop_words']
    all_stop_words = stop_words + role_stop_words
    freqdist = fd_result['frequency_distribution']
    memberdist = md_result['member_distribution']

    list_of_words = [i.lower() for i in tokenized_words if i.lower() not in all_stop_words]

    r_roles_found = {}
    for word in list_of_words:
        # IDEA: Find stem and lemma words
        if word in freqdist:
            found_roles = list(set(freqdist[word]))
            for role in found_roles:
                if role not in r_roles_found:
                    r_roles_found[role] = [word]
                else:
                    r_roles_found[role] += [word]

    result = []
    for role in r_roles_found:
        words_found = r_roles_found[role]
        role_length = len(memberdist[role])
        r = {}
        r['name'] = role
        r['pretty_name'] = format_name(role)
        r['words_found'] = words_found
        r['word_count'] = len(words_found)
        r['role_length'] = role_length
        r['document_length'] = len(tokenized_words)
        # IDEA: Find POS for each word here, too.
        r['scores'] = calculate_role_scores(len(words_found), role_length, len(tokenized_words))
        result.append(r)
    sorted_result = sorted(result, key=lambda x: x['scores']['role_density_score'], reverse=True)
    return sorted_result

def analyze_text(role_set=None, doc=None):
    if role_set == 'all_roles':
        if doc:
            result = process_text(doc)
            return {
                "status": "OK",
                "data": result
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
