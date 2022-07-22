#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from flask import Flask, Blueprint
from flask_cors import CORS
from Helper.mongo_connection import MongoConnection
from datetime import datetime, timedelta
from flask import send_from_directory
import csv,time,requests,json

app = Flask(__name__)
CORS(app)
app.config.from_object('settings')

connection = MongoConnection(db=app.config['MONGODB_DB'], host=app.config['MONGODB_HOST'], port=app.config['MONGODB_PORT'],
                             user=app.config['MONGODB_USERNAME'], password=app.config['MONGODB_PASSWORD'])
def get_chatlogs_with_limit(value):
    """
                This service can be used for list chat logs with limit. Mongo query gets last recorded logs according
                to defined limit
    """

    collection = connection.get_collection('chatlogs')
    return list(collection.find().sort([('creation_date', -1)]).limit(value))


def get_excel_export_for_all_chatlogs():
    """
                    This service can be used for export chat logs. Csv include below values;
                    - input
                    - username
                    - current_threshold
                    - intent
                    - confidence
                    - creation_date
                    - preConfidence
                    - preIntent

    """
    df = pd.DataFrame(
        columns=['id', 'input', 'username', 'cbid', 'intent', 'confidence', 'speechResponse', 'current_threshold', 'creation_date',
                 'preConfidence', 'preIntent', 'conversationType'])
    collection = connection.get_collection('chatlogs')
    for x in collection.find({"$and": [{"context.cbid": { "$exists": True }},
                                   {"creation_date": {'$lte': datetime.today()-timedelta(0)}},
                                   {"creation_date": {'$gte': datetime.today()-timedelta(360)}}]}):
        df = df.append({'id': x['_id'],
                        'input': x['input'],
                        'username': x['context']['username'],
                        'cbid': x['context']['cbid'],
                        'intent': x['intent']['id'],
                        'confidence': x['intent']['confidence'],
                        'speechResponse': x['speechResponse'],
                        'current_threshold': x['current_threshold'],
                        'creation_date': x['creation_date'],
                        'preConfidence': x['preConfidence'],
                        'preIntent': x['preIntent'],
                        'conversationType': x['conersationType']
                        }, ignore_index=True)

    writer=pd.ExcelWriter("../reports/chatlogs.xlsx")
    df.to_excel(writer, 'AllChats')
    writer.save()

    return send_from_directory("../reports/","chatlogs.xlsx", as_attachment=True)



def get_excel_export_for_all_intents():
    """
                    This service can be used for export all intents. Csv include below values;
                    - id
                    - text
                    - speechResponse

    """
    df = pd.DataFrame(columns=['name', 'intentId', 'speechResponse', 'trainingData', 'parametername', 'prompt'])
    df2 = pd.DataFrame(columns=['name', 'intentId', 'speechResponse'])

    collection = connection.get_collection('intent')
    for x in collection.find({"trainingData": { "$exists": True }}):
        for y in x['trainingData']:
            if ("'parameters': [{" in str(x)):
                for z in x['parameters']:
                    df = df.append({'name': x['name'],
                                    'intentId': x['intentId'],
                                    'speechResponse': x['speechResponse'],
                                    'trainingData': y['text'],
                                    'parametername': z['name'],
                                    'prompt': z['prompt']
                                    }, ignore_index=True)
            else:
                df = df.append({'name': x['name'],
                                'intentId': x['intentId'],
                                'speechResponse': x['speechResponse'],
                                'trainingData': y['text']
                                }, ignore_index=True)

    writer=pd.ExcelWriter("../reports/intents.xlsx")
    df.to_excel(writer, 'Intents and Trains')

    for x in collection.find():
        df2 = df2.append({'name': x['name'],
                          'intentId': x['intentId'],
                          'speechResponse': x['speechResponse']
                          }, ignore_index=True)

    df2.to_excel(writer, 'Intents')
    writer.save()

    return send_from_directory("../reports/","intents.xlsx", as_attachment=True)



