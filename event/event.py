import json
from collections import namedtuple
from json import JSONEncoder
from string import Template
from flask import Blueprint, render_template, request

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
    for event in events:
        print(event.status)
    return json.loads(json.dumps(events, default = lambda x: x.__dict__))

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
        print(f"ET: {type(event)}")
        global events
        events.append(event)
        for event in events:
            print(event.status)
        return event_json_str
    else:
        print("Unsupported content type: " + content_type)
        return 'Content-Type not supported!'