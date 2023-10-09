import json
from collections import namedtuple
from json import JSONEncoder
from string import Template
from config import db
import pymongo
from datetime import datetime
from bson import ObjectId 
from .models import Event
from app import app

from flask import Blueprint,jsonify, render_template, request

event_bp = Blueprint('event_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='assets')

class Events:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

events = []

def init():
    with app.app_context():
        collection = Event.query.all() 
        global events
        events=collection
        
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