def get_excel_export_for_chatlogs_acoording_to_date(year, month, day):
    """
                        This service can be used for export chat logs from posted date to now. Csv include below values;
                        - input
                        - username
                        - current_threshold
                        - intent
                        - confidence
                        - creation_date
                        - preConfidence
                        - preIntent

    """
    start = datetime(year, month, day)
    end = datetime.now()

    df = pd.DataFrame(
        columns=['id', 'input', 'username', 'cbid', 'intent', 'confidence', 'speechResponse', 'current_threshold', 'creation_date',
                 'preConfidence', 'preIntent', 'conversationType'])

    collection = connection.get_collection('chatlogs')

    for x in collection.find({"$and": [{"context.cbid": { "$exists": True }},
                                   {"creation_date": {'$lte': start-timedelta(-1)}},
                                   {"creation_date": {'$gte': start}}]}):
        df = df.append({'id': x['_id'],
                        'input': x['input'],
                        'username': x['context']['username'],
                        'cbid': x['context']['cbid'],
                        'intent': x['intent']['id'],
                        'confidence': x['intent']['confidence'],
                        'speechResponse': x['speechResponse'],
                        'current_threshold': x['current_threshold'],
                        'creation_date': x['creation_date'],
                        'preConfidence': x['preConfidence'],
                        'preIntent': x['preIntent'],
                        'conversationType': x['conersationType']
                        }, ignore_index=True)

    writer=pd.ExcelWriter("../reports/chatlogs_"+str(year)+str(month)+str(day)+".xlsx")
    df.to_excel(writer, 'AllChats')
    writer.save()

    return send_from_directory("../reports/","chatlogs_"+str(year)+str(month)+str(day)+".xlsx", as_attachment=True)


def get_excel_export_for_chatlogs_acoording_to_lastdate(value):
    """
                        This service can be used for export chat logs from posted date to now. Csv include below values;
                        - input
                        - username
                        - current_threshold
                        - intent
                        - confidence
                        - creation_date
                        - preConfidence
                        - preIntent

    """
    df = pd.DataFrame(
        columns=['id', 'input', 'username', 'cbid', 'dbid', 'category', 'intent', 'confidence', 'speechResponse', 'current_threshold', 'creation_date',
                 'preConfidence', 'preIntent', 'conversationType'])

    collection = connection.get_collection('chatlogs')
    for x in collection.find({"$and": [{"context.cbid": { "$exists": True }},
                                   {"creation_date": {'$lte': datetime.today()}},
                                   {"creation_date": {'$gte': datetime.today()-timedelta(value)}}]}):
        df = df.append({'id': x['_id'],
                        'input': x['input'],
                        'username': x['context']['username'] if (x['context'].get('username', None)) else "",
                        'cbid': x['context']['cbid'],
                        'dbid': x['context']['dbid'] if (x['context'].get('dbid', None)) else "",
                        'category': x['context']['category'] if (x['context'].get('category', None)) else "",
                        'intent': x['intent']['id'],
                        'confidence': x['intent']['confidence'],
                        'speechResponse': x['speechResponse'],
                        'current_threshold': x['current_threshold'],
                        'creation_date': x['creation_date'],
                        'preConfidence': x['preConfidence'],
                        'preIntent': x['preIntent'],
                        'conversationType': x['conersationType']
                        }, ignore_index=True)

    writer=pd.ExcelWriter("../reports/chatlogs_last_"+str(value)+"_days.xlsx")
    df.to_excel(writer, 'AllChats')
    writer.save()

    return send_from_directory("../reports/","chatlogs_last_"+str(value)+"_days.xlsx", as_attachment=True)



def get_chatlogs_session_count():
    """
                This service can be used for count os chat sessions
    """
    collection = connection.get_collection('chatlogs')
    result = {}
    result['result'] = collection.count()
    return result


def get_chatlogs_fallback_count():
    """
                This service can be used for count of fallbacks
    """
    collection = connection.get_collection('chatlogs')
    result = {'result': collection.find({'intent.id': 'fallback'}).count()}
    return result


def get_chatlogs_sessions_count_last_x_days(value):
    """
                This service can be used for count of fallbacks in 30 days
    """
    now = datetime.utcnow()
    last_d = now - timedelta(days=value)
    collection = connection.get_collection('chatlogs')
    result = {'result': collection.find({"creation_date": {"$gte": last_d}}).count()}
    return result


def get_chatlogs_fallbacks_count_last_x_days(value):
    """
                This service can be used for count of fallbacks in 30 days
    """
    now = datetime.utcnow()
    last_d = now - timedelta(days=value)
    collection = connection.get_collection('chatlogs')
    result = {'result': collection.find({'intent.id': 'fallback', "creation_date": {"$gte": last_d}}).count()}
    return result

