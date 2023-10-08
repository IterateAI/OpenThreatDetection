import json
from collections import namedtuple
from json import JSONEncoder
from string import Template
from config import db
import pymongo
from datetime import datetime
from bson import ObjectId 

from flask import Blueprint,jsonify, render_template, request

event_bp = Blueprint('event_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='assets')

class Event:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

events = []

def init():
    with open("config/events.json", "r") as read_file:
        print("convert json to dictionary")
        events_objs = json.load(read_file)
        print("json conversion done")
        global events
        events = [Event(**event_dict) for event_dict in events_objs["events"]]

def get_events():
    return events

def events_to_json():
    try:
        collection = db.db['notification']
        data = list(collection.find().sort("timestamp",pymongo.DESCENDING))
        for item in data:
            item['_id'] = str(item['_id'])
        # print(data)
        return jsonify(data)
    except:
        print("Error")

@event_bp.route('/')
def home():
    for event in events:
        print(event.status)
    return render_template("event/event.html", events=events)

@event_bp.route('/events', methods=["GET"])
def get_events_as_json():
    return events_to_json()



@event_bp.route('/events', methods=["POST"])
def add_event_as_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        event_json_str = request.json
        event_json = json.loads(event_json_str)
        print(f"event_json type: {type(event_json)}")
        print(f"event_json: {event_json}")
        event = Event(**event_json)
        event_json["timestamp"]=datetime.now()
        collection = db.db['notification']
        insert_data=collection.insert_one(event_json)
        print("DB isert",insert_data)
        print(f"ET: {type(event)}")
        # db.client.close()
        global events
        events.append(event)
        for event in events:
            print(event.status)
        return event_json_str
    else:
        print("Unsupported content type: " + content_type)
        return 'Content-Type not supported!'
    
@event_bp.route("/events/<string:event_id>", methods=["GET"])
def get_camera_configuration(event_id):
    print(event_id)
    alerts = db.db['notification'].find({"_id": ObjectId(str(event_id))})
    
    if alerts:
        data = list(alerts)
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify(data), 200
    return "Camera not found", 404  