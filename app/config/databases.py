from app import app
from flask_pymongo import PyMongo
from . import configurations

# File processing
import os
import csv

app.config['ROLECORPUS_DBNAME'] = 'role-corpus'
role_corpus = PyMongo(app, config_prefix='ROLECORPUS')

'''
Iniitlaize the application context with hash tables from mongo
'''
def common_set_roles(flaskResponse=None):

    #
    # Manually pruned data from CSV
    #

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "..\\..\\data\\meta_alternative_name_list.csv"
    abs_file_path = os.path.join(script_dir, rel_path)
    roles = {};

    with open(abs_file_path, encoding="utf8", newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in data:
            if row[2] == '1':
                if row[1] != '':
                    roles[row[0]] = row[1]
                else:
                    roles[row[0]] = row[0]

    csvfile.close();

    return roles

# This dict is useful for getting just the commons set
app.common_set_roles = common_set_roles()

def get_frequency_distribution():
    with app.app_context():
        rcd_cursor = role_corpus.db[configurations.freq_dist_collection].find({});
        frequency_distribution = {}
        for i in rcd_cursor:
            frequency_distribution[i['word']] = i['roles']
        return frequency_distribution

def get_bucketed_frequency_distribution():
    with app.app_context():
        rcd_cursor = role_corpus.db[configurations.freq_dist_collection].find({});
        frequency_distribution = {}
        for i in rcd_cursor:
            if len(i['roles']) not in frequency_distribution:
                frequency_distribution[len(i['roles'])] = [i['word']]
            else:
                frequency_distribution[len(i['roles'])].append(i['word'])

        return frequency_distribution

def get_role_stop_words():
    with app.app_context():
        data = get_bucketed_frequency_distribution()
        buckets = data
        stopwords = []
        # Add words that show up in over half of the roles.
        for bucket in buckets:
            if bucket > 444:
                stopwords += buckets[bucket]
        # Add words that show up in just once.
        stopwords += buckets[1]
        return stopwords

def get_member_distribution():
    with app.app_context():
        rcd_cursor = role_corpus.db[configurations.membership_collection].find({});
        member_distribution = {}
        for i in rcd_cursor:
            member_distribution[i['role']] = i['data']
        return member_distribution

def get_bucketed_member_distribution():
    with app.app_context():
        rcd_cursor = role_corpus.db[configurations.membership_collection].find({});
        member_distribution = {}
        for i in rcd_cursor:
            if len(i['data']) not in member_distribution:
                member_distribution[len(i['data'])] = [i['role']]
            else:
                member_distribution[len(i['data'])].append(i['role'])

        return member_distribution

# Iniitlaized hashtables
app.frequency_distribution = get_frequency_distribution()
app.bucketed_frequency_distribution = get_bucketed_frequency_distribution()
app.role_stop_words = get_role_stop_words()
app.member_distribution = get_member_distribution()
app.bucketed_member_distribution = get_bucketed_member_distribution()