def get_chatlogs_monthly_count():
    """
                This service can be used for count of fallbacks
    """
    collection = connection.get_collection('chatlogs')
    result = collection.aggregate([{"$group": {"_id": {"$month": "$creation_date"}, "count": {"$sum": 1}}}])
    list_of_months = ["nothing", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül",
                      "Ekim", "Kasım", "Aralık"]
    result_sorted = sorted(result, key=lambda x: x['_id'], reverse=False)
    month = {}
    for res in result_sorted:
        month[list_of_months[res['_id']]] = res['count']
    return month


def get_chatlogs_analytics():
    """
                This service can be used for some analytics results
    """
    result = {}
    collection = connection.get_collection('chatlogs')
    action = collection.find({"context.username": { "$exists": True }}).count()
    unique_user = len(collection.find({"context.username": { "$exists": True }}).distinct('context.username'))
    fallback = collection.find({"intent.id": "fallback" , "context.username": {"$exists": True}}).count()
    chat_to_live = collection.find({"intent.id": "chat_to_live","context.username": {"$exists": True}}).count()
    result['action'] = action
    if action:
        result['unique_user'] = unique_user
        result['fallback'] = fallback
        result['chat_to_live'] = chat_to_live
    if unique_user:
        result['average_question'] = action/unique_user
        result['completion_percentage'] = 100 - (chat_to_live / unique_user * 100)
    if action:
        result['response_percentage'] = 100 - (fallback / action * 100)
    if action:
        result['fallback_and_live'] = 100 - ((fallback + chat_to_live) / action * 100)

    return result


def get_excel_test_results():
    """
                    This service can be used for export all intents. Csv include below values;
                    - id
                    - text
                    - speechResponse

    """
    df = pd.DataFrame(columns=['name', 'intentId', 'speechResponse', 'trainingData', 'parametername', 'prompt'])
    df2 = pd.DataFrame(columns=['name', 'intentId', 'speechResponse'])
    df3 = pd.DataFrame(columns=['input', 'actualintent', 'intent', 'confidence', 'preIntent', 'preConfidence'])
    count = 0
    headers = {'Content-type': 'application/json'}

    collection = connection.get_collection('intent')

    for x in collection.find({"trainingData": { "$exists": True }}):
        for y in x['trainingData']:
            if ("'parameters': [{" in str(x)):
                for z in x['parameters']:
                    df = df.append({'name': x['name'],
                                    'intentId': x['intentId'],
                                    'speechResponse': x['speechResponse'],
                                    'trainingData': y['text'],
                                    'parametername': z['name'],
                                    'prompt': z['prompt']
                                    }, ignore_index=True)
            else:
                df = df.append({'name': x['name'],
                                'intentId': x['intentId'],
                                'speechResponse': x['speechResponse'],
                                'trainingData': y['text']
                                }, ignore_index=True)

    for x in collection.find():
        df2 = df2.append({'name': x['name'],
                          'intentId': x['intentId'],
                          'speechResponse': x['speechResponse']
                          }, ignore_index=True)

    for index, row in df.iterrows():
        count += 1
        # if count%100 ==0:
        # print(str(count) + " \t-\t " + time.asctime( time.localtime(time.time()) ))
        json_data = {}
        context = {}
        # context['username'] = "semih_bot1"
        # context['cbid'] = "007"
        json_data['context'] = context
        json_data['input'] = row[3]
        response = requests.post(app.config['SCORE_URL'], json=json_data, headers=headers)
        dataResp = response.text
        x = json.loads(dataResp)

        df3 = df3.append({
            'input': x['input'],
            'actualintent': row[1],
            'intent': x['intent']['id'],
            'confidence': x['intent']['confidence'],
            'preIntent': x['preIntent'],
            'preConfidence': x['preConfidence']
        }, ignore_index=True)

    df4 = df3[df3.actualintent != df3.intent]

    writer=pd.ExcelWriter("../reports/test_results.xlsx")
    df4.to_excel(writer, 'Errors')
    df3.to_excel(writer, 'All Results')
    writer.save()

    return send_from_directory("../reports/","test_results.xlsx", as_attachment=True)

